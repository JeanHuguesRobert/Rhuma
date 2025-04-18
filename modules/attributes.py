from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AttributeConfig:
    """Configuration d'un attribut de l'application"""
    default: Any
    type: type
    user_label: str
    description: str
    category: str
    min: Optional[Any] = None
    max: Optional[Any] = None
    unit: Optional[str] = None
    i18n: Dict[str, str] = None

# Configuration des attributs
ATTRIBUTE_CONFIGS = {
    # Métadonnées du projet
    'id': AttributeConfig(
        default='rhuma',
        type=str,
        user_label="ID du Projet",
        description="Identifiant technique utilisé pour les fichiers de configuration",
        category="Métadonnées",
        i18n={
            'en': "Project ID",
            'fr': "ID du Projet"
        }
    ),
    'label': AttributeConfig(
        default='Rhum Solaire de Corse',
        type=str,
        user_label="Label du Projet",
        description="Nom affiché dans l'interface utilisateur",
        category="Métadonnées",
        i18n={
            'en': "Project Label",
            'fr': "Label du Projet"
        }
    ),
    'version': AttributeConfig(
        default='1.0.0',
        type=str,
        user_label="Version",
        description="Version du projet",
        category="Métadonnées",
        i18n={
            'en': "Version",
            'fr': "Version"
        }
    ),
    
    # Tracker Solaire 3D - Paramètres de calcul astronomique
    'applyRefraction': AttributeConfig(
        default=True,
        type=bool,
        user_label="Appliquer la réfraction atmosphérique",
        description="Appliquer la correction de réfraction atmosphérique pour les calculs de position solaire",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Apply Atmospheric Refraction",
            'fr': "Appliquer la réfraction atmosphérique"
        }
    ),
    'timezone': AttributeConfig(
        default=1,
        type=int,
        min=-12,
        max=12,
        user_label="Fuseau horaire",
        description="Fuseau horaire (UTC+timezone)",
        unit="h",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Timezone",
            'fr': "Fuseau horaire"
        }
    ),
    
    # Tracker Solaire 3D - Contraintes mécaniques
    'minTiltX': AttributeConfig(
        default=15,
        type=float,
        min=0,
        max=45,
        user_label="Inclinaison minimale",
        description="Inclinaison minimale du panneau (axe X)",
        unit="°",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Minimum Tilt X",
            'fr': "Inclinaison minimale"
        }
    ),
    'maxTiltX': AttributeConfig(
        default=75,
        type=float,
        min=45,
        max=90,
        user_label="Inclinaison maximale",
        description="Inclinaison maximale du panneau (axe X)",
        unit="°",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Maximum Tilt X",
            'fr': "Inclinaison maximale"
        }
    ),
    'baseCableLength': AttributeConfig(
        default=80,
        type=float,
        min=30,
        max=150,
        user_label="Longueur de câble de base",
        description="Longueur de câble de base pour le système de tracking",
        unit="cm",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Base Cable Length",
            'fr': "Longueur de câble de base"
        }
    ),
    'tiltXFactor': AttributeConfig(
        default=0.35,
        type=float,
        min=0.1,
        max=1.0,
        user_label="Facteur d'inclinaison X",
        description="Facteur de conversion entre l'angle d'inclinaison et la longueur de câble",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Tilt X Factor",
            'fr': "Facteur d'inclinaison X"
        }
    ),
    'tiltZFactor': AttributeConfig(
        default=0.8,
        type=float,
        min=0.1,
        max=1.5,
        user_label="Facteur d'orientation Z",
        description="Facteur de conversion entre l'angle d'orientation et la longueur de câble",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Tilt Z Factor",
            'fr': "Facteur d'orientation Z"
        }
    ),
    'minLength': AttributeConfig(
        default=30,
        type=float,
        min=10,
        max=50,
        user_label="Longueur minimale de câble",
        description="Longueur minimale des câbles du système de tracking",
        unit="cm",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Minimum Cable Length",
            'fr': "Longueur minimale de câble"
        }
    ),
    'maxLength': AttributeConfig(
        default=120,
        type=float,
        min=80,
        max=200,
        user_label="Longueur maximale de câble",
        description="Longueur maximale des câbles du système de tracking",
        unit="cm",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Maximum Cable Length",
            'fr': "Longueur maximale de câble"
        }
    ),
    'maxDifference': AttributeConfig(
        default=50,
        type=float,
        min=20,
        max=100,
        user_label="Différence maximale entre câbles",
        description="Différence maximale autorisée entre les longueurs des deux câbles",
        unit="cm",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Maximum Cable Difference",
            'fr': "Différence maximale entre câbles"
        }
    ),
    'elasticity': AttributeConfig(
        default=0.05,
        type=float,
        min=0,
        max=0.2,
        user_label="Élasticité des câbles",
        description="Coefficient d'élasticité des câbles (0 = rigide, 1 = très élastique)",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Cable Elasticity",
            'fr': "Élasticité des câbles"
        }
    ),
    'demoSpeed': AttributeConfig(
        default=1,
        type=float,
        min=0.1,
        max=5,
        user_label="Vitesse de démonstration",
        description="Vitesse de la démonstration du tracker solaire",
        category="Tracker Solaire 3D",
        i18n={
            'en': "Demo Speed",
            'fr': "Vitesse de démonstration"
        }
    ),
    # Surface et Rendement
    'surface_canne': AttributeConfig(
        default=3000,
        type=int,
        min=0,
        max=10000,
        user_label="Surface canne",
        description="Surface totale dédiée à la culture de la canne à sucre",
        unit="m²",
        category="Surface et Rendement",
        i18n={
            'en': "Sugar Cane Surface",
            'fr': "Surface canne"
        }
    ),
    'rendement_canne': AttributeConfig(
        default=120,
        type=float,
        min=80,
        max=160,
        user_label="Rendement canne",
        description="Rendement annuel de la canne à sucre",
        unit="t/ha",
        category="Surface et Rendement",
        i18n={
            'en': "Sugar Cane Yield",
            'fr': "Rendement canne"
        }
    ),
    'teneur_sucre': AttributeConfig(
        default=15,
        type=float,
        min=10,
        max=20,
        user_label="Teneur sucre",
        description="Pourcentage de sucre dans la canne à sucre",
        unit="%",
        category="Surface et Rendement",
        i18n={
            'en': "Sugar Content",
            'fr': "Teneur sucre"
        }
    ),
    # Extraction et Distillation
    'efficacite_extraction': AttributeConfig(
        default=80,
        type=float,
        min=60,
        max=95,
        user_label="Efficacité extraction",
        description="Efficacité du processus d'extraction du sucre",
        unit="%",
        category="Extraction et Distillation",
        i18n={
            'en': "Extraction Efficiency",
            'fr': "Efficacité extraction"
        }
    ),
    'efficacite_distillation': AttributeConfig(
        default=85,
        type=float,
        min=60,
        max=95,
        user_label="Efficacité distillation",
        description="Efficacité du processus de distillation",
        unit="%",
        category="Extraction et Distillation",
        i18n={
            'en': "Distillation Efficiency",
            'fr': "Efficacité distillation"
        }
    ),
    # Énergie PV
    'pv_serre': AttributeConfig(
        default=300,
        type=float,
        min=0,
        max=500,
        user_label="Puissance PV (serre)",
        description="Puissance installée en panneaux photovoltaïques sur la serre",
        unit="kWc",
        category="Énergie PV",
        i18n={
            'en': "PV Power (Greenhouse)",
            'fr': "Puissance PV (serre)"
        }
    ),
    'pv_sol': AttributeConfig(
        default=200,
        type=float,
        min=100,
        max=500,
        user_label="Puissance PV (au sol)",
        description="Puissance installée en panneaux photovoltaïques au sol",
        unit="kWc",
        category="Énergie PV",
        i18n={
            'en': "PV Power (Ground)",
            'fr': "Puissance PV (au sol)"
        }
    ),
    'tarif_s24': AttributeConfig(
        default=0.12,
        type=float,
        min=0.05,
        max=0.20,
        user_label="Tarif S24",
        description="Tarif de rachat S24 pour la Corse",
        unit="€/kWh",
        category="Énergie PV",
        i18n={
            'en': "S24 Tariff",
            'fr': "Tarif S24"
        }
    ),
    'tva': AttributeConfig(
        default=5,
        type=float,
        min=0,
        max=20,
        user_label="TVA",
        description="Taux de TVA applicable",
        unit="%",
        category="Énergie PV",
        i18n={
            'en': "VAT",
            'fr': "TVA"
        }
    ),
    # Coûts
    'cout_fixe': AttributeConfig(
        default=1000,
        type=float,
        min=0,
        max=None,
        user_label="Coût système PV fixe",
        description="Coût d'installation du système PV fixe",
        unit="€/kWc",
        category="Coûts",
        i18n={
            'en': "Fixed PV System Cost",
            'fr': "Coût système PV fixe"
        }
    ),
    'cout_tracking': AttributeConfig(
        default=250,
        type=float,
        min=0,
        max=None,
        user_label="Coût système tracking",
        description="Coût d'installation du système de tracking",
        unit="€/kWc",
        category="Coûts",
        i18n={
            'en': "Tracking System Cost",
            'fr': "Coût système tracking"
        }
    ),
    'cout_construction': AttributeConfig(
        default=150,
        type=float,
        min=0,
        max=None,
        user_label="Coût construction serre",
        description="Coût de construction de la serre",
        unit="€/m²",
        category="Coûts",
        i18n={
            'en': "Greenhouse Construction Cost",
            'fr': "Coût construction serre"
        }
    ),
    'cout_maintenance': AttributeConfig(
        default=50,
        type=float,
        min=0,
        max=None,
        user_label="Coût maintenance",
        description="Coût annuel de maintenance",
        unit="€/kWc",
        category="Coûts",
        i18n={
            'en': "Maintenance Cost",
            'fr': "Coût maintenance"
        }
    ),
    'cout_assurance': AttributeConfig(
        default=20,
        type=float,
        min=0,
        max=None,
        user_label="Coût assurance",
        description="Coût annuel d'assurance",
        unit="€/kWc",
        category="Coûts",
        i18n={
            'en': "Insurance Cost",
            'fr': "Coût assurance"
        }
    ),
    'cout_production': AttributeConfig(
        default=30,
        type=float,
        min=0,
        max=None,
        user_label="Coût production",
        description="Coût annuel de production",
        unit="€/kWc",
        category="Coûts",
        i18n={
            'en': "Production Cost",
            'fr': "Coût production"
        }
    ),
    'tarif_heures_creuses': AttributeConfig(
        default=0.15,
        type=float,
        min=0,
        max=None,
        user_label="Tarif heures creuses",
        description="Tarif appliqué pendant les heures creuses",
        unit="€/kWh",
        category="Coûts",
        i18n={
            'en': "Off-Peak Tariff",
            'fr': "Tarif heures creuses"
        }
    ),
    'autoconsommation_fixe': AttributeConfig(
        default=100000.0,
        type=float,
        min=0,
        max=None,
        user_label="Autoconsommation fixe",
        description="Autoconsommation annuelle du système PV fixe",
        unit="kWh",
        category="Autoconsommation",
        i18n={
            'en': "Fixed Self-Consumption",
            'fr': "Autoconsommation fixe"
        }
    ),
    'autoconsommation_tracking': AttributeConfig(
        default=120000.0,
        type=float,
        min=0,
        max=None,
        user_label="Autoconsommation tracking",
        description="Autoconsommation annuelle du système de tracking",
        unit="kWh",
        category="Autoconsommation",
        i18n={
            'en': "Tracking Self-Consumption",
            'fr': "Autoconsommation tracking"
        }
    ),
    'prix_rhum': AttributeConfig(
        default=20.0,
        type=float,
        min=0,
        max=None,
        user_label="Prix du rhum",
        description="Prix de vente du rhum",
        unit="€/L",
        category="Prix",
        i18n={
            'en': "Rum Price",
            'fr': "Prix du rhum"
        }
    ),
    'pertes_pv': AttributeConfig(
        default=10.0,
        type=float,
        min=0,
        max=100,
        user_label="Pertes PV",
        description="Pourcentage de pertes du système PV",
        unit="%",
        category="Pertes",
        i18n={
            'en': "PV Losses",
            'fr': "Pertes PV"
        }
    ),
    'pertes_tracking': AttributeConfig(
        default=5.0,
        type=float,
        min=0,
        max=100,
        user_label="Pertes tracking",
        description="Pourcentage de pertes du système de tracking",
        unit="%",
        category="Pertes",
        i18n={
            'en': "Tracking Losses",
            'fr': "Pertes tracking"
        }
    ),
    'precision_tracking': AttributeConfig(
        default=0.2,
        type=float,
        min=0,
        max=1,
        user_label="Précision tracking",
        description="Précision du système de tracking",
        unit="°",
        category="Pertes",
        i18n={
            'en': "Tracking Precision",
            'fr': "Précision tracking"
        }
    ),
    'taux_interet': AttributeConfig(
        default=3.0,
        type=float,
        min=0,
        max=100,
        user_label="Taux d'intérêt",
        description="Taux d'intérêt annuel pour les calculs financiers",
        unit="%",
        category="Finances",
        i18n={
            'en': "Interest Rate",
            'fr': "Taux d'intérêt"
        }
    ),
    'duree_amortissement': AttributeConfig(
        default=20,
        type=int,
        min=1,
        max=None,
        user_label="Durée d'amortissement",
        description="Durée d'amortissement des investissements",
        unit="ans",
        category="Finances",
        i18n={
            'en': "Amortization Period",
            'fr': "Durée d'amortissement"
        }
    ),
    # Système de tracking solaire
    'baseCableLength': AttributeConfig(
        default=80,
        type=float,
        min=30,
        max=150,
        user_label="Longueur de base des câbles",
        description="Longueur de base des câbles du système de tracking",
        unit="cm",
        category="Tracking Solaire",
        i18n={
            'en': "Base Cable Length",
            'fr': "Longueur de base des câbles"
        }
    ),
    'tiltXFactor': AttributeConfig(
        default=0.35,
        type=float,
        min=0.1,
        max=1.0,
        user_label="Facteur d'inclinaison X",
        description="Facteur d'ajustement pour l'inclinaison nord-sud",
        unit="",
        category="Tracking Solaire",
        i18n={
            'en': "Tilt X Factor",
            'fr': "Facteur d'inclinaison X"
        }
    ),
    'tiltZFactor': AttributeConfig(
        default=0.8,
        type=float,
        min=0.1,
        max=1.5,
        user_label="Facteur d'orientation Z",
        description="Facteur d'ajustement pour l'orientation est-ouest",
        unit="",
        category="Tracking Solaire",
        i18n={
            'en': "Tilt Z Factor",
            'fr': "Facteur d'orientation Z"
        }
    ),
    'minLength': AttributeConfig(
        default=30,
        type=float,
        min=10,
        max=50,
        user_label="Longueur minimale des câbles",
        description="Longueur minimale des câbles du système de tracking",
        unit="cm",
        category="Tracking Solaire",
        i18n={
            'en': "Minimum Cable Length",
            'fr': "Longueur minimale des câbles"
        }
    ),
    'maxLength': AttributeConfig(
        default=120,
        type=float,
        min=80,
        max=200,
        user_label="Longueur maximale des câbles",
        description="Longueur maximale des câbles du système de tracking",
        unit="cm",
        category="Tracking Solaire",
        i18n={
            'en': "Maximum Cable Length",
            'fr': "Longueur maximale des câbles"
        }
    ),
    'maxDifference': AttributeConfig(
        default=50,
        type=float,
        min=20,
        max=100,
        user_label="Différence maximale entre câbles",
        description="Différence maximale autorisée entre les longueurs de câbles",
        unit="cm",
        category="Tracking Solaire",
        i18n={
            'en': "Maximum Cable Difference",
            'fr': "Différence maximale entre câbles"
        }
    ),
    # Système PV
    'trackingFactor': AttributeConfig(
        default=1.3,
        type=float,
        min=1.0,
        max=1.5,
        user_label="Facteur de gain tracking",
        description="Facteur moyen de gain de production avec le système de tracking",
        unit="",
        category="Énergie PV",
        i18n={
            'en': "Tracking Gain Factor",
            'fr': "Facteur de gain tracking"
        }
    ),
    'losses': AttributeConfig(
        default=14.0,
        type=float,
        min=0.0,
        max=30.0,
        user_label="Pertes système PV",
        description="Pertes standard du système PV (câblage, conversion, etc.)",
        unit="%",
        category="Pertes",
        i18n={
            'en': "PV System Losses",
            'fr': "Pertes système PV"
        }
    )
}

# Nouvelle fonction pour valider et normaliser les paramètres d'entrée
def validate_parameters(input_params: dict) -> dict:
    validated = {}
    for key, config in ATTRIBUTE_CONFIGS.items():
        # Utiliser la valeur fournie ou la valeur par défaut
        value = input_params.get(key, config.default)
        # S'assurer que la valeur est du bon type, sinon tenter la conversion
        try:
            if not isinstance(value, config.type):
                value = config.type(value)
        except Exception:
            value = config.default
        # Appliquer le minimum si défini
        if config.min is not None and value < config.min:
            value = config.min
        # Appliquer le maximum si défini
        if config.max is not None and value > config.max:
            value = config.max
        validated[key] = value
    return validated
