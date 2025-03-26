# 📚 Guide d'Utilisation

## 📋 Présentation

Ce guide vous aidera à comprendre et utiliser le simulateur de production de rhum en serre autonome. Le simulateur permet de visualiser l'impact des différents paramètres sur la production et les revenus du projet.

## 📊 Paramètres du Simulateur

### 1. Surface et Rendement

- **Surface dédiée à la canne** : De 6 000 à 10 000 m²
- **Rendement canne** : De 80 à 150 t/ha
- **Teneur en sucre** : De 12% à 20%

### 2. Extraction et Distillation

- **Efficacité extraction** : De 60% à 90%
- **Efficacité distillation** : De 70% à 95%

### 3. Énergie PV

- **Puissance PV (serre)** : De 100 à 500 kWc
- **Tarif S24** : De 0.10€ à 0.20€/kWh
- **TVA** : De 5% à 20%
- **Taxes** : De 0% à 10%
- **Efficacité panneaux** : De 15% à 25%

### 4. Énergie Solaire

- **Pertes PV** : De 0% à 30%
- **Autoconsommation** : De 0% à 100% (max 1 MWh)
- **Pertes de tracking** : De 0% à 30%

### 5. Coûts de Construction

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

## 📊 Résultats de la Simulation

### 1. Production

- Production annuelle de rhum
- Production d'énergie PV
- Autoconsommation
- Revente d'énergie

### 2. Finances

- Coûts initiaux
- Coûts annuels
- Revenus
- Bénéfices
- ROI
- Temps de retour sur investissement

### 3. Optimisation

- Comparaison systèmes PV fixe vs tracking
- Optimisation de l'autoconsommation
- Analyse des scénarios

## 📈 Export des Résultats

### 1. Format JSON

Le fichier JSON exporté contient les sections suivantes :

```json
{
    "metadata": {
        "timestamp": "2025-03-26T22:11:26+01:00",
        "version": "1.0"
    },
    "parameters": {
        "production_fixe": 1000000,  // Production annuelle en kWh
        "production_tracking": 1200000,  // Production annuelle avec tracking en kWh
        "tarifs": {
            "s24": 0.13,  // Tarif S24 en €/kWh
            "heures_creuses": 0.25  // Tarif heures creuses en €/kWh
        },
        "couts": {
            "fixe": 1000,  // Coût système PV fixe en €/kWc
            "tracking": 250,  // Coût supplémentaire tracking en €/kWc
            "construction_serre": 150,  // Coût construction serre en €/m²
            "maintenance": 50,  // Coûts annuels de maintenance en €/kWc
            "assurance": 20,  // Coûts annuels d'assurance en €/kWc
            "production": 30  // Coûts annuels de production en €/kWc
        }
    },
    "scenarios": [
        {
            "nom": "Revente EDF S24",
            "fixe": {
                "production": 1000000,
                "autoconsommation": 500000,
                "revente": 500000,
                "revenu": 65000,
                "cout_total": 135000,
                "benefice_annuel": -70000,
                "roi": -51.85,
                "temps_retour": -1.9
            },
            "tracking": {
                "production": 1200000,
                "autoconsommation": 600000,
                "revente": 600000,
                "revenu": 78000,
                "cout_total": 185000,
                "benefice_annuel": -107000,
                "roi": -57.84,
                "temps_retour": -1.7
            }
        }
        // ... autres scénarios
    ]
}
```

### 2. Google Sheets

Les résultats sont exportés dans une feuille Google Sheets structurée avec :

1. **Format structuré** : Les données sont organisées dans un format tabulaire clair et facile à lire.
2. **Partage collaboratif** : La feuille peut être partagée et modifiée en temps réel par plusieurs utilisateurs.
3. **Calculs dynamiques** : Les formules peuvent être ajoutées pour effectuer des calculs supplémentaires.
4. **Visualisation** : Graphiques et tableaux dynamiques peuvent être créés directement dans Google Sheets.

Pour utiliser l'export vers Google Sheets, vous devez :

1. Créer un projet Google Cloud Platform (GCP)
2. Activer l'API Google Sheets
3. Créer des credentials (fichier JSON) et les placer dans le répertoire du projet
4. Configurer les permissions d'accès

Une fois configuré, cliquez sur le bouton "Exporter vers Google Sheets" pour créer une nouvelle feuille avec tous les résultats et paramètres de la simulation. La feuille sera automatiquement partagée avec l'adresse email configurée.

## 📋 Support

Pour toute question ou problème, consultez la documentation technique ou contactez l'équipe de développement.

Email : institutmariani@gmail.com
Site : https://github.com/JeanHuguesRobert/Rhuma
