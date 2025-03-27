# 🌺 Rhum Solaire de Corse

## 🎯 Description

Simulateur de production de rhum sous serre solaire à Corte, Corse. L'application permet de simuler et optimiser la production de rhum en tenant compte des aspects énergétiques, agricoles et financiers.

## 📊 Fonctionnalités

- Simulation de la production PV avec tracking
- Simulation de la croissance de la canne
- Simulation de la production de rhum
- Optimisation des coûts
- Export des résultats vers JSON et Google Sheets
- Documentation intégrée

## 🚀 Installation

### 1. Cloner le Projet

```bash
git clone https://github.com/JeanHuguesRobert/Rhuma.git
cd Rhuma
```

### 2. Bootstrap (Linux/Mac)

```bash
chmod +x bootstrap.sh
./bootstrap.sh
```

### 2. Bootstrap (Windows)

```bash
bootstrap.bat
```

### 3. Lancer l'Application

```bash
npm start
```

## 🛠️ Démarrage

```bash
# Lancer l'application
streamlit run streamlit_app.py
```

## 📊 Configuration

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

## 📚 Documentation

- [Guide Utilisateur](docs/user_guide.md)
- [Architecture Technique](docs/ARCHITECTURE.md)
- [Guide de Déploiement](docs/DEPLOYMENT.md)
- [Roadmap](docs/ROADMAP.md)

## 📊 Métriques de Performance

### Production
- 150 000 L de rhum/an
- 1 500 000 kWh d'électricité/an
- 1 MWc d'autoconsommation
- 20% de gains avec le tracking

### Finances
- Coût PV fixe : 1000€/kWc
- Coût tracking : 250€/kWc
- Coût serre : 150€/m²
- Coût annuel : 100€/kWc

## 🛠️ Maintenance

### Mises à jour
- Mise à jour des dépendances
- Mise à jour des API
- Mise à jour des modèles

### Sauvegarde
- Sauvegarde des données
- Sauvegarde des configurations
- Sauvegarde des résultats

## 📈 Monitoring

- Logs d'application
- Logs d'erreurs
- Logs d'activité
- Métriques de performance

## 📝 License

Ce projet est sous licence MIT.
