/**
 * solar_calculations_enhanced.js
 * Module de calculs astronomiques précis pour le tracker solaire 3D
 * 
 * Ce module utilise la bibliothèque SunCalc pour effectuer des calculs
 * astronomiques précis concernant la position du soleil, avec des
 * améliorations pour la précision scientifique, les contraintes mécaniques
 * et l'extensibilité.
 */

// Importer SunCalc via CDN (sera chargé dans le HTML)
// <script src="https://cdnjs.cloudflare.com/ajax/libs/suncalc/1.9.0/suncalc.min.js"></script>

// Importer la fonction rhuma pour accéder aux attributs du système
import { rhuma } from './state_manager.js';

/**
 * Calcule la position du soleil (azimut et élévation) pour un lieu et un moment donnés
 * avec une précision < 0.1° et prise en compte des effets atmosphériques
 * 
 * @param {number} latitude - Latitude en degrés décimaux
 * @param {number} longitude - Longitude en degrés décimaux
 * @param {Date} date - Date et heure pour le calcul
 * @param {Object} options - Options supplémentaires (optionnel)
 * @param {boolean} options.applyRefraction - Appliquer la correction de réfraction atmosphérique
 * @returns {Object} Position du soleil avec azimut et élévation en degrés
 */
function getSunPosition(latitude, longitude, date, options = {}) {
    // Utiliser directement l'attribut via rhuma() ou l'option passée en paramètre
    const applyRefraction = options.applyRefraction !== undefined ? options.applyRefraction : rhuma('applyRefraction');
    
    // Utiliser SunCalc pour obtenir la position du soleil
    const sunPosition = SunCalc.getPosition(date, latitude, longitude);
    
    // Convertir l'altitude (élévation) de radians en degrés
    let elevation = sunPosition.altitude * 180 / Math.PI;
    
    // Appliquer la correction de réfraction atmosphérique si demandé
    if (applyRefraction && elevation > -1) {
        // Formule de réfraction atmosphérique basée sur l'algorithme PSA
        // Valable pour des élévations > -1° (sinon la réfraction devient très complexe)
        const elevationRad = elevation * Math.PI / 180;
        const refraction = 0.0002967 / Math.tan(elevationRad + 0.00312536 / (elevationRad + 0.089186));
        elevation += refraction;
    }
    
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
        rawAzimuth: sunPosition.azimuth,
        equationOfTime: calculateEquationOfTime(date)
    };
}

/**
 * Calcule l'équation du temps (différence entre temps solaire moyen et temps solaire vrai)
 * @param {Date} date - Date pour le calcul
 * @returns {number} Équation du temps en minutes
 */
function calculateEquationOfTime(date) {
    // Jour de l'année (1-365)
    const dayOfYear = getDayOfYear(date);
    
    // Angle du jour en radians
    const dayAngle = 2 * Math.PI * (dayOfYear - 1) / 365;
    
    // Calcul basé sur l'approximation de Spencer (1971)
    // Précision d'environ 30 secondes
    const eot = 229.18 * (
        0.000075 +
        0.001868 * Math.cos(dayAngle) -
        0.032077 * Math.sin(dayAngle) -
        0.014615 * Math.cos(2 * dayAngle) -
        0.040849 * Math.sin(2 * dayAngle)
    );
    
    return eot; // en minutes
}

/**
 * Obtient le jour de l'année (1-365 ou 366)
 * @param {Date} date - Date pour le calcul
 * @returns {number} Jour de l'année
 */
function getDayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start;
    const oneDay = 1000 * 60 * 60 * 24;
    return Math.floor(diff / oneDay);
}

/**
 * Convertit l'heure solaire en heure légale
 * @param {number} solarTime - Heure solaire (0-24)
 * @param {number} longitude - Longitude en degrés
 * @param {number} timezone - Fuseau horaire (UTC+timezone)
 * @param {Date} date - Date pour le calcul
 * @returns {number} Heure légale (0-24)
 */
function solarTimeToLocalTime(solarTime, longitude, timezone, date) {
    // Correction de longitude (4 minutes par degré)
    const longitudeCorrection = 4 * (longitude - (15 * timezone)) / 60; // en heures
    
    // Équation du temps
    const eot = calculateEquationOfTime(date) / 60; // convertir en heures
    
    // Heure légale = Heure solaire - Correction de longitude - Équation du temps
    let localTime = solarTime - longitudeCorrection - eot;
    
    // Normaliser entre 0 et 24
    localTime = (localTime + 24) % 24;
    
    return localTime;
}

/**
 * Convertit l'heure légale en heure solaire
 * @param {number} localTime - Heure légale (0-24)
 * @param {number} longitude - Longitude en degrés
 * @param {number} timezone - Fuseau horaire (UTC+timezone)
 * @param {Date} date - Date pour le calcul
 * @returns {number} Heure solaire (0-24)
 */
function localTimeToSolarTime(localTime, longitude, timezone, date) {
    // Correction de longitude (4 minutes par degré)
    const longitudeCorrection = 4 * (longitude - (15 * timezone)) / 60; // en heures
    
    // Équation du temps
    const eot = calculateEquationOfTime(date) / 60; // convertir en heures
    
    // Heure solaire = Heure légale + Correction de longitude + Équation du temps
    let solarTime = localTime + longitudeCorrection + eot;
    
    // Normaliser entre 0 et 24
    solarTime = (solarTime + 24) % 24;
    
    return solarTime;
}

/**
 * Calcule les heures de lever et coucher du soleil pour un lieu et une date donnés
 * @param {number} latitude - Latitude en degrés décimaux
 * @param {number} longitude - Longitude en degrés décimaux
 * @param {Date} date - Date pour le calcul
 * @param {Object} options - Options supplémentaires (optionnel)
 * @param {number} options.timezone - Fuseau horaire (UTC+timezone)
 * @returns {Object} Heures de lever et coucher du soleil et autres informations
 */
function getSunTimes(latitude, longitude, date, options = {}) {
    // Utiliser directement l'attribut via rhuma() ou l'option passée en paramètre
    const timezone = options.timezone !== undefined ? options.timezone : rhuma('timezone');
    
    // Obtenir les différents moments de la journée solaire
    const times = SunCalc.getTimes(date, latitude, longitude);
    
    // Calculer les heures solaires et légales
    const sunriseHours = times.sunrise.getHours() + times.sunrise.getMinutes() / 60;
    const sunsetHours = times.sunset.getHours() + times.sunset.getMinutes() / 60;
    const solarNoonHours = times.solarNoon.getHours() + times.solarNoon.getMinutes() / 60;
    
    // Durée du jour en heures
    const dayLength = (times.sunset - times.sunrise) / (1000 * 60 * 60);
    
    return {
        // Objets Date complets
        sunrise: times.sunrise,
        sunset: times.sunset,
        solarNoon: times.solarNoon,
        dawn: times.dawn,
        dusk: times.dusk,
        
        // Heures décimales (plus faciles à utiliser pour les calculs)
        sunriseHours: sunriseHours,
        sunsetHours: sunsetHours,
        solarNoonHours: solarNoonHours,
        
        // Durée du jour en heures
        dayLength: dayLength,
        
        // Informations formatées pour l'affichage
        sunriseFormatted: formatTime(times.sunrise),
        sunsetFormatted: formatTime(times.sunset),
        dayLengthFormatted: formatDuration(dayLength)
    };
}

/**
 * Formate une heure (objet Date) en chaîne HH:MM
 * @param {Date} date - Date à formater
 * @returns {string} Heure formatée
 */
function formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * Formate une durée en heures en chaîne HH h MM min
 * @param {number} hours - Durée en heures
 * @returns {string} Durée formatée
 */
function formatDuration(hours) {
    const h = Math.floor(hours);
    const min = Math.round((hours - h) * 60);
    return `${h} h ${min} min`;
}

/**
 * Calcule l'angle optimal du panneau solaire pour maximiser l'exposition
 * @param {number} elevation - Élévation du soleil en degrés
 * @param {number} azimuth - Azimut du soleil en degrés
 * @param {Object} constraints - Contraintes mécaniques à appliquer (optionnel)
 * @returns {Object} Angles optimaux d'inclinaison et d'orientation du panneau
 */
function calculateOptimalPanelAngles(elevation, azimuth, constraints = {}) {
    // Utiliser directement les attributs via rhuma() ou les contraintes passées en paramètre
    const minTiltX = constraints.minTiltX !== undefined ? constraints.minTiltX : rhuma('minTiltX');
    const maxTiltX = constraints.maxTiltX !== undefined ? constraints.maxTiltX : rhuma('maxTiltX');
    
    // L'inclinaison optimale est l'inverse de l'élévation par rapport à l'horizon
    let optimalTiltX = 90 - elevation;
    
    // Appliquer les contraintes d'inclinaison
    optimalTiltX = Math.max(minTiltX, Math.min(maxTiltX, optimalTiltX));
    
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
 * avec prise en compte des contraintes mécaniques réalistes
 * 
 * @param {number} tiltX - Inclinaison du panneau en degrés (axe X)
 * @param {number} tiltZ - Orientation du panneau en degrés (axe Z)
 * @param {Object} config - Configuration du système et contraintes mécaniques (optionnel)
 * @returns {Object} Longueurs calculées des câbles SE et SW et informations sur les contraintes
 */
function calculateCableLengths(tiltX, tiltZ, config = {}) {
    // Utiliser directement les attributs via rhuma() ou les valeurs du paramètre config
    const baseCableLength = config.baseCableLength !== undefined ? config.baseCableLength : rhuma('baseCableLength');
    const tiltXFactor = config.tiltXFactor !== undefined ? config.tiltXFactor : rhuma('tiltXFactor');
    const tiltZFactor = config.tiltZFactor !== undefined ? config.tiltZFactor : rhuma('tiltZFactor');
    const minLength = config.minLength !== undefined ? config.minLength : rhuma('minLength');
    const maxLength = config.maxLength !== undefined ? config.maxLength : rhuma('maxLength');
    const maxDifference = config.maxDifference !== undefined ? config.maxDifference : rhuma('maxDifference');
    
    // Coefficient d'élasticité des câbles (0 = rigide, 1 = très élastique)
    const elasticity = config.elasticity !== undefined ? config.elasticity : rhuma('elasticity');
    
    // Calcul des longueurs de câble idéales (sans contraintes)
    // Le câble SE s'allonge quand le panneau s'oriente vers l'ouest (tiltZ négatif)
    // et quand l'inclinaison augmente (tiltX positif)
    let seCableLength = baseCableLength - (tiltZ * tiltZFactor) + (tiltX * tiltXFactor);
    
    // Le câble SW s'allonge quand le panneau s'oriente vers l'est (tiltZ positif)
    // et quand l'inclinaison augmente (tiltX positif)
    let swCableLength = baseCableLength + (tiltZ * tiltZFactor) + (tiltX * tiltXFactor);
    
    // Variables pour suivre les contraintes appliquées
    const constraints = {
        minLengthApplied: false,
        maxLengthApplied: false,
        maxDifferenceApplied: false
    };
    
    // Limiter les longueurs de câble aux valeurs min/max
    if (seCableLength < minLength) {
        seCableLength = minLength;
        constraints.minLengthApplied = true;
    } else if (seCableLength > maxLength) {
        seCableLength = maxLength;
        constraints.maxLengthApplied = true;
    }
    
    if (swCableLength < minLength) {
        swCableLength = minLength;
        constraints.minLengthApplied = true;
    } else if (swCableLength > maxLength) {
        swCableLength = maxLength;
        constraints.maxLengthApplied = true;
    }
    
    // Appliquer la contrainte de différence maximale entre les câbles
    if (Math.abs(seCableLength - swCableLength) > maxDifference) {
        constraints.maxDifferenceApplied = true;
        const average = (seCableLength + swCableLength) / 2;
        if (seCableLength > swCableLength) {
            seCableLength = average + maxDifference / 2;
            swCableLength = average - maxDifference / 2;
        } else {
            seCableLength = average - maxDifference / 2;
            swCableLength = average + maxDifference / 2;
        }
        
        // S'assurer que les valeurs restent dans les limites
        if (seCableLength < minLength) {
            seCableLength = minLength;
            swCableLength = minLength + maxDifference;
            constraints.minLengthApplied = true;
        } else if (seCableLength > maxLength) {
            seCableLength = maxLength;
            swCableLength = maxLength - maxDifference;
            constraints.maxLengthApplied = true;
        }
        
        if (swCableLength < minLength) {
            swCableLength = minLength;
            seCableLength = minLength + maxDifference;
            constraints.minLengthApplied = true;
        } else if (swCableLength > maxLength) {
            swCableLength = maxLength;
            seCableLength = maxLength - maxDifference;
            constraints.maxLengthApplied = true;
        }
    }
    
    // Calculer la tension des câbles (approximation simplifiée)
    // Plus la longueur est proche des extrêmes, plus la tension est élevée
    const seTension = calculateCableTension(seCableLength, minLength, maxLength, elasticity);
    const swTension = calculateCableTension(swCableLength, minLength, maxLength, elasticity);
    
    return {
        seCableLength: seCableLength,
        swCableLength: swCableLength,
        seTension: seTension,
        swTension: swTension,
        constraints: constraints
    };
}

/**
 * Calcule la tension d'un câble en fonction de sa longueur et des limites
 * @param {number} length - Longueur actuelle du câble
 * @param {number} minLength - Longueur minimale
 * @param {number} maxLength - Longueur maximale
 * @param {number} elasticity - Coefficient d'élasticité (0-1)
 * @returns {number} Tension du câble (0-1)
 */
function calculateCableTension(length, minLength, maxLength, elasticity) {
    // Normaliser la longueur entre 0 et 1
    const normalizedLength = (length - minLength) / (maxLength - minLength);
    
    // La tension est plus élevée aux extrêmes (proche de min ou max)
    // et plus faible au milieu de la plage
    const tension = 1 - 4 * Math.pow(normalizedLength - 0.5, 2);
    
    // Appliquer l'élasticité (plus l'élasticité est élevée, moins la tension varie)
    return tension * (1 - elasticity);
}

/**
 * Calcule l'efficacité du panneau solaire en fonction de son orientation par rapport au soleil
 * @param {number} panelTiltX - Inclinaison actuelle du panneau en degrés (axe X)
 * @param {number} panelTiltZ - Orientation actuelle du panneau en degrés (axe Z)
 * @param {number} sunElevation - Élévation du soleil en degrés
 * @param {number} sunAzimuth - Azimut du soleil en degrés
 * @param {Object} options - Options supplémentaires (optionnel)
 * @returns {Object} Efficacité en pourcentage (0-100) et informations détaillées
 */
function calculatePanelEfficiency(panelTiltX, panelTiltZ, sunElevation, sunAzimuth, options = {}) {
    // Utiliser les attributs via rhuma() ou les options passées en paramètre
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
    const clampedEfficiency = Math.max(0, Math.min(100, efficiency));
    
    // Calculer la perte d'efficacité due à chaque axe
    const lossX = (1 - Math.cos(tiltXDiff * Math.PI / 180)) * 100;
    const lossZ = (1 - Math.cos(tiltZDiff * Math.PI / 180)) * 100;
    
    return {
        efficiency: clampedEfficiency,
        optimalAngles: optimalAngles,
        angleDifference: totalAngleDiff,
        losses: {
            tiltX: lossX,
            tiltZ: lossZ,
            total: 100 - clampedEfficiency
        }
    };
}

/**
 * Génère des données pour une démonstration prédéfinie
 * @param {string} demoType - Type de démonstration ('solsticeEte', 'solsticeHiver', etc.)
 * @param {Object} baseConfig - Configuration de base du système (optionnel)
 * @returns {Object} Configuration pour la démonstration
 */
function generateDemoConfig(demoType, baseConfig = {}) {
    // Configuration par défaut en utilisant directement l'attribut via rhuma()
    const config = {
        ...baseConfig,
        demoRunning: true,
        demoType: demoType,
        demoSpeed: rhuma('demoSpeed')
    };
    
    // Configurer selon le type de démonstration
    switch(demoType) {
        case 'solsticeEte':
            // 21 juin (jour 172)
            config.dayOfYear = 172;
            config.hour = 12; // Midi solaire
            config.tracking = true;
            break;
            
        case 'solsticeHiver':
            // 21 décembre (jour 355)
            config.dayOfYear = 355;
            config.hour = 12; // Midi solaire
            config.tracking = true;
            break;
            
        case 'equinoxe':
            // 21 mars (jour 80) ou 23 septembre (jour 266)
            config.dayOfYear = 80;
            config.hour = 12; // Midi solaire
            config.tracking = true;
            break;
            
        case 'journee':
            // Utiliser la date actuelle
            config.dayOfYear = getDayOfYear(new Date());
            config.hour = 6; // Commencer au lever du soleil
            config.demoSpeed = 2; // Plus rapide pour voir toute la journée
            config.tracking = true;
            break;
            
        case 'neige':
            // Simulation de charge de neige (panneau horizontal)
            config.dayOfYear = 355; // Hiver
            config.hour = 12;
            config.tracking = false;
            // Forcer une position horizontale pour le panneau
            config.cableSELength = 80;
            config.cableSWLength = 80;
            break;
            
        case 'vent':
            // Simulation de vent fort (panneau incliné au minimum)
            config.dayOfYear = 172; // Été
            config.hour = 12;
            config.tracking = false;
            // Forcer une position de protection contre le vent
            config.cableSELength = 30;
            config.cableSWLength = 30;
            break;
            
        case 'optimisation':
            // Démonstration d'optimisation énergétique
            config.dayOfYear = 172; // Été
            config.hour = 12;
            config.tracking = true;
            config.demoSpeed = 0.5; // Lent pour bien voir l'optimisation
            break;
    }
    
    return config;
}

// Exporter les fonctions pour utilisation dans d'autres modules
export {
    getSunPosition,
    getSunTimes,
    calculateEquationOfTime,
    solarTimeToLocalTime,
    localTimeToSolarTime,
    calculateOptimalPanelAngles,
    calculateCableLengths,
    calculateCableTension,
    calculatePanelEfficiency,
    generateDemoConfig,
    getDayOfYear,
    formatTime,
    formatDuration
};