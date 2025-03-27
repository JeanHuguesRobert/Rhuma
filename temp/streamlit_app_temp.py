import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from dotenv import load_dotenv
import zipfile
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
import tempfile
import shutil
from modules.data_export import export_to_google_sheets, export_to_excel, export_to_json
from modules.pvgis_analysis import pvgis_analysis_section
from modules.rhuma_state import rhuma

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'état RHUMA avec les valeurs par défaut
RHUMA = {
    "metadata": {
        "id": os.getenv('RHUMA_ID', 'rhuma'),
        "label": os.getenv('RHUMA_LABEL', 'Rhum Solaire de Corse'),
        "version": os.getenv('RHUMA_VERSION', "1.0.0"),
        "timestamp": datetime.now().isoformat()
    },
    "configuration": {
        "surface_canne": int(os.getenv('RHUMA_SURFACE_CANNE', '3000')),
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
        "duree_amortissement": int(os.getenv('RHUMA_DUREE_AMORTISSEMENT', '20'))
    }
}

# Constantes de configuration
SURFACE_CANNE_MIN = 1000  # m²
SURFACE_CANNE_MAX = 5000  # m²

RENDEMENT_CANNE_MIN = 80  # t/ha
RENDEMENT_CANNE_MAX = 160  # t/ha

TENEUR_SUCRE_MIN = 10  # %
TENEUR_SUCRE_MAX = 20  # %

EFFICACITE_EXTRACTION_MIN = 60  # %
EFFICACITE_EXTRACTION_MAX = 95  # %

EFFICACITE_DISTILLATION_MIN = 60  # %
EFFICACITE_DISTILLATION_MAX = 95  # %

PV_SERRE_MAX = 500  # kWc

PV_SOL_MAX = 500  # kWc

TARIF_S24_MIN = 0.05  # €/kWh
TARIF_S24_MAX = 0.20  # €/kWh

TVA_MIN = 0  # %
TVA_MAX = 20  # %

LIMITE_PUISSANCE_S24 = 500  # kWc
HEURES_PLEIN_SOLEIL = 1600  # heures/an
LIMITE_PRODUCTION_S24 = LIMITE_PUISSANCE_S24 * HEURES_PLEIN_SOLEIL  # kWh/an
TARIF_S24_DEPASSEMENT = 0.05  # €/kWh au-delà de la limite

# Configuration de la page
st.set_page_config(
    page_title="Rhum Solaire de Corse",
    page_icon="🌞",
    layout="wide"
)

# Titre principal
st.title("🌞 Rhum Solaire de Corse")

# Sidebar configuration
with st.sidebar:
    st.header("🛠️ Configuration")

    # 1. Surface et Rendement
    surface_canne = st.number_input("Surface dédiée à la canne (m²)", 
                                  SURFACE_CANNE_MIN, SURFACE_CANNE_MAX, 
                                  st.session_state.get('surface_canne', rhuma('surface_canne')))

    rendement_canne = st.slider("Rendement canne (t/ha)", 
                              RENDEMENT_CANNE_MIN, RENDEMENT_CANNE_MAX, 
                              st.session_state.get('rendement_canne', rhuma('rendement_canne')))

    teneur_sucre = st.slider("Teneur en sucre (%)", 
                           TENEUR_SUCRE_MIN, TENEUR_SUCRE_MAX, 
                           st.session_state.get('teneur_sucre', rhuma('teneur_sucre')))

    # 2. Extraction et Distillation
    efficacite_extraction = st.slider("Efficacité extraction (%)", 
                                   EFFICACITE_EXTRACTION_MIN, 
                                   EFFICACITE_EXTRACTION_MAX, 
                                   st.session_state.get('efficacite_extraction', rhuma('efficacite_extraction')))

    efficacite_distillation = st.slider("Efficacité distillation (%)", 
                                     EFFICACITE_DISTILLATION_MIN, 
                                     EFFICACITE_DISTILLATION_MAX, 
                                     st.session_state.get('efficacite_distillation', rhuma('efficacite_distillation')))

    # 3. Énergie PV
    puissance_pv = st.number_input("Puissance PV (serre) (kWc)", 
                                0, PV_SERRE_MAX, 
                                st.session_state.get('pv_serre', rhuma('pv_serre')),
                                help=f"Limite légale : {LIMITE_PUISSANCE_S24} kWc pour bénéficier du tarif S24")

    tarif_s24 = st.number_input("Tarif S24 (€/kWh)", 
                              TARIF_S24_MIN, TARIF_S24_MAX, 
                              st.session_state.get('tarif_s24', rhuma('tarif_s24')),
                              help="Tarif de rachat S24 pour la Corse")

    tarif_tva = st.number_input("TVA (%)", 
                              TVA_MIN, TVA_MAX, 
                              st.session_state.get('tva', rhuma('tva')))

    tarif_taxes = st.number_input("Taxes (%)", 
                               0, 100, 
                               st.session_state.get('taxes', 0))

    # 5. Énergie PV au sol
    capacite_au_sol = st.number_input("Capacité PV (au sol) (kWc)", 
                                     100, PV_SOL_MAX, 
                                     st.session_state.get('pv_sol', rhuma('pv_sol')),
                                     help="Production supplémentaire grâce aux panneaux au sol")

    # 6. Limites réglementaires
    st.write("### 📝 Limites Réglementaires")
    st.write(f"- Limite de puissance S24 : {LIMITE_PUISSANCE_S24} kWc")
    st.write(f"- Heures de plein soleil annuelles : {HEURES_PLEIN_SOLEIL} heures")
    st.write(f"- Limite de production S24 : {LIMITE_PRODUCTION_S24/1000:.2f} MWh/an")
    st.write(f"- Tarif au-delà de la limite : {TARIF_S24_DEPASSEMENT} €/kWh")

# Appel des sections
financial_simulation_section()
pvgis_analysis_section(RHUMA)

# Détails techniques
with st.expander("📊 Détails des Calculs"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📊 Production PV")
        st.write(f"- Production serre : {production_pv_ideal:.2f} MWh/an")
        st.write(f"- Production au sol : {production_au_sol:.2f} MWh/an")
        st.write(f"- Production totale : {production_total:.2f} MWh/an")
        
    with col2:
        st.write("### 💰 Revenus")
        st.write(f"- Revenu PV : {revenu_pv/1000:.2f} k€/an")
        st.write(f"- Revenu Rhum : {revenu_rhum/1000:.2f} k€/an")
        st.write(f"- Revenu total : {revenu_total/1000:.2f} k€/an")

# Export des données
with st.expander("💾 Export des Données"):
    export_all_formats()

{{ ... }}
