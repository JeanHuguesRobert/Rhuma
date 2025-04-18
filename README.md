# 📋 Rhuma - Simulateur de Production de Rhum Solaire

## 🎯 Description

Rhuma est un simulateur de production d'électricité et de rhum sous serre solaire en Corse. L'application permet de simuler et optimiser la production de rhum en tenant compte des aspects énergétiques, agricoles et financiers.

## 🌐 Accès à l'Application

L'application est accessible en ligne sur [Streamlit Cloud](https://acorsica.streamlit.app/)

## 🚀 Fonctionnalités

- Simulation de la production PV avec tracking
- Simulation de la croissance de la canne
- Simulation de la production de rhum
- Optimisation des coûts
- Export des résultats vers JSON et Google Sheets
- Documentation intégrée

## 🛠️ Installation

### 1. Cloner le Projet

```bash
git clone https://github.com/JeanHuguesRobert/Rhuma.git
cd Rhuma
```

### 2. Configuration de l'Environnement

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# Installer les dépendances
pip install streamlit pandas matplotlib numpy gspread oauth2client
```

### 3. Lancer l'Application

```bash
streamlit run streamlit_app.py
```

## 📚 Documentation

- [Guide Utilisateur](docs/user_guide.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Déploiement](docs/DEPLOYMENT.md)
- [Documentation Technique](docs/README_TECH.md)

## 📋 Configuration

### Variables d'Environnement

Le projet utilise des variables d'environnement pour la configuration. Voir la [documentation complète](docs/user_guide.md#configuration) pour la liste complète des variables et leurs descriptions.

#### Configuration Générale

- `RHUMA_ID` : ID technique utilisé pour les fichiers de configuration (lettres, chiffres, underscores)
- `RHUMA_LABEL` : Nom affiché dans l'interface utilisateur
- `RHUMA_VERSION` : Version de l'application
- `RHUMA_LANGUAGE` : Langue de l'interface

#### Configuration Google Sheets

Les variables pour la configuration de Google Sheets sont préfixées par `RHUMA_GOOGLE_SHEETS_` :

- `GOOGLE_SHEETS_CREDENTIALS_FILE` : Chemin vers le fichier de credentials

#### Paramètres de Simulation

Les paramètres de simulation sont préfixés par `RHUMA_` :

- `RHUMA_SURFACE_CANNE` : Surface dédiée à la canne (m²)
- `RHUMA_RENDEMENT_CANNE` : Rendement canne (t/ha)
- `RHUMA_TENEUR_SUCRE` : Teneur en sucre (%)
- `RHUMA_EFFICACITE_EXTRACTION` : Efficacité extraction (%)
- `RHUMA_EFFICACITE_DISTILLATION` : Efficacité distillation (%)
- `RHUMA_PV_SERRE` : Puissance PV (serre) (kWc)
- `RHUMA_PV_SOL` : Puissance PV au sol (kWc)
- `RHUMA_TARIF_S24` : Tarif S24 (€/kWh)
- `RHUMA_TVA` : TVA (%)

## 📊 Paramètres de Simulation

### Surface et Rendement

- Surface canne : 6000 m² (min: 0, max: 10000)
- Rendement canne : 120 t/ha (min: 80, max: 160)
- Teneur sucre : 15% (min: 12, max: 20)

### Extraction et Distillation

- Efficacité extraction : 80% (min: 60, max: 90)
- Efficacité distillation : 85% (min: 70, max: 95)

### Énergie PV

- Puissance PV serre : 500 kWc
- Puissance PV sol : 500 kWc
- Tarif S24 : 0.13 €/kWh
- TVA : 5%

### Coûts de Construction

- Coût PV fixe : 1000€/kWc
- Coût tracking : 250€/kWc
- Coût serre : 150€/m²
- Coût annuel : 100€/kWc

## 📈 Métriques Financières

- Prix du rhum : 30€/L
- Durée d'amortissement : 15 ans
- Taux d'intérêt annuel : 3%

## 🏅 Kudos - Système de Monnaie Complémentaire

Le système Kudos est une monnaie complémentaire qui permet aux usagers de s'échanger de l'énergie sous forme de dons plutôt que de ventes, de façon publique et nominative, selon la réputation attribué à chacun par tous.

Les Kudos sont attribués aux producteurs et aux consommateurs d'énergie et peuvent être utilisés pour recevoir de l'énergie d'autres producteurs, dont la distillerie solaire principalement mais aussi des usagers qui auraient par exemple des panneaux solaires chez eux.

Les échanges de Kudos sont considérés comme des dons, et sont à ce titre non soumis à la TVA. Ceci en raison de l'incertitude sur la réciprocité des échanges, contrairement à une vente.

- **Attribution** : 1 Kudos = 1 kWh d'énergie produite
- **Utilisation** : 1 Kudos = 1 kWh d'énergie reçue
- **Plafond mensuel** : 5000 Kudos
- **Expiration** : 12 mois

Pour plus de détails, consultez le [guide Kudos](modules/kudos/kudos_README.md).
