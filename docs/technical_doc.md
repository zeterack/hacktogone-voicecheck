# 🔧 Guide Technique - Architecture Blend AI + OpenAI

## Vue d'ensemble

VoiceCheck AI utilise une architecture en 3 étapes pour vérifier les contacts :

1. **Blend AI** : Gère les appels téléphoniques et la conversation vocale
2. **Transcript** : Récupération de l'enregistrement de la conversation
3. **OpenAI GPT-3.5** : Analyse du transcript pour extraire consentement et identité

---

## 🎯 Flow complet d'un appel

```
┌─────────────────┐
│  VoiceCheck AI  │
│   (Streamlit)   │
└────────┬────────┘
         │
         │ 1. Initier appel
         ▼
┌─────────────────┐
│   Blend AI API  │ ◄── Prompt personnalisé avec:
│   /v1/calls     │     - Demande consentement RGPD
└────────┬────────┘     - Vérification identité
         │
         │ 2. Appel téléphonique
         ▼
┌─────────────────┐
│    Contact      │
│  (téléphone)    │
└────────┬────────┘
         │
         │ 3. Conversation enregistrée
         ▼
┌─────────────────┐
│  Blend AI API   │
│  Transcript     │ ◄── Polling toutes les 5s
└────────┬────────┘     jusqu'à "completed"
         │
         │ 4. Transcript texte
         ▼
┌─────────────────┐
│  OpenAI GPT-3.5 │
│   Analyse NLP   │ ◄── Extraction:
└────────┬────────┘     - consent: true/false
         │              - identity_confirmed: true/false
         │
         │ 5. Résultat structuré
         ▼
┌─────────────────┐
│   results.json  │
│   (Database)    │
└─────────────────┘
```

---

## 📋 Détails des services

### 1. BlendService (`services/twilio_service.py`)

**Méthode `make_call()`**
```python
def make_call(self, to_number: str, contact_id: str, task_prompt: str, ...) -> Dict
```

Envoie une requête POST à `https://api.bland.ai/v1/calls` avec :

**Payload envoyée :**
```json
{
  "phone_number": "+33695550023",
  "voice": "429bae88-a95f-4dd3-bc9e-d6c2c3a51efa",
  "record": true,
  "max_duration": 12,
  "language": "fr",
  "task": "<prompt_personnalisé>",
  "first_sentence": "Bonjour, je suis une assistante virtuelle...",
  "metadata": {
    "contact_id": "123"
  }
}
```

**Réponse Blend AI :**
```json
{
  "call_id": "abc-123-def",
  "status": "queued"
}
```

---

**Méthode `fetch_call_result(call_id)`**

Envoie GET à `https://api.bland.ai/v1/calls/{call_id}` pour récupérer le statut et le transcript.

**Réponse (appel terminé) :**
```json
{
  "call_id": "abc-123-def",
  "status": "completed",
  "duration": 78,
  "transcript": "Assistant: Bonjour, je suis une assistante virtuelle...\nPerson: Oui j'accepte...",
  "recording_url": "https://...",
  "metadata": {
    "contact_id": "123"
  }
}
```

---

**Méthode `build_task_prompt(nom, prenom)`**

Construit le prompt détaillé pour Blend AI qui guide la conversation :

```text
Objectif: Vérifier les coordonnées d'un contact...

Flux de l'appel:
1. INTRODUCTION
   - Présentez-vous: "Bonjour, je suis une assistante virtuelle..."
   
2. CONSENTEMENT RGPD (OBLIGATOIRE)
   - Demandez: "Conformément au RGPD, acceptez-vous de poursuivre..."
   - Si OUI: Passez à l'étape 3
   - Si NON: Terminez poliment
   
3. VÉRIFICATION D'IDENTITÉ
   - Posez: "Confirmez-vous être {prenom} {nom}?"
   - Si OUI: Remerciez et terminez
   - Si NON: Notez et terminez
```

Ce prompt guide l'IA de Blend pour avoir une conversation naturelle tout en suivant le flow requis.

---

### 2. OpenAIService (`services/openai_service.py`)

**Méthode `analyze_consent_and_identity()`**

Envoie le transcript complet à OpenAI GPT-3.5 pour extraire les informations critiques.

**Prompt système :**
```text
Tu es un assistant d'analyse de conversations téléphoniques pour la conformité RGPD.
Ton rôle est d'analyser le transcript et d'extraire:

1. CONSENTEMENT RGPD: accepté/refusé/pas clair?
2. CONFIRMATION D'IDENTITÉ: confirmé/refusé/pas clair?

Réponds UNIQUEMENT en JSON:
{
  "consent": true/false/null,
  "identity_confirmed": true/false/null,
  "reasoning": "explication"
}
```

**Exemple de transcript analysé :**
```
Assistant: Bonjour, je suis une assistante virtuelle de VoiceCheck AI.
Assistant: Conformément au RGPD, acceptez-vous de poursuivre cet échange?
Person: Oui, d'accord.
Assistant: Merci. Confirmez-vous être Jean Dupont?
Person: Oui, c'est bien moi.
Assistant: Parfait, merci. Au revoir.
```

**Réponse OpenAI :**
```json
{
  "consent": true,
  "identity_confirmed": true,
  "reasoning": "La personne a clairement accepté le consentement RGPD et confirmé son identité"
}
```

---

## 🔄 Implémentation dans app.py

### Mode MOCK (par défaut)

```python
if is_mock:
    # Simulation instantanée
    call_sid = twilio_service.make_call(...)
    consent_result = twilio_service.simulate_consent_response()
    identity_result = twilio_service.simulate_identity_confirmation()
    # Pas d'appel réel, résultats aléatoires
```

### Mode RÉEL (avec clés API)

```python
else:
    # 1. Construire le prompt
    task_prompt = twilio_service.build_task_prompt(nom, prenom)
    
    # 2. Initier l'appel Blend
    call_response = twilio_service.make_call(
        to_number=telephone,
        contact_id=contact_id,
        task_prompt=task_prompt,
        language="fr"
    )
    call_id = call_response['call_id']
    
    # 3. Polling: attendre que l'appel se termine
    while attempt < 60:  # Max 5 minutes
        time.sleep(5)
        call_status = twilio_service.fetch_call_result(call_id)
        
        if call_status['status'] == 'completed':
            transcript = call_status['transcript']
            break
    
    # 4. Analyser avec OpenAI
    analysis = openai_service.analyze_consent_and_identity(
        transcript=transcript,
        nom=nom,
        prenom=prenom
    )
    
    # 5. Sauvegarder dans results.json
    result = {
        'contact_id': contact_id,
        'consent': analysis['consent'],
        'identity_confirmed': analysis['identity_confirmed'],
        'transcription': transcript,
        'reasoning': analysis['reasoning']
    }
    db.save_result(result)
```

---

## ⚙️ Configuration requise

### Mode MOCK
```bash
USE_MOCK_SERVICES=True
# Aucune clé API nécessaire
```

### Mode RÉEL
```bash
USE_MOCK_SERVICES=False
BLEND_API_KEY=your_blend_api_key_here
BLEND_ENDPOINT=https://api.bland.ai/v1/calls
OPENAI_API_KEY=sk-proj-...
```

**Obtention des clés :**
- Blend AI : https://app.bland.ai → Settings → API Keys
- OpenAI : https://platform.openai.com → API Keys

---

## 📊 Structure des données

### Contact (contacts.json)
```json
{
  "id": "1",
  "nom": "Dupont",
  "prenom": "Jean",
  "telephone": "+33612345678",
  "status": "pending",
  "created_at": "2024-11-13T10:30:00"
}
```

### Résultat (results.json)
```json
{
  "contact_id": "1",
  "nom": "Dupont",
  "prenom": "Jean",
  "telephone": "+33612345678",
  "call_sid": "blend-call-abc123",
  "consent": true,
  "identity_confirmed": true,
  "no_response": false,
  "transcription": "Assistant: Bonjour...\nPerson: Oui...",
  "reasoning": "Consentement et identité confirmés",
  "timestamp": "2024-11-13T10:35:42"
}
```

---

## 🐛 Debugging

### Vérifier le mode actif
```python
from utils.config import Config
print(f"Mode mock: {Config.is_mock_mode()}")
print(f"Blend API Key: {Config.BLEND_API_KEY[:10]}..." if Config.BLEND_API_KEY else "Non défini")
```

### Tester l'appel Blend manuellement
```python
from services.twilio_service import BlendService

blend = BlendService()
response = blend.make_call(
    to_number="+33612345678",
    contact_id="test",
    task_prompt="Test simple",
    first_sentence="Bonjour, ceci est un test"
)
print(response)
```

### Tester l'analyse OpenAI
```python
from services.openai_service import OpenAIService

openai_svc = OpenAIService()
result = openai_svc.analyze_consent_and_identity(
    transcript="Person: Oui j'accepte. Person: Oui c'est moi.",
    nom="Dupont",
    prenom="Jean"
)
print(result)
```

---

## ⚠️ Limitations et considérations

### Temps d'attente
- L'appel Blend peut durer de 30 secondes à 2-3 minutes
- Le polling attend jusqu'à 5 minutes maximum
- Pendant ce temps, l'interface Streamlit affiche "⏳ Appel en cours..."

### Coûts
- **Blend AI** : ~0.09$/minute d'appel
- **OpenAI GPT-3.5** : ~0.002$ par analyse (200 tokens)
- Budget estimé : ~0.10-0.15$ par appel complet

### Gestion des erreurs
- Si Blend ne répond pas : `no_response = True`
- Si le transcript est vide : `consent = None, identity_confirmed = None`
- Si OpenAI échoue : le raisonnement contient l'erreur

### RGPD
- Le consentement est explicitement demandé en début d'appel
- Les enregistrements sont stockés localement (data/results.json)
- Les transcripts complets sont sauvegardés pour audit

---

## 🚀 Prochaines améliorations possibles

1. **Webhook** : Utiliser les webhooks Blend au lieu du polling
2. **Async** : Traiter plusieurs appels en parallèle
3. **Retry** : Gestion des appels échoués avec retry automatique
4. **Dashboard temps réel** : WebSocket pour mise à jour live
5. **Export audio** : Télécharger les enregistrements audio
6. **Analyse avancée** : Détection du sentiment, de la satisfaction client

---

## 📞 Support

Pour toute question technique :
- Documentation Blend AI : https://docs.bland.ai
- Documentation OpenAI : https://platform.openai.com/docs
- Code source : Voir les fichiers `services/` et `app.py`
