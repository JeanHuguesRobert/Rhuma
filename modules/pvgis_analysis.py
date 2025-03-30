import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import json
from modules.state_manager import StateManager

def pvgis_analysis_section():
    """
    Section d'analyse PVGIS dans l'interface Streamlit
    """
    st.header("🌞 Analyse PVGIS")
    
    # Initialiser le gestionnaire d'état
    state_manager = StateManager()
    
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
                                     value=state_manager.get_attribute('pv_serre') + state_manager.get_attribute('pv_sol'), 
                                     min_value=0.0)
            tilt = st.slider("Angle de pose (°)", 0, 90, 30)
            orientation = st.slider("Orientation (°)", -180, 180, -180)
            tracking = st.checkbox("Utiliser le suivi de soleil")
            
    # Carte interactive
    st.subheader("🗺️ Localisation")
    location_data = pd.DataFrame({
        'latitude': [latitude],
        'longitude': [longitude]
    })
    st.map(location_data, zoom=12)
    
    # Bouton d'analyse
    if st.button("🔍 Analyser"):
        with st.spinner("Analyse en cours..."):
            # Préparer les paramètres
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'peakPower': capacity,
                'angle': tilt,
                'aspect': orientation,
                'isTracking': tracking,
                'losses': 14,  # Perte standard de 14%
                'rhuma_state': state_manager.get_state()
            }
            
            # Appeler pvgis.js avec les paramètres
            try:
                result = subprocess.run(
                    ['node', 'modules/pvgis/pvgis.js', json.dumps(params)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Analyser la sortie JSON
                result_data = json.loads(result.stdout)
                
                # Afficher les résultats
                st.subheader("📊 Résultats")
                
                # Configuration optimale
                with st.expander("🎯 Configuration Optimale"):
                    st.metric("Angle optimal", f"{result_data['optimal_angle']}°")
                    st.metric("Production annuelle", f"{result_data['annual_production']:,.0f} kWh")
                
                # Production mensuelle
                if result_data.get('monthly_production'):
                    st.subheader("📈 Production Mensuelle")
                    st.line_chart({
                        'Production mensuelle (kWh)': result_data['monthly_production']
                    })
                
                # Analyse financière
                if result_data.get('financial_analysis'):
                    with st.expander("💰 Analyse Financière"):
                        fa = result_data['financial_analysis']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Coût du système", f"{fa['system_cost']:,.0f} €")
                        with col2:
                            st.metric("ROI annuel", f"{fa['roi']:.1f}%")
                        with col3:
                            st.metric("Temps de retour", f"{fa['payback_period']:.1f} ans")
                
                # Comparaison système fixe vs tracking
                if result_data.get('comparison'):
                    with st.expander("📊 Comparaison Systèmes"):
                        comp = result_data['comparison']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Production fixe", f"{comp['fixed']['production']:,.0f} kWh")
                            st.metric("Coût fixe", f"{comp['fixed']['cost']:,.0f} €")
                            st.metric("ROI fixe", f"{comp['fixed']['roi']:.1f}%")
                        with col2:
                            st.metric("Production tracking", f"{comp['tracking']['production']:,.0f} kWh")
                            st.metric("Coût tracking", f"{comp['tracking']['cost']:,.0f} €")
                            st.metric("ROI tracking", f"{comp['tracking']['roi']:.1f}%")
                        st.metric("Gain de production", f"{comp['gain_percentage']:.1f}%")
                
            except subprocess.CalledProcessError as e:
                st.error(f"Erreur lors de l'analyse PVGIS: {e.stderr}")
            except json.JSONDecodeError:
                st.error("Erreur lors de la lecture des résultats")
            except Exception as e:
                st.error(f"Erreur inattendue: {str(e)}")
