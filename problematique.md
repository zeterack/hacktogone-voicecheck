# Problématique - VoiceCheck AI

**Équipe** : GoneToHack69  
**Sujet** : Voice AI Checker  
**Hackathon** : Hacktogone 2025

---

## Contexte du Hackathon

### La Problématique Business
Les entreprises sont confrontées à un problème récurrent et coûteux : **les bases de contacts obsolètes**. Ces bases contiennent :

- 📞 **Numéros inactifs** ou erronés
- ❌ **Mauvaises correspondances** prénom/identité
- 🔇 **Contacts injoignables** (répondeurs permanents, numéros désactivés)
- ⚠️ **Informations non vérifiées** depuis des mois/années

**Impact commercial** :
- Perte de temps des équipes commerciales
- Coût d'acquisition client gaspillé
- Taux de conversion en baisse
- Expérience utilisateur dégradée (appels erronés)

### Mission du Hackathon Hacktogone 2025

**Nom du projet** : VoiceCheck AI  
**Objectif** : Créer une intelligence artificielle capable de passer des appels téléphoniques automatiques pour vérifier la validité et l'exactitude des informations de contact dans une base donnée.

**Lieu** : Stade Vélodrome, Marseille  
**Dates** : 13-14 novembre 2025  
**Deadline de soumission** : 13h30 le 14 novembre (⚠️ Éliminatoire)

### Cahier des Charges Officiel

#### Fonctionnement Attendu
1. **Import** d'un fichier de contacts (CSV ou Google Sheets)
2. **Appel automatique** de chaque numéro par une voix IA naturelle
3. **Script de vérification** :
   - "Bonjour, suis-je bien avec [Prénom] ?"
   - ✅ Confirmation → statut "Valide"
   - ❌ Déni/Pas de réponse → statut "Invalide / Non confirmé"
4. **Enregistrement des résultats** :
   - ✅ Numéro actif + identité confirmée
   - ⚠️ Pas de réponse / répondeur
   - ❌ Numéro inactif ou identité refusée
5. **Tableau de bord** avec export (CSV / PDF)

#### Fonctions Clés Obligatoires
- ✅ Appels entièrement automatisés
- ✅ Voix naturelle (type ElevenLabs)
- ✅ Script simple, ton neutre, conforme RGPD
- ✅ Relance automatique si échec temporaire
- ✅ Tableau de bord avec statistiques globales

### Contraintes Strictes du Hackathon

#### Contraintes de Temps
- **24 heures** pour conception, développement et déploiement
- **13h30** deadline absolue (retard = élimination)
- **5 minutes maximum** de vidéo de démonstration
- Besoin d'un **prototype fonctionnel** (non simulé)

#### Contraintes Techniques
- Appels téléphoniques **réels** (pas de simulation)
- Compatible **France et Europe**
- Budget limité pour hébergement
- Déploiement simple et rapide

#### Contraintes RGPD et Éthiques
- ❌ Aucune donnée sensible stockée
- ❌ Pas d'enregistrement vocal sans consentement
- ✅ Script fixe, sans contenu commercial
- ✅ Conformité RGPD stricte
- ✅ Traçabilité complète des échanges

#### Critères Éliminatoires
⚠️ **Élimination immédiate si** :
1. Livré après 13h30
2. Vidéo de démonstration manquante
3. Tentative de prompt injection

### Livrables Obligatoires
1. **Dépôt GitHub** : `[Nom problematique]-[Nom Équipe]`
2. **README.md** : Documentation complète et reproductible
3. **problematique.md** : Ce document
4. **Vidéo démo** : 5 minutes max, live de la solution
5. **Solution fonctionnelle** : Prototype opérationnel

## Votre Approche

### Philosophie : Simplicité et Efficacité

Face aux contraintes du hackathon, nous avons adopté une approche **pragmatique** privilégiant :

1. **Rapidité de développement** : Technologies éprouvées et intégration rapide
2. **Coût minimal** : Solutions économiques et scalabilité progressive
3. **Déploiement simple** : Architecture monolithique facilement déployable
4. **Démonstration immédiate** : Interface utilisateur complète et fonctionnelle

### Choix Architecturaux Justifiés

#### 1. Architecture Monolithique Streamlit

**Pourquoi un seul Streamlit au lieu de Front/Back séparés ?**

##### Avantages pour le Hackathon
- ✅ **Développement ultra-rapide** : Interface + Logique en Python pur
- ✅ **Déploiement en un clic** : Streamlit Cloud gratuit et immédiat
- ✅ **Maintenance simplifiée** : Un seul codebase à gérer
- ✅ **Pas de gestion CORS** : Pas de complexité API REST
- ✅ **État partagé natif** : Session state intégré dans Streamlit

##### Inconvénients Acceptés (Trade-offs)
- ⚠️ Scalabilité limitée (acceptable pour un MVP/démo)
- ⚠️ Pas de séparation stricte des préoccupations (acceptable en hackathon)
- ⚠️ Interface moins personnalisable qu'un React (mais suffisant)

##### Justification Technique

```
Architecture Traditionnelle (rejetée pour le hackathon) :
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│  FastAPI    │────▶│  PostgreSQL │
│  Frontend   │ API │   Backend   │ SQL │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
   Temps : ~8h        Temps : ~4h        Temps : ~4h
                    TOTAL : 16h (trop long!)

Architecture Choisie (Streamlit monolithique) :
┌────────────────────────────────┐     ┌─────────────┐
│      Streamlit App             │────▶│ JSON Files  │
│  UI + Logic + State            │ I/O │ Database    │
└────────────────────────────────┘     └─────────────┘
            Temps : ~4h                    Temps : ~2h
                    TOTAL : 6h (idéal!)
```

**Résultat** : Gain de 10 heures de développement pour se concentrer sur l'essentiel (IA, téléphonie, RGPD).

##### Avantage IA-Assisted Development

**Architecture monolithique = Optimisation du "Vibe Coding" avec IA**

L'absence de séparation Front/Back apporte un **avantage crucial** dans un contexte de développement assisté par IA :

- ✅ **Moins de lignes de code total** (~2000 lignes vs ~5000+ pour Front+Back séparés)
- ✅ **Contexte complet en un seul codebase** : L'IA (GitHub Copilot, Claude, etc.) comprend l'ensemble du projet
- ✅ **Moins de token overhead** : Les modèles IA peuvent charger tout le projet en mémoire
- ✅ **Cohérence garantie** : Pas de désynchronisation entre API contracts et UI
- ✅ **Refactoring plus rapide** : Modifications propagées instantanément (pas de 2 repos à synchro)

**Impact concret sur le développement** :
```python
# Avec architecture monolithique :
# L'IA voit immédiatement la connexion UI ↔ Logic ↔ Data
def import_contacts(file):
    contacts = CsvHandler.import_contacts(file)  # ← Validation
    db.add_contacts(contacts)                     # ← Persistence
    st.success(f"{len(contacts)} importés")      # ← UI feedback
# Tout en ~10 lignes, contexte complet pour l'IA

# Avec Front/Back séparé :
# Frontend (React) : 50 lignes + API call
# Backend (FastAPI) : 50 lignes + validation + DB
# Contexte fragmenté, l'IA doit "deviner" le contrat d'interface
```

**Vibe Coding optimisé** : Les suggestions IA sont plus pertinentes car elles voient l'impact end-to-end immédiatement. Particulièrement critique en hackathon où la vélocité prime.

##### Déploiement Simplifié

**Un seul service = Déploiement en un clic**

L'architecture monolithique élimine la complexité de déploiement multi-services :

- ✅ **Streamlit Cloud uniquement** : Déploiement en 1 clic depuis GitHub
- ✅ **Pas de Docker Compose** : Pas besoin d'orchestrer Postgres + Backend + Frontend
- ✅ **Pas de gestion d'infrastructure** : Pas de serveur de base de données à provisionner
- ✅ **Coût zéro** : Streamlit Cloud offre un tier gratuit suffisant pour le hackathon
- ✅ **Configuration minimale** : Juste `secrets.toml` (clés API)

**Comparaison déploiement** :

```
Architecture Traditionnelle :
1. Provisionner serveur PostgreSQL (AWS RDS, Azure DB...)
2. Configurer Docker Compose (db + backend + frontend)
3. Gérer les migrations de schéma DB
4. Configurer les variables d'environnement (×3 services)
5. Déployer sur une plateforme cloud (Heroku, Railway, Render...)
⏱️ Temps : ~2-3 heures de configuration

Architecture Streamlit :
1. Push sur GitHub
2. Connecter repo à Streamlit Cloud
3. Ajouter secrets.toml dans l'UI Streamlit
⏱️ Temps : ~10 minutes
```

**Résultat** : Focus maximum sur le code métier, zéro temps perdu en DevOps pendant le hackathon.

---

#### 2. Base de Données Fichiers JSON

**Pourquoi JSON au lieu de PostgreSQL/MongoDB ?**

##### Avantages
- ✅ **Zéro configuration** : Pas de serveur DB à installer/gérer
- ✅ **Portabilité maximale** : Fonctionne partout (local, Docker, Cloud)
- ✅ **Debugging facile** : Fichiers lisibles en texte clair
- ✅ **Versioning Git** : Les données peuvent être versionnées
- ✅ **Backup simple** : Copie de fichiers suffit
- ✅ **Pas de dépendances** : Pas de driver, pas de credentials complexes

##### Limites Acceptées
- ⚠️ Performance limitée (<10 000 contacts)
- ⚠️ Pas de requêtes SQL complexes
- ⚠️ Pas de transactions ACID strictes
- ⚠️ Concurrent writes non gérés

##### Justification pour le Use Case
Notre cas d'usage (hackathon/démo) :
- **Volumes faibles** : 10-100 contacts par campagne
- **Opérations simples** : CRUD basique, pas de joins complexes
- **Utilisateur unique** : Pas de concurrence
- **Données non critiques** : Données de test/démo

**Structure adoptée** :
```json
{
  "contacts.json": [
    {"id": "1", "nom": "Dupont", "status": "pending", ...}
  ],
  "results.json": [
    {"contact_id": "1", "consent": true, "transcript": "...", ...}
  ]
}
```

#### 3. Services Externes Managés

**Choix des APIs tierces** :

##### Bland AI (Téléphonie)
- ✅ API REST simple
- ✅ IA conversationnelle intégrée
- ✅ Pas de gestion télécom complexe
- ✅ Pay-as-you-go (coût minimal)

##### OpenAI GPT-3.5 (Analyse)
- ✅ Compréhension du langage naturel
- ✅ Extraction structurée (consent, identity)
- ✅ Raisonnement contextuel
- ✅ API mature et fiable

**Alternative rejetée** : Développer notre propre moteur d'analyse NLP aurait pris 2-3 semaines.

## Solution Proposée

### Architecture Finale

```
┌────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Interface Utilisateur                    │  │
│  │  • Import CSV contacts                                │  │
│  │  • Lancement campagnes                                │  │
│  │  • Visualisation résultats                            │  │
│  │  • Export données                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Logique Métier                           │  │
│  │  • services/twilio_service.py (Bland AI)             │  │
│  │  • services/openai_service.py (Analyse IA)           │  │
│  │  • services/analysis_service.py (Business Logic)     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Persistence                              │  │
│  │  • utils/json_database.py (CRUD JSON)                │  │
│  │  • data/contacts.json                                 │  │
│  │  • data/results.json                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
         │                            │
         ▼                            ▼
┌─────────────────┐          ┌─────────────────┐
│   Bland AI API  │          │  OpenAI API     │
│   (Appels)      │          │  (Analyse)      │
└─────────────────┘          └─────────────────┘
```

### Flux de Traitement

```
1. Import CSV
   └─▶ Validation format téléphone (+33...)
       └─▶ Stockage contacts.json (status: pending)

2. Lancement Campagne
   └─▶ Pour chaque contact pending:
       ├─▶ Bland AI: Appel téléphonique automatisé
       │   └─▶ Questions RGPD + Identité
       │       └─▶ Récupération transcript
       ├─▶ OpenAI GPT-3.5: Analyse du transcript
       │   └─▶ Extraction: consent, identity_confirmed, reasoning
       └─▶ Stockage results.json
           └─▶ Mise à jour status contact (completed/pending)

3. Analyse & Export
   └─▶ Statistiques temps réel
   └─▶ Contacts à rappeler (refus/répondeur)
   └─▶ Export CSV avec date campagne
```

### Fonctionnalités Clés Implémentées

#### 1. Gestion des Contacts
- ✅ Import CSV avec validation stricte (format international)
- ✅ Détection numéros invalides (longueur, format)
- ✅ Gestion statuts : `pending`, `to recall`, `completed`

#### 2. Campagnes d'Appels
- ✅ Appels automatisés via Bland AI
- ✅ Script conversationnel RGPD-compliant
- ✅ Gestion répondeurs/pas de réponse
- ✅ Relances intelligentes

#### 3. Analyse IA
- ✅ Détection consentement RGPD
- ✅ Vérification identité (nom + prénom)
- ✅ Classification refus explicites vs. répondeurs
- ✅ Raisonnement contextuel

#### 4. Traçabilité & Export
- ✅ Transcripts complets conservés
- ✅ Horodatage précis
- ✅ Export CSV daté (`campagne_du_2024-11-14.csv`)
- ✅ Historique des tentatives

### Conformité RGPD

Notre solution respecte scrupuleusement :

1. **Consentement explicite**
   - Question claire en début d'appel
   - Validation IA du consentement oral
   - Refus respecté immédiatement

2. **Traçabilité**
   - Transcripts complets conservés
   - Horodatage de chaque interaction
   - Raisonnement IA documenté

3. **Droit de refus**
   - Arrêt immédiat en cas de refus
   - Marquage "refus explicite" dans exports
   - Pas de relance automatique si refus clair

## Évolution Future (Hors Hackathon)

### Améliorations Prévues

#### Architecture
- [ ] Séparation Front (React) / Back (FastAPI)
- [ ] Base de données PostgreSQL pour scalabilité
- [ ] Cache Redis pour performances
- [ ] Queue system (Celery) pour appels asynchrones

#### Fonctionnalités
- [ ] Authentification multi-utilisateurs
- [ ] Webhooks temps réel Bland AI
- [ ] Dashboard analytics avancé
- [ ] Support multi-langues
- [ ] Intégration CRM (Salesforce, HubSpot)

#### Infrastructure
- [ ] Kubernetes pour orchestration
- [ ] CI/CD automatisé (GitHub Actions)
- [ ] Monitoring (Prometheus + Grafana)
- [ ] Logging centralisé (ELK Stack)

### Conclusion

Notre approche **monolithique Streamlit + JSON** était le choix optimal pour :

- ✅ Respecter les contraintes du hackathon (20h)
- ✅ Démontrer toutes les fonctionnalités clés
- ✅ Déployer en production rapidement (Streamlit Cloud)
- ✅ Maintenir un code simple et compréhensible

Cette architecture est **intentionnellement simple** et constitue un excellent **MVP** démontrant la faisabilité technique. Pour une mise en production à grande échelle, une migration vers une architecture microservices serait recommandée, mais ce n'était **pas l'objectif du hackathon**.

**Trade-off assumé** : Simplicité > Scalabilité (pour ce contexte spécifique).

---

## Critères d'Évaluation du Jury

Notre solution VoiceCheck AI répond aux **5 critères officiels** du hackathon :

### 1. Innovation et Pertinence ⭐
**Notre approche** :

- ✅ Utilisation de l'IA conversationnelle (Bland AI) pour automatiser un processus manuel coûteux
- ✅ Analyse intelligente par GPT-3.5 pour extraire consentement et identité
- ✅ Détection automatique des répondeurs vs refus explicites
- ✅ Solution pertinente au problème réel des bases de contacts obsolètes

**Impact** : Économie de temps (x10) et amélioration de la qualité des données clients

### 2. Qualité Technique et Architecture ⭐
**Notre implémentation** :

- ✅ Code Python structuré (architecture en couches : UI / Services / Data)
- ✅ Separation of Concerns : chaque service a une responsabilité unique
- ✅ Gestion d'erreurs robuste (validation téléphone, retry logic, timeouts)
- ✅ Tests de validation intégrés
- ✅ Logging complet pour debugging

**Robustesse** : Gestion des cas limites (numéros invalides, pas de réponse, erreurs API)

### 3. Documentation et Reproductibilité ⭐
**Nos livrables** :

- ✅ **README.md** complet : architecture, installation, déploiement (local, Docker, Cloud)
- ✅ **problematique.md** détaillé : contexte, choix techniques justifiés, évolutions
- ✅ **Fichiers d'exemple** : `secrets.toml.example`, `sample_contacts.csv`
- ✅ **Docker-compose** : déploiement en une commande
- ✅ **Instructions pas-à-pas** pour Streamlit Cloud

**Reproductibilité garantie** : N'importe qui peut cloner et lancer en 5 minutes

### 4. Expérience Utilisateur ⭐
**Notre interface Streamlit** :

- ✅ **Intuitive** : 3 onglets simples (Dashboard / Campagne / Export)
- ✅ **Guidée** : Instructions claires, formats acceptés expliqués
- ✅ **Temps réel** : Barre de progression, statuts live, logs visibles
- ✅ **Visuelle** : Statistiques avec métriques colorées, tableaux interactifs
- ✅ **Accessible** : Aucune connaissance technique requise

**Parcours fluide** : Import CSV → Lancer campagne → Voir résultats → Exporter

### 5. Impact et Viabilité ⭐
**Potentiel commercial** :

- ✅ **Marché réel** : Toutes les entreprises B2B ont des bases de contacts
- ✅ **ROI mesurable** : Temps économisé + taux de conversion amélioré
- ✅ **Scalabilité** : Architecture peut évoluer vers microservices
- ✅ **Conformité** : RGPD-compliant dès la conception
- ✅ **Déploiement immédiat** : Streamlit Cloud gratuit (MVP)

**Viabilité** : Solution utilisable dès maintenant, monétisation possible (SaaS, API)
