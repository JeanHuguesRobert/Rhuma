# Rhumba Deployment Guide

## Deployment Overview
Comprehensive guide for deploying the Rhumba rhum production optimization system in a greenhouse environment.

## Prerequisites

### Hardware Requirements
- Medium-sized greenhouse in Corti, Corsica
- Solar panel installation
- IoT sensor network
- Compute infrastructure (local or cloud)

### Software Requirements
- Node.js (v18+ recommended)
- Docker
- Kubernetes
- MongoDB
- WebSocket-compatible infrastructure

## Deployment Stages

### 1. Environment Preparation
- Prepare greenhouse infrastructure
- Install IoT sensor network
- Configure solar panel systems
- Set up compute infrastructure

### 2. Software Deployment

#### 2.1 Core System Installation
```bash
# Clone the Rhumba repository
git clone https://github.com/JeanHuguesRobert/Rhumba.git
cd rhumba

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env with specific configuration
```

#### 2.2 Docker Containerization
```bash
# Build Docker containers
docker-compose build

# Start services
docker-compose up -d
```

#### 2.3 Kubernetes Deployment
```bash
# Deploy to Kubernetes cluster
kubectl apply -f k8s/

# Verify deployment
kubectl get deployments
kubectl get services
```

## Configuration

### Environment Variables
- `GREENHOUSE_LOCATION`: Corti, Corsica
- `SOLAR_PANEL_CAPACITY`: Specific to installation
- `PRODUCTION_OPTIMIZATION_LEVEL`: Tuning parameter
- `DATA_RETENTION_PERIOD`: Logging and analytics configuration

## Monitoring and Logging

### Logging Setup
- Centralized logging system
- Performance metric collection
- Real-time monitoring dashboard

### Health Checks
- Service availability monitoring
- Performance threshold alerts
- Automated diagnostic reporting

## Scaling Considerations
- Horizontal scaling configuration
- Resource allocation strategies
- Multi-instance deployment support

## Troubleshooting

### Common Deployment Issues
- Sensor connectivity problems
- Data synchronization challenges
- Performance bottlenecks

### Diagnostic Commands
```bash
# Check system health
npm run diagnostic

# View logs
docker logs rhumba-core-service

# Performance monitoring
kubectl top pods
```

## Security Considerations
- Secure API endpoints
- Encryption of sensitive data
- Role-based access control
- Regular security audits

## Post-Deployment Validation
- Sensor network verification
- Initial performance baseline
- Optimization algorithm testing

## Maintenance

### Regular Updates
- Software patches
- Algorithm improvements
- Security updates

### Periodic Recalibration
- Seasonal adjustments
- Performance optimization
- Sensor network recalibration

## Rollback Procedure
```bash
# Rollback to previous stable version
kubectl rollout undo deployment/rhumba-core
```

## Documentation and Support
- Maintain detailed deployment logs
- Create support documentation
- Establish communication channels for technical support

## Future Deployment Considerations
- Multi-site expansion
- Cloud migration strategies
- Advanced IoT integration

## Additional Deployment Options

### Streamlit Deployment

# 📅 Déploiement du Projet Rhuma

## 📋 Vue d'ensemble

Le projet Rhuma est une application de simulation et d'optimisation de la production de rhum solaire en Corse. Cette documentation fournit les informations nécessaires pour son déploiement et sa maintenance.

## 🛠️ Configuration

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

### 2. Configuration des Variables d'Environnement

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

### 1. Prérequis

```bash
# Installer les dépendances
pip install streamlit pandas matplotlib numpy gspread oauth2client

# Initialiser l'environnement
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

### 2. Configuration Google Sheets

```bash
# Créer un projet Google Cloud
gcloud projects create rhuma-project

gcloud services enable sheets.googleapis.com

gcloud iam service-accounts create rhuma-sa

gcloud iam service-accounts keys create credentials.json \
  --iam-account rhuma-sa@rhuma-project.iam.gserviceaccount.com
```

### 3. Déploiement Heroku

```bash
# Créer une application Heroku
heroku create rhuma-app

# Configurer les variables d'environnement
heroku config:set RHUMA_ID=rhuma
heroku config:set RHUMA_LABEL="Rhum Solaire de Corse"

# Déployer l'application
git push heroku main
```

## 🔄 Maintenance

### 1. Mises à Jour

```bash
# Mettre à jour les dépendances
pip install --upgrade pip
pip install --upgrade streamlit pandas numpy
```

### 2. Sauvegarde

- Sauvegarde quotidienne des configurations
- Sauvegarde hebdomadaire des résultats
- Archivage mensuel des rapports

## 📊 Surveillance

### 1. Logs

- Logs de démarrage
- Logs d'erreurs
- Logs d'activité

### 2. Métriques

- Temps de réponse
- Utilisation des ressources
- Nombre d'utilisateurs

## 🐳 Déploiement Docker (Optionnel)

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
