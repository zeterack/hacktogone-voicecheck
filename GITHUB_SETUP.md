# 🚀 Guide de publication sur GitHub

## Étapes pour publier sur GitHub (compte zeterack)

### 1. Créer le dépôt sur GitHub
1. Va sur https://github.com/new
2. Connecte-toi avec ton compte **zeterack**
3. Remplis les informations :
   - **Repository name** : `voicecheck-ai` ou `hacktogone-voicecheck`
   - **Description** : "🤖 VoiceCheck AI - Vérification automatisée des contacts avec appels vocaux IA (Bland AI + OpenAI) et conformité RGPD"
   - **Visibilité** : 
     - ✅ **Public** (si tu veux le partager)
     - ⚠️ **Private** (si tu veux le garder privé)
   - ⚠️ **NE PAS** cocher "Initialize with README" (on a déjà un README)
4. Clique sur **Create repository**

### 2. Lier ton dépôt local avec GitHub

Une fois le dépôt créé sur GitHub, copie l'URL qui apparaît (format : `https://github.com/zeterack/REPO_NAME.git`)

Puis exécute ces commandes dans ton terminal :

```bash
cd /home/ldaniel/Documents/projet/blueway/hacktogone

# Ajouter le remote GitHub
git remote add origin https://github.com/zeterack/REPO_NAME.git

# Renommer la branche principale en 'main' (convention GitHub)
git branch -M main

# Pousser le code sur GitHub
git push -u origin main
```

### 3. Authentification GitHub

Si c'est la première fois que tu push sur GitHub depuis cet ordinateur :

**Option A : Avec Personal Access Token (recommandé)**
1. Va sur https://github.com/settings/tokens
2. Clique sur "Generate new token" → "Generate new token (classic)"
3. Donne un nom : "VoiceCheck AI - Laptop"
4. Sélectionne les permissions : **repo** (toutes les cases)
5. Clique sur "Generate token"
6. **COPIE LE TOKEN** (tu ne pourras plus le revoir)
7. Quand Git demande le mot de passe, colle le TOKEN (pas ton mot de passe GitHub)

**Option B : Avec SSH (plus rapide après configuration)**
```bash
# Générer une clé SSH
ssh-keygen -t ed25519 -C "ldaniel@blueway.fr"

# Copier la clé publique
cat ~/.ssh/id_ed25519.pub

# Aller sur https://github.com/settings/keys
# Cliquer "New SSH key", coller la clé
# Puis utiliser l'URL SSH au lieu de HTTPS :
git remote set-url origin git@github.com:zeterack/REPO_NAME.git
```

### 4. Vérifier que ça a marché

```bash
# Vérifier le remote
git remote -v

# Voir l'état
git status
```

Ensuite, va sur `https://github.com/zeterack/REPO_NAME` pour voir ton code en ligne ! 🎉

---

## 📝 Commits futurs

Pour envoyer de nouvelles modifications sur GitHub :

```bash
# Voir les fichiers modifiés
git status

# Ajouter les modifications
git add .

# Créer un commit
git commit -m "Description des changements"

# Envoyer sur GitHub
git push
```

---

## ⚠️ Fichiers ignorés (pour ta sécurité)

Les fichiers suivants ne seront **jamais** envoyés sur GitHub (grâce au `.gitignore`) :

- ❌ `.env` - Clés API (BLAND_API_KEY, OPENAI_API_KEY)
- ❌ `data/contacts.json` - Données personnelles des contacts
- ❌ `data/results.json` - Résultats des appels
- ❌ `logs/` - Logs avec informations sensibles
- ❌ `.venv/` - Environnement virtuel Python

À la place, on a créé :
- ✅ `.env.example` - Template pour les variables d'environnement
- ✅ `data/contacts.example.json` - Fichier vide exemple
- ✅ `data/results.example.json` - Fichier vide exemple

---

## 🔐 Sécurité

**IMPORTANT :** Vérifie que ton fichier `.env` n'est PAS dans le dépôt :

```bash
git ls-files | grep .env
# Si ça affiche ".env", c'est un problème !
# Sinon, c'est bon ✅
```

Si tu as accidentellement commité `.env`, supprime-le IMMÉDIATEMENT :

```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

Puis **régénère toutes tes clés API** car elles sont maintenant publiques !

---

**Ton dépôt est prêt ! 🚀**
