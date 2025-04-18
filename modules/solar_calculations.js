/**
 * solar_calculations.js
 * Module de calculs astronomiques précis pour le tracker solaire 3D
 * 
 * Ce module utilise la bibliothèque SunCalc pour effectuer des calculs
 * astronomiques précis concernant la position du soleil.
 */

// Importer SunCalc via CDN (sera chargé dans le HTML)
// <script src="https://cdnjs.cloudflare.com/ajax/libs/suncalc/1.9.0/suncalc.min.js"></script>

/**
 * Calcule la position du soleil (azimut et élévation) pour un lieu et un moment donnés
 * @param {number} latitude - Latitude en degrés décimaux
 * @param {number} longitude - Longitude en degrés décimaux
 * @param {Date} date - Date et heure pour le calcul
 * @returns {Object} Position du soleil avec azimut et élévation en degrés
 */
function getSunPosition(latitude, longitude, date) {
    // Utiliser SunCalc pour obtenir la position du soleil
    const sunPosition = SunCalc.getPosition(date, latitude, longitude);
    
    // Convertir l'altitude (élévation) de radians en degrés
    const elevation = sunPosition.altitude * 180 / Math.PI;
    
    // Convertir l'azimut de radians en degrés et ajuster pour la convention géographique
    // SunCalc donne l'azimut par rapport au sud (0) dans le sens horaire
    // Nous voulons l'azimut par rapport au nord (0) dans le sens horaire
    let azimuth = sunPosition.azimuth * 180 / Math.PI + 180;
    
    // Normaliser l'azimut entre 0 et 360 degrés
    azimuth = (azimuth + 360) % 360;
    
    return {
        elevation: elevation,
        azimuth: azimuth,
        // Ajouter des informations supplémentaires utiles
        rawAltitude: sunPosition.altitude,
        rawAzimuth: sunPosition.azimuth
    };
}

/**
 * Calcule les heures de lever et coucher du soleil pour un lieu et une date donnés
 * @param {number} latitude - Latitude en degrés décimaux
 * @param {number} longitude - Longitude en degrés décimaux
 * @param {Date} date - Date pour le calcul
 * @returns {Object} Heures de lever et coucher du soleil
 */
function getSunTimes(latitude, longitude, date) {
    // Obtenir les différents moments de la journée solaire
    const times = SunCalc.getTimes(date, latitude, longitude);
    
    return {
        sunrise: times.sunrise,
        sunset: times.sunset,
        solarNoon: times.solarNoon,
        dawn: times.dawn,
        dusk: times.dusk,
        // Durée du jour en heures
        dayLength: (times.sunset - times.sunrise) / (1000 * 60 * 60)
    };
}

/**
 * Calcule l'angle optimal du panneau solaire pour maximiser l'exposition
 * @param {number} elevation - Élévation du soleil en degrés
 * @param {number} azimuth - Azimut du soleil en degrés
 * @returns {Object} Angles optimaux d'inclinaison et d'orientation du panneau
 */
function calculateOptimalPanelAngles(elevation, azimuth) {
    // L'inclinaison optimale est l'inverse de l'élévation par rapport à l'horizon
    const optimalTiltX = 90 - elevation;
    
    // L'orientation optimale doit suivre l'azimut du soleil
    // Convertir l'azimut (0-360°) en orientation du panneau (-180 à 180°)
    let optimalTiltZ;
    if (azimuth > 180) {
        optimalTiltZ = azimuth - 360;
    } else {
        optimalTiltZ = azimuth;
    }
    // Inverser car le panneau doit faire face au soleil
    optimalTiltZ = -optimalTiltZ;
    
    return {
        tiltX: optimalTiltX,
        tiltZ: optimalTiltZ
    };
}

/**
 * Calcule les longueurs de câble nécessaires pour atteindre une orientation donnée du panneau
 * @param {number} tiltX - Inclinaison du panneau en degrés (axe X)
 * @param {number} tiltZ - Orientation du panneau en degrés (axe Z)
 * @param {Object} config - Configuration du système (longueurs de base, facteurs d'ajustement)
 * @returns {Object} Longueurs calculées des câbles SE et SW
 */
function calculateCableLengths(tiltX, tiltZ, config) {
    // Récupérer les valeurs depuis la configuration ou utiliser les valeurs par défaut
    // Ces valeurs devraient idéalement provenir du système d'attributs Rhuma
    const baseCableLength = config?.baseCableLength || (config?.rhuma_state?.configuration?.baseCableLength || 80);
    const tiltXFactor = config?.tiltXFactor || (config?.rhuma_state?.configuration?.tiltXFactor || 0.35);
    const tiltZFactor = config?.tiltZFactor || (config?.rhuma_state?.configuration?.tiltZFactor || 0.8);
    const minLength = config?.minLength || (config?.rhuma_state?.configuration?.minLength || 30);
    const maxLength = config?.maxLength || (config?.rhuma_state?.configuration?.maxLength || 120);
    const maxDifference = config?.maxDifference || (config?.rhuma_state?.configuration?.maxDifference || 50); // Contrainte mécanique
    
    // Calcul des longueurs de câble
    // Le câble SE s'allonge quand le panneau s'oriente vers l'ouest (tiltZ négatif)
    // et quand l'inclinaison augmente (tiltX positif)
    let seCableLength = baseCableLength - (tiltZ * tiltZFactor) + (tiltX * tiltXFactor);
    
    // Le câble SW s'allonge quand le panneau s'oriente vers l'est (tiltZ positif)
    // et quand l'inclinaison augmente (tiltX positif)
    let swCableLength = baseCableLength + (tiltZ * tiltZFactor) + (tiltX * tiltXFactor);
    
    // Limiter les longueurs de câble aux valeurs min/max
    seCableLength = Math.max(minLength, Math.min(maxLength, seCableLength));
    swCableLength = Math.max(minLength, Math.min(maxLength, swCableLength));
    
    // Appliquer la contrainte de différence maximale entre les câbles
    if (Math.abs(seCableLength - swCableLength) > maxDifference) {
        const average = (seCableLength + swCableLength) / 2;
        if (seCableLength > swCableLength) {
            seCableLength = average + maxDifference / 2;
            swCableLength = average - maxDifference / 2;
        } else {
            seCableLength = average - maxDifference / 2;
            swCableLength = average + maxDifference / 2;
        }
        
        // S'assurer que les valeurs restent dans les limites
        seCableLength = Math.max(minLength, Math.min(maxLength, seCableLength));
        swCableLength = Math.max(minLength, Math.min(maxLength, swCableLength));
    }
    
    return {
        seCableLength: seCableLength,
        swCableLength: swCableLength
    };
}

/**
 * Calcule l'efficacité du panneau solaire en fonction de son orientation par rapport au soleil
 * @param {number} panelTiltX - Inclinaison actuelle du panneau en degrés (axe X)
 * @param {number} panelTiltZ - Orientation actuelle du panneau en degrés (axe Z)
 * @param {number} sunElevation - Élévation du soleil en degrés
 * @param {number} sunAzimuth - Azimut du soleil en degrés
 * @returns {number} Efficacité en pourcentage (0-100)
 */
function calculatePanelEfficiency(panelTiltX, panelTiltZ, sunElevation, sunAzimuth) {
    // Calculer l'angle optimal du panneau
    const optimalAngles = calculateOptimalPanelAngles(sunElevation, sunAzimuth);
    
    // Calculer l'écart entre l'orientation actuelle et l'orientation optimale
    const tiltXDiff = Math.abs(panelTiltX - optimalAngles.tiltX);
    const tiltZDiff = Math.abs(panelTiltZ - optimalAngles.tiltZ);
    
    // Calculer l'angle total entre le vecteur normal du panneau et la direction du soleil
    // (approximation simplifiée)
    const totalAngleDiff = Math.sqrt(tiltXDiff * tiltXDiff + tiltZDiff * tiltZDiff);
    
    // L'efficacité diminue avec le cosinus de l'angle d'incidence
    // (loi du cosinus pour l'irradiance)
    const efficiency = Math.cos(totalAngleDiff * Math.PI / 180) * 100;
    
    // Limiter l'efficacité entre 0 et 100%
    return Math.max(0, Math.min(100, efficiency));
}

// Exporter les fonctions pour utilisation dans d'autres modules
export {
    getSunPosition,
    getSunTimes,
    calculateOptimalPanelAngles,
    calculateCableLengths,
    calculatePanelEfficiency
};