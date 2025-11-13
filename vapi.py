"""
Script d'appel automatisé avec Vapi.ai
Gestion intelligente des scénarios : non-réponse, refus, vérification identité
"""

import requests
import json
from typing import Optional, Dict, Any
import time

class VapiCaller:
    """Gestionnaire d'appels avec Vapi.ai"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.vapi.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_assistant(self, assistant_config: Dict[str, Any]) -> str:
        """Crée un assistant avec la configuration donnée"""
        response = requests.post(
            f"{self.base_url}/assistant",
            headers=self.headers,
            json=assistant_config
        )
        response.raise_for_status()
        return response.json()["id"]
    
    def make_call(
        self,
        phone_number: str,
        assistant_id: Optional[str] = None,
        assistant_config: Optional[Dict[str, Any]] = None,
        customer_name: str = "le client"
    ) -> Dict[str, Any]:
        """
        Passe un appel
        
        Args:
            phone_number: Numéro à appeler (format international: +33...)
            assistant_id: ID d'un assistant existant
            assistant_config: Configuration d'assistant (si pas d'ID)
            customer_name: Nom du client pour personnalisation
        """
        payload = {
            "phoneNumberId": None,  # Vapi utilisera un numéro par défaut
            "customer": {
                "number": phone_number,
                "name": customer_name
            }
        }
        
        # Utiliser assistant existant ou en créer un nouveau
        if assistant_id:
            payload["assistantId"] = assistant_id
        elif assistant_config:
            payload["assistant"] = assistant_config
        else:
            raise ValueError("Fournir soit assistant_id soit assistant_config")
        
        response = requests.post(
            f"{self.base_url}/call/phone",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """Récupère le statut d'un appel"""
        response = requests.get(
            f"{self.base_url}/call/{call_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()


def get_assistant_prompt() -> str:
    """
    Prompt principal avec routage intelligent des scénarios
    """
    return """Tu es un assistant téléphonique professionnel et courtois qui appelle au nom de [NOM DE VOTRE ENTREPRISE].

## OBJECTIF DE L'APPEL
[Décrire l'objectif : prise de rendez-vous, enquête de satisfaction, confirmation de commande, etc.]

## DÉROULEMENT DE L'APPEL

### ÉTAPE 1 : OUVERTURE ET VÉRIFICATION D'IDENTITÉ
Commence TOUJOURS par :
"Bonjour, je suis [NOM], assistant virtuel de [ENTREPRISE]. J'essaie de joindre [NOM_PROSPECT]. Est-ce bien vous ?"

**SCÉNARIOS POSSIBLES :**

A) La personne CONFIRME son identité :
   → Continue à l'étape 2
   
B) La personne dit que ce N'EST PAS elle :
   → Dis : "Je vous prie de m'excuser pour le dérangement. Bonne journée !"
   → TERMINE L'APPEL IMMÉDIATEMENT avec <end_call/>

C) La personne ne comprend pas ou hésite :
   → Répète une fois : "Je cherche à joindre [NOM_PROSPECT]. Êtes-vous cette personne ?"
   → Si toujours pas clair : "Désolé pour la confusion. Bonne journée !"
   → TERMINE L'APPEL avec <end_call/>

### ÉTAPE 2 : DEMANDE DE CONSENTEMENT ENREGISTREMENT
Si identité confirmée, dis :
"Parfait. Avant de continuer, je vous informe que cet appel peut être enregistré à des fins de qualité. Êtes-vous d'accord pour poursuivre ?"

**SCÉNARIOS POSSIBLES :**

A) La personne ACCEPTE ("oui", "d'accord", "pas de problème") :
   → Continue à l'étape 3
   
B) La personne REFUSE ("non", "je ne veux pas", "pas d'accord") :
   → Dis : "Je comprends parfaitement. Dans ce cas, je ne peux malheureusement pas continuer cet entretien. Je vous remercie et vous souhaite une excellente journée."
   → TERMINE L'APPEL IMMÉDIATEMENT avec <end_call/>
   
C) La personne demande des précisions :
   → Explique : "L'enregistrement nous permet d'améliorer notre service et de vérifier les informations échangées. Acceptez-vous ?"
   → Attends la réponse et applique A ou B

### ÉTAPE 3 : CORPS DE L'APPEL
[ICI, DÉTAILLE TON SCRIPT PRINCIPAL]

Exemples selon ton objectif :

**Si PRISE DE RENDEZ-VOUS :**
"Parfait. Je vous appelle pour planifier un rendez-vous concernant [SUJET]. Seriez-vous disponible [PROPOSER CRÉNEAUX] ?"

**Si ENQUÊTE SATISFACTION :**
"Excellent. Je souhaite recueillir votre avis sur [PRODUIT/SERVICE]. Avez-vous 2 minutes pour répondre à quelques questions ?"

**Si CONFIRMATION COMMANDE :**
"Merci. Je vous appelle pour confirmer votre commande n°[NUMERO]. Avez-vous bien reçu [DÉTAILS] ?"

### GESTION DES INTERRUPTIONS

**Si la personne dit "Je suis occupé" / "Pas le temps" :**
→ "Je comprends parfaitement. Quel serait le meilleur moment pour vous rappeler ? [Proposer créneaux]"
→ Si elle refuse complètement : "Pas de problème. Bonne journée !" + <end_call/>

**Si la personne pose des questions hors sujet :**
→ Réponds brièvement puis recentre : "Pour en revenir à l'objet de mon appel..."

**Si la personne devient agressive :**
→ Reste calme : "Je comprends votre réaction. Si vous préférez, je peux terminer cet appel. Bonne journée." + <end_call/>

## RÈGLES IMPORTANTES

1. **IDENTIFICATION** : Vérifie TOUJOURS l'identité avant de continuer
2. **CONSENTEMENT** : Demande TOUJOURS l'accord pour l'enregistrement
3. **CLARTÉ** : Parle lentement et clairement en français
4. **CONCISION** : Sois direct, ne dépasse pas 2-3 minutes
5. **POLITESSE** : Reste courtois même en cas de refus
6. **TERMINAISON** : Utilise <end_call/> pour terminer proprement

## COMMANDES SPÉCIALES

- Pour terminer l'appel : Dis au revoir ET ajoute <end_call/>
- Pour transférer à un humain (si disponible) : <transfer_call to="support"/>

## EXEMPLE DE DIALOGUE RÉUSSI

Assistant : "Bonjour, je suis Sophie, assistante virtuelle de TechCorp. J'essaie de joindre Monsieur Dupont. Est-ce bien vous ?"
Client : "Oui, c'est moi."
Assistant : "Parfait. Avant de continuer, je vous informe que cet appel peut être enregistré à des fins de qualité. Êtes-vous d'accord pour poursuivre ?"
Client : "Oui, pas de problème."
Assistant : "Merci. Je vous appelle pour..."

## TONALITÉ
Reste naturel, professionnel mais amical. Adapte-toi au rythme de ton interlocuteur.
"""


def get_assistant_config(
    nom_assistant: str = "Sophie",
    nom_entreprise: str = "Votre Entreprise",
    nom_prospect: str = "le client",
    objectif: str = "prendre rendez-vous"
) -> Dict[str, Any]:
    """
    Configuration complète de l'assistant avec routage intelligent
    
    Args:
        nom_assistant: Prénom de l'assistant virtuel
        nom_entreprise: Nom de votre entreprise
        nom_prospect: Nom de la personne à contacter
        objectif: Objectif de l'appel
    """
    
    # Personnalisation du prompt
    prompt = get_assistant_prompt()
    prompt = prompt.replace("[NOM]", nom_assistant)
    prompt = prompt.replace("[ENTREPRISE]", nom_entreprise)
    prompt = prompt.replace("[NOM_PROSPECT]", nom_prospect)
    prompt = prompt.replace("[SUJET]", objectif)
    
    return {
        "name": f"Assistant {nom_assistant} - {objectif}",
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.7,
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                }
            ]
        },
        "voice": {
            "provider": "11labs",  # ElevenLabs pour voix naturelle
            "voiceId": "21m00Tcm4TlvDq8ikWAM",  # Voix féminine française (Rachel)
            # Autres options françaises :
            # "EXAVITQu4vr4xnSDxMaL" - Bella (féminine, calme)
            # "pNInz6obpgDQGcFmaJgB" - Adam (masculine, professionnelle)
            "stability": 0.5,
            "similarityBoost": 0.75,
            "optimizeStreamingLatency": 2
        },
        "language": "fr",  # Français
        "firstMessage": f"Bonjour, je suis {nom_assistant}, assistante virtuelle de {nom_entreprise}. J'essaie de joindre {nom_prospect}. Est-ce bien vous ?",
        "recordingEnabled": True,  # Enregistrer l'appel
        "endCallMessage": "Merci pour votre temps. Au revoir !",
        "endCallPhrases": [
            "au revoir",
            "bonne journée",
            "à bientôt",
            "<end_call/>"
        ],
        "voicemailMessage": f"Bonjour, vous êtes bien sur la messagerie de {nom_prospect}. Je suis {nom_assistant} de {nom_entreprise}. Je vous rappellerai ultérieurement. Bonne journée.",
        "maxDurationSeconds": 300,  # 5 minutes max
        "silenceTimeoutSeconds": 30,  # Timeout si silence
        "responseDelaySeconds": 0.5,  # Délai avant de répondre
        "interruptionsEnabled": True  # Permettre les interruptions
    }


# ============================================
# EXEMPLES D'UTILISATION
# ============================================

def exemple_appel_simple():
    """Exemple : Passer un appel simple"""
    
    # Votre clé API Vapi (à obtenir sur vapi.ai)
    API_KEY = "votre_cle_api_vapi"
    
    # Initialiser
    caller = VapiCaller(API_KEY)
    
    # Configuration de l'assistant
    assistant_config = get_assistant_config(
        nom_assistant="Sophie",
        nom_entreprise="TechSolutions",
        nom_prospect="Monsieur Dupont",
        objectif="confirmer le rendez-vous du 15 novembre"
    )
    
    # Passer l'appel
    try:
        result = caller.make_call(
            phone_number="+33612345678",  # Numéro au format international
            assistant_config=assistant_config,
            customer_name="M. Dupont"
        )
        
        print(f"✅ Appel lancé avec succès !")
        print(f"ID de l'appel : {result['id']}")
        print(f"Statut : {result['status']}")
        
        # Attendre quelques secondes et vérifier le statut
        time.sleep(10)
        status = caller.get_call_status(result['id'])
        print(f"Statut après 10s : {status['status']}")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")


def exemple_appel_multiple():
    """Exemple : Passer plusieurs appels avec le même assistant"""
    
    API_KEY = "votre_cle_api_vapi"
    caller = VapiCaller(API_KEY)
    
    # Créer l'assistant une fois
    assistant_config = get_assistant_config(
        nom_assistant="Sophie",
        nom_entreprise="TechSolutions",
        objectif="enquête de satisfaction"
    )
    
    # Créer l'assistant et récupérer son ID
    assistant_id = caller.create_assistant(assistant_config)
    print(f"✅ Assistant créé : {assistant_id}")
    
    # Liste de prospects
    prospects = [
        {"phone": "+33612345678", "name": "M. Dupont"},
        {"phone": "+33687654321", "name": "Mme Martin"},
        {"phone": "+33698765432", "name": "M. Bernard"}
    ]
    
    # Appeler chaque prospect
    for prospect in prospects:
        try:
            result = caller.make_call(
                phone_number=prospect["phone"],
                assistant_id=assistant_id,  # Réutiliser le même assistant
                customer_name=prospect["name"]
            )
            print(f"✅ Appel lancé pour {prospect['name']} - ID: {result['id']}")
            time.sleep(2)  # Délai entre les appels
            
        except Exception as e:
            print(f"❌ Erreur pour {prospect['name']}: {e}")


def exemple_prompt_personnalise():
    """Exemple : Créer un prompt très personnalisé"""
    
    API_KEY = "votre_cle_api_vapi"
    caller = VapiCaller(API_KEY)
    
    # Configuration personnalisée
    custom_config = get_assistant_config(
        nom_assistant="Marc",
        nom_entreprise="AutoExpert",
        nom_prospect="Mme Lefebvre",
        objectif="rappel révision de votre Renault Clio"
    )
    
    # Modifier le prompt pour ajouter des informations spécifiques
    custom_config["model"]["messages"][0]["content"] += """

## INFORMATIONS SPÉCIFIQUES À CE CLIENT
- Véhicule : Renault Clio 4 (2019)
- Dernière révision : il y a 11 mois
- Kilométrage estimé : ~25 000 km
- Garage habituel : AutoExpert Marseille

## PROPOSITIONS À FAIRE
Si le client accepte le rendez-vous, propose :
1. Mardi 14 novembre à 9h
2. Jeudi 16 novembre à 14h
3. Vendredi 17 novembre à 10h

Si aucun créneau ne convient, demande ses disponibilités.
"""
    
    # Passer l'appel
    try:
        result = caller.make_call(
            phone_number="+33623456789",
            assistant_config=custom_config,
            customer_name="Mme Lefebvre"
        )
        print(f"✅ Appel personnalisé lancé : {result['id']}")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")


# ============================================
# SCRIPT PRINCIPAL
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("VAPI CALLER - Appels automatisés avec IA")
    print("=" * 60)
    print()
    print("⚠️  AVANT DE COMMENCER :")
    print("1. Créez un compte sur vapi.ai")
    print("2. Obtenez votre clé API")
    print("3. Remplacez 'votre_cle_api_vapi' dans le code")
    print("4. Testez d'abord avec VOTRE numéro !")
    print()
    print("Exemples disponibles :")
    print("- exemple_appel_simple()")
    print("- exemple_appel_multiple()")
    print("- exemple_prompt_personnalise()")
    print()
    print("=" * 60)
    
    # Décommentez pour tester :
    # exemple_appel_simple()