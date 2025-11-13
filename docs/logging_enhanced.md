# Améliorations du système de logging

**Date:** 13 novembre 2025  
**Objectif:** Traçabilité complète du processus d'appel avec Bland.ai + analyse OpenAI

---

## 📊 Nouveaux logs ajoutés

### 1. **app.py** - Flux principal
#### Polling des appels
- ⏳ `"Polling tentative X/60 pour call_id: XXX"`
- 🔍 `"Status actuel: completed/started/..."`
- ✅ `"Appel terminé! Transcript récupéré (longueur: XXX caractères)"`
- ⚠️ `"Timeout: Appel non terminé après 60 tentatives"`
- ⚠️ `"Aucun transcript disponible pour call_id: XXX"`

#### Analyse OpenAI
- 🤖 `"Début de l'analyse OpenAI pour [Prénom Nom]"`
- ✅ `"Analyse OpenAI terminée: consent=true, identity=true"`
- 📊 `"Reasoning: ..."`
- ❌ `"Erreur lors de l'analyse OpenAI: [message]"`

#### Sauvegarde des résultats
- 📝 `"Création du résultat avec no_response=True pour contact X"`
- 💾 `"Sauvegarde du résultat pour contact X"`
- ✅ `"Contact X marqué comme 'completed' (consent + identity OK)"`
- ⏸️ `"Contact X reste en 'pending' (consent=false, identity=null)"`

---

### 2. **services/openai_service.py** - Analyse IA
- 🤖 `"OpenAIService initialisé"`
- 🤖 `"Appel OpenAI pour analyser transcript (longueur: XXX caractères)"`
- 📝 `"Transcript envoyé: [200 premiers caractères]..."`
- ✅ `"Réponse OpenAI reçue: {JSON}"`
- 📊 `"Résultat parsé: consent=X, identity_confirmed=Y"`
- ❌ `"Erreur de parsing JSON: [message]"`
- ❌ `"Erreur OpenAI: [message]"`

---

### 3. **utils/json_database.py** - Persistance
- 📁 `"JsonDatabase initialisée - contacts: data/contacts.json"`
- 💾 `"Début de la sauvegarde du résultat pour contact_id: X"`
- 🔍 `"Résultat à sauvegarder: {JSON complet}"`
- ✅ `"Résultat sauvegardé dans data/results.json (total: X résultats)"`
- 📝 `"Mise à jour du statut du contact X -> completed"`
- ✅ `"Contact X mis à jour: Jean Dupont -> completed"`
- ⚠️ `"Contact X non trouvé lors de la mise à jour du statut"`

---

### 4. **services/twilio_service.py** - API Bland.ai (déjà existant)
- 🔗 `"BlendService initialisé - Endpoint: https://api.bland.ai/v1/calls"`
- 📞 `"=== APPEL BLEND AI ==="`
- 🆔 `"Contact ID: X"`
- 📱 `"Numéro: +33XXXXXXXXX"`
- 🌐 `"Endpoint: https://api.bland.ai/v1/calls"`
- 📊 `"Status Code: 200"`
- ✅ `"Récupération du résultat pour call_id: XXX"`
- 📄 `"Result: {JSON complet de Bland.ai}"`

---

## 🔍 Exemple de flux complet dans les logs

```log
# 1. Initialisation
21:58:00 - OpenAIService initialisé
21:58:00 - JsonDatabase initialisée - contacts: data/contacts.json

# 2. Appel Bland.ai
21:58:00 - === APPEL BLEND AI ===
21:58:00 - Contact ID: 4
21:58:00 - Numéro: +33695550023
21:58:02 - Status Code: 200

# 3. Polling
21:58:07 - ⏳ Polling tentative 1/60 pour call_id: abc123
21:58:07 - Status actuel: started
21:58:13 - ⏳ Polling tentative 2/60 pour call_id: abc123
21:58:13 - Status actuel: started
...
21:59:10 - ⏳ Polling tentative 12/60 pour call_id: abc123
21:59:10 - Status actuel: completed
21:59:10 - ✅ Appel terminé! Transcript récupéré (longueur: 450 caractères)
21:59:10 - Transcript complet: assistant: Bonjour...\nuser: Oui...

# 4. Analyse OpenAI
21:59:11 - 🤖 Début de l'analyse OpenAI pour Daniel Lucas
21:59:11 - 🤖 Appel OpenAI pour analyser transcript (longueur: 450 caractères)
21:59:11 - Transcript envoyé: assistant: Bonjour, je suis une assistante...
21:59:13 - ✅ Réponse OpenAI reçue: {"consent": true, "identity_confirmed": true, "reasoning": "..."}
21:59:13 - 📊 Résultat parsé: consent=True, identity_confirmed=True
21:59:13 - ✅ Analyse OpenAI terminée: consent=True, identity=True

# 5. Sauvegarde
21:59:13 - 💾 Sauvegarde du résultat pour contact 4
21:59:13 - 💾 Début de la sauvegarde du résultat pour contact_id: 4
21:59:13 - Résultat à sauvegarder: {...complet JSON...}
21:59:13 - ✅ Résultat sauvegardé dans data/results.json (total: 6 résultats)

# 6. Mise à jour du statut
21:59:13 - ✅ Contact 4 marqué comme 'completed' (consent + identity OK)
21:59:13 - 📝 Mise à jour du statut du contact 4 -> completed
21:59:13 - ✅ Contact 4 mis à jour: Daniel Lucas -> completed
```

---

## 📁 Fichiers de logs

### `logs/app.log`
Contient tous les logs de l'application Streamlit (niveau INFO et supérieur)

### `logs/blend_api.log`
Contient tous les logs de l'API Bland.ai avec requêtes/réponses complètes

---

## 🛠️ Utilisation

### Voir les logs en temps réel
```bash
# Logs application
tail -f logs/app.log

# Logs Bland API
./watch_logs.sh
# ou
tail -f logs/blend_api.log
```

### Chercher des erreurs
```bash
# Erreurs dans app.log
grep "ERROR" logs/app.log

# Dernière erreur
python view_logs.py --last-error

# Toutes les erreurs
python view_logs.py --errors-only
```

### Suivre un appel spécifique
```bash
# Par call_id
grep "abc-123-def" logs/blend_api.log

# Par contact_id
grep "contact_id: 4" logs/app.log
```

---

## 🎯 Émojis utilisés

| Émoji | Signification |
|-------|---------------|
| ⏳ | En attente / Polling |
| ✅ | Succès |
| ❌ | Erreur |
| ⚠️ | Avertissement |
| 🤖 | OpenAI / IA |
| 📞 | Appel téléphonique |
| 💾 | Sauvegarde |
| 📝 | Mise à jour |
| 🔍 | Vérification |
| 📊 | Résultat / Stats |
| 🆔 | Identifiant |
| 📱 | Numéro de téléphone |
| 🌐 | Endpoint API |

---

## 🔧 Niveaux de logging

- **INFO**: Événements normaux du flux (début appel, fin appel, sauvegarde)
- **DEBUG**: Détails techniques (JSON complets, transcripts, statuts intermédiaires)
- **WARNING**: Situations anormales non bloquantes (timeout, transcript vide)
- **ERROR**: Erreurs bloquantes (API error, parsing error, exception)

---

## ✅ Checklist de débogage

Quand un appel échoue, vérifiez dans l'ordre :

1. ☑️ **Logs Bland API** (`logs/blend_api.log`)
   - L'appel a-t-il été initié ? (Status 200 ?)
   - Quel est le `call_id` ?
   - Le statut est-il "completed" ?
   - Y a-t-il un `concatenated_transcript` ?

2. ☑️ **Logs Application** (`logs/app.log`)
   - Le polling a-t-il détecté la fin de l'appel ?
   - Le transcript a-t-il été récupéré ?
   - L'analyse OpenAI a-t-elle été lancée ?
   - Y a-t-il eu une erreur lors de l'analyse ?

3. ☑️ **Fichiers de données**
   - Le résultat est-il dans `data/results.json` ?
   - Le statut du contact est-il à jour dans `data/contacts.json` ?

---

**Note:** Tous les logs incluent maintenant des timestamps et des émojis pour faciliter la lecture et le débogage.
