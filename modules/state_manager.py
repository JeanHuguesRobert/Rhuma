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
                "id": os.getenv('RHUMA_ID', 'rhuma'),
                "label": os.getenv('RHUMA_LABEL', 'Rhum Solaire de Corse'),
                "version": os.getenv('RHUMA_VERSION', "1.0.0"),
                "timestamp": datetime.now().isoformat(),
                "language": os.getenv('RHUMA_LANGUAGE', 'fr')
            },
            "configuration": {}
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
    
    def get_all(self) -> Dict[str, Any]:
        """Obtient l'état complet"""
        return self.state

# Instance unique du StateManager
state_manager = StateManager()

# Fonction utilitaire pour accéder facilement à l'état
def rhuma(key: str, value: Any = None) -> Any:
    """Fonction utilitaire pour accéder/modifier l'état"""
    if value is not None:
        state_manager.set(key, value)
    return state_manager.get(key)
