# modules/solar_tracker_3d.py
# Module pour intégrer la simulation 3D du tracker solaire dans l'application Streamlit

import streamlit as st
import os

def get_tracker_3d_html():
    """Récupère le contenu HTML du modèle 3D du tracker solaire"""
    html_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'solar-tracker-3d-model.html')
    
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    return html_content

def display_solar_tracker_3d(height=700):
    """Affiche le modèle 3D du tracker solaire dans Streamlit
    
    Args:
        height (int): Hauteur du composant HTML en pixels
    """
    html_content = get_tracker_3d_html()
    
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
            .controls {{ max-width: 300px; }}
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
    """Section complète pour la simulation 3D du tracker solaire"""
    st.header("🔆 Simulation 3D du Tracker Solaire")
    
    st.write("""
    Cette simulation interactive vous permet de visualiser le fonctionnement du tracker solaire à trois mâts 
    et de comprendre comment l'ajustement des câbles permet d'orienter le panneau vers le soleil.
    """)
    
    # Afficher le modèle 3D
    display_solar_tracker_3d(height=700)
    
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
        
        - Augmentation de la production d'environ 28% par rapport à des panneaux fixes
        - Conception mécanique simple et robuste
        - Maintenance facilitée (pas de moteurs sur le panneau)
        - Résistance accrue aux conditions météorologiques
        """)