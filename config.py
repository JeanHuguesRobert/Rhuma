# Configuration du projet Rhum Solaire de Corte

# Constantes du projet
PROJECT_NAME = "Rhum Solaire de Corte"
LOCATION = "Corte, Corse"

# Paramètres techniques
SURFACE_TOTALE = 10000  # m² (1 hectare)
SURFACE_CANNE_MIN = 6000  # m²
SURFACE_CANNE_MAX = 10000  # m²
SURFACE_LOCAUX = 1000  # m²

# Puissance PV
PV_SERRE_MAX = 500  # kWc
PV_SOL_MAX = 500  # kWc

# Limites réglementaires
LIMITE_AUTOCONSOMMATION = 1000  # kWh/an (1 MWh)
LIMITE_HEURES_ENSOLEILLEMENT = 1600  # heures/an
TARIF_S24_MAX = 0.20  # €/kWh
TARIF_AU_DELA = 0.05  # €/kWh

# Paramètres de production
RENDEMENT_CANNE_MIN = 50  # t/ha
RENDEMENT_CANNE_MAX = 150  # t/ha
TENEUR_SUCRE_MIN = 10  # %
TENEUR_SUCRE_MAX = 20  # %

# Efficacités
EFFICACITE_EXTRACTION_MIN = 60  # %
EFFICACITE_EXTRACTION_MAX = 95  # %
EFFICACITE_DISTILLATION_MIN = 70  # %
EFFICACITE_DISTILLATION_MAX = 95  # %

# Paramètres énergétiques
PERTES_PV_MAX = 30  # %
PERTES_TRACKING_MAX = 30  # %

# Tarifs
TARIF_S24_MIN = 0.10  # €/kWh
TARIF_S24_MAX = 0.20  # €/kWh
TVA_MIN = 5  # %
TVA_MAX = 20  # %
TAXES_MAX = 10  # %

# Prix du rhum
PRIX_RHUM_MIN = 15  # €/L
PRIX_RHUM_MAX = 60  # €/L

# Objectifs de crowdfunding
CROWDFUNDING_PHASES = {
    1: {"montant": 100000, "description": "Validation technique"},
    2: {"montant": 900000, "description": "Construction de la serre"},
    3: {"montant": 500000, "description": "Développement de l'autoconsommation collective"}
}

# Liens utiles
LINKS = {
    "simulateur": "https://acorsica.streamlit.app/",
    "site_web": "https://github.com/jeanhuguesrobert/Rhuma",
    "facebook": "https://facebook.com/institutmariani",
    "linkedin": "https://linkedin.com/company/jeanhuguesrobert",
}

# Contact
EMAIL_CONTACT = "institutmariani@]gmail.com"
