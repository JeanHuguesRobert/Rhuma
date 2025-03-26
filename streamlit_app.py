# streamlit_app.py
#   Rhuma, rhum solaire de Corse
#
# (c) Jean Hugues Robert, 03/2025
# MIT License

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


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
TAXES_MAX = 30  # %
PERTES_PV_MAX = 30  # %
PERTES_TRACKING_MAX = 30  # %
PRIX_RHUM_MIN = 10  # €/L
PRIX_RHUM_MAX = 50  # €/L
LIMITE_PUISSANCE_S24 = 500  # kWc
HEURES_PLEIN_SOLEIL = 1600  # heures/an
LIMITE_PRODUCTION_S24 = LIMITE_PUISSANCE_S24 * HEURES_PLEIN_SOLEIL  # kWh/an
TARIF_S24_DEPASSEMENT = 0.05  # €/kWh au-delà de la limite


import numpy as np

class TrackingSystemSimulation:
    def __init__(self, standard_panel_efficiency=0.22):
        self.base_efficiency = standard_panel_efficiency
        
    def calculate_tracking_gains(self, tracking_precision=0.2, panel_orientation_precision=2):
        """
        Calcule les gains de production dus au tracking
        
        Args:
        - tracking_precision (float): Précision du tracking en degrés
        - panel_orientation_precision (float): Précision de l'orientation du panneau
        
        Returns:
        - Dict avec gains et détails de performance
        """
        # Modèle simplifié de gain de production
        base_tracking_gain = {
            "single_axis": 0.15,  # 15% de gain avec tracking monoaxe
            "dual_axis": 0.25,    # 25% de gain avec tracking biaxe
        }
        
        # Bonus lié à la précision
        precision_bonus = {
            "low": 0.05,   # précision > 1°
            "medium": 0.10, # précision 0.5-1°
            "high": 0.15   # précision < 0.5°
        }
        
        precision_category = (
            "high" if tracking_precision < 0.5 else
            "medium" if tracking_precision < 1 else
            "low"
        )
        
        gains = {
            "single_axis_gain": base_tracking_gain["single_axis"] + precision_bonus[precision_category],
            "dual_axis_gain": base_tracking_gain["dual_axis"] + precision_bonus[precision_category]
        }
        
        # Impact de l'orientation du panneau
        orientation_loss = panel_orientation_precision * 0.02
        
        for key in gains:
            gains[key] = max(0, gains[key] - orientation_loss)
        
        return gains
    
    def simulate_microinverter_performance(self, input_voltage=40, output_voltage=230):
        """
        Simulation des performances du micro-onduleur
        
        Args:
        - input_voltage (float): Tension d'entrée DC
        - output_voltage (float): Tension de sortie AC
        
        Returns:
        - Dict avec caractéristiques de performance
        """
        conversion_efficiency = min(0.96, 1 - abs(input_voltage - 40)/100)
        
        return {
            "max_power": 350,  # Watts
            "conversion_efficiency": conversion_efficiency,
            "input_voltage_range": [30, 60],
            "output_voltage": output_voltage,
            "temperature_coefficient": -0.4  # % par °C
        }
    
    def monte_carlo_solar_production(self, base_production, num_simulations=1000):
        """
        Simulation Monte Carlo des variations de production
        
        Args:
        - base_production (float): Production de base
        - num_simulations (int): Nombre de simulations
        
        Returns:
        - Dict avec statistiques de production
        """
        np.random.seed(42)
        
        # Variations possibles
        variations = np.random.normal(1, 0.05, num_simulations)
        productions = base_production * variations
        
        return {
            "mean_production": np.mean(productions),
            "median_production": np.median(productions),
            "std_deviation": np.std(productions),
            "min_production": np.min(productions),
            "max_production": np.max(productions)
        }


def tracking_optimization_section(production_pv_ideal):
    st.header("🔍 Optimisation du Tracking Solaire")
    
    # Initialisation du simulateur de tracking
    tracker = TrackingSystemSimulation()
    
    # Colonnes pour les paramètres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tracking_strategy = st.selectbox(
            "Stratégie de Tracking", 
            ["Statique", "Single-Axis", "Dual-Axis"],
            help="Sélectionnez la stratégie de suivi solaire"
        )
    
    with col2:
        tracking_precision = st.slider(
            "Précision de Tracking", 
            0.1, 5.0, 0.2,
            help="Précision angulaire du système de tracking (en degrés)"
        )
    
    with col3:
        panel_orientation = st.slider(
            "Précision d'Orientation", 
            0.5, 5.0, 2.0,
            help="Précision de l'orientation initiale du panneau"
        )
    
    # Calcul des gains de tracking
    tracking_gains = tracker.calculate_tracking_gains(
        tracking_precision, 
        panel_orientation
    )
    
    # Simulation des performances du micro-onduleur
    microinverter_perf = tracker.simulate_microinverter_performance()
    
    # Simulation Monte Carlo de la production
    monte_carlo_result = tracker.monte_carlo_solar_production(production_pv_ideal)
    
    # Création de colonnes pour afficher les résultats
    st.subheader("📊 Résultats de l'Optimisation")
    
    gains_col1, gains_col2, gains_col3 = st.columns(3)
    
    with gains_col1:
        st.metric(
            "Gain Tracking Monoaxe", 
            f"{tracking_gains['single_axis_gain']*100:.1f}%",
            help="Augmentation de production avec tracking monoaxe"
        )
    
    with gains_col2:
        st.metric(
            "Gain Tracking Biaxe", 
            f"{tracking_gains['dual_axis_gain']*100:.1f}%",
            help="Augmentation de production avec tracking biaxe"
        )
    
    with gains_col3:
        st.metric(
            "Efficacité Micro-onduleur", 
            f"{microinverter_perf['conversion_efficiency']*100:.1f}%",
            help="Efficacité de conversion du micro-onduleur"
        )
    
    # Section Analyse de Production
    st.subheader("📈 Analyse de Production")
    
    prod_col1, prod_col2, prod_col3 = st.columns(3)
    
    with prod_col1:
        st.metric(
            "Production Moyenne", 
            f"{monte_carlo_result['mean_production']/1000:.2f} MWh",
            help="Production moyenne estimée par simulation Monte Carlo"
        )
    
    with prod_col2:
        st.metric(
            "Écart-type", 
            f"{monte_carlo_result['std_deviation']/1000:.2f} MWh",
            help="Variation de la production"
        )
    
    with prod_col3:
        st.metric(
            "Plage Production", 
            f"{monte_carlo_result['min_production']/1000:.2f} - {monte_carlo_result['max_production']/1000:.2f} MWh",
            help="Fourchette de production estimée"
        )
    
    # Paramètres avancés
    with st.expander("🛠️ Paramètres Techniques Avancés"):
        st.write("### Caractéristiques du Micro-onduleur")
        st.write(f"- Puissance max : {microinverter_perf['max_power']} W")
        st.write(f"- Plage tension entrée : {microinverter_perf['input_voltage_range']} V")
        st.write(f"- Tension sortie : {microinverter_perf['output_voltage']} V")
        st.write(f"- Coefficient température : {microinverter_perf['temperature_coefficient']}%/°C")
        
        st.write("\n### Stratégies de Tracking")
        st.write("- **Statique** : Orientation fixe, aucun suivi")
        st.write("- **Single-Axis** : Suivi sur un axe (est-ouest)")
        st.write("- **Dual-Axis** : Suivi précis sur deux axes")
        
        st.write("\n### Impact de la Précision")
        st.write(f"- Précision de tracking : {tracking_precision}°")
        st.write(f"- Précision d'orientation : {panel_orientation}°")
        st.write("- Moins de précision = Pertes de performance")


# Configuration de la page
st.set_page_config(page_title="Simulateur Rhuma, rhum solaire en Corse", layout="wide")
st.title("🍹🌞 Rhuma, rhum sous serre autonome, Corte, Corse")


def read_markdown_file(markdown_file):
    """Lire et retourner le contenu d'un fichier Markdown."""
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Erreur lors de la lecture du fichier: {str(e)}"


# Lecture et affichage des documents Markdown
DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


st.markdown("""
## 📚 Documentation
""")


# Créer des onglets pour la documentation
doc_tabs = st.tabs(["Crowdfunding", "Documentation technique", "Guide utilisateur"])

with doc_tabs[0]:
    crowdfunding_content = read_markdown_file(os.path.join(DOCS_DIR, "crowdfunding.md"))
    st.markdown(crowdfunding_content)

with doc_tabs[1]:
    technical_content = read_markdown_file(os.path.join(DOCS_DIR, "technical.md"))
    st.markdown(technical_content)

with doc_tabs[2]:
    guide_content = read_markdown_file(os.path.join(DOCS_DIR, "user_guide.md"))
    st.markdown(guide_content)


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
                                    help=f"Limite légale : {LIMITE_PUISSANCE_S24} kWc pour bénéficier du tarif S24")
tarif_s24 = st.sidebar.number_input("Tarif S24 (€/kWh)", 
                                 TARIF_S24_MIN, TARIF_S24_MAX, 
                                 0.13,
                                 help="Tarif garanti pour la vente d'électricité")
tarif_tva = st.sidebar.number_input("TVA (%)", 
                                 TVA_MIN, TVA_MAX, 
                                 20)
tarif_taxes = st.sidebar.number_input("Taxes (%)", 
                                  0, TAXES_MAX, 
                                  0)
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
                                  30, 
                                  help="Partie de l'électricité utilisée pour la production de rhum")
pertes_tracking = st.sidebar.slider("Pertes de tracking (%)", 
                                 0, PERTES_TRACKING_MAX, 
                                 15,
                                 help="Pertes liées à l'absence de trackers solaires")
prix_alcool = st.sidebar.number_input("Prix de l'alcool (€/L)", 
                                    PRIX_RHUM_MIN, PRIX_RHUM_MAX, 
                                    20,
                                 help="L'alcool n'est qu'une partie du prix du rhum, s'ajoute d'autres coûts et taxes")

# 5. Énergie PV au sol
capacite_au_sol = st.sidebar.number_input("Capacité PV (au sol) (kWc)", 
                                          100, PV_SOL_MAX, 
                                          PV_SOL_MAX,
                                          help="Production supplémentaire grâce aux panneaux au sol")

# 6. Limites réglementaires
st.sidebar.header("Limites Réglementaires")
with st.sidebar.expander("🔍 Détails des Limites"):
    st.write("- **Tarif S24** :")
    st.write(f"  - Limite de puissance : {LIMITE_PUISSANCE_S24} kWc")
    st.write(f"  - Limite de production : {LIMITE_PRODUCTION_S24/1000:.0f} MWh/an")
    st.write(f"  - Tarif jusqu'à la limite : {tarif_s24}€/kWh")
    st.write(f"  - Tarif au-delà : {TARIF_S24_DEPASSEMENT}€/kWh")
    st.write("- **Production annuelle** :")
    st.write(f"  - Base : {HEURES_PLEIN_SOLEIL} heures équivalent pleine puissance")
    st.write("  - Au-delà : tarif dégradé")

# 7. Tarification clients
st.sidebar.header("Tarification Clients")
with st.sidebar.expander("💰 Tarification Clients"):
    st.write("- **Électricité Verte** :")
    st.write("  - Tarif : Des heures toujours creuses !")
    st.write("  - Application : 24h/24h")
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

# Calcul de la production PV au sol
monthly_au_sol_production = {}
monthly_au_sol_production_ideal = {}
for month, irradiation in monthly_production.items():
    # Production au sol idéale (sans pertes de tracking)
    monthly_au_sol_production_ideal[month] = capacite_au_sol * irradiation * (1 - losses_pv / 100)
    # Production au sol avec pertes de tracking
    monthly_au_sol_production[month] = monthly_au_sol_production_ideal[month] * (1 - pertes_tracking / 100)

# Calcul des productions totales
production_pv = sum(monthly_pv_production.values())
production_pv_ideal = sum(monthly_pv_production_ideal.values())
production_au_sol = sum(monthly_au_sol_production.values())
production_au_sol_ideal = sum(monthly_au_sol_production_ideal.values())
production_totale = production_pv + production_au_sol
production_totale_ideal = production_pv_ideal + production_au_sol_ideal

# Calcul des productions vendues
# Calcul de l'autoconsommation en kWh
autoconsommation_kWh = production_pv * (autoconsommation / 100)

# Calcul de la production vendue
production_vendue = production_pv - autoconsommation_kWh
production_vendue_ideal = production_pv_ideal - autoconsommation_kWh  # Même autoconsommation pour l'idéal

# Calcul du tarif collectif
tarif_collectif = tarif_s24 * (1 + tarif_tva/100) * (1 + tarif_taxes/100)

# Modification du calcul du revenu PV
def calcul_tarif_production(production_kwh):
    """Calcule le revenu en tenant compte du seuil des 1600h à pleine puissance"""
    if production_kwh <= LIMITE_PRODUCTION_S24:
        return production_kwh * tarif_s24
    else:
        return (LIMITE_PRODUCTION_S24 * tarif_s24 + 
                (production_kwh - LIMITE_PRODUCTION_S24) * TARIF_S24_DEPASSEMENT)

# Remplacement du calcul simple par le nouveau calcul
revenu_pv = calcul_tarif_production(production_vendue)
revenu_pv_ideal = calcul_tarif_production(production_vendue_ideal)

# Calcul des CA idéaux et réels
chiffre_affaires_collectif = production_au_sol * tarif_collectif
chiffre_affaires_collectif_ideal = production_au_sol_ideal * tarif_collectif
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

# Création du tableau de production au sol
data_au_sol = {
    "Mois": list(monthly_production.keys()) + ["Total annuel"],
    "Production au sol idéale (MWh)": [x/1000 for x in list(monthly_au_sol_production_ideal.values())] + [production_au_sol_ideal/1000],
    "Production au sol (MWh)": [x/1000 for x in list(monthly_au_sol_production.values())] + [production_au_sol/1000]
}

df_au_sol = pd.DataFrame(data_au_sol)

# Affichage du tableau
st.write("\n## Production électrique de la serre")
st.dataframe(df)

# Affichage du tableau de production au sol
st.write("\n## Production électrique au sol")
st.dataframe(df_au_sol)

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
    col1.metric("⚡ Capacité collective", f"{capacite_au_sol:.0f} kWc")
    col2.metric("⚡ Production au sol idéale", f"{production_au_sol_ideal/1000:.1f} MWh/an")
    col3.metric("⚡ Production au sol réelle", f"{production_au_sol/1000:.1f} MWh/an")

    # Résumé du CA
    st.write("\n## Résumé du CA")
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 CA total", f"{chiffre_affaires_total:.0f} €/an")
    col2.metric("📊 CA idéal", f"{chiffre_affaires_total_ideal:.0f} €/an")
    col3.metric("📊 Delta CA", f"{delta_ca:.0f} €/an")

    # Ajout d'espaces verticaux pour une meilleure lisibilité
    st.write("")
    st.write("")

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



    # Ajout d'icônes et de couleurs dans les graphiques
    # Création du graphique des surfaces
    ax.pie([surface_canne, surface_panneaux, surface_locaux], 
        labels=["Canne à sucre", "Panneaux PV", "Locaux"], 
        colors=["#4CAF50", "#FFC107", "#9E9E9E"],
        autopct='%1.1f%%', startangle=90)
    ax.set_title("Répartition dans la serre", color="#4CAF50")

    # Création du graphique des sources de CA
    fig2, ax2 = plt.subplots()
    sources_ca = [
        "Rhum", "PV (vente)", "PV (au sol)", "PV (idéal)"]
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

    # Affichage des graphiques
    st.pyplot(fig)
    # Ajout d'espaces verticaux pour une meilleure lisibilité
    st.write("")
    st.write("")
    st.pyplot(fig2)

    # Dans votre script Streamlit principal, ajoutez ceci après vos sections existantes
    tracking_optimization_section(production_pv_ideal)

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
        st.write(f"- Capacité PV (au sol) : {capacite_au_sol} kWc")
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
        st.write(f"- Production au sol idéale : {production_au_sol_ideal/1000:.1f} MWh")
        st.write(f"- Production au sol réelle : {production_au_sol/1000:.1f} MWh")
        st.write(f"- Production totale idéale : {(production_pv_ideal + production_au_sol_ideal)/1000:.1f} MWh")
        st.write(f"- Production totale réelle : {(production_pv + production_au_sol)/1000:.1f} MWh")
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
        "Production collective (MWh)": [x/1000 for x in list(monthly_au_sol_production.values())] + [production_au_sol/1000],
        "CA collectif (€)": [chiffre_affaires_collectif] * 12 + [chiffre_affaires_collectif]
    })
    st.download_button("⬇️ Télécharger", df_export.to_csv(index=False), "production_rhum_solaire.csv", "text/csv")

# Lien vers le dépôt GitHub
st.markdown("[GitHub Repository](https://github.com/JeanHuguesRobert/Rhuma)")
