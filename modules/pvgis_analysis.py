import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pvgis import PVGIS  # Import du module PVGIS
from modules.rhuma_state import rhuma

def pvgis_analysis_section(rhuma_state):
    """
    Section d'analyse PVGIS dans l'interface Streamlit
    
    Args:
        rhuma_state (dict): État global du projet RHUMA
    """
    st.header("🌞 Analyse PVGIS")
    
    # Paramètres de configuration
    with st.expander("🔧 Configuration du Système PV"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Configuration de l'emplacement
            st.subheader("📍 Emplacement")
            address = st.text_input("Adresse", "Corte, Corse")
            latitude = st.number_input("Latitude", value=42.703611, min_value=-90.0, max_value=90.0)
            longitude = st.number_input("Longitude", value=9.085278, min_value=-180.0, max_value=180.0)
            
        with col2:
            # Configuration du système PV
            st.subheader("⚡ Configuration PV")
            capacity = st.number_input("Capacité installée (kWc)", 
                                     value=rhuma('pv_serre') + rhuma('pv_sol'), 
                                     min_value=0.0)
            tilt = st.slider("Angle de pose (°)", 0, 90, 30)
            orientation = st.slider("Orientation (°)", -180, 180, -180)
            tracking = st.checkbox("Utiliser le suivi de soleil")
            
    # Bouton d'analyse
    if st.button("🔍 Analyser"):
        with st.spinner("Analyse en cours..."):
            # Initialiser l'API PVGIS
            pvgis = PVGIS()
            
            # Préparer les paramètres avec l'état RHUMA
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'capacity': capacity,
                'tilt': tilt,
                'orientation': orientation,
                'tracking': tracking,
                'rhuma_state': rhuma_state
            }
            
            # Appeler l'API avec les paramètres configurés
            result = pvgis.calculate(
                latitude=latitude,
                longitude=longitude,
                capacity=capacity,
                tilt=tilt,
                orientation=orientation,
                tracking=tracking,
                rhuma_state=rhuma_state
            )
            
            # Extraire les données de production
            monthly_production = result.get('monthly_production', {})
            total_production = result.get('total_production', 0)
            
            # Affichage des résultats
            with st.expander("📊 Résultats de l'Analyse"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Production annuelle", f"{total_production/1000:.2f} MWh")
                    st.metric("Irradiation moyenne", f"{result.get('irradiation', 0):.2f} kWh/m²")
                    
                with col2:
                    st.metric("Facteur de charge", f"{result.get('load_factor', 0):.2f}")
                    st.metric("Temps de retour", f"{result.get('payback_time', 0):.1f} ans")
            
            # Graphique de production mensuelle
            if monthly_production:
                st.subheader("📈 Production Mensuelle")
                months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.bar(months, [monthly_production.get(i, 0)/1000 for i in range(1, 13)])
                ax.set_ylabel("Production mensuelle (MWh)")
                ax.set_title("Distribution de la production mensuelle")
                st.pyplot(fig)
            
            # Comparaison système fixe vs tracking
            if tracking:
                st.subheader("📊 Comparaison Système Fixe vs Tracking")
                
                # Récupérer les données de comparaison
                tracking_data = result.get('tracking_comparison', {})
                if tracking_data:
                    # Graphique comparatif
                    fig2, ax2 = plt.subplots(figsize=(12, 6))
                    ax2.bar([
                        "Système Fixe", 
                        "Tracking"
                    ], 
                    [
                        tracking_data.get('fixed_production', 0)/1000,
                        tracking_data.get('tracking_production', 0)/1000
                    ],
                    color=["#4CAF50", "#FFC107"])
                    ax2.set_ylabel("Production annuelle (MWh)")
                    ax2.set_title("Comparaison de la production annuelle")
                    st.pyplot(fig2)
                    
                    # Tableau de comparaison
                    comparison = pd.DataFrame({
                        "Système": ["Fixe", "Tracking"],
                        "Production annuelle (MWh)": [
                            f"{tracking_data.get('fixed_production', 0)/1000:.2f}",
                            f"{tracking_data.get('tracking_production', 0)/1000:.2f}"
                        ],
                        "Gain de production": [
                            "0%",
                            f"{tracking_data.get('gain_percentage', 0):.1f}%"
                        ],
                        "Revenu annuel (k€)": [
                            f"{(tracking_data.get('fixed_production', 0)*rhuma('tarif_s24'))/1000:.2f}",
                            f"{(tracking_data.get('tracking_production', 0)*rhuma('tarif_s24'))/1000:.2f}"
                        ]
                    })
                    st.dataframe(comparison, hide_index=True)
