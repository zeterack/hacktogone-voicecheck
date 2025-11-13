# 📞 VoiceCheck AI

Système automatisé de vérification de contacts par téléphone avec intelligence artificielle.

## 🎯 Description

VoiceCheck AI est une application développée pour un hackathon de 20h permettant de vérifier automatiquement la validité d'une base de contacts via des appels téléphoniques intelligents. Le système intègre :

- ✅ Conformité RGPD avec consentement explicite vocal
- 🤖 Appels automatisés via Blend AI
- 🧠 Analyse des transcripts avec OpenAI GPT-3.5
- 📊 Dashboard de suivi en temps réel
- 🔄 Système de relances manuelles
- 📥 Export des résultats en CSV

## 🚀 Démarrage rapide

### Avec Docker (recommandé)

```bash
# 1. Copier le fichier d'environnement
cp .env.example .env

# 2. Lancer avec Docker Compose
docker-compose up --build

# 3. Accéder à l'application
# Ouvrir http://localhost:8501
```

### Sans Docker

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Copier le fichier d'environnement
cp .env.example .env

# 3. Lancer l'application
streamlit run app.py
```

## 🧪 Mode MOCK (sans API)

Par défaut, l'application fonctionne en **mode MOCK** qui simule les appels Twilio et la reconnaissance vocale OpenAI. C'est idéal pour tester sans frais et sans clés API.

**Caractéristiques du mode MOCK :**
- ✅ Simulation de 70% de consentements acceptés
- ✅ Simulation de 80% d'identités confirmées
- ✅ Aucun vrai appel téléphonique effectué
- ✅ Temps de réponse simulés réalistes

Pour activer le mode MOCK, dans le fichier `.env` :
```
USE_MOCK_SERVICES=True
```

## 🔑 Mode RÉEL (avec API Blend AI et OpenAI)

Pour utiliser les vraies API :

1. Obtenir les clés API :
   - Compte Blend AI : https://app.bland.ai (pour les appels téléphoniques)
   - Clé OpenAI : https://platform.openai.com (pour l'analyse des transcripts)

2. Configurer le fichier `.env` :
```bash
USE_MOCK_SERVICES=False
BLEND_API_KEY=votre_clé_blend
BLEND_ENDPOINT=https://api.bland.ai/v1/calls
OPENAI_API_KEY=sk-...
```

3. Relancer l'application

**Note importante**: En mode réel, l'application :
- Initie les appels via Blend AI avec un prompt personnalisé
- Attend la fin de l'appel et récupère le transcript (polling toutes les 5 secondes)
- Envoie le transcript à OpenAI GPT-3.5 pour extraire le consentement RGPD et la confirmation d'identité
- Sauvegarde les résultats dans la base de données JSON

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

## 🔄 Processus d'appel

Le système effectue un appel unique en deux étapes vocales :

### Étape 1 : Consentement RGPD (vocal)
- Message vocal : "Conformément au règlement RGPD, acceptez-vous de poursuivre cet échange ?"
- L'utilisateur répond oralement : "oui" / "non"
- Blend AI enregistre la réponse audio
- Pas de réponse = À rappeler

### Étape 2 : Vérification d'identité (IA vocale)
- Question : "Confirmez-vous être [Prénom] [Nom] ?"
- L'utilisateur répond oralement : "oui" / "non" / "c'est moi"
- Blend AI enregistre la conversation complète

### Étape 3 : Analyse avec OpenAI
- Récupération du transcript complet de la conversation
- Envoi à OpenAI GPT-3.5 pour analyse
- Extraction automatique du consentement et de la confirmation d'identité
- Sauvegarde des résultats dans la base de données

## 📁 Structure du projet

```
hacktogone/
├── app.py                          # Application Streamlit principale
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Configuration Docker
├── docker-compose.yml              # Orchestration Docker
├── .env.example                    # Exemple de configuration
├── services/
│   ├── twilio_service.py          # Service Twilio réel
│   ├── twilio_mock_service.py     # Service Twilio simulé
│   ├── speech_service.py          # Service OpenAI Whisper réel
│   ├── speech_mock_service.py     # Service OpenAI simulé
│   └── analysis_service.py        # Service d'analyse
├── utils/
│   ├── json_database.py           # Gestion base de données JSON
│   ├── csv_handler.py             # Import/Export CSV
│   └── config.py                  # Configuration centralisée
└── data/
    ├── contacts.json              # Base de contacts
    ├── results.json               # Résultats des appels
    └── sample_contacts.csv        # Exemple de CSV
```

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

## 🛠️ Technologies

- **Python 3.11** : Langage principal
- **Streamlit** : Interface web
- **Blend AI** : API d'appels téléphoniques avec IA conversationnelle
- **OpenAI GPT-3.5** : Analyse des transcripts et extraction d'informations
- **Docker** : Conteneurisation
- **JSON** : Base de données légère
- **Requests** : Client HTTP pour les APIs

## 📝 Licence

Projet développé dans le cadre d'un hackathon de 20h.

## 👥 Support

Pour toute question ou problème, consultez la documentation dans le dossier `docs/`.
