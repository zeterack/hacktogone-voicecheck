# Guide de débogage - Erreurs Bland AI

## 📋 Fichiers de logs

Les logs sont maintenant enregistrés dans :
- `logs/blend_api.log` : Tous les appels à l'API Blend AI (requêtes, réponses, erreurs)
- `logs/app.log` : Logs généraux de l'application

## 🔍 Comment voir les logs

### Option 1 : Script de visualisation

```bash
# Voir tous les logs
python view_logs.py

# Suivre les logs en temps réel (comme tail -f)
python view_logs.py --tail

# Voir uniquement les erreurs
python view_logs.py --errors-only

# Voir la dernière erreur détaillée
python view_logs.py --last-error
```

### Option 2 : Directement dans le terminal

```bash
# Voir le fichier complet
cat logs/blend_api.log

# Suivre en temps réel
tail -f logs/blend_api.log

# Voir uniquement les erreurs
grep -A 10 "ERROR" logs/blend_api.log
```

## 📊 Informations loggées

Pour chaque appel à Blend AI, les logs contiennent :

### Requête
- ✅ Contact ID
- ✅ Numéro de téléphone
- ✅ Endpoint utilisé
- ✅ Headers (avec API key masquée)
- ✅ **Payload JSON complet** (tous les paramètres envoyés)

### Réponse
- ✅ Status Code HTTP
- ✅ Headers de réponse
- ✅ Body de réponse complet

### Erreurs (si erreur 400)
- ❌ Code d'erreur HTTP
- ❌ Message d'erreur de Bland
- ❌ URL de la requête
- ❌ Headers envoyés
- ❌ Body de la requête
- ❌ Body de la réponse (détails de l'erreur)

## 🐛 Erreur 400 - Causes communes

### 1. Clé API invalide
```
❌ ERREUR HTTP 400
Response Body: {"error": "Invalid API key"}
```
**Solution** : Vérifier `BLEND_API_KEY` dans `.env`

### 2. Format de numéro incorrect
```
Response Body: {"error": "Invalid phone number format"}
```
**Solution** : Le numéro doit être au format international : `+33612345678`

### 3. Paramètre manquant ou invalide
```
Response Body: {"error": "Missing required field: task"}
```
**Solution** : Vérifier que tous les champs obligatoires sont présents

### 4. Voice ID invalide
```
Response Body: {"error": "Invalid voice ID"}
```
**Solution** : Vérifier le `voice` ID utilisé (actuellement : `429bae88-a95f-4dd3-bc9e-d6c2c3a51efa`)

### 5. Language non supporté
```
Response Body: {"error": "Unsupported language"}
```
**Solution** : Bland supporte `en`, `es`, `fr`, etc. Vérifier la valeur du paramètre `language`

## 🔧 Débogage étape par étape

### Étape 1 : Vérifier la configuration

```python
python -c "
from utils.config import Config
print(f'Mode mock: {Config.is_mock_mode()}')
print(f'Blend API Key: {Config.BLEND_API_KEY[:20]}...' if Config.BLEND_API_KEY else 'Non défini')
print(f'Endpoint: {Config.BLEND_ENDPOINT}')
"
```

### Étape 2 : Lancer un appel test et voir les logs

```bash
# Terminal 1 : Suivre les logs
python view_logs.py --tail

# Terminal 2 : Lancer l'app et faire un appel
streamlit run app.py
```

### Étape 3 : Analyser la dernière erreur

```bash
python view_logs.py --last-error
```

### Étape 4 : Comparer avec la documentation Bland

Endpoint officiel : `https://api.bland.ai/v1/calls`

Paramètres requis selon la doc Bland :
- `phone_number` (string) ✅
- `task` (string) ✅
- `voice` (string, optionnel) ✅
- `language` (string, optionnel) ✅

## 📝 Exemple de log complet

```
2024-11-13 15:30:45 - services.twilio_service - INFO - === APPEL BLEND AI ===
2024-11-13 15:30:45 - services.twilio_service - INFO - Contact ID: 1
2024-11-13 15:30:45 - services.twilio_service - INFO - Numéro: +33612345678
2024-11-13 15:30:45 - services.twilio_service - INFO - Endpoint: https://api.bland.ai/v1/calls
2024-11-13 15:30:45 - services.twilio_service - DEBUG - Headers: {
  "Authorization": "sk-1234567890abcdef...",
  "Content-Type": "application/json"
}
2024-11-13 15:30:45 - services.twilio_service - DEBUG - Payload complet:
{
  "phone_number": "+33612345678",
  "voice": "429bae88-a95f-4dd3-bc9e-d6c2c3a51efa",
  "wait_for_greeting": false,
  "record": true,
  "task": "Objectif: Vérifier les coordonnées...",
  ...
}
2024-11-13 15:30:47 - services.twilio_service - INFO - Status Code: 400
2024-11-13 15:30:47 - services.twilio_service - ERROR - ❌ ERREUR HTTP 400
2024-11-13 15:30:47 - services.twilio_service - ERROR - Response Body: {"error": "Invalid parameter X"}
```

## 🆘 Obtenir de l'aide

1. **Consulter les logs** : `python view_logs.py --last-error`
2. **Vérifier la documentation Bland** : https://docs.bland.ai
3. **Tester l'API manuellement** avec curl :

```bash
curl -X POST https://api.bland.ai/v1/calls \
  -H "Authorization: VOTRE_CLE" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+33612345678",
    "task": "Test simple",
    "voice": "429bae88-a95f-4dd3-bc9e-d6c2c3a51efa"
  }'
```

4. **Partager les logs** : Copier la sortie de `python view_logs.py --last-error`

## ✅ Checklist avant de lancer un appel

- [ ] `.env` configuré avec `BLEND_API_KEY`
- [ ] `USE_MOCK_SERVICES=False` dans `.env`
- [ ] Numéro au format international (+33...)
- [ ] Dossier `logs/` existe
- [ ] Application relancée après modification de `.env`
- [ ] Logs activés : `python view_logs.py --tail` dans un autre terminal
