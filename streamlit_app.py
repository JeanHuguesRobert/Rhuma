import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Simulateur Rhum Solaire Corse", layout="wide")
st.title("🍹🌞 Production de Rhum en Serre Autonome (Corte, Corse)")

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
# Puissance PV ajustée pour correspondre aux données de PVGIS
puissance_pv = st.sidebar.number_input("Puissance PV (kWc)", 100, 500, 500)  # Ajusté pour correspondre aux données de PVGIS
tarif_s24 = st.sidebar.number_input("Tarif S24 (€/kWh)", 0.10, 0.20, 0.13)
peak_efficiency = st.sidebar.slider("Efficacité maximale des panneaux (%)", 15, 25, 20)

# 4. Énergie solaire et heures d'ensoleillement
# Ajout d'un paramètre pour les pertes PV
losses_pv = st.sidebar.slider("Pertes PV (%)", 0, 30, 12)  # 12% arrondi de 11.78 selon PVGIS
# Ajout d'un paramètre pour l'autoconsommation
autoconsommation = st.sidebar.slider("Autoconsommation (%)", 0, 100, 50)  # 50% par défaut

# Production mensuelle selon PVGIS
monthly_production = {
    "janvier": 106.44,
    "février": 118.02,
    "mars": 152.77,
    "avril": 166.63,
    "mai": 184.76,
    "juin": 193.52,
    "juillet": 214.82,
    "août": 204.68,
    "septembre": 167.58,
    "octobre": 142.96,
    "novembre": 100.93,
    "décembre": 103.13
}

# Calcul du total annuel
total_annuel = sum(monthly_production.values())

# Calcul de la production PV mensuelle en fonction de la puissance installée
# Utilisation de la formule PVGIS : Production PV = puissance * irradiation * (1 - pertes/100)
monthly_pv_production = {}
for month, irradiation in monthly_production.items():
    # Production PV = puissance * irradiation * (1 - pertes/100)
    monthly_pv_production[month] = puissance_pv * irradiation * (1 - losses_pv / 100)

# Création du tableau
data = {
    "Mois": list(monthly_production.keys()) + ["Total annuel"],
    "Irradiation (kWh/m²)": list(monthly_production.values()) + [total_annuel],
    "Production PV (MWh)": [x/1000 for x in list(monthly_pv_production.values())] + [sum(monthly_pv_production.values())/1000]
}

df = pd.DataFrame(data)

# Affichage du tableau
st.write("\n## Production Électrique Mensuelle")
st.dataframe(df)

# Affichage du total annuel
st.write(f"\n### Total Annuel")
st.write(f"- Irradiation totale : {total_annuel:.2f} kWh/m²")
st.write(f"- Production PV totale : {sum(monthly_pv_production.values())/1000:.1f} MWh")

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
production_pv = sum(monthly_pv_production.values())  # kWh/an
autoconsommation_kWh = production_pv * (autoconsommation / 100)
production_vendue = production_pv - autoconsommation_kWh
revenu_pv = production_vendue * tarif_s24

# Affichage des résultats

# Production de Rhum
st.write("\n## Production de Rhum")
col1, col2, col3 = st.columns(3)
col1.metric("📦 Production Canne", f"{canne/1000:.1f} t")
col2.metric("🍬 Sucre Extrait", f"{sucre/1000:.1f} t")
col3.metric("🥃 Alcool Pur", f"{alcool:.0f} L")

# Production d'Énergie
st.write("\n## Production d'Énergie")
col1, col2, col3 = st.columns(3)
col1.metric("⚡ Puissance PV installée", f"{puissance_pv:.0f} kWc")
col2.metric("⚡ Production PV", f"{production_pv/1000:.1f} MWh/an")
col3.metric("💰 Revenu PV", f"{revenu_pv:.0f} €/an")

# Détails de l'autoconsommation
st.write("\n## Détails de l'Autoconsommation")
col1, col2, col3 = st.columns(3)
col1.metric("⚡ Autoconsommation", f"{autoconsommation}%")
col2.metric("⚡ Électricité autoconsommée", f"{autoconsommation_kWh/1000:.1f} MWh/an")
col3.metric("⚡ Électricité vendue", f"{production_vendue/1000:.1f} MWh/an")

# Graphiques
fig, ax = plt.subplots()
# Calcul des surfaces en m² pour 1 hectare (10000 m²)
surface_totale = 10000
surface_locaux = 1000  # 10% de l'hectare
surface_canne = surface_canne  # Surface dédiée à la canne
surface_panneaux = surface_totale - surface_locaux - surface_canne  # Reste pour les panneaux

# Création du graphique
ax.pie([surface_canne, surface_panneaux, surface_locaux], 
       labels=["Canne à sucre", "Panneaux PV", "Locaux"], 
       colors=["#4CAF50", "#FFC107", "#9E9E9E"],
       autopct='%1.1f%%')
ax.set_title("Répartition des surfaces sur 1 hectare")

# Affichage des surfaces
st.write("\n### Répartition des surfaces")
st.write(f"- Surface totale : {surface_totale} m²")
st.write(f"- Surface canne : {surface_canne} m²")
st.write(f"- Surface locaux : {surface_locaux} m²")
st.write(f"- Surface panneaux : {surface_panneaux} m²")

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
    
# Lien vers le dépôt GitHub
st.markdown("[GitHub Repository](https://github.com/JeanHuguesRobert/Rhuma)")    