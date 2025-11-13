import openai
from openai import OpenAI
from typing import Dict, Any
from utils.config import Config
import logging
import json

# Configuration du logger
logger = logging.getLogger(__name__)


class OpenAIService:
    """Service d'analyse des transcripts via OpenAI pour extraire consentement et identité."""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        logger.info("OpenAIService initialisé")
    
    def analyze_consent_and_identity(self, transcript: str, nom: str, prenom: str) -> Dict[str, Any]:
        """Analyse le transcript complet pour extraire consentement RGPD et confirmation d'identité.
        
        Args:
            transcript: Le texte complet de la conversation enregistrée par Blend.
            nom: Nom de famille du contact.
            prenom: Prénom du contact.
        
        Returns:
            Dict avec:
                - consent: True/False/None (consentement RGPD donné)
                - identity_confirmed: True/False/None (identité confirmée)
                - reasoning: Explication du raisonnement
        """
        
        system_prompt = f"""Tu es un assistant d'analyse de conversations téléphoniques pour la conformité RGPD.
Ton rôle est d'analyser le transcript d'un appel et d'extraire deux informations critiques.

⚠️ RÈGLE CRITIQUE: DÉTECTION DE RÉPONDEUR/MESSAGERIE VOCALE
Si tu détectes un répondeur ou une messagerie vocale, tu DOIS mettre consent=false et identity_confirmed=false.

Indices de répondeur/messagerie:
- Phrases comme: "je ne suis pas disponible", "laissez un message", "rappellerai", "boîte vocale"
- Message pré-enregistré mentionnant le nom de la personne
- Marqueur technique: "<Call ended due to voicemail detection>"
- Pas d'interaction réelle (juste un message enregistré)
- Aucune réponse aux questions de l'assistant

IMPORTANT: Même si le message du répondeur mentionne le nom "{prenom} {nom}", ce n'est PAS une confirmation d'identité car c'est un message pré-enregistré, pas une personne réelle qui répond.

1. CONSENTEMENT RGPD: La PERSONNE RÉELLE a-t-elle explicitement accepté de poursuivre l'échange?
   - ✅ Acceptation: "oui j'accepte", "oui je consens", "d'accord", "oui", "vas-y"
   - ❌ Refus: "non", "je refuse", "non merci", "pas intéressé"
   - ❌ Répondeur: TOUJOURS false si répondeur détecté
   - ⚠️ Pas clair: null seulement si personne réelle mais réponse ambiguë

2. CONFIRMATION D'IDENTITÉ: La PERSONNE RÉELLE a-t-elle confirmé être {prenom} {nom}?
   - ✅ Confirmation: "oui c'est moi", "oui", "exact", "confirme", "c'est bien moi"
   - ❌ Refus: "non ce n'est pas moi", "non", "vous vous trompez"
   - ❌ Répondeur: TOUJOURS false si répondeur détecté (même si le nom est mentionné)
   - ⚠️ Pas clair: null seulement si personne réelle mais réponse ambiguë

Réponds UNIQUEMENT avec un JSON valide au format:
{{
  "consent": true/false/null,
  "identity_confirmed": true/false/null,
  "reasoning": "explication courte (mentionne 'répondeur détecté' si c'est le cas)"
}}
"""
        
        user_prompt = f"""Analyse ce transcript d'appel pour {prenom} {nom}:

TRANSCRIPT:
{transcript}

Extrais le consentement RGPD et la confirmation d'identité."""

        logger.info(f"🤖 Appel OpenAI pour analyser transcript (longueur: {len(transcript)} caractères)")
        logger.debug(f"Transcript envoyé: {transcript[:200]}..." if len(transcript) > 200 else f"Transcript envoyé: {transcript}")

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            logger.info(f"✅ Réponse OpenAI reçue: {result_text}")
            
            # Parse le JSON retourné
            result = json.loads(result_text)
            
            # Normalise les valeurs null en None
            if result.get('consent') is None or result.get('consent') == 'null':
                result['consent'] = None
            if result.get('identity_confirmed') is None or result.get('identity_confirmed') == 'null':
                result['identity_confirmed'] = None
            
            logger.info(f"📊 Résultat parsé: consent={result.get('consent')}, identity_confirmed={result.get('identity_confirmed')}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erreur de parsing JSON: {str(e)}")
            logger.error(f"Raw response: {result_text if 'result_text' in locals() else 'N/A'}")
            return {
                'consent': None,
                'identity_confirmed': None,
                'reasoning': f'Erreur de parsing JSON: {str(e)}',
                'raw_response': result_text if 'result_text' in locals() else ''
            }
        except Exception as e:
            logger.error(f"❌ Erreur OpenAI: {str(e)}")
            logger.exception(e)
            return {
                'consent': None,
                'identity_confirmed': None,
                'reasoning': f'Erreur OpenAI: {str(e)}'
            }
    
    def quick_sentiment_check(self, text: str) -> str:
        """Analyse rapide du sentiment (positif/négatif/neutre) d'une réponse courte."""
        text_lower = text.lower().strip()
        
        # Mots-clés positifs
        positive = ['oui', 'yes', 'ok', 'd\'accord', 'dacord', 'confirme', 'exact', 'correct', 'vas-y', 'accepte']
        # Mots-clés négatifs
        negative = ['non', 'no', 'jamais', 'refuse', 'pas', 'aucun']
        
        if any(word in text_lower for word in positive):
            return 'positive'
        elif any(word in text_lower for word in negative):
            return 'negative'
        else:
            return 'neutral'
