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

```bash
# 🚀 Guide de Déploiement

## 📋 Prérequis

### 1. Environnement Python
- Python 3.8+
- pip
- virtualenv

### 2. Dépendances
- Streamlit
- Pandas
- NumPy
- Matplotlib
- gspread
- oauth2client
- python-dotenv
- requests
- plotly
- scipy
- pytest
- black
- isort

## 📦 Installation

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Installer les outils de développement
pip install pytest black isort
```

## 📁 Structure du Projet

```
rhuma/
├── src/
│   ├── data/         # Données et configurations
│   ├── models/       # Modèles de simulation
│   │   ├── energy/    # Modèles énergie
│   │   ├── production/ # Modèles production
│   │   └── financial/  # Modèles financiers
│   └── utils/        # Utilitaires
├── docs/             # Documentation
└── tests/            # Tests
```

## 🚀 Déploiement Local

```bash
# 1. Configurer les variables d'environnement
export GOOGLE_SHEETS_CREDENTIALS="path/to/credentials.json"

# 2. Lancer l'application
streamlit run streamlit_app.py
```

## 🌐 Déploiement Cloud

### 1. Streamlit Cloud

```bash
# 1. Créer un compte Streamlit Cloud
# 2. Configurer les variables d'environnement
# 3. Déployer l'application
```

### 2. Heroku

```bash
# 1. Créer une application Heroku
# 2. Configurer les variables d'environnement
# 3. Déployer l'application
```

## 🔐 Configuration Google Sheets

1. Créer un projet Google Cloud
2. Activer l'API Google Sheets
3. Créer des credentials
4. Configurer les permissions
5. Placer le fichier `credentials.json` dans le répertoire

## 🛠️ Maintenance

### 1. Mises à jour
- Mise à jour des dépendances
- Mise à jour des API
- Mise à jour des modèles

### 2. Sauvegarde
- Sauvegarde des données
- Sauvegarde des configurations
- Sauvegarde des résultats

## 📊 Monitoring

### 1. Logs
- Logs d'application
- Logs d'erreurs
- Logs d'activité

### 2. Métriques
- Temps de réponse
- Utilisation des ressources
- Nombre d'utilisateurs
```

### Local Deployment

```bash
# 1. Configurer les variables d'environnement
export GOOGLE_SHEETS_CREDENTIALS="path/to/credentials.json"

# 2. Lancer l'application
streamlit run streamlit_app.py
```

### Cloud Deployment

#### Streamlit Cloud

```bash
# 1. Créer un compte Streamlit Cloud
# 2. Configurer les variables d'environnement
# 3. Déployer l'application
```

#### Heroku

```bash
# 1. Créer une application Heroku
# 2. Configurer les variables d'environnement
# 3. Déployer l'application
```

### Google Sheets Configuration

1. Créer un projet Google Cloud
2. Activer l'API Google Sheets
3. Créer des credentials
4. Configurer les permissions
5. Placer le fichier `credentials.json` dans le répertoire

### Maintenance

#### Updates

- Mise à jour des dépendances
- Mise à jour des API
- Mise à jour des modèles

#### Backup

- Sauvegarde des données
- Sauvegarde des configurations
- Sauvegarde des résultats

### Monitoring

#### Logs

- Logs d'application
- Logs d'erreurs
- Logs d'activité

#### Metrics

- Temps de réponse
- Utilisation des ressources
- Nombre d'utilisateurs

### Docker Deployment (Optional)

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
