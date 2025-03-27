# Rhumba Project Architecture

## System Overview
Rhumba is a modular, service-oriented architecture designed to optimize rhum production in a solar-powered greenhouse environment. The system has been updated with the latest changes to improve its performance and efficiency.

## Architectural Components

### 1. Core System Architecture
- Microservices-based design
- Event-driven architecture
- Modular JavaScript solver

#### Key Modules
1. **Sensor Data Acquisition Service**
   - Collect environmental and production data
   - Real-time data streaming
   - Interface with IoT sensors

2. **Solar Energy Management Service**
   - Monitor solar panel output
   - Energy allocation optimization
   - Predictive energy generation modeling

3. **Production Optimization Service**
   - Algorithmic production efficiency management
   - Machine learning-based predictive modeling
   - Continuous performance adjustment

4. **Data Analytics Service**
   - Historical data processing
   - Performance metric calculation
   - Visualization and reporting

### 2. Technology Stack
- **Backend**: Node.js
- **Data Processing**: JavaScript
- **Machine Learning**: TensorFlow.js
- **Database**: PostgreSQL
- **IoT Communication**: MQTT, LoRaWAN
- **Real-time Communication**: WebSockets

### 3. Data Flow
```
Sensors -> Data Acquisition -> 
Data Processing -> Optimization Service -> 
Production Recommendations -> 
Greenhouse Management -> Feedback Loop
```

## Infrastructure Design

### Deployment Topology
- Cloud-based microservices
- Containerized deployment (Docker)
- Kubernetes orchestration
- Scalable and resilient architecture

### Security Considerations
- Encrypted data transmission
- Role-based access control
- Secure API endpoints
- Compliance with data protection regulations

## Integration Points

### External Systems
- Weather forecasting APIs
- Agricultural management platforms
- Energy grid interfaces

### Internal Interfaces
- Greenhouse control systems
- Solar panel management
- Production tracking systems

## Scalability Strategy
- Horizontal scaling capabilities
- Modular service design
- Dynamic resource allocation
- Cloud-native architecture

## Monitoring and Observability
- Distributed tracing
- Performance metrics
- Real-time system health monitoring
- Automated alerting system

## Future Expansion Considerations
- Multi-site deployment support
- Advanced AI/ML integration
- Edge computing capabilities
- Enhanced IoT sensor integration

## Technical Constraints
- Location-specific implementation (Corsica)
- Limited computational resources
- Energy efficiency requirements
- Regulatory compliance

## Architectural Principles
- Modularity
- Scalability
- Flexibility
- Performance optimization
- Sustainable design

## Technical Architecture Update
The system's technical architecture has been updated to include the following components:

### 1. Structure du Projet

```
rhuma/
├── modules/          # Modules
│   ├── data_export.py    # Export des données
│   ├── pvgis_analysis.py # Analyse PVGIS
│   ├── attributes.py     # Configuration des attributs
│   └── state_manager.py  # Gestionnaire d'état
├── docs/             # Documentation
└── tests/            # Tests
```

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

## 🏗️ Structure du Projet

```
rhuma/
├── modules/          # Modules
│   ├── data_export.py    # Export des données
│   ├── pvgis_analysis.py # Analyse PVGIS
│   ├── attributes.py     # Configuration des attributs
│   └── state_manager.py  # Gestionnaire d'état
├── docs/             # Documentation
└── tests/            # Tests
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
