import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Simulateur Rhum Solaire Corse", layout="wide")
st.title("🍹🌞 Production de Rhum en Serre Autonome (Corse)")

# Sidebar - Paramètres du projet
st.sidebar.header("Paramètres d'Entrée")

# 1. Surface et Rendement
surface_canne = st.sidebar.number_input("Surface dédiée à la canne (m²)", 6000, 10000, 6000)
rendement_canne = st.sidebar.slider("Rendement canne (t/ha)", 80, 150, 120)
teneur_sucre = st.sidebar.slider("Teneur en sucre (%)", 12, 20, 18)

# 2. Extraction et Distillation
efficacite_extraction = st.sidebar.slider("Efficacité extraction (%)", 60, 90, 85)
efficacite_distillation = st.sidebar.slider("Efficacité distillation (%)", 70, 95, 90)

# 3. Énergie PV
puissance_pv = st.sidebar.number_input("Puissance PV (kWc)", 100, 500, 300)
tarif_s24 = st.sidebar.number_input("Tarif S24 (€/kWh)", 0.10, 0.20, 0.13)
peak_efficiency = st.sidebar.slider("Efficacité maximale des panneaux (%)", 15, 25, 20)

# 4. Énergie solaire et heures d'ensoleillement
def calculate_total_solar_energy(hours):
    # 100 kWh/m² par heure d'ensoleillement
    return hours * 100

def calculate_hours_of_sunlight(energy):
    # 100 kWh/m² par heure d'ensoleillement
    return max(1000, min(3000, int(energy / 100)))

# Initialisation des paramètres
hours_of_sunlight_input = st.sidebar.number_input("Nombre d'heures d'ensoleillement", 1000, 3000, 1700)
total_solar_energy = calculate_total_solar_energy(hours_of_sunlight_input)

# Affichage des valeurs
st.write(f"Nombre d'heures d'ensoleillement : {hours_of_sunlight_input:.2f}")
st.write(f"Énergie solaire totale reçue : {total_solar_energy:.2f} kWh/m²")

# Calcul de la production électrique mensuelle
monthly_production = total_solar_energy / 12
best_month = monthly_production * 1.2  # Assuming best month has 20% more production
worst_month = monthly_production * 0.8  # Assuming worst month has 20% less production

# Affichage des résultats
st.write(f"Meilleur mois de production : {best_month:.2f} kWh/m²")
st.write(f"Pire mois de production : {worst_month:.2f} kWh/m²")

# Calculs de production
def calcul_production(surface, rendement, sucre, extraction, distillation):
    canne_kg = (surface / 10000) * rendement * 1000  # kg
    sucre_kg = canne_kg * (sucre / 100) * (extraction / 100)
    alcool_l = sucre_kg * 0.51 * (distillation / 100)
    return canne_kg, sucre_kg, alcool_l

canne, sucre, alcool = calcul_production(surface_canne, rendement_canne, teneur_sucre, 
                                        efficacite_extraction, efficacite_distillation)

# Calcul revenus
revenu_rhum = alcool * 20  # 20€/L
production_pv = puissance_pv * 1400  # kWh/an
revenu_pv = production_pv * tarif_s24

# Affichage des résultats
col1, col2, col3 = st.columns(3)
col1.metric("📦 Production Canne", f"{canne/1000:.1f} t")
col2.metric("🍬 Sucre Extrait", f"{sucre/1000:.1f} t")
col3.metric("🥃 Alcool Pur", f"{alcool:.0f} L")

col1.metric("💰 Revenu Rhum", f"{revenu_rhum:.0f} €/an")
col2.metric("⚡ Production PV", f"{production_pv:.0f} kWh/an")
col3.metric("💶 Revenu PV", f"{revenu_pv:.0f} €/an")

# Graphiques
fig, ax = plt.subplots()
ax.pie([surface_canne, 3000, 1000], 
       labels=["Canne à sucre", "Panneaux PV", "Locaux"], 
       colors=["#4CAF50", "#FFC107", "#9E9E9E"],
       autopct='%1.1f%%')
st.pyplot(fig)

# Détails techniques
with st.expander("📊 Détails des Calculs"):
    st.write(f"""
    - **Rendement canne** : {rendement_canne} t/ha
    - **Kg de canne/L alcool** : {canne/alcool:.1f} kg/L
    - **Surface totale** : 10 000 m² (1 ha)
    """)

# Export des résultats
if st.button("💾 Exporter en CSV"):
    df = pd.DataFrame({
        "Paramètre": ["Surface canne (m²)", "Rendement (t/ha)", "Alcool (L)", "Revenu Rhum (€)", "Production PV (kWh)"],
        "Valeur": [surface_canne, rendement_canne, alcool, revenu_rhum, production_pv]
    })
    st.download_button("⬇️ Télécharger", df.to_csv(index=False), "rhum_solaire.csv", "text/csv")