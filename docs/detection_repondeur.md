# Amélioration détection répondeur - OpenAI

**Date:** 13 novembre 2025  
**Objectif:** Éviter de valider le consentement/identité lorsqu'on tombe sur un répondeur

---

## 🐛 **Problème identifié**

### Cas d'Alexis de Saint-Jean
**Transcript:**
```
assistant: Bonjour, je suis une assistante virtuelle de VoiceCheck AI.
user: Bonjour, Alexis de Saint-Jean, Société Gouet. Je ne suis pas disponible 
      pour l'instant, n'hésitez pas à me laisser un message. Très bonne journée.
assistant: <Call ended due to voicemail detection>
```

**Résultat AVANT la correction ❌:**
- `consent`: `true`
- `identity_confirmed`: `true`
- `reasoning`: "La personne a confirmé son identité en se présentant comme Alexis de Saint-Jean"

**Le problème:** L'IA a considéré le message du répondeur comme une vraie personne qui répond !

---

## ✅ **Solution appliquée**

### Nouveau prompt système pour OpenAI

Le prompt a été amélioré avec :

1. **⚠️ RÈGLE CRITIQUE** en tête du prompt
2. **Détection explicite des répondeurs** avec indices clairs :
   - Phrases typiques: "je ne suis pas disponible", "laissez un message"
   - Marqueur technique de Bland.ai: `<Call ended due to voicemail detection>`
   - Message pré-enregistré mentionnant le nom
   - Absence d'interaction réelle

3. **Instruction claire** :
   > "Même si le message du répondeur mentionne le nom 'Alexis de Saint-Jean', 
   > ce n'est PAS une confirmation d'identité car c'est un message pré-enregistré, 
   > pas une personne réelle qui répond."

4. **Valeurs forcées pour répondeur** :
   - `consent`: **TOUJOURS false**
   - `identity_confirmed`: **TOUJOURS false**
   - `reasoning`: Doit mentionner "répondeur détecté"

---

## 🧪 **Tests de validation**

### Test 1: Répondeur détecté ✅
**Input:**
```
user: Bonjour, Alexis de Saint-Jean, Société Gouet. 
      Je ne suis pas disponible pour l'instant, 
      n'hésitez pas à me laisser un message.
assistant: <Call ended due to voicemail detection>
```

**Output:**
```json
{
  "consent": false,
  "identity_confirmed": false,
  "reasoning": "répondeur détecté"
}
```
✅ **SUCCÈS**

---

### Test 2: Vraie personne validée ✅
**Input:**
```
assistant: Conformément au règlement RGPD, acceptez-vous de poursuivre...
user: Oui.
assistant: Confirmez-vous être Daniel Lucas?
user: Oui.
```

**Output:**
```json
{
  "consent": true,
  "identity_confirmed": true,
  "reasoning": "Les réponses du client indiquent un consentement clair..."
}
```
✅ **SUCCÈS**

---

## 📊 **Indices de détection répondeur**

L'IA détecte maintenant un répondeur si elle trouve :

| Type d'indice | Exemples |
|---------------|----------|
| **Phrases typiques** | "je ne suis pas disponible", "laissez un message", "rappellerai", "boîte vocale" |
| **Marqueur technique** | `<Call ended due to voicemail detection>` (Bland.ai) |
| **Message pré-enregistré** | Présentation automatique avec nom/société |
| **Pas d'interaction** | Aucune réponse aux questions de l'assistant |
| **Ton formel** | Message standard sans réaction personnalisée |

---

## 🎯 **Impact attendu**

### Avant
- ❌ Répondeurs validés comme "consentement donné"
- ❌ Contacts marqués "completed" à tort
- ❌ Faux positifs dans les statistiques

### Après
- ✅ Répondeurs détectés et rejetés automatiquement
- ✅ Contacts restent "pending" pour rappel
- ✅ Statistiques exactes (vrais consentements uniquement)

---

## 🔄 **Prochains appels**

Les nouveaux appels bénéficieront automatiquement de cette amélioration.

Pour **ré-analyser les anciens résultats** avec répondeur :
1. Identifier les résultats suspects dans `data/results.json`
2. Vérifier la présence de marqueurs répondeur dans `transcription`
3. Mettre à jour manuellement `consent` et `identity_confirmed` à `false`
4. Mettre le contact en `pending` dans `data/contacts.json`

---

## 📝 **Fichiers modifiés**

- `services/openai_service.py` - Prompt système amélioré (40 lignes)
- `docs/detection_repondeur.md` - Cette documentation

---

## ✅ **Validation**

- ✅ Tests unitaires passés (répondeur + vraie personne)
- ✅ Prompt amélioré avec f-string pour injecter le nom
- ✅ Logging conservé (pas de régression)
- ✅ Compatible avec l'API OpenAI 2.8.0

---

**Auteur:** Assistant IA  
**Date de déploiement:** 13 novembre 2025, 22:51
