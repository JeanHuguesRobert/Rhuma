from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AttributeConfig:
    """Configuration d'un attribut de l'application"""
    default: Any
    type: type
    min: Optional[Any] = None
    max: Optional[Any] = None
    user_label: str
    description: str
    unit: Optional[str] = None
    category: str
    i18n: Dict[str, str] = None

# Configuration des attributs
ATTRIBUTE_CONFIGS = {
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
    )
}
