# 📋 Spécifications du Projet Rhum Solaire de Corte, Rhuma

## 🎯 Objectif du Projet
Optimiser la production de rhum dans une serre solaire, avec une première implémentation à Corte, en Corse, en utilisant un simulateur Python et une interface Streamlit.

## 🏗️ Spécifications Techniques

### 1. Architecture
- Application web avec Streamlit
- Backend Python avec modèles de simulation
- Intégration Google Sheets pour l'export
- API PVGIS pour les données météorologiques

### 2. Fonctionnalités

#### Simulation
- Simulation de la production PV
- Simulation de la croissance de la canne
- Simulation de la production de rhum
- Optimisation des coûts
- Export des résultats

#### Interface
- Interface utilisateur intuitive
- Graphiques et visualisations
- Export vers JSON et Google Sheets
- Documentation intégrée

### 3. Dépendances
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

## 📊 Spécifications Fonctionnelles

### 1. Simulation de Production
- Simulation de la production PV avec tracking
- Optimisation de l'autoconsommation
- Calcul des coûts de construction
- Simulation des coûts annuels
- Analyse du ROI

### 2. Gestion des Données
- Import des données météorologiques
- Sauvegarde des simulations
- Export des résultats
- Historique des simulations

### 3. Interface Utilisateur
- Interface en français
- Visualisation des résultats
- Export des données
- Documentation intégrée

## 📈 Métriques de Performance

### 1. Production
- 150 000 L de rhum/an
- 1 500 000 kWh d'électricité/an
- 1 MWc d'autoconsommation
- 20% de gains avec le tracking

### 2. Finances
- Coût PV fixe : 1000€/kWc
- Coût tracking : 250€/kWc
- Coût serre : 150€/m²
- Coût annuel : 100€/kWc

### 3. Durabilité
- 100% d'énergie verte
- 5 ans d'amortissement
- 25 ans de durée de vie

## 🛠️ Spécifications Techniques

### 1. Structure du Projet

```
rhuma/
├── modules/          # Modules
├── docs/             # Documentation
└── tests/            # Tests
```

### 2. Configuration
- Variables d'environnement
- Configuration Google Sheets
- Paramètres de simulation
- Métriques de performance

### 3. Tests
- Tests unitaires
- Tests d'intégration
- Tests de performance
- Tests d'acceptation

## 📊 Indicateurs de Performance

### 1. Production
- Volume de production
- Qualité du produit
- Efficacité énergétique

### 2. Finances
- Coûts initiaux
- Coûts annuels
- ROI
- Temps de retour

### 3. Technique
- Temps de réponse
- Utilisation des ressources
- Nombre d'utilisateurs

## 🛠️ Maintenance

### 1. Mises à jour
- Mise à jour des dépendances
- Mise à jour des API
- Mise à jour des modèles

### 2. Sauvegarde
- Sauvegarde des données
- Sauvegarde des configurations
- Sauvegarde des résultats

### 3. Monitoring
- Logs d'application
- Logs d'erreurs
- Logs d'activité
- Métriques de performance
