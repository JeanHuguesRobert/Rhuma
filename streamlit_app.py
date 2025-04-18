# streamlit_app.py
#   Rhuma, rhum solaire de Corse
#
# (c) Jean Hugues Robert, 03/2025
# MIT License

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
import numpy as np
from dotenv import load_dotenv

from modules.exports import export_to_google_sheets, get_google_sheet_client
from modules.pvgis_analysis import pvgis_analysis_section
from modules.state_manager import rhuma, StateManager
from modules.solar_tracker_3d import solar_tracker_3d_section
from modules.financial import financial_simulation_section, simulate_financial_scenarios, calculate_total_costs
from modules.exports import export_to_json, export_to_csv, export_to_excel, export_all_formats
from modules.tracking import tracking_optimization_section, tracking_comparison_section  # <-- new import

# Charger les variables d'environnement
load_dotenv()

# Initialiser le gestionnaire d'état
state_manager = StateManager()

# Initialiser l'état avec les valeurs par défaut
state_manager.get_state()

# Configuration de la page
st.set_page_config(page_title="Simulateur Rhuma, rhum solaire en Corse", layout="wide")
st.title(f"{rhuma('label')}")  # using rhuma("label") inline

# Lecture et affichage des documents Markdown
DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

def read_markdown_file(markdown_file):
    """Lire et retourner le contenu d'un fichier Markdown."""
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Erreur lors de la lecture du fichier: {str(e)}"

st.markdown("""
## 📚 Documentation

- [Guide Utilisateur](docs/user_guide.md)
- [Architecture Technique](docs/ARCHITECTURE.md)
- [Guide de Déploiement](docs/DEPLOYMENT.md)
- [Roadmap](docs/ROADMAP.md) - Vision stratégique du projet et objectifs à long terme
- [TODO](docs/TODO.md) - Liste des tâches opérationnelles et en cours

[GitHub Repository](https://github.com/JeanHuguesRobert/Rhuma)
""")

# Créer des onglets pour la documentation et les simulations
doc_tabs = st.tabs(["Crowdfunding", "Documentation technique", "Guide utilisateur", "Simulation 3D du Tracker"])

with doc_tabs[0]:
    crowdfunding_content = read_markdown_file(os.path.join(DOCS_DIR, "crowdfunding.md"))
    st.markdown(crowdfunding_content)

with doc_tabs[1]:
    technical_content = read_markdown_file(os.path.join(DOCS_DIR, "ARCHITECTURE.md"))
    st.markdown(technical_content)

with doc_tabs[2]:
    guide_content = read_markdown_file(os.path.join(DOCS_DIR, "user_guide.md"))
    st.markdown(guide_content)
    
with doc_tabs[3]:
    # Afficher la simulation 3D du tracker solaire
    solar_tracker_3d_section()

# Dans votre script Streamlit principal, ajoutez ceci après vos sections existantes
financial_simulation_section()
pvgis_analysis_section()

# Section de simulation du tracking présentant les deux résultats avec delta
st.header("Simulation du Tracking")
# Baseline : sans tracking = valeur de base
baseline_value = float(rhuma("pv_serre"))
# Avec tracking calculé (simulé avec facteur 1.05)
tracking_value = baseline_value * 1.05
delta_tracking = tracking_value - baseline_value

col1, col2, col3 = st.columns(3)
col1.subheader("Sans Tracking")
col1.write(f"{baseline_value:.2f} kWc")

col2.subheader("Avec Tracking")
col2.write(f"{tracking_value:.2f} kWc")

col3.subheader("Delta")
col3.write(f"{delta_tracking:.2f} kWc")

# Export des résultats
st.header("Exporter les Résultats")

# Bouton d'export complet
if st.button("💾 Exporter tout"):    
    # Stocker les résultats dans le gestionnaire d'état
    state_manager.set("production_pv", rhuma("pv_serre"))
    state_manager.set("production_au_sol", rhuma("pv_sol"))
    state_manager.set("autoconsommation", 30)  # Exemple de valeur
    state_manager.set("revente", 70)          # Exemple de valeur
    state_manager.set("revenu_pv", 10000)      # Exemple de valeur
    state_manager.set("revenu_rhum", 20000)    # Exemple de valeur
    state_manager.set("cout_pv", 5000)         # Exemple de valeur
    state_manager.set("cout_serre", 10000)     # Exemple de valeur
    state_manager.set("cout_total", 15000)     # Exemple de valeur
    state_manager.set("benefice_net", 5000)    # Exemple de valeur
    state_manager.set("roi", 10)               # Exemple de valeur
    state_manager.set("temps_retour", 5)       # Exemple de valeur
    state_manager.set("monthly_production", {})  # Exemple de valeur
    state_manager.set("scenarios", [])            # Exemple de valeur
    
    # Utiliser directement les résultats du gestionnaire d'état
    export_all_formats(state_manager.get_results())

# Lien vers le dépôt GitHub
st.markdown("[GitHub Repository](https://github.com/JeanHuguesRobert/Rhuma)")
