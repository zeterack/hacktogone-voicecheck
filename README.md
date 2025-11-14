# 📞 VoiceCheck AI

> Système automatisé de vérification de contacts par téléphone avec intelligence artificielle vocale

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)](https://streamlit.io/)

**🌐 Production** : [https://hacktogone-voicecheck-bg7ywpabyeghzwkwgrgddl.streamlit.app/](https://hacktogone-voicecheck-bg7ywpabyeghzwkwgrgddl.streamlit.app/)

**Équipe** : GoneToHack69  
**Sujet** : Voice AI Checker  
**Hackathon** : Hacktogone 2025 - Stade Vélodrome, Marseille

---

## 🎯 Description

**VoiceCheck AI** est une solution développée lors du hackathon Hacktogone 2025 (48h) pour automatiser la vérification de bases de contacts via des appels téléphoniques intelligents avec IA conversationnelle.

### ✨ Fonctionnalités principales

- 🤖 **Appels automatisés** - Intégration Bland AI pour des conversations naturelles en français
- 🔒 **Conformité RGPD** - Recueil explicite du consentement vocal avant toute vérification
- � **Analyse intelligente** - OpenAI GPT-3.5 pour extraire automatiquement les consentements et identités
- 📞 **Détection de répondeur** - Identification automatique des messageries vocales pour éviter les faux positifs
- 📊 **Dashboard en temps réel** - Suivi visuel des campagnes avec statistiques et graphiques
- 🔄 **Système de relances** - Gestion intelligente des contacts à rappeler
- 📥 **Export CSV** - Extraction des résultats avec colonnes détaillées (refus, répondeur, etc.)
- 📝 **Logging complet** - Traçabilité totale avec émojis pour faciliter le debug

---

## 🚀 Installation et démarrage

### Prérequis

- Python 3.11 ou supérieur
- Compte Bland AI (pour les appels réels)
- Clé API OpenAI (pour l'analyse)

### Option 1 : Avec Docker 🐳 (recommandé)

```bash
# 1. Cloner le dépôt
git clone https://github.com/zeterack/hacktogone-voicecheck.git
cd hacktogone-voicecheck

# 2. Configurer les secrets Streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Éditer .streamlit/secrets.toml avec vos clés API

# 3. Lancer avec Docker Compose
docker-compose up --build

# 4. Accéder à l'application
# 🌐 Ouvrir http://localhost:8501
```

### Option 2 : Installation locale 💻

```bash
# 1. Cloner le dépôt
git clone https://github.com/zeterack/hacktogone-voicecheck.git
cd hacktogone-voicecheck

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Linux/Mac
# .venv\Scripts\activate   # Sur Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les secrets Streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Éditer .streamlit/secrets.toml avec vos clés API Bland AI et OpenAI

# 5. Créer les dossiers nécessaires
mkdir -p data logs

# 6. Lancer l'application
streamlit run app.py

# 7. Accéder à l'application
# 🌐 Ouvrir http://localhost:8501
```

### Configuration `.streamlit/secrets.toml`

```toml
# OpenAI Configuration
OPENAI_API_KEY = "sk-VOTRE_CLE_OPENAI"

# Bland AI Configuration
BLEND_API_KEY = "org_VOTRE_CLE_BLAND_AI"
BLEND_ENDPOINT = "https://api.bland.ai/v1/calls"
```

> ⚠️ **Sécurité** : Ne jamais commiter `secrets.toml` ! Il est déjà dans `.gitignore`.

### Option 3 : Déploiement sur Streamlit Cloud ☁️

1. **Pusher le code sur GitHub** (sans secrets.toml)
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

2. **Créer une app sur Streamlit Cloud**
   - Aller sur [share.streamlit.io](https://share.streamlit.io)
   - Connecter votre dépôt GitHub
   - Sélectionner `hacktogone-voicecheck`
   - Fichier principal : `app.py`

3. **Configurer les secrets dans Streamlit Cloud**
   - Dans les paramètres de l'app, section "Secrets"
   - Copier le contenu de votre `secrets.toml` local
   - Sauvegarder

4. **Déployer** 🚀
   - L'app se déploie automatiquement
   - URL de production : [https://hacktogone-voicecheck-bg7ywpabyeghzwkwgrgddl.streamlit.app/](https://hacktogone-voicecheck-bg7ywpabyeghzwkwgrgddl.streamlit.app/)

> 💡 **Astuce** : Les secrets Streamlit Cloud sont chiffrés et ne sont jamais exposés dans les logs.

---

## 💡 Utilisation

### 1. Importer des contacts

1. Préparer un fichier CSV avec les colonnes : `nom,prenom,telephone`
2. Dans l'onglet **"Campagne"**, cliquer sur "Choisir un fichier CSV"
3. Vérifier l'aperçu et cliquer sur "Ajouter à la base"

### 2. Lancer une campagne

1. Dans l'onglet **"Campagne"**, section "Lancer la campagne"
2. Cliquer sur **"🚀 Lancer la campagne"**
3. L'application appellera automatiquement tous les contacts en attente
4. Suivre la progression en temps réel

### 3. Consulter les résultats

1. Onglet **"Dashboard"** : Statistiques globales et graphiques
2. Section **"Résultats détaillés"** : Tableau complet avec colonnes :
   - Consentement, Refus explicite, Identité confirmée
   - Répondeur détecté, Raison de la décision
3. Onglet **"Export"** : Télécharger les résultats en CSV

### 4. Relancer les contacts

Dans l'onglet **"Campagne"**, section "Relances manuelles" :
- Les contacts sans réponse claire ou avec répondeur apparaissent automatiquement
- Cliquer sur **"📞 Relancer ces contacts"** pour les remettre en file d'attente

## 📋 Fonctionnalités

### 1. Dashboard
- Vue d'ensemble des statistiques
- Taux de consentement et confirmation
- Graphiques de répartition
- Résultats détaillés

### 2. Campagne
- Import de contacts (CSV)
- Lancement d'appels automatisés
- Système de relances manuelles
- Suivi en temps réel

### 3. Export
- Export CSV des résultats
- Données complètes des appels
- Statistiques détaillées

---

## 🔄 Flux d'appel automatisé

L'application effectue un appel unique en 2 étapes vocales + 1 analyse IA :

### 📞 Étape 1 : Consentement RGPD (Bland AI)

```
IA: "Bonjour, conformément au règlement RGPD, acceptez-vous de 
     poursuivre cet échange pour la vérification de vos données?"
```

- ✅ **Oui** → Passage à l'étape 2
- ❌ **Non** → Fin de l'appel, contact à relancer
- ⚪ **Pas de réponse** → À rappeler

### 🔍 Étape 2 : Vérification d'identité (Bland AI)

```
IA: "Confirmez-vous être [Prénom] [Nom]?"
```

- ✅ **Oui / C'est moi** → Identité confirmée
- ❌ **Non** → Identité rejetée
- ⚪ **Pas de réponse** → À rappeler

### 🧠 Étape 3 : Analyse automatique (OpenAI GPT-3.5)

- 📝 Récupération du transcript complet (polling toutes les 5s)
- 🤖 Envoi à OpenAI pour extraction structurée :
  - `consent`: `true`/`false`/`null`
  - `identity_confirmed`: `true`/`false`/`null`
  - `reasoning`: Explication de la décision
- 📞 **Détection de répondeur** : Si "je ne suis pas disponible" détecté → `consent=false`
- 💾 Sauvegarde dans `data/results.json`

---

## 📁 Structure du projet

```
hacktogone-voicecheck/
├── 📄 app.py                       # Application Streamlit principale
├── 📦 requirements.txt             # Dépendances Python (streamlit, openai>=2.8.0, requests)
├── 🐳 Dockerfile                   # Image Docker
├── 🐳 docker-compose.yml           # Orchestration multi-conteneurs
├── 🔐 .env.example                 # Template de configuration
├── 📚 docs/                        # Documentation complète
│   ├── technical_doc.md           # Architecture détaillée
│   ├── detection_repondeur.md     # Logique de détection voicemail
│   ├── logging_enhanced.md        # Système de logs avec émojis
│   └── quick_start.md             # Guide de démarrage rapide
├── 🤖 services/
│   ├── twilio_service.py          # BlendService - API Bland AI
│   ├── openai_service.py          # Analyse transcripts avec GPT-3.5
│   └── analysis_service.py        # Statistiques et métriques
├── 🛠️ utils/
│   ├── json_database.py           # CRUD sur fichiers JSON
│   ├── csv_handler.py             # Import/Export CSV avec format FR
│   └── config.py                  # Configuration centralisée (.env)
└── 💾 data/
    ├── contacts.json              # Base de contacts (gitignored)
    ├── results.json               # Résultats des appels (gitignored)
    ├── contacts.example.json      # Fichier vide pour référence
    └── sample_contacts.csv        # Exemple de format CSV
```

> **Note :** Les fichiers sensibles (`contacts.json`, `results.json`, `.env`, `logs/`) sont exclus du dépôt Git.

## 📊 Format CSV pour l'import

```csv
nom,prenom,telephone
Dupont,Jean,+33612345678
Martin,Marie,+33687654321
```

**Colonnes obligatoires :**
- `nom` : Nom de famille
- `prenom` : Prénom
- `telephone` : Numéro au format international (+33...)

---

## 🛠️ Stack technique

| Technologie | Version | Usage |
|------------|---------|-------|
| **Python** | 3.11+ | Langage principal |
| **Streamlit** | 1.29.0 | Interface web interactive |
| **Bland AI** | API v1 | Appels vocaux avec IA conversationnelle |
| **OpenAI** | 2.8.0+ | Analyse transcripts (GPT-3.5-turbo) |
| **Pandas** | 2.1.3 | Manipulation CSV et DataFrames |
| **Requests** | 2.31.0 | Client HTTP pour APIs REST |
| **Docker** | - | Conteneurisation multi-environnements |

---

## 📊 Exemple de résultats exportés

| Nom | Prénom | Téléphone | Consentement | Refus explicite | Identité confirmée | Répondeur détecté | Raison |
|-----|--------|-----------|--------------|-----------------|-------------------|-------------------|--------|
| Dupont | Jean | +33612345678 | ✅ True | ❌ False | ✅ True | ❌ False | Consentement et identité confirmés |
| Martin | Sophie | +33698765432 | ❌ False | ❌ False | ❌ False | ✅ True | répondeur détecté |
| Bernard | Marc | +33687654321 | ❌ False | ✅ True | ❌ False | ❌ False | Refus explicite du consentement |
---

## 🤝 Contribution

Développé lors du hackathon Blueway 2025 (20h).

**Équipe :**
- Développement IA vocale
- Intégration API Bland AI + OpenAI
- Conformité RGPD

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📞 Support

- 📚 Documentation complète : `docs/`
- 🐛 Rapporter un bug : [GitHub Issues](https://github.com/zeterack/hacktogone-voicecheck/issues)
- 💬 Questions : Ouvrir une discussion GitHub

---

**Made with ❤️ during Hackathon 2025**
