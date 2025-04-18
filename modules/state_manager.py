from typing import Dict, Any, Optional
from dataclasses import dataclass
from modules.attributes import ATTRIBUTE_CONFIGS, AttributeConfig
import os
from dotenv import load_dotenv
from datetime import datetime

@dataclass
class StateManager:
    """Gestionnaire d'état global de l'application"""
    
    def __init__(self):
        self.load_environment()
        self.initialize_state()
    
    def load_environment(self) -> None:
        """Charge les variables d'environnement"""
        load_dotenv()
        
    def initialize_state(self) -> None:
        """Initialise l'état global avec les valeurs par défaut"""
        self.state = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "language": os.getenv('RHUMA_LANGUAGE', 'fr')
            },
            "configuration": {},
            "results": {}
        }
        
        # Initialise les attributs avec leurs valeurs par défaut
        for attr_name, config in ATTRIBUTE_CONFIGS.items():
            self.state["configuration"][attr_name] = config.default
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtient une valeur de l'état"""
        try:
            # D'abord chercher dans configuration
            return self.state["configuration"][key]
        except KeyError:
            # Puis dans results
            try:
                return self.state["results"][key]
            except KeyError:
                # Puis dans metadata
                try:
                    return self.state["metadata"][key]
                except KeyError:
                    return default
                
    def get_state(self) -> dict:
        """Retourne l'état complet"""
        return self.state
    
    def set(self, key: str, value: Any) -> None:
        """Définit une valeur dans l'état"""
        # Vérifie que la valeur est du bon type
        if key in ATTRIBUTE_CONFIGS:
            config = ATTRIBUTE_CONFIGS[key]
            if not isinstance(value, config.type):
                raise TypeError(f"La valeur pour {key} doit être de type {config.type.__name__}")
            
            # Vérifie les limites si définies
            if config.min is not None and value < config.min:
                raise ValueError(f"La valeur pour {key} ne peut pas être inférieure à {config.min}")
            if config.max is not None and value > config.max:
                raise ValueError(f"La valeur pour {key} ne peut pas être supérieure à {config.max}")
            
            self.state["configuration"][key] = value
        else:
            # Déterminer si c'est un résultat ou une métadonnée
            # Liste des clés de résultats connues
            result_keys = [
                "production_pv", "production_au_sol", "autoconsommation", "revente",
                "revenu_pv", "revenu_rhum", "cout_pv", "cout_serre", "cout_total",
                "benefice_net", "roi", "temps_retour", "monthly_production", "scenarios",
                "couts_annuels"
            ]
            
            if key in result_keys:
                # Pour les résultats, on ne fait pas de validation
                self.state["results"][key] = value
            else:
                # Pour les métadonnées, on ne fait pas de validation
                self.state["metadata"][key] = value
    
    def get_config(self, key: str) -> Optional[AttributeConfig]:
        """Obtient la configuration d'un attribut"""
        return ATTRIBUTE_CONFIGS.get(key)
    
    def get_i18n(self, key: str, lang: Optional[str] = None) -> str:
        """Obtient la traduction d'un attribut"""
        if lang is None:
            lang = self.state["metadata"]["language"]
            
        config = self.get_config(key)
        if config and config.i18n and lang in config.i18n:
            return config.i18n[lang]
        return config.user_label if config else key
    
    def get_metadata(self) -> Dict[str, Any]:
        """Obtient les métadonnées de l'état"""
        return self.state["metadata"]
    
    def get_results(self) -> Dict[str, Any]:
        """Obtient les résultats de l'état"""
        return self.state["results"]
    
    def get_configuration(self) -> Dict[str, Any]:
        """Obtient la configuration de l'état"""
        return self.state["configuration"]
    
    def get_all(self) -> Dict[str, Any]:
        """Obtient l'état complet"""
        return self.state

# Instance unique du StateManager
state_manager = StateManager()

# Fonction utilitaire pour accéder facilement à l'état
def rhuma(key: str) -> Any:
    """Fonction utilitaire pour accéder/modifier l'état"""
    value = state_manager.get(key)
    if value is None:
        config = ATTRIBUTE_CONFIGS.get(key)
        if config:
            return config.default
    return value

# Fonctions utilitaires pour accéder aux labels et descriptions des attributs
def rhuma_label(key: str, lang: Optional[str] = None) -> str:
    """Fonction utilitaire pour obtenir le label utilisateur d'un attribut"""
    config = ATTRIBUTE_CONFIGS.get(key)
    if config:
        if lang is not None and config.i18n and lang in config.i18n:
            return config.i18n[lang]
        return config.user_label
    return key

def rhuma_description(key: str) -> str:
    """Fonction utilitaire pour obtenir la description d'un attribut"""
    config = ATTRIBUTE_CONFIGS.get(key)
    if config:
        return config.description
    return ""

def get_attribute_config(key: str) -> Optional[AttributeConfig]:
    """Fonction utilitaire pour obtenir la configuration complète d'un attribut"""
    return ATTRIBUTE_CONFIGS.get(key)

def get_attribute_unit(key: str) -> str:
    """Fonction utilitaire pour obtenir l'unité d'un attribut"""
    config = ATTRIBUTE_CONFIGS.get(key)
    if config and config.unit:
        return config.unit
    return ""

def get_attribute_category(key: str) -> str:
    """Fonction utilitaire pour obtenir la catégorie d'un attribut"""
    config = ATTRIBUTE_CONFIGS.get(key)
    if config:
        return config.category
    return ""

def get_all_attributes() -> Dict[str, AttributeConfig]:
    """Fonction utilitaire pour obtenir tous les attributs configurés"""
    return ATTRIBUTE_CONFIGS

def get_attributes_by_category() -> Dict[str, Dict[str, AttributeConfig]]:
    """Fonction utilitaire pour obtenir les attributs regroupés par catégorie"""
    categories = {}
    for key, config in ATTRIBUTE_CONFIGS.items():
        if config.category not in categories:
            categories[config.category] = {}
        categories[config.category][key] = config
    return categories
