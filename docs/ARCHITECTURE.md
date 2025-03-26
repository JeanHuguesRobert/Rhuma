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

### 1. Variables d'Environnement
- Clés API
- Paramètres de connexion
- Configuration Google Sheets
- Paramètres système

### 2. Configuration Locale
- Paramètres par défaut
- Chemins de fichiers
- Configuration des API
- Paramètres de simulation
