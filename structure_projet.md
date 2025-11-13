# Structure du Projet VoiceCheck AI

## 📁 Arborescence Complète

```
voicecheck-ai/
│
├── 📄 README.md                          # Documentation principale du projet
├── 📄 requirements.txt                   # Dépendances Python
├── 📄 .env.example                       # Exemple de variables d'environnement
├── 📄 .gitignore                         # Fichiers à ignorer par Git
│
├── � Dockerfile                         # Image Docker pour l'application
├── 🐳 docker-compose.yml                 # Orchestration Docker Compose
│
├── �📂 app.py                             # ⭐ APPLICATION STREAMLIT PRINCIPALE
│
├── 📂 services/                          # Services métier
│   ├── __init__.py
│   ├── twilio_service.py                 # Gestion des appels Twilio (DTMF + TTS)
│   ├── twilio_mock_service.py            # 🎭 Mock de Twilio (pour tests sans API)
│   ├── speech_service.py                 # Transcription vocale (Whisper)
│   ├── speech_mock_service.py            # 🎭 Mock de OpenAI Whisper (pour tests sans API)
│   └── analysis_service.py               # Analyse des réponses (détection oui/non)
│
├── 📂 utils/                             # Utilitaires
│   ├── __init__.py
│   ├── json_database.py                  # Gestion CRUD des fichiers JSON
│   ├── csv_handler.py                    # Import/Export CSV
│   └── config.py                         # Configuration (chargement .env)
│
├── 📂 data/                              # Données et base de données JSON
│   ├── contacts.json                     # Base de données des contacts (vide au départ)
│   ├── results.json                      # Résultats des appels (vide au départ)
│   └── sample_contacts.csv               # Fichier CSV exemple pour tests
│
├── 📂 assets/                            # Ressources visuelles
│   └── logo.png                          # Logo VoiceCheck AI (optionnel)
│
└── 📂 docs/                              # Documentation
    ├── user_guide.md                     # Guide utilisateur
    ├── technical_doc.md                  # Documentation technique
    └── api_setup.md                      # Guide de configuration des APIs
```

---

## 📄 Détail des Fichiers Principaux

### 1. **app.py** (Application Streamlit)
```python
"""
Application Streamlit principale
- Page d'import CSV
- Lancement de campagne d'appels
- Dashboard avec statistiques en temps réel
- Bouton de rappel des non-répondus
- Export des résultats
"""
```

**Sections de l'app** :
- 🎨 Configuration de la page (`st.set_page_config`)
- 📂 Sidebar : Import CSV
- 📊 Tab 1 : Dashboard (statistiques + graphiques)
- 📞 Tab 2 : Campagne (bouton lancer + bouton rappeler)
- 📥 Tab 3 : Export (télécharger CSV/PDF)

---

### 2. **services/twilio_service.py**
```python
"""
Gestion des appels Twilio avec système hybride :
- Étape 1 : Demande consentement RGPD (DTMF)
- Étape 2 : Vérification identité (Enregistrement vocal)
"""
```

**Fonctions principales** :
- `create_consent_call(telephone, prenom, nom)` → Génère TwiML pour consentement
- `handle_consent(digit_pressed)` → Traite réponse DTMF (1 ou 2)
- `handle_identity_with_ai(prenom, nom)` → Lance enregistrement vocal
- `initiate_call(contact)` → Lance un appel Twilio

---

### 3. **services/speech_service.py**
```python
"""
Service de transcription et analyse vocale
- Utilise OpenAI Whisper pour transcription
- Télécharge les enregistrements depuis Twilio
"""
```

**Fonctions principales** :
- `transcribe_audio(recording_url)` → Télécharge audio et transcrit avec Whisper
- `download_recording(url)` → Télécharge fichier audio depuis Twilio

---

### 4. **services/analysis_service.py**
```python
"""
Analyse intelligente des réponses vocales
- Détection de "oui" / "non"
- Regex ou GPT selon configuration
"""
```

**Fonctions principales** :
- `analyze_response(text)` → Analyse texte et retourne statut (VALIDE/INVALIDE/NON_CONFIRME)
- `detect_positive_response(text)` → Détecte mots positifs
- `detect_negative_response(text)` → Détecte mots négatifs

---

### 5. **utils/json_database.py**
```python
"""
Classe pour gérer les fichiers JSON comme base de données
- CRUD complet (Create, Read, Update, Delete)
- Gestion de contacts.json et results.json
"""
```

**Classe** :
```python
class JsonDatabase:
    def load()           # Charge les données
    def save(data)       # Sauvegarde les données
    def add(item)        # Ajoute un élément
    def update(id, updates) # Met à jour un élément
    def get_by_status(status) # Filtre par statut
    def delete(id)       # Supprime un élément
```

---

### 6. **utils/csv_handler.py**
```python
"""
Import et export de fichiers CSV
- Parse CSV uploadé
- Convertit en format JSON pour contacts.json
- Exporte results.json en CSV
"""
```

**Fonctions principales** :
- `parse_csv(uploaded_file)` → Parse fichier CSV uploadé
- `import_contacts_from_csv(file)` → Importe contacts dans JSON
- `export_results_to_csv(results)` → Exporte résultats en CSV

---

### 7. **utils/config.py**
```python
"""
Configuration centralisée
- Charge variables d'environnement depuis .env
- Valide les clés API
- Active le mode MOCK si pas de clés
"""
```

**Variables** :
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `OPENAI_API_KEY`
- `USE_MOCK_SERVICES` (True si pas de clés API)

---

### 8. **services/twilio_mock_service.py** 🎭
```python
"""
Mock du service Twilio pour développement sans API
- Simule les appels téléphoniques
- Génère des réponses aléatoires (consentement + identité)
- Permet de tester l'application sans crédits Twilio
"""
```

**Fonctions principales** :
- `mock_create_call(contact)` → Simule un appel et retourne un résultat
- `mock_consent_response()` → Génère une réponse DTMF aléatoire (1 ou 2)
- `mock_identity_response()` → Génère une réponse vocale simulée ("oui" ou "non")
- `simulate_call_delay()` → Ajoute un délai réaliste (2-5 secondes)

**Comportement** :
- 70% de consentement accepté (touche 1)
- 80% d'identité confirmée (dit "oui")
- 10% de non-répondus
- Logs détaillés de la simulation

---

### 9. **services/speech_mock_service.py** 🎭
```python
"""
Mock du service OpenAI Whisper pour développement sans API
- Simule la transcription audio → texte
- Génère des réponses vocales réalistes
- Permet de tester l'application sans clé OpenAI
"""
```

**Fonctions principales** :
- `mock_transcribe_audio(recording_url)` → Retourne transcription simulée
- `mock_voice_responses()` → Liste de réponses possibles
- Réponses variées : "oui c'est moi", "non pas du tout", "oui exact", etc.

**Comportement** :
- Sélection aléatoire de réponses prédéfinies
- Simulation de délai de transcription (1-2 secondes)
- Logs de la transcription mockée

---

## 📊 Structure des Données JSON

### **contacts.json**
```json
[
  {
    "id": 1,
    "nom": "Dupont",
    "prenom": "Jean",
    "telephone": "+33612345678",
    "entreprise": "TechCorp",
    "email": "jean.dupont@techcorp.fr",
    "statut": "non_appele",
    "tentatives": 0,
    "date_import": "2025-11-13T10:30:00"
  }
]
```

### **results.json**
```json
[
  {
    "id": 1,
    "contact_id": 1,
    "nom": "Dupont",
    "prenom": "Jean",
    "telephone": "+33612345678",
    "statut": "valide",
    "consentement": true,
    "date_appel": "2025-11-13T14:25:30",
    "duree_appel": 18,
    "tentative": 1,
    "transcription": "oui c'est bien moi",
    "cycle": 1,
    "etape_atteinte": "verification_identite"
  }
]
```

### **Statuts possibles** :
- ✅ `valide` : Consentement + Identité confirmée
- ❌ `invalide` : Identité refusée
- ❌ `refus` : Consentement refusé (touche 2)
- ⚠️ `non_confirme` : Pas de réponse / timeout
- ❌ `inactif` : Numéro inexistant

---

## 📄 Fichiers de Configuration

### **.env.example**
```env
# Twilio Configuration (laisser vide pour mode MOCK)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# OpenAI Configuration (laisser vide pour mode MOCK)
OPENAI_API_KEY=

# Application Configuration
APP_PORT=8501
DEBUG=True
USE_MOCK_SERVICES=True  # True = utilise les mocks, False = utilise les vraies API
```

**💡 Mode MOCK activé par défaut** :
- Si les clés API sont vides, le système utilise automatiquement les services mockés
- Aucune configuration requise pour démarrer
- Idéal pour développement et démonstration sans crédits API

### **requirements.txt**
```txt
streamlit==1.29.0
twilio==8.11.0
openai==1.6.0
pandas==2.1.4
plotly==5.18.0
python-dotenv==1.0.0
requests==2.31.0
```

### **.gitignore**
```
# Environment
.env
venv/
__pycache__/

# Data
data/contacts.json
data/results.json
*.log

# Temporary
temp_recordings/
*.wav

# Docker
.dockerignore
```

---

## 🐳 Fichiers Docker

### **Dockerfile**
```dockerfile
# Image Python officielle
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances système nécessaires pour audio
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p data temp_recordings

# Exposer le port Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Commande de démarrage
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **docker-compose.yml**
```yaml
version: '3.8'

services:
  voicecheck-ai:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: voicecheck-ai
    ports:
      - "8501:8501"
    volumes:
      # Montage du code pour développement (hot reload)
      - ./app.py:/app/app.py
      - ./services:/app/services
      - ./utils:/app/utils
      # Montage des données (persistance)
      - ./data:/app/data
      # Montage des enregistrements temporaires
      - ./temp_recordings:/app/temp_recordings
    environment:
      # Variables d'environnement depuis .env
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
      - TWILIO_PHONE_NUMBER=${TWILIO_PHONE_NUMBER}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - APP_PORT=8501
      - DEBUG=${DEBUG:-False}
    env_file:
      - .env
    restart: unless-stopped
    networks:
      - voicecheck-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  voicecheck-network:
    driver: bridge

volumes:
  voicecheck-data:
    driver: local
```

### **.dockerignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Data
data/contacts.json
data/results.json
temp_recordings/

# Git
.git
.gitignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# Documentation
docs/
*.md
!README.md

# Logs
*.log

# Environment
.env
.env.local
```

---

## 📝 Fichier CSV d'Exemple

### **data/sample_contacts.csv**
```csv
nom,prenom,telephone,entreprise,email
Dupont,Jean,+33612345678,TechCorp,jean.dupont@techcorp.fr
Martin,Sophie,+33623456789,InnoSoft,sophie.martin@innosoft.fr
Bernard,Pierre,+33634567890,DataFlow,pierre.bernard@dataflow.fr
Petit,Marie,+33645678901,CloudTech,marie.petit@cloudtech.fr
Dubois,Luc,+33656789012,WebSolutions,luc.dubois@websolutions.fr
```

---

## 🎨 Interface Streamlit (app.py)

### Structure des Tabs

**Tab 1 - 📊 Dashboard**
```
┌─────────────────────────────────────────────────────┐
│  Métriques (3 colonnes)                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Total   │  │  Appels  │  │   Taux   │          │
│  │ Contacts │  │ Effectués│  │ Validité │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│                                                      │
│  Graphiques                                          │
│  ┌────────────────────┐  ┌────────────────────┐    │
│  │   Répartition      │  │   Évolution         │    │
│  │   des statuts      │  │   dans le temps     │    │
│  │   (Pie Chart)      │  │   (Line Chart)      │    │
│  └────────────────────┘  └────────────────────┘    │
│                                                      │
│  Tableau des résultats détaillés                    │
│  ┌───────────────────────────────────────────┐     │
│  │ Nom │ Prénom │ Téléphone │ Statut │ ...  │     │
│  └───────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

**Tab 2 - 📞 Campagne**
```
┌─────────────────────────────────────────────────────┐
│  Boutons d'action (2 colonnes)                       │
│  ┌──────────────────────┐  ┌──────────────────────┐│
│  │  🚀 Lancer           │  │  🔄 Rappeler les     ││
│  │  la campagne         │  │  non-répondus (15)   ││
│  └──────────────────────┘  └──────────────────────┘│
│                                                      │
│  Statut en temps réel                                │
│  ┌────────────────────────────────────────────┐    │
│  │  📞 Appel en cours : Jean Dupont           │    │
│  │  ⏱️  Durée : 12s                            │    │
│  │  📊 Progression : 45/100 contacts          │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Logs des appels                                     │
│  ┌────────────────────────────────────────────┐    │
│  │  14:25:30 - Jean Dupont : ✅ VALIDE        │    │
│  │  14:26:15 - Sophie Martin : ❌ REFUS       │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**Tab 3 - 📥 Export**
```
┌─────────────────────────────────────────────────────┐
│  Options d'export                                    │
│  ┌──────────────────────┐  ┌──────────────────────┐│
│  │  📄 Télécharger CSV  │  │  📋 Télécharger PDF  ││
│  └──────────────────────┘  └──────────────────────┘│
│                                                      │
│  Filtres                                             │
│  ☑️ Valides  ☑️ Invalides  ☑️ Refus  ☑️ Non confirmés│
│                                                      │
│  Aperçu des données à exporter                       │
│  ┌───────────────────────────────────────────┐     │
│  │ 45 contacts valides                        │     │
│  │ 15 contacts non confirmés                  │     │
│  │ 10 refus de consentement                   │     │
│  └───────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

---

## 🔄 Flux de Données

```
1. Import CSV
   └─> parse_csv()
       └─> contacts.json

2. Lancer Campagne
   └─> config.py vérifie USE_MOCK_SERVICES
       │
       ├─> 🎭 MODE MOCK (si pas de clés API):
       │   └─> Pour chaque contact:
       │       ├─> twilio_mock_service.mock_create_call()
       │       │   ├─> mock_consent_response() → Simule DTMF (1 ou 2)
       │       │   └─> mock_identity_response() → Simule réponse vocale
       │       ├─> speech_mock_service.mock_transcribe_audio()
       │       │   └─> Retourne transcription simulée
       │       └─> analysis_service.analyze_response()
       │           └─> Statut: VALIDE/INVALIDE/REFUS
       │
       └─> 🌐 MODE RÉEL (avec clés API):
           └─> Pour chaque contact:
               ├─> twilio_service.create_consent_call()
               │   └─> ÉTAPE 1: Message consentement + DTMF
               │       ├─> Si touche 1 : handle_consent()
               │       │   └─> handle_identity_with_ai()
               │       │       └─> ÉTAPE 2: Enregistrement vocal
               │       │           └─> speech_service.transcribe_audio()
               │       │               └─> analysis_service.analyze_response()
               │       │                   └─> Statut: VALIDE/INVALIDE
               │       └─> Si touche 2 : Statut: REFUS
               └─> Sauvegarde dans results.json

3. Dashboard Temps Réel
   └─> Rafraîchissement auto avec st.rerun()
       └─> Lecture de results.json
           └─> Affichage stats + graphiques
           └─> Indicateur MODE MOCK ou MODE RÉEL

4. Export
   └─> Lecture de results.json
       └─> csv_handler.export_results_to_csv()
           └─> Téléchargement fichier
```

---

## 🚀 Commandes de Démarrage

### Option 1 : Lancement avec Docker Compose (RECOMMANDÉ)

```bash
# 1. Copier et configurer .env
cp .env.example .env
# Éditer .env avec vos clés API (Twilio, OpenAI)

# 2. Construire et lancer l'application
docker-compose up --build

# 3. Accéder à l'application
# Ouvrir http://localhost:8501 dans le navigateur
```

**Commandes utiles Docker** :
```bash
# Lancer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter l'application
docker-compose down

# Redémarrer après modifications du code
docker-compose restart

# Reconstruire l'image après changement de dépendances
docker-compose up --build
```

### Option 2 : Lancement Local (Sans Docker)

```bash
# 1. Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Copier et configurer .env
cp .env.example .env
# Éditer .env avec vos clés API

# 4. Lancer l'application
streamlit run app.py
```

### Test avec données exemple
```bash
# L'application inclut data/sample_contacts.csv
# Vous pouvez l'utiliser pour tester ou uploader votre propre CSV
```

---

## ✅ Points Clés de l'Architecture

1. ✅ **Séparation des responsabilités** : Services distincts pour Twilio, Speech, Analyse
2. ✅ **Base de données simple** : JSON pour facilité de debug et hackathon
3. ✅ **Interface intuitive** : Streamlit avec tabs clairs
4. ✅ **Temps réel** : Mise à jour live des résultats
5. ✅ **RGPD compliant** : Consentement DTMF en étape 1
6. ✅ **IA vocale** : Reconnaissance naturelle en étape 2
7. ✅ **Extensible** : Architecture modulaire facile à améliorer
8. ✅ **Dockerisé** : Déploiement en une commande avec Docker Compose
9. ✅ **Hot reload** : Modifications de code prises en compte instantanément
10. ✅ **Persistance** : Données sauvegardées dans volumes Docker
11. ✅ **🎭 Services mockés** : Fonctionne SANS clés API (Twilio + OpenAI)
12. ✅ **Mode développement** : Testable immédiatement sans configuration

---

## 🎭 Mode MOCK - Fonctionnement

### Activation automatique
Le mode MOCK s'active automatiquement si :
- `USE_MOCK_SERVICES=True` dans `.env`
- OU si les clés API sont vides/invalides

### Comportement des Mocks

**Twilio Mock** :
- ✅ Simule des appels téléphoniques avec délais réalistes (2-5 secondes)
- ✅ 70% d'acceptation du consentement (touche 1)
- ✅ 80% de confirmation d'identité (réponse "oui")
- ✅ 10% de non-répondus aléatoires
- ✅ Logs détaillés de chaque étape simulée

**OpenAI Mock** :
- ✅ Simule la transcription Whisper
- ✅ Banque de réponses réalistes : "oui c'est moi", "non pas du tout", "oui exact", etc.
- ✅ Sélection aléatoire pour variété des résultats
- ✅ Délai de transcription simulé (1-2 secondes)

### Indicateurs visuels
- 🎭 Badge "MODE MOCK" visible dans l'interface Streamlit
- 💡 Message d'information au lancement
- 📊 Statistiques générées de manière réaliste

### Passage au mode RÉEL
Pour utiliser les vraies API :
1. Ajouter les clés dans `.env`
2. Changer `USE_MOCK_SERVICES=False`
3. Redémarrer l'application

---

## 📌 Prochaines Étapes (Après Validation)

1. Générer tous les fichiers de la structure
2. Implémenter `app.py` avec interface Streamlit
3. Coder les services (Twilio, Speech, Analysis)
4. Créer les utilitaires (JSON DB, CSV Handler)
5. Ajouter fichiers de config et documentation
6. Tester le flux complet avec sample_contacts.csv

---

**Prêt à recevoir vos retours pour ajustements ! 🎯**
