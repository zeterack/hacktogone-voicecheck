# 🚀 Guide de démarrage rapide - VoiceCheck AI

## Prérequis

- Python 3.11+
- Docker (optionnel)
- Git

---

## ⚡ Installation rapide (5 minutes)

### Option 1 : Avec Docker (recommandé)

```bash
# 1. Cloner le projet
cd /chemin/vers/projet

# 2. Copier la configuration
cp .env.example .env

# 3. Lancer avec Docker
docker-compose up --build

# 4. Accéder à l'application
# Ouvrir http://localhost:8501
```

### Option 2 : Sans Docker

```bash
# 1. Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Copier la configuration
cp .env.example .env

# 4. Lancer l'application
streamlit run app.py

# 5. Accéder à l'application
# Ouvrir http://localhost:8501
```

---

## 🎯 Premier test (Mode MOCK)

Par défaut, l'application fonctionne en **mode MOCK** (simulation sans vraies API).

### 1. Importer des contacts

Dans l'onglet **"📞 Campagne"** :

1. Cliquez sur **"Choisir un fichier CSV"**
2. Sélectionnez `data/sample_contacts.csv` (fichier d'exemple fourni)
3. Cliquez sur **"Ajouter à la base"**

✅ 5 contacts d'exemple sont ajoutés !

### 2. Lancer une campagne d'appels

1. Dans la section **"3. Lancer les appels"**
2. Cliquez sur **"🚀 Lancer la campagne d'appels"**
3. Observez la progression en temps réel

⏱️ Les appels sont simulés (1-2 secondes par contact)

### 3. Voir les résultats

Dans l'onglet **"📊 Dashboard"** :

- **Contacts totaux** : 5
- **Appels effectués** : 5
- **Consentements** : ~3-4 (70% de succès simulé)
- **Identités confirmées** : ~3-4 (80% de succès simulé)
- **Taux de succès global** : ~60-70%

### 4. Export des résultats

Dans l'onglet **"📥 Export"** :

1. Visualisez le tableau des résultats
2. Cliquez sur **"📥 Télécharger en CSV"**
3. Ouvrez le fichier `voicecheck_results.csv`

---

## 🔑 Passer en mode RÉEL (avec API)

### Étape 1 : Obtenir les clés API

#### Blend AI (Appels téléphoniques)
1. Créer un compte sur https://app.bland.ai
2. Aller dans **Settings → API Keys**
3. Copier votre clé API

#### OpenAI (Analyse des transcripts)
1. Créer un compte sur https://platform.openai.com
2. Aller dans **API Keys**
3. Créer une nouvelle clé et la copier

### Étape 2 : Configurer les clés

Ouvrir le fichier `.env` et modifier :

```bash
# Passer en mode réel
USE_MOCK_SERVICES=False

# Ajouter vos clés
BLEND_API_KEY=votre_clé_blend_ici
OPENAI_API_KEY=sk-proj-votre_clé_openai_ici
```

### Étape 3 : Relancer l'application

```bash
# Si Docker
docker-compose restart

# Si sans Docker
streamlit run app.py
```

### Étape 4 : Vérifier le mode

L'application affiche maintenant :
```
✅ Mode RÉEL - Les appels Blend AI seront effectués
```

au lieu de :
```
⚠️ Mode MOCK activé - Les appels sont simulés
```

---

## 📋 Format du CSV d'import

Votre fichier CSV doit contenir 3 colonnes obligatoires :

```csv
nom,prenom,telephone
Dupont,Jean,+33612345678
Martin,Marie,+33687654321
Durand,Pierre,+33698765432
```

**Important :**
- Le téléphone doit être au format international : `+33...` (France)
- Pas d'espaces dans les numéros
- Encodage UTF-8 recommandé

---

## 🐛 Résolution de problèmes

### Erreur : "externally-managed-environment"

**Solution :**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### L'application ne démarre pas

**Vérifier :**
1. Python version : `python --version` (doit être 3.11+)
2. Dépendances installées : `pip list | grep streamlit`
3. Port disponible : Le port 8501 doit être libre

**Solution :**
```bash
# Changer de port
streamlit run app.py --server.port 8502
```

### Mode MOCK ne se désactive pas

**Vérifier :**
1. Le fichier `.env` existe (pas `.env.example`)
2. La ligne `USE_MOCK_SERVICES=False` (sans espace)
3. Les clés API sont définies et non vides

**Commande de test :**
```bash
python -c "from utils.config import Config; print(Config.is_mock_mode())"
# Doit afficher : False
```

### Erreur Blend AI : "Invalid API Key"

**Solution :**
1. Vérifier que la clé est correcte (sans espaces)
2. Format attendu dans `.env` : `BLEND_API_KEY=votre_clé` (sans guillemets)
3. Vérifier sur https://app.bland.ai que la clé est active

### Erreur OpenAI : "Rate limit exceeded"

**Solution :**
- Vous avez dépassé le quota gratuit
- Ajouter des crédits sur https://platform.openai.com/billing
- Ou attendre la réinitialisation du quota (mensuelle)

---

## 📊 Coûts en mode RÉEL

### Par appel complet
- Blend AI : ~0.09 $/minute (durée moyenne : 1-2 min)
- OpenAI GPT-3.5 : ~0.002 $ par analyse

**Total estimé : 0.10 - 0.20 $ par appel**

### Budget pour 100 contacts
- Blend AI : ~15 $ (100 appels × 1.5 min × 0.09 $/min)
- OpenAI : ~0.20 $ (100 analyses)

**Total : ~15-20 $**

### Conseils pour économiser
- Testez d'abord en mode MOCK (gratuit)
- Limitez la durée max des appels : `max_duration: 12` (dans le code)
- Utilisez GPT-3.5-turbo au lieu de GPT-4 (déjà configuré)

---

## 🎓 Tutoriel pas à pas

### Scénario complet : Vérifier 10 contacts

**1. Préparer le CSV**
```csv
nom,prenom,telephone
Dupont,Jean,+33612345678
Martin,Sophie,+33687654321
Bernard,Lucas,+33698765432
...
```

**2. Importer dans l'application**
- Onglet "Campagne" → Upload CSV → Ajouter

**3. Lancer les appels**
- Cliquer "🚀 Lancer la campagne"
- Attendre 2-3 minutes par appel (mode réel)
- Observer la progression

**4. Analyser les résultats**
- Onglet "Dashboard" → Voir les statistiques
- Identifier les contacts à rappeler

**5. Relancer si nécessaire**
- Section "Relances manuelles"
- Cliquer "📞 Relancer ces contacts"

**6. Exporter**
- Onglet "Export" → Télécharger CSV
- Traiter dans Excel/Google Sheets

---

## 📞 Support et aide

### Documentation
- **Guide technique** : `docs/technical_doc.md`
- **README complet** : `README.md`

### Liens utiles
- Blend AI Docs : https://docs.bland.ai
- OpenAI Docs : https://platform.openai.com/docs
- Streamlit Docs : https://docs.streamlit.io

### Code source
- Services : `services/`
- Interface : `app.py`
- Configuration : `utils/config.py`

---

## ✅ Checklist de démarrage

- [ ] Python 3.11+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` configuré
- [ ] Application lancée (Streamlit démarre)
- [ ] Accès à http://localhost:8501
- [ ] Import de contacts réussi
- [ ] Premier appel (mock) effectué
- [ ] Résultats visibles dans le Dashboard
- [ ] Export CSV fonctionnel

**Si toutes les cases sont cochées : 🎉 Vous êtes prêt !**

---

## 🚀 Prochaines étapes

1. **Tester en mode MOCK** avec des données d'exemple
2. **Obtenir les clés API** Blend + OpenAI
3. **Passer en mode RÉEL** avec 2-3 contacts test
4. **Valider les résultats** et ajuster si nécessaire
5. **Lancer la campagne complète** sur votre base

Bon courage ! 💪
