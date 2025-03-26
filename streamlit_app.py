import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from config import *
from streamlit_extras.add_vertical_space import add_vertical_space  # Ajouté

# Configuration de la page
st.set_page_config(page_title="Simulateur Rhum Solaire Corse", layout="wide")
st.title("🍹🌞 Production de Rhum en Serre Autonome (Corte, Corse)")

# Lien vers l'argumentaire de crowdfunding
st.markdown("""
## 📚 Documentation

- [Lire l'argumentaire de crowdfunding](docs/crowdfunding.md)
- [Documentation technique](docs/technical.md)
- [Guide d'utilisation](docs/user_guide.md)
""")

# Sidebar - Paramètres du projet
st.sidebar.header("Paramètres d'Entrée")

# 1. Surface et Rendement
surface_canne = st.sidebar.number_input("Surface dédiée à la canne (m²)", 
                                      SURFACE_CANNE_MIN, SURFACE_CANNE_MAX, 
                                      SURFACE_CANNE_MIN)
rendement_canne = st.sidebar.slider("Rendement canne (t/ha)", 
                                  RENDEMENT_CANNE_MIN, RENDEMENT_CANNE_MAX, 
                                  120)
teneur_sucre = st.sidebar.slider("Teneur en sucre (%)", 
                              TENEUR_SUCRE_MIN, TENEUR_SUCRE_MAX, 
                              18)

# 2. Extraction et Distillation
efficacite_extraction = st.sidebar.slider("Efficacité extraction (%)", 
                                      EFFICACITE_EXTRACTION_MIN, 
                                      EFFICACITE_EXTRACTION_MAX, 
                                      85)
efficacite_distillation = st.sidebar.slider("Efficacité distillation (%)", 
                                        EFFICACITE_DISTILLATION_MIN, 
                                        EFFICACITE_DISTILLATION_MAX, 
                                        90)

# 3. Énergie PV
puissance_pv = st.sidebar.number_input("Puissance PV (serre) (kWc)", 
                                    100, PV_SERRE_MAX, 
                                    PV_SERRE_MAX,
                                    help=f"Limite légale : {PV_SERRE_MAX} kWc pour bénéficier du tarif S24")
tarif_s24 = st.sidebar.number_input("Tarif S24 (€/kWh)", 
                                 TARIF_S24_MIN, TARIF_S24_MAX, 
                                 0.13,
                                 help="Tarif garanti pour la vente d'électricité")
tarif_tva = st.sidebar.number_input("TVA (%)", 
                                 TVA_MIN, TVA_MAX, 
                                 5)
tarif_taxes = st.sidebar.number_input("Taxes (%)", 
                                  0, TAXES_MAX, 
                                  3)
peak_efficiency = st.sidebar.slider("Efficacité maximale des panneaux (%)", 
                                 15, 25, 
                                 20)

# 4. Énergie solaire et heures d'ensoleillement
losses_pv = st.sidebar.slider("Pertes PV (%)", 
                            0, PERTES_PV_MAX, 
                            12, 
                            help="12% arrondi de 11.78 selon PVGIS")
autoconsommation = st.sidebar.slider("Autoconsommation (%)", 
                                  0, 100, 
                                  50, 
                                  help=f"Maximum {LIMITE_AUTOCONSOMMATION/1000} MWh pour éviter les droits d'accise")
pertes_tracking = st.sidebar.slider("Pertes de tracking (%)", 
                                 0, PERTES_TRACKING_MAX, 
                                 15,
                                 help="Pertes dues à l'absence de tracker double faces")
prix_alcool = st.sidebar.number_input("Prix de l'alcool (€/L)", 
                                    PRIX_RHUM_MIN, PRIX_RHUM_MAX, 
                                    20)

# 5. Auto-consommation collective
capacite_complementaire = st.sidebar.number_input("Capacité PV (au sol) (kWc)", 
                                                100, PV_SOL_MAX, 
                                                PV_SOL_MAX,
                                                help="Production supplémentaire pour l'autoconsommation collective")

# 6. Limites réglementaires
st.sidebar.header("Limites Réglementaires")
with st.sidebar.expander("🔍 Détails des Limites"):
    st.write("- **Tarif S24** :")
    st.write("  - Limite : 500 kWc")
    st.write(f"  - Tarif : {tarif_s24}€/kWh")
    st.write("  - Au-delà : 0.05€/kWh")
    st.write("- **Autoconsommation** :")
    st.write("  - Maximum : 1 MWh/an")
    st.write("  - Évite les droits d'accise")
    st.write("- **Heures d'ensoleillement** :")
    st.write("  - Limite S24 : 1600 heures/an")
    st.write("  - Au-delà : 0.05€/kWh")

# 7. Tarification clients
st.sidebar.header("Tarification Clients")
with st.sidebar.expander("💰 Tarification Clients"):
    st.write("- **Électricité Verte** :")
    st.write("  - Tarif : Tarif heure creuse")
    st.write("  - Application : 24/24")
    st.write("- **Rhum** :")
    st.write(f"  - Prix : {prix_alcool}€/L")
    st.write("  - Production : 100% locale")

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
monthly_pv_production_ideal = {}
for month, irradiation in monthly_production.items():
    # Production PV idéale (sans pertes de tracking)
    monthly_pv_production_ideal[month] = puissance_pv * irradiation * (1 - losses_pv / 100)
    # Production PV avec pertes de tracking
    monthly_pv_production[month] = monthly_pv_production_ideal[month] * (1 - pertes_tracking / 100)

# Calcul de la production collective
monthly_collective_production = {}
monthly_collective_production_ideal = {}
for month, irradiation in monthly_production.items():
    # Production collective idéale (sans pertes de tracking)
    monthly_collective_production_ideal[month] = capacite_complementaire * irradiation * (1 - losses_pv / 100)
    # Production collective avec pertes de tracking
    monthly_collective_production[month] = monthly_collective_production_ideal[month] * (1 - pertes_tracking / 100)

# Calcul des productions totales
production_pv = sum(monthly_pv_production.values())
production_pv_ideal = sum(monthly_pv_production_ideal.values())
production_collective = sum(monthly_collective_production.values())
production_collective_ideal = sum(monthly_collective_production_ideal.values())
production_totale = production_pv + production_collective
production_totale_ideal = production_pv_ideal + production_collective_ideal

# Calcul de l'autoconsommation (limitée à 1 MWh)
if production_totale * (autoconsommation / 100) > LIMITE_AUTOCONSOMMATION:
    autoconsommation_kWh = LIMITE_AUTOCONSOMMATION  # 1 MWh maximum
else:
    autoconsommation_kWh = production_totale * (autoconsommation / 100)

# Calcul des productions vendues
production_vendue = production_pv - autoconsommation_kWh
production_vendue_ideal = production_pv_ideal - autoconsommation_kWh  # Même autoconsommation pour l'idéal

# Calcul du tarif collectif
tarif_collectif = tarif_s24 * (1 + tarif_tva/100) * (1 + tarif_taxes/100)

# Calcul des CA idéaux et réels
chiffre_affaires_collectif = production_collective * tarif_collectif
chiffre_affaires_collectif_ideal = production_collective_ideal * tarif_collectif
revenu_pv = production_vendue * tarif_s24
revenu_pv_ideal = production_vendue_ideal * tarif_s24
chiffre_affaires_total = revenu_pv + chiffre_affaires_collectif
chiffre_affaires_total_ideal = revenu_pv_ideal + chiffre_affaires_collectif_ideal
delta_ca = chiffre_affaires_total_ideal - chiffre_affaires_total

# Création du tableau
data = {
    "Mois": list(monthly_production.keys()) + ["Total annuel"],
    "Irradiation (kWh/m²)": list(monthly_production.values()) + [total_annuel],
    "Production serre idéale (MWh)": [x/1000 for x in list(monthly_pv_production_ideal.values())] + [production_pv_ideal/1000],
    "Production serre (MWh)": [x/1000 for x in list(monthly_pv_production.values())] + [production_pv/1000]
}

df = pd.DataFrame(data)

# Création du tableau de production collective
data_collective = {
    "Mois": list(monthly_production.keys()) + ["Total annuel"],
    "Production au sol idéale (MWh)": [x/1000 for x in list(monthly_collective_production_ideal.values())] + [production_collective_ideal/1000],
    "Production au sol (MWh)": [x/1000 for x in list(monthly_collective_production.values())] + [production_collective/1000]
}

df_collective = pd.DataFrame(data_collective)

# Affichage du tableau
st.write("\n## Production Électrique Mensuelle")
st.dataframe(df)

# Affichage du tableau de production collective
st.write("\n## Production Collective Mensuelle")
st.dataframe(df_collective)

# Affichage du total annuel
st.write(f"\n### Total Annuel")
st.write(f"- Irradiation totale : {total_annuel:.2f} kWh/m²")
st.write(f"- Production serre idéale : {production_pv_ideal/1000:.1f} MWh")
st.write(f"- Production serre réelle : {production_pv/1000:.1f} MWh")

# Calculs de production
def calcul_production(surface, rendement, sucre, extraction, distillation):
    canne_kg = (surface / 10000) * rendement * 1000  # kg
    sucre_kg = canne_kg * (sucre / 100) * (extraction / 100)
    alcool_l = sucre_kg * 0.51 * (distillation / 100)
    return canne_kg, sucre_kg, alcool_l

canne, sucre, alcool = calcul_production(surface_canne, rendement_canne, teneur_sucre, 
                                        efficacite_extraction, efficacite_distillation)

# Calcul revenus
revenu_rhum = alcool * prix_alcool  # Prix de l'alcool paramétrable

# Barre de progression pour les calculs
with st.spinner("🔄 Calculs en cours..."):
    # Affichage des résultats

    # Organisation des résultats dans des sections collapsibles
    with st.expander("📊 Résultats de la Production de Rhum"):
        st.write("\n## Production de Rhum")
        col1, col2, col3 = st.columns(3)
        col1.metric("📦 Production Canne", f"{canne/1000:.1f} t")
        col2.metric("🍬 Sucre Extrait", f"{sucre/1000:.1f} t")
        col3.metric("🥃 Alcool Pur", f"{alcool:.0f} L")

    with st.expander("⚡ Résultats de la Production d'Énergie"):
        st.write("\n## Production d'Énergie")
        col1, col2, col3 = st.columns(3)
        col1.metric("⚡ Puissance PV (serre) installée", f"{puissance_pv:.0f} kWc")
        col2.metric("⚡ Production serre idéale", f"{production_pv_ideal/1000:.1f} MWh/an")
        col3.metric("⚡ Production serre réelle", f"{production_pv/1000:.1f} MWh/an")

    # Détails de l'autoconsommation
    st.write("\n## Détails de l'Autoconsommation")
    col1, col2, col3 = st.columns(3)
    col1.metric("⚡ Autoconsommation", f"{autoconsommation}%")
    col2.metric("⚡ Électricité autoconsommée", f"{autoconsommation_kWh/1000:.1f} MWh/an")
    col3.metric("⚡ Électricité vendue", f"{production_vendue/1000:.1f} MWh/an")

    # Auto-consommation collective
    st.write("\n## Auto-consommation collective")
    col1, col2, col3 = st.columns(3)
    col1.metric("⚡ Capacité collective", f"{capacite_complementaire:.0f} kWc")
    col2.metric("⚡ Production au sol idéale", f"{production_collective_ideal/1000:.1f} MWh/an")
    col3.metric("⚡ Production au sol réelle", f"{production_collective/1000:.1f} MWh/an")

    # Résumé du CA
    st.write("\n## Résumé du CA")
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 CA total", f"{chiffre_affaires_total:.0f} €/an")
    col2.metric("📊 CA idéal", f"{chiffre_affaires_total_ideal:.0f} €/an")
    col3.metric("📊 Delta CA", f"{delta_ca:.0f} €/an")

    # Ajout d'espaces verticaux pour une meilleure lisibilité
    add_vertical_space(2)

    # Graphiques
    fig, ax = plt.subplots()
    # Calcul des surfaces en m² pour 1 hectare (10000 m²)
    surface_totale = 10000
    surface_locaux = 1000  # 10% de l'hectare
    surface_canne = surface_canne  # Surface dédiée à la canne
    surface_panneaux = surface_totale - surface_locaux - surface_canne  # Reste pour les panneaux

    # Validation visuelle pour les entrées utilisateur
    if surface_canne + surface_locaux > surface_totale:
        st.error("⚠️ La surface totale dépasse 1 hectare. Veuillez ajuster les paramètres.")
    else:
        st.success("✅ Les paramètres sont valides.")


    # Ajout d'icônes et de couleurs dans les graphiques
    # Création du graphique des surfaces
    ax.pie([surface_canne, surface_panneaux, surface_locaux], 
        labels=["Canne à sucre", "Panneaux PV", "Locaux"], 
        colors=["#4CAF50", "#FFC107", "#9E9E9E"],
        autopct='%1.1f%%', startangle=90)
    ax.legend(loc="upper right")
    ax.set_title("Répartition des surfaces sur 1 hectare", color="#4CAF50")

    # Création du graphique des sources de CA
    fig2, ax2 = plt.subplots()
    sources_ca = [
        "Rhum", "PV (vente)", "PV (collectif)", "PV (idéal)"]
    values_ca = [
        revenu_rhum,
        revenu_pv,
        chiffre_affaires_collectif,
        chiffre_affaires_total_ideal - chiffre_affaires_total
    ]

    # Création du graphique en camembert
    ax2.pie(values_ca, 
            labels=sources_ca, 
            colors=["#4CAF50", "#FFC107", "#9E9E9E", "#607D8B"],
            autopct='%1.1f%%', startangle=90)
    ax2.set_title("Répartition des sources de CA")
    ax.legend(loc="upper right")

    # Affichage des graphiques
    st.pyplot(fig)
    st.pyplot(fig2)

    # Détails techniques
    with st.expander("📊 Détails des Calculs"):
        st.write("### 🏗️ Bâtiment (Serre)")
        st.write(f"- Surface totale : {surface_totale} m² (1 ha)")
        st.write(f"- Surface locaux : {surface_locaux} m² (10%)")
        st.write(f"- Surface panneaux en toiture : {surface_panneaux} m²")
        st.write(f"- Surface canne : {surface_canne} m²")

        st.write("\n### 🍯 Production de Rhum")
        st.write(f"- Rendement canne : {rendement_canne} t/ha")
        st.write(f"- Teneur en sucre : {teneur_sucre}%")
        st.write(f"- Efficacité extraction : {efficacite_extraction}%")
        st.write(f"- Efficacité distillation : {efficacite_distillation}%")
        st.write(f"- Kg de canne/L alcool : {canne/alcool:.1f} kg/L")
        st.write(f"- Prix de l'alcool : {prix_alcool}€/L")

        st.write("\n### 🌞 Énergie Solaire")
        st.write(f"- Puissance PV (serre) : {puissance_pv} kWc")
        st.write(f"- Capacité PV (au sol) : {capacite_complementaire} kWc")
        st.write(f"- Pertes PV : {losses_pv}%")
        st.write(f"- Pertes de tracking : {pertes_tracking}%")
        st.write(f"- Efficacité panneaux : {peak_efficiency}%")
        st.write(f"- Tarif S24 : {tarif_s24}€/kWh")
        st.write(f"- TVA : {tarif_tva}%")
        st.write(f"- Taxes : {tarif_taxes}%")
        st.write(f"- Tarif collectif : {tarif_collectif:.3f}€/kWh")

        st.write("\n### 📊 Production Électrique")
        st.write(f"- Production serre idéale : {production_pv_ideal/1000:.1f} MWh")
        st.write(f"- Production serre réelle : {production_pv/1000:.1f} MWh")
        st.write(f"- Production au sol idéale : {production_collective_ideal/1000:.1f} MWh")
        st.write(f"- Production au sol réelle : {production_collective/1000:.1f} MWh")
        st.write(f"- Production totale idéale : {(production_pv_ideal + production_collective_ideal)/1000:.1f} MWh")
        st.write(f"- Production totale réelle : {(production_pv + production_collective)/1000:.1f} MWh")
        st.write(f"- Autoconsommation (%) : {autoconsommation}%")
        st.write(f"- Autoconsommation (MWh) : {autoconsommation_kWh/1000:.1f} MWh")
        st.write(f"- Électricité vendue : {production_vendue/1000:.1f} MWh")

        st.write("\n### 💰 Revenus")
        st.write(f"- Revenu Rhum : {revenu_rhum:.0f}€/an")
        st.write(f"- Revenu PV (vente) : {revenu_pv:.0f}€/an")
        st.write(f"- CA collectif : {chiffre_affaires_collectif:.0f}€/an")
        st.write(f"- CA collectif idéal : {chiffre_affaires_collectif_ideal:.0f}€/an")
        st.write(f"- CA total : {chiffre_affaires_total:.0f}€/an")
        st.write(f"- CA total idéal : {chiffre_affaires_total_ideal:.0f}€/an")
        st.write(f"- Delta CA : {delta_ca:.0f}€/an")

# Export des résultats
if st.button("💾 Exporter en CSV"):
    
    df_export = pd.DataFrame({
        "Mois": list(monthly_production.keys()) + ["Total annuel"],
        "Production serre (MWh)": [x/1000 for x in list(monthly_pv_production.values())] + [production_pv/1000],
        "Production collective (MWh)": [x/1000 for x in list(monthly_collective_production.values())] + [production_collective/1000],
        "CA collectif (€)": [chiffre_affaires_collectif] * 12 + [chiffre_affaires_collectif]
    })
    st.download_button("⬇️ Télécharger", df_export.to_csv(index=False), "production_rhum_solaire.csv", "text/csv")

# Lien vers le dépôt GitHub
st.markdown("[GitHub Repository](https://github.com/JeanHuguesRobert/Rhuma)")
