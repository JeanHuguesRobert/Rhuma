# Rhuma Project Architecture

## System Overview
Rhuma is a modular, service-oriented architecture designed to optimize rhum production in a solar-powered greenhouse environment.

## Architectural Components

### 1. Structure du Projet

```
rhuma/
├── modules/          
│   ├── data_export.py    # Export des données vers Google Sheets, Excel, JSON...
│   ├── exports.py        # Gestion des exports (JSON, CSV, Excel, ZIP)
│   ├── financial.py      # Calculs financiers et simulation de scénarios
│   ├── pvgis_analysis.py # Analyse PVGIS
│   ├── state_manager.py  # Gestionnaire d'état
│   └── solar_tracker_3d.py  # Simulation 3D du tracker
├── docs/                # Documentation (mise à jour)
└── tests/               # Tests unitaires et d'intégration
```

### 2. Modules Mis à Jour
- Le module **financial.py** contient désormais le calcul des coûts et la simulation financière.
- Le module **exports.py** centralise tous les exports vers JSON, CSV, Excel et un fichier ZIP complet.
- La documentation a été actualisée pour refléter ces changements.

## Architectural Components

### 2. Composants Principaux

#### 1. Modèle Énergie
- Simulation de la production PV
- Optimisation de l'autoconsommation
- Calcul des gains de tracking
- Intégration PVGIS API

#### 2. Modèle Production
- Simulation de la croissance de la canne
- Calcul des rendements
- Estimation de la production de rhum
- Optimisation des processus

#### 3. Modèle Financier
- Calcul des coûts initiaux
- Simulation des coûts annuels
- Analyse du retour sur investissement
- Optimisation des investissements

## API et Services

### 1. Google Sheets API
- Export des résultats
- Partage collaboratif
- Calculs dynamiques
- Intégration avec Streamlit

### 2. PVGIS API
- Données météorologiques
- Simulation de production PV
- Optimisation du tracking
- Prévisions énergétiques

## Base de Données

### 1. Configuration
- Paramètres par défaut
- Coûts standard
- Tarifs énergétiques
- Métriques de performance

### 2. Historique
- Sauvegarde des simulations
- Comparaison des résultats
- Analyse des tendances
- Optimisation continue

## Analyse des Données

### 1. Visualisation
- Graphiques comparatifs
- Tableaux de bord
- Export des résultats
- Analyse en temps réel

### 2. Optimisation
- Recherche de paramètres optimaux
- Analyse de sensibilité
- Optimisation des coûts
- Prévisions

## Développement

### 1. Tests
- Tests unitaires
- Tests d'intégration
- Tests de performance
- Tests d'acceptation

### 2. Documentation
- Guide d'utilisation
- Documentation technique
- API reference
- Exemples d'utilisation

## Configuration

### Variables d'Environnement

Le projet utilise des variables d'environnement pour la configuration. Les principales variables sont :

#### Google Sheets

Les variables pour la configuration de Google Sheets sont préfixées par `RHUMA_GOOGLE_SHEETS_` :

- `RHUMA_GOOGLE_SHEETS_TYPE` : Type de compte de service ("service_account")
- `RHUMA_GOOGLE_SHEETS_PROJECT_ID` : ID du projet Google Cloud
- `RHUMA_GOOGLE_SHEETS_PRIVATE_KEY_ID` : ID de la clé privée
- `RHUMA_GOOGLE_SHEETS_PRIVATE_KEY` : Clé privée (format PEM)
- `RHUMA_GOOGLE_SHEETS_CLIENT_EMAIL` : Email du compte de service
- `RHUMA_GOOGLE_SHEETS_CLIENT_ID` : ID du client
- `RHUMA_GOOGLE_SHEETS_AUTH_URI` : URI d'authentification
- `RHUMA_GOOGLE_SHEETS_TOKEN_URI` : URI du token
- `RHUMA_GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL` : URL du certificat
- `RHUMA_GOOGLE_SHEETS_CLIENT_X509_CERT_URL` : URL du certificat client

#### Structure des Variables

Les variables d'environnement suivent la convention suivante :
- Préfixe `RHUMA_` pour identifier les variables du projet
- Sous-préfixe pour identifier la catégorie (ex: `GOOGLE_SHEETS_`)
- Noms en majuscules avec underscores
- Chaque attribut sur une ligne séparée

### Configuration Locale

Pour configurer l'application localement, créez un fichier `.env` à partir du fichier `.env.example` :

```bash
cp .env.example .env
```

Puis remplacez les valeurs par défaut par vos propres configurations.

## 🏗️ Architecture du Projet Rhuma

## 🎯 Objectif

L'architecture de Rhuma est conçue pour optimiser la production de rhum dans une serre solaire, avec une première implémentation à Corte, en Corse.

## 🛠️ Structure du Projet

```
rhuma/
├── modules/          
│   ├── data_export.py    # Export des données vers Google Sheets, Excel, JSON...
│   ├── exports.py        # Gestion des exports (JSON, CSV, Excel, ZIP)
│   ├── financial.py      # Calculs financiers et simulation de scénarios
│   ├── pvgis_analysis.py # Analyse PVGIS
│   ├── state_manager.py  # Gestionnaire d'état
│   └── solar_tracker_3d.py  # Simulation 3D du tracker
├── docs/                # Documentation (mise à jour)
└── tests/               # Tests unitaires et d'intégration
```

## 🛠️ Configuration Technique

### 1. Environnement

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# Installer les dépendances
pip install streamlit pandas matplotlib numpy gspread oauth2client
```

### 2. Variables d'Environnement

```bash
# .env
RHUMA_ID=rhuma
RHUMA_LABEL="Rhum Solaire de Corse"
RHUMA_VERSION="1.0.0"
RHUMA_LANGUAGE=fr

# API Keys
PVGIS_API_KEY=v3.1

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
```

### 3. Structure des Données

```json
{
  "metadata": {
    "id": "rhuma",
    "label": "Rhum Solaire de Corse",
    "version": "1.0.0",
    "timestamp": "2025-03-27T08:45:20+01:00",
    "language": "fr"
  },
  "configuration": {
    "surface_canne": 3000,
    "rendement_canne": 120,
    "teneur_sucre": 15,
    "efficacite_extraction": 80,
    "efficacite_distillation": 85,
    "pv_serre": 300,
    "pv_sol": 200,
    "tarif_s24": 0.12,
    "tva": 5
  }
}
```

## 🚀 Déploiement

### 1. Développement Local

```bash
# Lancer l'application
streamlit run streamlit_app.py
```

### 2. Déploiement Cloud

#### Heroku

```bash
# Créer une application Heroku
heroku create rhuma-app

# Configurer les variables d'environnement
heroku config:set RHUMA_ID=rhuma
heroku config:set RHUMA_LABEL="Rhum Solaire de Corse"

# Déployer l'application
git push heroku main
```

#### Docker (Optionnel)

```bash
# 1. Cloner le dépôt
gh repo clone JeanHuguesRobert/Rhuma

cd Rhuma

# 2. Créer un nouveau dépôt
gh repo create votre-nom-de-projet --public

# 3. Configurer le nouveau dépôt
git remote rename origin upstream
git remote add origin https://github.com/votre-username/votre-nom-de-projet.git
git push -u origin main
```

## 🛠️ Technologie

### Backend
- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- gspread
- oauth2client

### Frontend
- Streamlit UI
- Components personnalisés
- Internationalisation (i18n)

### Base de Données
- Google Sheets (via API)
- Configuration locale (.env)

## 📋 Configuration

### Variables d'Environnement

- `RHUMA_ID` : ID technique
- `RHUMA_LABEL` : Nom affiché
- `RHUMA_VERSION` : Version
- `RHUMA_LANGUAGE` : Langue
- `GOOGLE_SHEETS_CREDENTIALS_FILE` : Fichier de credentials

### Paramètres de Simulation

- **Production**
  - Surface canne : 0-10000 m²
  - Rendement canne : 80-160 t/ha
  - Teneur sucre : 12-20%
  - Efficacité extraction : 60-90%
  - Efficacité distillation : 70-95%

- **Énergie PV**
  - Puissance serre : 0-1000 kWc
  - Puissance sol : 0-1000 kWc
  - Tarif S24 : 0.05-0.20 €/kWh
  - TVA : 0-20%

- **Coûts**
  - PV fixe : 1000€/kWc
  - Tracking : 250€/kWc
  - Serre : 150€/m²
  - Maintenance : 50€/kWc/an
  - Assurance : 20€/kWc/an
  - Production : 30€/kWc/an

## 📊 Métriques

### Production

- Volume annuel de rhum
- Production PV
- Autoconsommation
- Revenus énergétiques

### Finances

- Investissement initial
- Coûts annuels
- Revenus
- ROI
- Durée d'amortissement

## 🔄 Maintenance

### Mises à Jour

- Dépendances Python
- API Google Sheets
- Modèles de simulation

### Sauvegarde

- Configuration
- Données de simulation
- Historique

## 📈 Monitoring

### Logs

- Démarrage
- Erreurs
- Activité

### Métriques

- Performance
- Utilisation
- Erreurs
