# 📚 Guide d'Utilisation

## 📋 Présentation

Ce guide vous aidera à comprendre et utiliser le simulateur de production de rhum en serre autonome. Le simulateur permet de visualiser l'impact des différents paramètres sur la production et les revenus du projet.

## 📊 Paramètres du Simulateur

### 1. Surface et Rendement

- **Surface canne** : De 0 à 10 000 m² (défaut : 3000 m²)
- **Rendement canne** : De 80 à 160 t/ha (défaut : 120 t/ha)
- **Teneur en sucre** : De 12% à 20% (défaut : 15%)

### 2. Extraction et Distillation

- **Efficacité extraction** : De 60% à 90% (défaut : 80%)
- **Efficacité distillation** : De 70% à 95% (défaut : 85%)

### 3. Énergie PV

- **Puissance PV (serre)** : De 0 à 1000 kWc (défaut : 300 kWc)
- **Puissance PV (sol)** : De 0 à 1000 kWc (défaut : 200 kWc)
- **Tarif S24** : De 0.05€ à 0.20€/kWh (défaut : 0.12€/kWh)
- **TVA** : De 0% à 20% (défaut : 5%)

### 4. Coûts de Construction

- **Coûts PV**
  - Système fixe : 1000€/kWc
  - Système tracking (supplémentaire) : 250€/kWc
- **Coûts de construction de la serre**
  - Prix moyen : 150€/m²
  - Plage de variation : 100 à 200€/m²
- **Coûts annuels**
  - Maintenance : 50€/kWc/an
  - Assurance : 20€/kWc/an
  - Production : 30€/kWc/an

## 📋 Configuration

### Variables d'Environnement

Le projet utilise des variables d'environnement pour la configuration. Les principales variables sont :

#### Configuration Générale

- `RHUMA_ID` : ID technique utilisé pour les fichiers de configuration (lettres, chiffres, underscores)
- `RHUMA_LABEL` : Nom affiché dans l'interface utilisateur
- `RHUMA_VERSION` : Version de l'application
- `RHUMA_LANGUAGE` : Langue de l'interface

#### Configuration Google Sheets

- `GOOGLE_SHEETS_CREDENTIALS_FILE` : Chemin vers le fichier de credentials

#### Paramètres de Simulation

- `RHUMA_SURFACE_CANNE` : Surface dédiée à la canne (m²)
- `RHUMA_RENDEMENT_CANNE` : Rendement canne (t/ha)
- `RHUMA_TENEUR_SUCRE` : Teneur en sucre (%)
- `RHUMA_EFFICACITE_EXTRACTION` : Efficacité extraction (%)
- `RHUMA_EFFICACITE_DISTILLATION` : Efficacité distillation (%)
- `RHUMA_PV_SERRE` : Puissance PV (serre) (kWc)
- `RHUMA_PV_SOL` : Puissance PV au sol (kWc)
- `RHUMA_TARIF_S24` : Tarif S24 (€/kWh)
- `RHUMA_TVA` : TVA (%)

Pour configurer l'application, créez un fichier `.env` à partir du fichier `.env.example` et remplacez les valeurs par défaut par vos propres configurations.

## 📊 Résultats de la Simulation

### Production de Rhum

- Volume annuel de rhum produit
- Coût de production par litre
- Revenus annuels
- Retour sur investissement

### Production Énergétique

- Production PV annuelle
- Autoconsommation
- Revenus énergétiques
- Émissions de CO2 évitées

### Coûts et Investissements

- Investissement initial
- Coûts annuels
- Coûts d'exploitation
- Coûts de maintenance

### Analyse Financière

- Retour sur investissement
- Durée d'amortissement
- Rentabilité
- Sensibilité aux paramètres
