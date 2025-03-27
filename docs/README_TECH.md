# 🚀 Technical Documentation for Rhuma Project

## 📋 Overview

Rhuma is a simulation and optimization application for solar rum production in Corsica. This technical documentation provides detailed information for developers and technical stakeholders.

## 🛠️ Project Structure

```
rhuma/
├── modules/          # Application modules
│   ├── data_export.py    # Data export functionality
│   ├── pvgis_analysis.py # PVGIS analysis module
│   ├── attributes.py     # Attribute configuration
│   └── state_manager.py  # State management
├── docs/             # Documentation
└── tests/            # Tests
```

## 🛠️ Technical Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install streamlit pandas matplotlib numpy gspread oauth2client
```

### 2. Environment Variables

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

## 📊 Data Structure

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

## 🚀 Deployment

### 1. Local Development

```bash
# Run the application
streamlit run streamlit_app.py
```

### 2. Cloud Deployment

#### Heroku

```bash
# Create Heroku app
heroku create rhuma-app

# Set environment variables
heroku config:set RHUMA_ID=rhuma
heroku config:set RHUMA_LABEL="Rhum Solaire de Corse"

# Deploy the application
git push heroku main
```

#### Docker (Optional)

```bash
# 1. Clone the repository
gh repo clone JeanHuguesRobert/Rhuma

cd Rhuma

# 2. Create a new repository
gh repo create your-project-name --public

# 3. Configure the new repository
git remote rename origin upstream
git remote add origin https://github.com/your-username/your-project-name.git
git push -u origin main
```
