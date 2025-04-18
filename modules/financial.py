import streamlit as st
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from modules.state_manager import rhuma, rhuma_label, rhuma_description, StateManager, state_manager
from modules.tracking import TrackingSystemSimulation

def get_pv_production_data():
    """Récupère les données de production PV depuis l'état global"""
    monthly_pv_production = rhuma('monthly_pv_production')
    total_pv_production = rhuma('total_pv_production')
    return monthly_pv_production, total_pv_production

def get_google_sheet_client():
    """Retourne un client Google Sheets configuré"""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials.from_authorized_user_info(rhuma('google_sheets_credentials'))
        return build('sheets', 'v4', credentials=creds).spreadsheets()
    except Exception as e:
        st.error(f"Erreur de configuration Google Sheets: {str(e)}")
        return None



def calculate_total_costs(puissance_pv, surface_serre, params):
    cout_pv = puissance_pv * (params['cout_fixe'] + params['cout_tracking'])
    cout_serre = surface_serre * params['cout_construction']
    cout_total = cout_pv + cout_serre
    return {'cout_pv': cout_pv, 'cout_serre': cout_serre, 'cout_total': cout_total}

def simulate_financial_scenarios(production_fixe, production_tracking, params):
    # Scénario 1: Revente EDF S24
    scenario_1 = {
        'nom': 'Revente EDF S24',
        'fixe': {
            'production': production_fixe,
            'autoconsommation': params['autoconsommation_fixe'],
            'revente': production_fixe - params['autoconsommation_fixe'],
            'revenu': (production_fixe - params['autoconsommation_fixe'])* params['tarif_s24'],
            'cout_total': params['cout_fixe'] + params['cout_maintenance'] + params['cout_assurance'] + params['cout_production']
        },
        'tracking': {
            'production': production_tracking,
            'autoconsommation': params['autoconsommation_tracking'],
            'revente': production_tracking - params['autoconsommation_tracking'],
            'revenu': (production_tracking - params['autoconsommation_tracking'])* params['tarif_s24'],
            'cout_total': params['cout_fixe'] + params['cout_tracking'] + params['cout_maintenance'] + params['cout_assurance'] + params['cout_production']
        }
    }
    # Scénario 2: Autoconsommation collective
    scenario_2 = {
        'nom': 'Autoconsommation Collective',
        'fixe': {
            'production': production_fixe,
            'autoconsommation': production_fixe,
            'revente': 0,
            'revenu': production_fixe * params['tarif_heures_creuses'],
            'cout_total': params['cout_fixe'] + params['cout_maintenance'] + params['cout_assurance'] + params['cout_production']
        },
        'tracking': {
            'production': production_tracking,
            'autoconsommation': production_tracking,
            'revente': 0,
            'revenu': production_tracking * params['tarif_heures_creuses'],
            'cout_total': params['cout_fixe'] + params['cout_tracking'] + params['cout_maintenance'] + params['cout_assurance'] + params['cout_production']
        }
    }
    # Scénario 3: Mixte (autoconsommation + revente)
    scenario_3 = {
        'nom': 'Mixte (Autoconsommation + Revente)',
        'fixe': {
            'production': production_fixe,
            'autoconsommation': params['autoconsommation_fixe'],
            'revente': production_fixe - params['autoconsommation_fixe'],
            'revenu': (params['autoconsommation_fixe'] * params['tarif_heures_creuses'] + (production_fixe - params['autoconsommation_fixe'])* params['tarif_s24']),
            'cout_total': params['cout_fixe'] + params['cout_maintenance'] + params['cout_assurance'] + params['cout_production']
        },
        'tracking': {
            'production': production_tracking,
            'autoconsommation': params['autoconsommation_tracking'],
            'revente': production_tracking - params['autoconsommation_tracking'],
            'revenu': (params['autoconsommation_tracking'] * params['tarif_heures_creuses'] + (production_tracking - params['autoconsommation_tracking'])* params['tarif_s24']),
            'cout_total': params['cout_fixe'] + params['cout_tracking'] + params['cout_maintenance'] + params['cout_assurance'] + params['cout_production']
        }
    }
    scenarios = [scenario_1, scenario_2, scenario_3]
    # Calcul des ROI et temps de retour
    for scenario in scenarios:
        for system in ['fixe', 'tracking']:
            benefice = scenario[system]['revenu'] - scenario[system]['cout_total']
            investissement = scenario[system]['cout_total']
            if benefice > 0:
                roi = (benefice / investissement) * 100
                temps_retour = investissement / benefice
            else:
                roi = 0
                temps_retour = float('inf')
            scenario[system]['benefice_annuel'] = benefice
            scenario[system]['roi'] = roi
            scenario[system]['temps_retour'] = temps_retour
    return scenarios

def financial_simulation_section():
    st.header("📊 Simulation Financière")

def simulate_financial_scenarios(production_fixe, production_tracking):
    """
    Simule les trois scénarios financiers et retourne les résultats
    """
    # Scénario 1: Revente à EDF au tarif S24
    scenario_1 = {
        'nom': 'Revente EDF S24',
        'fixe': {
            'production': production_fixe,
            'autoconsommation': rhuma('autoconsommation_fixe'),
            'revente': production_fixe - rhuma('autoconsommation_fixe'),
            'revenu': (production_fixe - rhuma('autoconsommation_fixe')) * rhuma('tarif_s24'),
            'cout_total': rhuma('cout_fixe') + rhuma('cout_maintenance') + rhuma('cout_assurance') + rhuma('cout_production')
        },
        'tracking': {
            'production': production_tracking,
            'autoconsommation': rhuma('autoconsommation_tracking'),
            'revente': production_tracking - rhuma('autoconsommation_tracking'),
            'revenu': (production_tracking - rhuma('autoconsommation_tracking')) * rhuma('tarif_s24'),
            'cout_total': rhuma('cout_fixe') + rhuma('cout_tracking') + rhuma('cout_maintenance') + rhuma('cout_assurance') + rhuma('cout_production')
        }
    }

    # Scénario 2: Autoconsommation collective
    scenario_2 = {
        'nom': 'Autoconsommation Collective',
        'fixe': {
            'production': production_fixe,
            'autoconsommation': production_fixe,
            'revente': 0,
            'revenu': production_fixe * rhuma('tarif_heures_creuses'),
            'cout_total': rhuma('cout_fixe') + rhuma('cout_maintenance') + rhuma('cout_assurance') + rhuma('cout_production')
        },
        'tracking': {
            'production': production_tracking,
            'autoconsommation': production_tracking,
            'revente': 0,
            'revenu': production_tracking * rhuma('tarif_heures_creuses'),
            'cout_total': rhuma('cout_fixe') + rhuma('cout_tracking') + rhuma('cout_maintenance') + rhuma('cout_assurance') + rhuma('cout_production')
        }
    }

    # Scénario 3: Mixte (autoconsommation + revente)
    scenario_3 = {
        'nom': 'Mixte (Autoconsommation + Revente)',
        'fixe': {
            'production': production_fixe,
            'autoconsommation': rhuma('autoconsommation_fixe'),
            'revente': production_fixe - rhuma('autoconsommation_fixe'),
            'revenu': (rhuma('autoconsommation_fixe') * rhuma('tarif_heures_creuses') + (production_fixe - rhuma('autoconsommation_fixe')) * rhuma('tarif_s24')),
            'cout_total': rhuma('cout_fixe') + rhuma('cout_maintenance') + rhuma('cout_assurance') + rhuma('cout_production')
        },
        'tracking': {
            'production': production_tracking,
            'autoconsommation': rhuma('autoconsommation_tracking'),
            'revente': production_tracking - rhuma('autoconsommation_tracking'),
            'revenu': (rhuma('autoconsommation_tracking') * rhuma('tarif_heures_creuses') + (production_tracking - rhuma('autoconsommation_tracking')) * rhuma('tarif_s24')),
            'cout_total': rhuma('cout_fixe') + rhuma('cout_tracking') + rhuma('cout_maintenance') + rhuma('cout_assurance') + rhuma('cout_production')
        }
    }

    # Calcul du ROI pour chaque scénario
    scenarios = [scenario_1, scenario_2, scenario_3]
    for scenario in scenarios:
        for system in ['fixe', 'tracking']:
            # Calcul du bénéfice annuel
            benefice_annuel = scenario[system]['revenu'] - scenario[system]['cout_total']
            
            # Calcul du ROI
            investissement = scenario[system]['cout_total']
            if benefice_annuel > 0:
                roi = (benefice_annuel / investissement) * 100
                temps_retour = investissement / benefice_annuel
            else:
                roi = 0
                temps_retour = float('inf')
            
            scenario[system]['benefice_annuel'] = benefice_annuel
            scenario[system]['roi'] = roi
            scenario[system]['temps_retour'] = temps_retour

    return scenarios

def financial_simulation_section():
    st.header("📊 Simulation Financière")
    
    # Get PVGIS data
    monthly_pv_production, total_pv_production = get_pv_production_data()
    
    # Calcul de la puissance PV installée
    puissance_pv = rhuma('pv_serre')
    
    # Calcul de la production PV idéale (sans pertes)
    production_pv_ideal = total_pv_production / (1 - rhuma('pertes_pv'))
    production_au_sol_ideal = rhuma('pv_sol') / (1 - rhuma('pertes_pv'))
    production_pv = total_pv_production
    production_au_sol = rhuma('pv_sol')
    
    # Initialisation du simulateur de tracking
    tracker = TrackingSystemSimulation()
    
    # Calcul des gains de tracking
    tracking_gains = tracker.calculate_tracking_gains(rhuma('precision_tracking'), rhuma('precision_tracking'))
    production_tracking = total_pv_production * (1 + tracking_gains['single_axis_gain'])
    
    # Simulation des scénarios
    scenarios = simulate_financial_scenarios(total_pv_production, production_tracking)
    
    # Création des tableaux de comparaison
    st.subheader("📈 Comparaison des Scénarios")
    
    # Tableau comparatif
    comparison_data = []
    for scenario in scenarios:
        comparison_data.append({
            'Scénario': scenario['nom'],
            'Système': 'Fixe',
            'Production (MWh)': f"{total_pv_production/1000:.2f}",
            'Autoconsommation (MWh)': f"{scenario['fixe']['autoconsommation']/1000:.2f}",
            'Revente (MWh)': f"{scenario['fixe']['revente']/1000:.2f}",
            'Revenu annuel (k€)': f"{scenario['fixe']['revenu']/1000:.2f}",
            'Bénéfice annuel (k€)': f"{scenario['fixe']['benefice_annuel']/1000:.2f}",
            'ROI (%)': f"{scenario['fixe']['roi']:.1f}",
            'Temps retour (ans)': f"{scenario['fixe']['temps_retour']:.1f}"
        })
        comparison_data.append({
            'Scénario': scenario['nom'],
            'Système': 'Tracking',
            'Production (MWh)': f"{production_tracking/1000:.2f}",
            'Autoconsommation (MWh)': f"{scenario['tracking']['autoconsommation']/1000:.2f}",
            'Revente (MWh)': f"{scenario['tracking']['revente']/1000:.2f}",
            'Revenu annuel (k€)': f"{scenario['tracking']['revenu']/1000:.2f}",
            'Bénéfice annuel (k€)': f"{scenario['tracking']['benefice_annuel']/1000:.2f}",
            'ROI (%)': f"{scenario['tracking']['roi']:.1f}",
            'Temps retour (ans)': f"{scenario['tracking']['temps_retour']:.1f}"
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, hide_index=True)
    
    # Création des graphiques comparatifs
    st.subheader("📊 Analyse Graphique")
    
    # Graphique des revenus
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    
    # Revenus par scénario
    for scenario in scenarios:
        ax1.bar([f"{scenario['nom']} - Fixe"], 
                [scenario['fixe']['revenu']/1000], 
                color='#4CAF50',
                alpha=0.6)
        ax1.bar([f"{scenario['nom']} - Tracking"], 
                [scenario['tracking']['revenu']/1000], 
                color='#FFC107',
                alpha=0.6)
    
    ax1.set_ylabel('Revenu annuel (k€)')
    ax1.set_title('Comparaison des Revenus Annuels par Scénario')
    st.pyplot(fig1)
    
    # Graphique des bénéfices
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    # Bénéfices par scénario
    for scenario in scenarios:
        ax2.bar([f"{scenario['nom']} - Fixe"], 
                [scenario['fixe']['benefice_annuel']/1000], 
                color='#4CAF50',
                alpha=0.6)
        ax2.bar([f"{scenario['nom']} - Tracking"], 
                [scenario['tracking']['benefice_annuel']/1000], 
                color='#FFC107',
                alpha=0.6)
    
    ax2.set_ylabel('Bénéfice annuel (k€)')
    ax2.set_title('Comparaison des Bénéfices Annuels par Scénario')
    st.pyplot(fig2)
    
    # Graphique des temps de retour
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    
    # Temps de retour par scénario
    for scenario in scenarios:
        ax3.bar([f"{scenario['nom']} - Fixe"], 
                [scenario['fixe']['temps_retour']], 
                color='#4CAF50',
                alpha=0.6)
        ax3.bar([f"{scenario['nom']} - Tracking"], 
                [scenario['tracking']['temps_retour']], 
                color='#FFC107',
                alpha=0.6)
    
    ax3.set_ylabel('Temps de retour (ans)')
    ax3.set_title('Comparaison des Temps de Retour sur Investissement')
    st.pyplot(fig3)
    
    # Section de conclusion
    with st.expander("📝 Analyse des Résultats"):
        st.write("### Synthèse des Scénarios")
        
        # Meilleur scénario par critère
        best_scenarios = {
            'Revenu': max(scenarios, key=lambda x: x['tracking']['revenu']),
            'Bénéfice': max(scenarios, key=lambda x: x['tracking']['benefice_annuel']),
            'ROI': max(scenarios, key=lambda x: x['tracking']['roi']),
            'Temps retour': min(scenarios, key=lambda x: x['tracking']['temps_retour'])
        }
        
        for critere, scenario in best_scenarios.items():
            st.write(f"- Meilleur {critere} : {scenario['nom']} - Tracking")
            st.write(f"  * Revenu : {scenario['tracking']['revenu']/1000:.2f} k€")
            st.write(f"  * Bénéfice : {scenario['tracking']['benefice_annuel']/1000:.2f} k€")
            st.write(f"  * ROI : {scenario['tracking']['roi']:.1f}%")
            st.write(f"  * Temps retour : {scenario['tracking']['temps_retour']:.1f} ans")
            st.write("---")
        
        st.write("### Recommandations")
        st.write("""
        - Le système tracking est toujours plus rentable que le système fixe
        - Le scénario mixte (autoconsommation + revente) offre généralement le meilleur retour sur investissement
        - La durée d'amortissement doit être adaptée aux besoins de financement
        - Les coûts d'exploitation (maintenance, assurance) doivent être soigneusement budgétisés
        """)

def export_to_google_sheets(data, sheet_name="Simulation Rhuma"):
    """
    Exporte les données vers une nouvelle feuille Google Sheets avec une structure optimisée
    """
    try:
        # Initialiser le client
        client = get_google_sheet_client()
        if not client:
            return "Configuration Google Sheets non valide"
            
        # Créer un nouveau spreadsheet
        spreadsheet = client.create(sheet_name)
        
        # Partager le spreadsheet avec l'utilisateur
        email = os.getenv('RHUMA_GOOGLE_SHEETS_CLIENT_EMAIL', '')  # Default to empty string if not set
        spreadsheet.share(
            email,  # Now guaranteed to be a string
            perm_type='user',
            role='writer'
        )
        
        # Créer les différentes feuilles
        config_sheet = spreadsheet.add_worksheet(title="Configuration", rows="200", cols="20")
        results_sheet = spreadsheet.add_worksheet(title="Résultats", rows="200", cols="20")
        calculations_sheet = spreadsheet.add_worksheet(title="Calculs", rows="200", cols="20")
        simulation_sheet = spreadsheet.add_worksheet(title="Simulation", rows="200", cols="20")
        
        # 1. Configuration générale
        config_general = {
            rhuma_label('id'): rhuma('id'),
            rhuma_label('label'): rhuma('label'),
            rhuma_label('version'): rhuma('version'),
            "Timestamp": datetime.now().isoformat()
        }
        
        # 2. Paramètres de Simulation
        config_simulation = {
            "Surface canne": rhuma('surface_canne'),
            "Rendement canne": rhuma('rendement_canne'),
            "Teneur sucre": rhuma('teneur_sucre'),
            "Efficacité extraction": rhuma('efficacite_extraction'),
            "Efficacité distillation": rhuma('efficacite_distillation'),
            "Puissance PV (serre)": rhuma('pv_serre'),
            "Puissance PV (au sol)": rhuma('pv_sol'),
            "Tarif S24": rhuma('tarif_s24'),
            "TVA": rhuma('tva'),
            "Coût système PV fixe": rhuma('cout_fixe'),
            "Coût système tracking": rhuma('cout_tracking'),
            "Coût construction serre": rhuma('cout_construction'),
            "Coût maintenance": rhuma('cout_maintenance'),
            "Coût assurance": rhuma('cout_assurance'),
            "Coût production": rhuma('cout_production'),
            "Tarif heures creuses": rhuma('tarif_heures_creuses'),
            "Autoconsommation fixe": rhuma('autoconsommation_fixe'),
            "Autoconsommation tracking": rhuma('autoconsommation_tracking'),
            "Prix du rhum": rhuma('prix_rhum'),
            "Pertes PV": rhuma('pertes_pv'),
            "Pertes tracking": rhuma('pertes_tracking'),
            "Précision tracking": rhuma('precision_tracking'),
            "Taux d'intérêt": rhuma('taux_interet'),
            "Durée d'amortissement": rhuma('duree_amortissement')
        }
        
        # 3. Résultats de la simulation
        results = data
        
        # 4. Calculs intermédiaires
        calculations = {
            "Production PV (serre)": f"=Configuration!B8",
            "Production PV (au sol)": f"=Configuration!B9",
            "Production totale": "=Calculs!B1 + Calculs!B2",
            "Autoconsommation totale": "=Configuration!B10 + Configuration!B11",
            "Revente totale": "=Calculs!B3 - Calculs!B4",
            "Revenu PV": "=Calculs!B5 * Configuration!B12",
            "Revenu Rhum": "=Calculs!B6 * Configuration!B13",
            "Bénéfice net": "=Calculs!B7 - Configuration!B14 - Configuration!B15 - Configuration!B16"
        }
        
        # Créer les données pour chaque feuille
        config_data = [
            ["Configuration Générale"] + [""] * (len(config_general) - 1),
            *[[k, v] for k, v in config_general.items()],
            ["\nParamètres de Simulation"] + [""] * (len(config_simulation) - 1),
            *[[k, v] for k, v in config_simulation.items()]
        ]
        
        results_data = [
            ["Résultats de la Simulation"] + [""] * (len(results) - 1),
            *[[k, v] for k, v in results.items()]
        ]
        
        calculations_data = [
            ["Calculs Intermédiaires"] + [""] * (len(calculations) - 1),
            *[[k, v] for k, v in calculations.items()]
        ]
        
        # Ajouter les formules pour la simulation
        simulation_formulas = [
            ["Paramètre", "Formule", "Description"],
            ["Surface canne", "=Configuration!B2", "Surface totale dédiée à la canne"],
            ["Rendement canne", "=Configuration!B3", "Rendement annuel de la canne"],
            ["Production PV", "=Calculs!B3", "Puissance PV installée"],
            ["Revenu total", "=Calculs!B7", "Revenu total annuel"],
            ["Bénéfice net", "=Calculs!B8", "Bénéfice net après déduction des coûts"],
            ["ROI", "=Calculs!B8 / Configuration!B14", "Retour sur investissement"],
            ["Temps retour", "=Configuration!B17 / Calculs!B8", "Durée d'amortissement"]
        ]
        
        # Écrire les données dans les feuilles
        config_sheet.update('A1', config_data)
        results_sheet.update('A1', results_data)
        calculations_sheet.update('A1', calculations_data)
        simulation_sheet.update('A1', simulation_formulas)
        
        # Ajouter des notes explicatives
        config_sheet.insert_note('A1', 'Configuration du projet - Ne pas modifier')
        results_sheet.insert_note('A1', 'Résultats de la simulation - Ne pas modifier')
        calculations_sheet.insert_note('A1', 'Calculs intermédiaires - Ne pas modifier')
        simulation_sheet.insert_note('A1', 'Feuille de simulation - Modifiez les valeurs ici')
        
        # Ajouter des formats conditionnels pour les calculs
        calculations_sheet.format('A1:B100', {
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
            'textFormat': {'bold': True}
        })
        
        st.success("Données exportées avec succès vers Google Sheets")
        st.info(f"Ouvrir le fichier : {spreadsheet.url}")
        st.info("""
        Structure des feuilles :
        - "Configuration" : Paramètres de base (ne pas modifier)
        - "Résultats" : Résultats de la simulation (ne pas modifier)
        - "Calculs" : Calculs intermédiaires (ne pas modifier)
        - "Simulation" : Feuille de travail (à modifier pour faire vos propres simulations)
        
        Pour faire une nouvelle simulation :
        1. Copiez la feuille "Simulation"
        2. Modifiez les valeurs dans la nouvelle feuille
        3. Les formules se mettront à jour automatiquement
        4. Les résultats seront mis à jour en temps réel
        """)
        
        return spreadsheet.url
        
    except Exception as e:
        st.error(f"Erreur lors de l'export vers Google Sheets: {str(e)}")
        return None

def export_to_excel(data, filename="simulation_rhum.xlsx"):
    """
    Exporte les données au format Excel (.xlsx) avec une structure claire et formatée
    
    Args:
        data (dict): Données à exporter
        filename (str): Nom du fichier Excel
        
    Returns:
        dict: Données exportées
    """
    try:
        # Créer un nouveau workbook Excel
        wb = Workbook()
        
        # 1. Feuille de Configuration
        config_ws = wb.active
        config_ws.title = "Configuration"
        
        # Style pour les titres
        title_font = Font(bold=True, size=14)
        header_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
        
        # Ajouter les métadonnées
        config_ws.append(["Configuration Générale"])
        config_ws['A1'].font = title_font
        config_ws.append([rhuma_label('id'), rhuma('id')])
        config_ws.append([rhuma_label('label'), rhuma('label')])
        config_ws.append([rhuma_label('version'), rhuma('version')])
        config_ws.append(["Timestamp", datetime.now().isoformat()])
        
        # Espacement
        config_ws.append([])
        
        # Ajouter les paramètres de simulation
        config_ws.append(["Paramètres de Simulation"])
        config_ws['A7'].font = title_font
        
        # Ajouter les paramètres avec style
        for idx, (key, value) in enumerate(state_manager.get_configuration().items(), start=8):
            cell = config_ws.cell(row=idx, column=1, value=key)
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="right")
            config_ws.cell(row=idx, column=2, value=value)
        
        # 2. Feuille de Résultats
        results_ws = wb.create_sheet("Résultats")
        
        # Préparer les données de résultats
        results_data = {
            "Production PV (serre)": data.get("production_pv", 0),
            "Production PV (au sol)": data.get("production_au_sol", 0),
            "Production totale": data.get("production_pv", 0) + data.get("production_au_sol", 0),
            "Autoconsommation": data.get("autoconsommation", 0),
            "Revente": data.get("revente", 0),
            "Revenu PV": data.get("revenu_pv", 0),
            "Revenu Rhum": data.get("revenu_rhum", 0),
            "Revenu total": data.get("revenu_pv", 0) + data.get("revenu_rhum", 0),
            "Coût PV": data.get("cout_pv", 0),
            "Coût serre": data.get("cout_serre", 0),
            "Coût total": data.get("cout_total", 0),
            "Bénéfice net": data.get("benefice_net", 0),
            "ROI": data.get("roi", 0),
            "Temps retour": data.get("temps_retour", 0)
        }
        
        # Ajouter les données
        results_ws.append(["Résultats de la Simulation"])
        results_ws['A1'].font = title_font
        
        for row in results_data.items():
            results_ws.append(row)
            results_ws.cell(row=results_ws.max_row, column=1).fill = header_fill
            results_ws.cell(row=results_ws.max_row, column=1).alignment = Alignment(horizontal="right")
        
        # 3. Feuille de Production Mensuelle
        monthly_ws = wb.create_sheet("Production Mensuelle")
        
        # Préparer les données de production mensuelle
        monthly_data = list(data.get("monthly_production", {}).items())
        monthly_ws.append(["Mois", "Production (kWh)"])
        
        for month, production in monthly_data:
            monthly_ws.append([month, production])
        
        # 4. Feuille de Scénarios
        scenarios_ws = wb.create_sheet("Scénarios")
        
        # Préparer les données de scénarios
        scenarios_data = data.get("scenarios", [])
        if scenarios_data:
            scenarios_ws.append(["Scénario", "Description", "Valeur"])
            for scenario in scenarios_data:
                scenarios_ws.append([
                    scenario.get("nom", ""),
                    scenario.get("description", ""),
                    scenario.get("valeur", "")
                ])
        
        # Sauvegarder le fichier Excel
        wb.save(filename)
        
        # Télécharger le fichier
        with open(filename, 'rb') as f:
            st.download_button(
                label="Télécharger l'export Excel",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        st.success("Données exportées avec succès au format Excel")
        
        return data
        
    except Exception as e:
        st.error(f"Erreur lors de l'export Excel: {str(e)}")
        return None

# Sidebar - Paramètres du projet
st.sidebar.header("Paramètres d'Entrée")

# Coûts de construction
st.sidebar.subheader("Coûts de Construction")

# Coûts PV
st.sidebar.markdown("### Coûts PV")
cout_fixe = st.sidebar.number_input(
    "Coût système PV fixe (€/kWc)",
    min_value=0,
    value=int(os.getenv('RHUMA_COUT_FIXE', 1000)),  # Prix moyen d'un système PV fixe en 2024
    step=100,
    help="Coût d'installation d'un système PV fixe par kWc"
)

# Coûts tracking
cout_tracking = st.sidebar.number_input(
    "Coût supplémentaire tracking (€/kWc)",
    min_value=0,
    value=int(os.getenv('RHUMA_COUT_TRACKING', 250)),  # Prix moyen du système tracking en 2024
    step=50,
    help="Coût supplémentaire pour le système de tracking par kWc"
)

# Coûts de construction
cout_construction = st.sidebar.number_input(
    "Coût construction serre (€/m²)",
    min_value=0,
    value=int(os.getenv('RHUMA_COUT_CONSTRUCTION', 150)),  # Prix moyen d'une serre standard en 2024
    step=50,
    help="Coût de construction de la serre par m². Pour une serre standard, les prix varient généralement entre 100 et 200€/m² selon les équipements."
)

# Coûts annuels
st.sidebar.markdown("### Coûts Annuels")
cout_maintenance = st.sidebar.number_input(
    "Coût maintenance annuel (€/kWc)",
    min_value=0,
    value=int(os.getenv('RHUMA_COUT_MAINTENANCE', 50)),  # Prix moyen de maintenance en 2024
    step=10,
    help="Coût annuel de maintenance par kWc"
)

cout_assurance = st.sidebar.number_input(
    "Coût assurance annuel (€/kWc)",
    min_value=0,
    value=int(os.getenv('RHUMA_COUT_ASSURANCE', 20)),  # Prix moyen d'assurance en 2024
    step=5,
    help="Coût annuel d'assurance par kWc"
)

cout_production = st.sidebar.number_input(
    "Coût production annuel (€/kWc)",
    min_value=0,
    value=float(os.getenv('RHUMA_COUT_PRODUCTION', 30.0)),
    step=1.0,
    help="Coût annuel de production de la canne à sucre et distillation"
)

# Calcul des coûts totaux
def calculate_total_costs(puissance_pv, surface_serre):
    """
    Calcule les coûts totaux du projet
    """
    # Coûts initiaux
    cout_pv = puissance_pv * (cout_fixe + cout_tracking)
    cout_serre = surface_serre * cout_construction
    
    # Coûts annuels
    couts_annuels = {
        'maintenance': puissance_pv * cout_maintenance,
        'assurance': puissance_pv * cout_assurance,
        'production': puissance_pv * cout_production
    }
    
    return {
        'cout_pv': cout_pv,
        'cout_serre': cout_serre,
        'cout_total': cout_pv + cout_serre,
        'couts_annuels': couts_annuels
    }

# Paramètres financiers
cost_col1, cost_col2 = st.sidebar.columns(2)

with cost_col1:
    # Tarifs et revenus
    st.write("### Tarifs et Revenus")
    
    # Tarifs EDF
    st.write("### Tarifs EDF")
    tarif_s24 = st.number_input(
        "Tarif S24 (€/kWh)",
        min_value=0.0,
        value=float(os.getenv('RHUMA_TARIF_S24', 0.13)),
        step=0.0001,
        help="Tarif de rachat S24 pour la Corse"
    )
    
    tarif_heures_creuses = st.number_input(
        "Tarif Heures Creuses (€/kWh)",
        min_value=0.0,
        value=float(os.getenv('RHUMA_TARIF_HEURES_CREUSES', 0.15)),
        step=0.0001,
        help="Tarif d'achat pour l'autoconsommation collective"
    )
    
    # Autoconsommation
    st.write("### Autoconsommation")
    autoconsommation_fixe = st.number_input(
        "Autoconsommation système fixe (kWh)",
        min_value=0.0,
        value=float(os.getenv('RHUMA_AUTOCONSOOMMATION_FIXE', 100000.0)),
        step=1000.0,
        help="Quantité d'énergie autoconsommée par an"
    )
    
    autoconsommation_tracking = st.number_input(
        "Autoconsommation système tracking (kWh)",
        min_value=0.0,
        value=float(os.getenv('RHUMA_AUTOCONSOOMMATION_TRACKING', 120000.0)),
        step=1000.0,
        help="Quantité d'énergie autoconsommée par an"
    )

with cost_col2:
    st.write("### Coûts de Production")
    prix_rhum = st.number_input(
        "Prix du rhum (€/L)",
        min_value=0.0,
        value=float(os.getenv('RHUMA_PRIX_RHUM', 20.0)),
        step=1.0,
        help="Prix de vente du rhum"
    )

# Paramètres techniques
tech_col1, tech_col2 = st.sidebar.columns(2)

with tech_col1:
    st.subheader("⚙️ Paramètres Techniques")
    
    # Paramètres de production
    st.write("### Production PV")
    puissance_pv = st.number_input(
        "Puissance installée (kWc)",
        min_value=0.0,
        value=int(os.getenv('RHUMA_PUISSANCE_PV', 500.0)),
        step=50.0,
        help="Puissance totale du système PV"
    )
    
    losses_pv = st.number_input(
        "Pertes PV (%)",
        min_value=0.0,
        max_value=100.0,
        value=int(os.getenv('RHUMA_PERTES_PV', 10.0)),
        step=1.0,
        help="Pertes techniques du système PV"
    )

with tech_col2:
    st.write("### Tracking")
    pertes_tracking = st.number_input(
        "Pertes de tracking (%)",
        min_value=0.0,
        max_value=100.0,
        value=int(os.getenv('RHUMA_PERTES_TRACKING', 5.0)),
        step=1.0,
        help="Pertes liées à l'absence de trackers solaires"
    )
    
    precision_tracking = st.number_input(
        "Précision tracking (°)",
        min_value=0.0,
        max_value=5.0,
        value=float(os.getenv('RHUMA_PRECISION_TRACKING', 0.2)),
        step=0.1,
        help="Précision du système de tracking"
    )

# Paramètres économiques
econ_col1, econ_col2 = st.sidebar.columns(2)

with econ_col1:
    st.subheader("🏦 Paramètres Économiques")
    
    taux_interet = st.number_input(
        "Taux d'intérêt annuel (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(os.getenv('RHUMA_TAUX_INTERET', 3.0)),
        step=0.1,
        help="Taux d'intérêt annuel pour le calcul du ROI"
    )
    
    duree_amortissement = st.number_input(
        "Durée d'amortissement (ans)",
        min_value=1,
        max_value=30,
        value=int(os.getenv('RHUMA_DUREE_AMORTISSEMENT', 20)),
        step=1,
        help="Durée sur laquelle l'investissement est amorti"
    )

with econ_col2:
    cout_production = st.number_input(
        "Coût production annuel (€/kWc)",
        min_value=0.0,
        value=float(os.getenv('RHUMA_COUT_PRODUCTION', 30.0)),
        step=1.0,
        help="Coût annuel de production de la canne à sucre et distillation"
    )
    
    prix_alcool = st.number_input(
        "Prix de l'alcool (€/L)",
        min_value=0.0,
        value=float(os.getenv('RHUMA_PRIX_ALCOOL', 20.0)),
        step=1.0,
        help="Prix de vente de l'alcool"
    )

# 1. Surface et Rendement
st.session_state['surface_canne'] = rhuma('surface_canne')
st.session_state['rendement_canne'] = rhuma('rendement_canne')
st.session_state['teneur_sucre'] = rhuma('teneur_sucre')
st.session_state['efficacite_extraction'] = rhuma('efficacite_extraction')
st.session_state['efficacite_distillation'] = rhuma('efficacite_distillation')
st.session_state['pv_serre'] = rhuma('pv_serre')
st.session_state['pv_sol'] = rhuma('pv_sol')

def calcul_production(surface, rendement, sucre, extraction, distillation):
    canne_kg = (surface / 10000) * rendement * 1000  # kg
    sucre_kg = canne_kg * (sucre / 100) * (extraction / 100)
    alcool_l = sucre_kg * 0.51 * (distillation / 100)
    return canne_kg, sucre_kg, alcool_l

canne, sucre, alcool = calcul_production(rhuma('surface_canne'), rhuma('rendement_canne'), rhuma('teneur_sucre'),
                                        rhuma('efficacite_extraction'), rhuma('efficacite_distillation'))

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
    tracking_comparison_section(production_pv_ideal)
    financial_simulation_section()
    pvgis_analysis_section()

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
        st.write(f"- Tarif S24 : {0.1772}€/kWh")
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

        st.write("\n### 💰 Revenus")
        st.write(f"- Revenu Rhum : {revenu_rhum:.0f}€/an")
        st.write(f"- Revenu PV (vente) : {revenu_pv:.0f}€/an")
        st.write(f"- CA collectif : {chiffre_affaires_collectif:.0f}€/an")
        st.write(f"- CA collectif idéal : {chiffre_affaires_collectif_ideal:.0f}€/an")
        st.write(f"- CA total : {chiffre_affaires_total:.0f}€/an")
        st.write(f"- CA total idéal : {chiffre_affaires_total_ideal:.0f}€/an")
        st.write(f"- Delta CA : {delta_ca:.0f}€/an")
