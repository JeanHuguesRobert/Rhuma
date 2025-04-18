"""
Configuration pivot pour Rhuma
"""

import os
from datetime import datetime
from config import (
    SURFACE_CANNE_MIN,
    SURFACE_CANNE_MAX,
    RENDEMENT_CANNE_MIN,
    RENDEMENT_CANNE_MAX,
    TENEUR_SUCRE_MIN,
    TENEUR_SUCRE_MAX,
    EFFICACITE_EXTRACTION_MIN,
    EFFICACITE_EXTRACTION_MAX,
    EFFICACITE_DISTILLATION_MIN,
    EFFICACITE_DISTILLATION_MAX,
    PV_SERRE_MAX,
    PV_SOL_MAX,
    TARIF_S24_MIN,
    TARIF_S24_MAX,
    TVA_MIN,
    TVA_MAX,
    LIMITE_PUISSANCE_S24,
    HEURES_PLEIN_SOLEIL,
    LIMITE_PRODUCTION_S24,
    TARIF_S24_DEPASSEMENT
)

# Configuration pivot de Rhuma
RHUMA = {
    "metadata": {
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "project_id": os.getenv('RHUMA_ID', 'rhuma'),
        "project_label": os.getenv('RHUMA_LABEL', 'Rhum Solaire de Corse')
    },
    "configuration": {
        "surface_canne": float(os.getenv('RHUMA_SURFACE_CANNE', '3000')),
        "rendement_canne": float(os.getenv('RHUMA_RENDEMENT_CANNE', '120')),
        "teneur_sucre": float(os.getenv('RHUMA_TENEUR_SUCRE', '15')),
        "efficacite_extraction": float(os.getenv('RHUMA_EFFICACITE_EXTRACTION', '80')),
        "efficacite_distillation": float(os.getenv('RHUMA_EFFICACITE_DISTILLATION', '85')),
        "pv_serre": float(os.getenv('RHUMA_PV_SERRE', '300')),
        "pv_sol": float(os.getenv('RHUMA_PV_SOL', '200')),
        "tarif_s24": float(os.getenv('RHUMA_TARIF_S24', '0.12')),
        "tva": float(os.getenv('RHUMA_TVA', '5')),
        "cout_fixe": float(os.getenv('RHUMA_COUT_FIXE', '1000')),
        "cout_tracking": float(os.getenv('RHUMA_COUT_TRACKING', '250')),
        "cout_construction": float(os.getenv('RHUMA_COUT_CONSTRUCTION', '150')),
        "cout_maintenance": float(os.getenv('RHUMA_COUT_MAINTENANCE', '50')),
        "cout_assurance": float(os.getenv('RHUMA_COUT_ASSURANCE', '20')),
        "cout_production": float(os.getenv('RHUMA_COUT_PRODUCTION', '30')),
        "tarif_heures_creuses": float(os.getenv('RHUMA_TARIF_HEURES_CREUSES', '0.15')),
        "autoconsommation_fixe": float(os.getenv('RHUMA_AUTOCONSOOMMATION_FIXE', '100000.0')),
        "autoconsommation_tracking": float(os.getenv('RHUMA_AUTOCONSOOMMATION_TRACKING', '120000.0')),
        "prix_rhum": float(os.getenv('RHUMA_PRIX_RHUM', '20.0')),
        "pertes_pv": float(os.getenv('RHUMA_PERTES_PV', '10.0')),
        "pertes_tracking": float(os.getenv('RHUMA_PERTES_TRACKING', '5.0')),
        "precision_tracking": float(os.getenv('RHUMA_PRECISION_TRACKING', '0.2')),
        "taux_interet": float(os.getenv('RHUMA_TAUX_INTERET', '3.0')),
        "duree_amortissement": float(os.getenv('RHUMA_DUREE_AMORTISSEMENT', '20'))
    }
}

# Fonction pour mettre à jour le timestamp
def update_timestamp():
    """
    Met à jour le timestamp dans la configuration
    """
    RHUMA["metadata"]["timestamp"] = datetime.now().isoformat()

# Fonction pour mettre à jour la version
def update_version(version):
    """
    Met à jour la version dans la configuration
    
    Args:
        version (str): Nouvelle version
    """
    RHUMA["metadata"]["version"] = version

# Fonction pour mettre à jour un paramètre de configuration
def update_config(key, value):
    """
    Met à jour un paramètre de configuration
    
    Args:
        key (str): Clé du paramètre
        value: Nouvelle valeur
    """
    if key in RHUMA["configuration"]:
        RHUMA["configuration"][key] = value
        update_timestamp()

# Fonction pour obtenir la configuration complète
def get_config():
    """
    Retourne la configuration complète
    
    Returns:
        dict: Configuration complète
    """
    return RHUMA.copy()

# Fonction pour obtenir une valeur de configuration
def get_config_value(key):
    """
    Retourne une valeur de configuration
    
    Args:
        key (str): Clé du paramètre
        
    Returns:
        any: Valeur du paramètre
    """
    return RHUMA["configuration"].get(key)

# Fonction pour obtenir les métadonnées
def get_metadata():
    """
    Retourne les métadonnées
    
    Returns:
        dict: Métadonnées
    """
    return RHUMA["metadata"].copy()
