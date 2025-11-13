import requests
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from utils.config import Config

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler pour fichier
file_handler = logging.FileHandler('logs/blend_api.log')
file_handler.setLevel(logging.DEBUG)

# Handler pour console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format des logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class BlendService:
    """Service d'intégration avec l'API Blend AI (remplace Twilio).

    Ce service envoie la payload fournie à l'endpoint de Blend et retourne
    la réponse brute. Le service n'effectue pas d'analyse de la transcription
    — l'application doit récupérer le transcript et le passer à OpenAI pour
    l'analyse/validation d'identité.
    """

    def __init__(self):
        config = Config()
        self.api_key = config.BLEND_API_KEY
        self.endpoint = config.BLEND_ENDPOINT or "https://api.bland.ai/v1/calls"
        self.headers = {
            "Authorization": self.api_key,  # Blend utilise la clé directement, pas Bearer
            "Content-Type": "application/json",
        }
        logger.info(f"BlendService initialisé - Endpoint: {self.endpoint}")
        logger.debug(f"API Key présente: {bool(self.api_key)} (longueur: {len(self.api_key) if self.api_key else 0})")

    def make_call(self,
                  to_number: str,
                  contact_id: str,
                  task_prompt: str,
                  first_sentence: str = "hello, je suis une IA",
                  voice: str = "e10f0745-ff46-4b37-9be1-34cbda38af91",
                  max_duration: int = 12,
                  language: str = "fr") -> Dict[str, Any]:
        """Initie un appel via Blend API.

        Args:
            to_number: Numéro de téléphone cible (format international).
            contact_id: Identifiant interne du contact (pour corrélation).
            task_prompt: Prompt détaillé décrivant le flow/contexte de l'appel.
            first_sentence: Phrase d'ouverture pour le modèle vocal.

        Returns:
            La réponse JSON renvoyée par l'API Blend (ou un dict d'erreur).
        """

        data = {
            "phone_number": to_number,
            "voice": voice,
            "wait_for_greeting": False,
            "record": True,
            "answered_by_enabled": True,
            "noise_cancellation": False,
            "interruption_threshold": 500,
            "block_interruptions": False,
            "max_duration": max_duration,
            "model": "base",
            "language": language,
            "background_track": "none",
            "endpoint": self.endpoint,
            "voicemail_action": "hangup",
            "isCallActive": False,
            "task": task_prompt,
            "first_sentence": first_sentence,
            "metadata": {
                "contact_id": contact_id
            }
        }

        # Logging de la requête
        logger.info(f"=== APPEL BLEND AI ===")
        logger.info(f"Contact ID: {contact_id}")
        logger.info(f"Numéro: {to_number}")
        logger.info(f"Endpoint: {self.endpoint}")
        logger.debug(f"Headers: {json.dumps({k: v[:20] + '...' if k == 'Authorization' and len(v) > 20 else v for k, v in self.headers.items()}, indent=2)}")
        logger.debug(f"Payload complet:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
        
        try:
            resp = requests.post(self.endpoint, headers=self.headers, json=data, timeout=30)
            
            # Log de la réponse
            logger.info(f"Status Code: {resp.status_code}")
            logger.debug(f"Response Headers: {dict(resp.headers)}")
            
            try:
                response_json = resp.json()
                logger.debug(f"Response Body:\n{json.dumps(response_json, indent=2, ensure_ascii=False)}")
            except:
                logger.debug(f"Response Body (raw): {resp.text}")
            
            resp.raise_for_status()
            return response_json if 'response_json' in locals() else resp.json()
            
        except requests.HTTPError as e:
            logger.error(f"❌ ERREUR HTTP {e.response.status_code}")
            logger.error(f"Response Body: {e.response.text}")
            logger.error(f"Request URL: {e.request.url}")
            logger.error(f"Request Headers: {dict(e.request.headers)}")
            logger.error(f"Request Body: {e.request.body}")
            
            return {
                "error": True,
                "message": str(e),
                "status_code": e.response.status_code,
                "response_body": e.response.text,
                "request_url": e.request.url,
                "request_body": data
            }
        except requests.RequestException as e:
            logger.error(f"❌ ERREUR REQUÊTE: {str(e)}")
            return {
                "error": True,
                "message": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }

    def fetch_call_result(self, call_id: str) -> Dict[str, Any]:
        """Récupère l'état ou le résultat d'un appel (si l'API le permet).

        Retourne typiquement un objet contenant au minimum un identifiant
        d'enregistrement et l'URL du transcript/recording.
        """
        # L'endpoint Blend pour récupérer le résultat d'un appel
        # est typiquement GET /v1/calls/{call_id}
        base_url = self.endpoint.replace('/v1/calls', '')
        url = f"{base_url}/v1/calls/{call_id}"
        
        logger.info(f"Récupération du résultat pour call_id: {call_id}")
        logger.debug(f"URL: {url}")
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
            logger.info(f"Status Code: {resp.status_code}")
            
            resp.raise_for_status()
            result = resp.json()
            logger.debug(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
            
        except requests.HTTPError as e:
            logger.error(f"❌ ERREUR HTTP lors de fetch_call_result: {e.response.status_code}")
            logger.error(f"Response: {e.response.text}")
            return {"error": True, "message": str(e), "response": e.response.text}
        except requests.RequestException as e:
            logger.error(f"❌ ERREUR lors de fetch_call_result: {str(e)}")
            return {"error": True, "message": str(e)}
    
    def build_task_prompt(self, nom: str, prenom: str) -> str:
        """Construit le prompt de tâche pour l'appel Blend incluant consentement RGPD et vérification d'identité.
        
        Args:
            nom: Nom de famille du contact
            prenom: Prénom du contact
        
        Returns:
            Le prompt complet formaté pour Blend AI
        """
        
        task = f"""Objectif: Vérifier les coordonnées d'un contact dans notre base de données en respectant le RGPD.

Flux de l'appel:

1. CONSENTEMENT RGPD (OBLIGATOIRE)
   - Demandez le consentement explicite: "Bonjour, conformément au règlement RGPD, acceptez-vous de poursuivre cet échange pour la vérification de vos données? Merci de répondre par oui ou par non."
   - Attendez la réponse claire (oui/non)
   - Si OUI: Passez à l'étape 2
   - Si NON: Terminez poliment: "Je comprends, merci de votre temps. Au revoir."
   - Si pas de réponse claire: Répétez une fois, puis terminez poliment

2. VÉRIFICATION D'IDENTITÉ
   - Posez la question: "Confirmez-vous être {prenom} {nom}? Merci de répondre par oui ou par non."
   - Attendez la réponse (oui/non)
   - Si OUI: Remerciez: "Parfait, merci pour votre confirmation. Au revoir."
   - Si NON: "Je comprends, nous allons corriger nos données. Merci et au revoir."

Contexte:
Vous êtes une IA développée par VoiceCheck AI pour automatiser la vérification de bases de données clients.
L'appel doit être court (moins de 1 minute), direct et respectueux du RGPD.
Vous devez obtenir des réponses claires avant de passer à l'étape suivante.

Contact ciblé: {prenom} {nom}

Exemple de dialogue:

Vous: Bonjour, conformément au règlement RGPD, acceptez-vous de poursuivre cet échange pour la vérification de vos données? Merci de répondre par oui ou par non.

Personne: Oui.

Vous: Confirmez-vous être {prenom} {nom}? Merci de répondre par oui ou par non.

Personne: Oui.

Vous: Parfait, merci pour votre confirmation. Au revoir.
"""
        return task

