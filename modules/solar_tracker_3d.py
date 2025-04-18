# modules/solar_tracker_3d.py
# Module pour intégrer la simulation 3D du tracker solaire dans l'application Streamlit
# avec améliorations de précision scientifique, performances graphiques et UX

import streamlit as st
import os
import json

def get_tracker_3d_html():
    """Récupère le contenu HTML du modèle 3D du tracker solaire
    
    Returns:
        str: Contenu HTML du modèle 3D
    """
    html_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'solar-tracker-3d-model.html')
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    return html_content

def display_solar_tracker_3d(height=700, location=None, constraints=None):
    """Affiche le modèle 3D du tracker solaire dans Streamlit avec options avancées
    
    Args:
        height (int): Hauteur du composant HTML en pixels
    """
    html_content = get_tracker_3d_html()
    
    # Valeurs par défaut pour les paramètres, Corte
    if location is None:
        location = {
            "latitude": 42.3,
            "longitude": 9.15,
            "timezone": 2
        }
    
    if constraints is None:
        constraints = {
            "minTiltX": 15,
            "maxTiltX": 75,
            "maxCableDifference": 50,
            "elasticity": 0.05
        }
    
    # Convertir les paramètres en JSON pour l'injection dans le JavaScript
    location_json = json.dumps(location)
    constraints_json = json.dumps(constraints)
    
    # Ajuster le HTML pour qu'il fonctionne correctement dans un iframe Streamlit
    # - Supprimer les balises DOCTYPE, html, head et body
    # - Conserver uniquement le contenu et les scripts
    # - Ajuster la taille pour s'adapter à l'iframe
    
    # Extraire le contenu entre les balises body
    body_start = html_content.find('<body>')
    body_end = html_content.find('</body>')
    
    if body_start != -1 and body_end != -1:
        body_content = html_content[body_start + len('<body>'):body_end]
    else:
        body_content = html_content
    
    # Extraire les styles
    style_start = html_content.find('<style>')
    style_end = html_content.find('</style>')
    
    if style_start != -1 and style_end != -1:
        style_content = html_content[style_start:style_end + len('</style>')]
    else:
        style_content = ""
    
    # Extraire les scripts
    script_tags = []
    script_start = 0
    while True:
        script_start = html_content.find('<script', script_start)
        if script_start == -1:
            break
        
        script_end = html_content.find('</script>', script_start)
        if script_end == -1:
            break
        
        script_tags.append(html_content[script_start:script_end + len('</script>')])
        script_start = script_end + len('</script>')
    
    # Préparer le script d'injection des paramètres
    config_script = f"""
    <script>
        // Configuration injectée par Streamlit
        document.addEventListener('DOMContentLoaded', function() {{
            // Attendre que la configuration soit chargée
            setTimeout(function() {{
                // Injecter les paramètres de localisation
                if (typeof config !== 'undefined') {{
                    // Paramètres de localisation
                    const location = {location_json};
                    config.latitude = location.latitude;
                    config.longitude = location.longitude;
                    config.timezone = location.timezone;
                    
                    // Contraintes mécaniques
                    const constraints = {constraints_json};
                    if (constraints.minTiltX !== undefined) config.minTiltX = constraints.minTiltX;
                    if (constraints.maxTiltX !== undefined) config.maxTiltX = constraints.maxTiltX;
                    if (constraints.maxCableDifference !== undefined) config.maxCableDifference = constraints.maxCableDifference;
                    if (constraints.elasticity !== undefined) config.elasticity = constraints.elasticity;
                    
                    // Mettre à jour l'interface utilisateur
                    if (document.getElementById('latitude')) {{
                        document.getElementById('latitude').value = config.latitude;
                        document.getElementById('latitudeValue').textContent = config.latitude + '°' + (config.latitude >= 0 ? 'N' : 'S');
                    }}
                    if (document.getElementById('longitude')) {{
                        document.getElementById('longitude').value = config.longitude;
                        document.getElementById('longitudeValue').textContent = config.longitude + '°' + (config.longitude >= 0 ? 'E' : 'O');
                    }}
                    if (document.getElementById('timezone')) {{
                        document.getElementById('timezone').value = config.timezone;
                        document.getElementById('timezoneValue').textContent = 'UTC' + (config.timezone >= 0 ? '+' : '') + config.timezone;
                    }}
                    
                    // Mettre à jour la position du soleil et du panneau
                    if (typeof updateSunPosition === 'function') {{
                        updateSunPosition();
                    }}
                }}
            }}, 1000);
        }});
    </script>
    """
    script_tags.append(config_script)
    
    # Construire le HTML adapté pour Streamlit
    adapted_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        {style_content}
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; }}
            canvas {{ width: 100%; height: 100%; display: block; }}
            .controls {{ max-width: 350px; }}
        </style>
    </head>
    <body>
        {body_content}
        {''.join(script_tags)}
    </body>
    </html>
    """
    
    # Afficher le HTML dans un composant iframe
    st.components.v1.html(adapted_html, height=height, scrolling=True)

def solar_tracker_3d_section():
    """Section complète pour la simulation 3D du tracker solaire avec options avancées"""
    st.header("🔆 Simulation 3D du Tracker Solaire")
    
    st.write("""
    Cette simulation interactive vous permet de visualiser le fonctionnement du tracker solaire à trois mâts 
    et de comprendre comment l'ajustement des câbles permet d'orienter le panneau vers le soleil.
    """)
    
    # Options avancées
    with st.expander("⚙️ Options avancées"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Options de qualité graphique
            st.subheader("Qualité graphique")
            quality = st.radio(
                "Qualité des ombres",
                options=["auto", "low", "medium", "high"],
                index=0,
                help="Ajuste la qualité des ombres en fonction de la puissance de votre appareil"
            )
            
            # Options de démonstration
            st.subheader("Modes de démonstration")
            demo_mode = st.selectbox(
                "Scénario prédéfini",
                options=[
                    "none", "solsticeEte", "solsticeHiver", "equinoxe", 
                    "journee", "neige", "vent", "optimisation"
                ],
                format_func=lambda x: {
                    "none": "Aucun",
                    "solsticeEte": "Solstice d'été (21 juin)",
                    "solsticeHiver": "Solstice d'hiver (21 décembre)",
                    "equinoxe": "Équinoxe (21 mars)",
                    "journee": "Journée complète",
                    "neige": "Charge de neige",
                    "vent": "Vent fort",
                    "optimisation": "Optimisation énergétique"
                }[x],
                index=0,
                help="Lance une démonstration prédéfinie pour illustrer différents scénarios"
            )
        
        with col2:
            # Options de localisation
            st.subheader("Localisation")
            latitude = st.slider(
                "Latitude",
                min_value=-60.0,
                max_value=60.0,
                value=42.3,
                step=0.1,
                format="%.1f°",
                help="Latitude du lieu en degrés (positif = Nord, négatif = Sud)"
            )
            longitude = st.slider(
                "Longitude",
                min_value=-180.0,
                max_value=180.0,
                value=9.15,
                step=0.1,
                format="%.1f°",
                help="Longitude du lieu en degrés (positif = Est, négatif = Ouest)"
            )
            timezone = st.slider(
                "Fuseau horaire",
                min_value=-12,
                max_value=12,
                value=2,
                step=1,
                format="UTC%+d",
                help="Fuseau horaire par rapport à UTC"
            )
            
            # Options de contraintes mécaniques
            st.subheader("Contraintes mécaniques")
            min_tilt = st.slider(
                "Inclinaison minimale",
                min_value=0,
                max_value=45,
                value=15,
                step=5,
                format="%d°",
                help="Angle minimal d'inclinaison du panneau"
            )
            max_tilt = st.slider(
                "Inclinaison maximale",
                min_value=45,
                max_value=90,
                value=75,
                step=5,
                format="%d°",
                help="Angle maximal d'inclinaison du panneau"
            )
            max_diff = st.slider(
                "Différence max entre câbles",
                min_value=20,
                max_value=80,
                value=50,
                step=5,
                format="%d cm",
                help="Différence maximale autorisée entre les longueurs des câbles Sud-Est et Sud-Ouest"
            )
    
    # Préparer les paramètres pour le modèle 3D
    location = {
        "latitude": latitude if 'latitude' in locals() else 42.3,
        "longitude": longitude if 'longitude' in locals() else 9.15,
        "timezone": timezone if 'timezone' in locals() else 2
    }
    
    constraints = {
        "minTiltX": min_tilt if 'min_tilt' in locals() else 15,
        "maxTiltX": max_tilt if 'max_tilt' in locals() else 75,
        "maxCableDifference": max_diff if 'max_diff' in locals() else 50,
        "elasticity": 0.05  # Valeur par défaut pour l'élasticité des câbles
    }
    
    # Afficher le modèle 3D avec les options configurées
    display_solar_tracker_3d(
        height=700,
        location=location,
        constraints=constraints
    )
    
    # Informations complémentaires
    with st.expander("ℹ️ À propos du tracker solaire à trois mâts"):
        st.write("""
        ### Principe de fonctionnement
        
        Le tracker solaire à trois mâts est composé de :
        - Un mât fixe au Nord qui sert de pivot
        - Deux mâts au Sud équipés de treuils motorisés
        - Un panneau solaire suspendu par des câbles
        
        Les treuils ajustent automatiquement la longueur des câbles Sud-Est et Sud-Ouest pour orienter 
        le panneau perpendiculairement aux rayons du soleil tout au long de la journée, maximisant ainsi 
        la production d'énergie.
        
        ### Avantages
        
        - Augmentation de la production d'environ 30% par rapport à des panneaux fixes
        - Conception mécanique simple et robuste
        - Arrimage au sol par de simples piquets
        - Mise en sécurité facile par grand vent
        """)