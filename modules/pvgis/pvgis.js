const axios = require('axios');
const commander = require('commander');

// Configuration de base
const BASE_URL = 'https://re.jrc.ec.europa.eu/api';
const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';
const TIMEOUT = 30000;

// Erreur personnalisée
function PVError(message, statusCode) {
    this.name = 'PVError';
    this.message = message;
    this.statusCode = statusCode;
}
PVError.prototype = Object.create(Error.prototype);
PVError.prototype.constructor = PVError;

// Client PVGIS
class PVGISClient {
    constructor() {
        this.client = axios.create({
            baseURL: BASE_URL,
            timeout: TIMEOUT
        });
    }

    async getPVData(system) {
        try {
            const params = {
                lat: system.latitude,
                lon: system.longitude,
                peakpower: system.peakPower,
                loss: system.losses,
                outputformat: 'json'
            };

            if (system.isTracking) {
                params.trackingtype = 1;
                params.angle = system.angle;
                params.aspect = system.aspect;
            } else {
                params.optimalinclination = system.useOptimalAngle ? 1 : 0;
                params.angle = system.angle;
                params.aspect = system.aspect;
            }

            const response = await this.client.get('/PVcalc', { params });

            if (response.status >= 400) {
                throw new PVError(
                    `Erreur API PVGIS (${response.status}): ${response.statusText}`,
                    response.status
                );
            }

            return this.parsePVResult(response.data);
        } catch (error) {
            if (error instanceof PVError) {
                throw error;
            }
            throw new PVError(`Erreur de communication avec PVGIS: ${error.message}`);
        }
    }

    async getMonthlyRadiation(latitude, longitude) {
        try {
            const response = await this.client.get('/MRcalc', {
                params: {
                    lat: latitude,
                    lon: longitude,
                    outputformat: 'json'
                }
            });

            if (response.status >= 400) {
                throw new PVError(
                    `Erreur API PVGIS (${response.status}): ${response.statusText}`,
                    response.status
                );
            }

            return response.data;
        } catch (error) {
            if (error instanceof PVError) {
                throw error;
            }
            throw new PVError(`Erreur de communication avec PVGIS: ${error.message}`);
        }
    }

    parsePVResult(data) {
        const monthlyProduction = {};
        if (data.outputs?.monthly) {
            Object.entries(data.outputs.monthly).forEach(([month, value]) => {
                monthlyProduction[month] = value.E_m;
            });
        }

        return {
            monthlyProduction,
            annualProduction: data.outputs?.totals?.fixed?.E_y || 0,
            optimalAngle: data.outputs?.optimalangles?.angle
        };
    }
}

// Géocodage
class Geocoder {
    static async getCoordinates(address) {
        try {
            const params = {
                q: address,
                format: 'json',
                limit: 1
            };

            const response = await axios.get(NOMINATIM_URL, { params });

            if (response.status >= 400) {
                throw new PVError(
                    `Erreur API Nominatim (${response.status}): ${response.statusText}`,
                    response.status
                );
            }

            const results = response.data;
            if (!results || results.length === 0) {
                throw new PVError('Aucun résultat trouvé pour cette adresse');
            }

            const result = results[0];
            return {
                latitude: parseFloat(result.lat),
                longitude: parseFloat(result.lon),
                display_name: result.display_name
            };
        } catch (error) {
            if (error instanceof PVError) {
                throw error;
            }
            throw new PVError(`Erreur de géocodage: ${error.message}`);
        }
    }
}

// Formattage des sorties
function formatOutput(data, format) {
    switch (format) {
        case 'json':
            return JSON.stringify(data, null, 2);
        case 'env':
            return Object.entries(data)
                .map(([key, value]) => `PV_${key.toUpperCase()}=${value}`)
                .join('\n');
        default:
            return data;
    }
}

// CLI
class PVGISCLI {
    constructor() {
        this.client = new PVGISClient();
        this.program = new commander.Command();
        this.setupCommands();
    }

    setupCommands() {
        this.program
            .name('pvgis')
            .description('Client CLI pour l\'API PVGIS')
            .version('1.0.0')
            .option('-f, --format <format>', 'Format de sortie (json|env|text)', 'text');

        this.program
            .command('pv <latitude> <longitude> [options]')
            .description('Obtenir les données PV pour un système')
            .option('-p, --peak-power <number>', 'Puissance crête (kWc)', 1.0)
            .option('-l, --losses <number>', 'Pertes (%)', 14.0)
            .option('-a, --angle <number>', 'Angle d\'inclinaison', 30.0)
            .option('--aspect <number>', 'Orientation (0=sud)', 0.0)
            .option('--tracking', 'Utiliser le suivi de soleil')
            .option('--optimal', 'Utiliser l\'angle optimal')
            .action(async (latitude, longitude, options) => {
                try {
                    const system = {
                        latitude: parseFloat(latitude),
                        longitude: parseFloat(longitude),
                        peakPower: parseFloat(options.peakPower),
                        losses: parseFloat(options.losses),
                        angle: parseFloat(options.angle),
                        aspect: parseFloat(options.aspect),
                        isTracking: options.tracking,
                        useOptimalAngle: options.optimal
                    };

                    const result = await this.client.getPVData(system);
                    console.log(formatOutput(result, options.format));
                } catch (error) {
                    console.error(error.message);
                    process.exit(1);
                }
            });

        this.program
            .command('radiation <latitude> <longitude>')
            .description('Obtenir les données de rayonnement mensuel')
            .action(async (latitude, longitude, options) => {
                try {
                    const result = await this.client.getMonthlyRadiation(
                        parseFloat(latitude),
                        parseFloat(longitude)
                    );
                    console.log(formatOutput(result, options.format));
                } catch (error) {
                    console.error(error.message);
                    process.exit(1);
                }
            });

        this.program
            .command('geocode <address>')
            .description('Obtenir les coordonnées à partir d\'une adresse')
            .action(async (address, options) => {
                try {
                    const result = await Geocoder.getCoordinates(address);
                    console.log(formatOutput(result, options.format));
                } catch (error) {
                    console.error(error.message);
                    process.exit(1);
                }
            });
    }

    run() {
        this.program.parse(process.argv);
    }
}

// Export
module.exports = {
    PVError,
    PVGISClient,
    PVGISCLI,
    Geocoder
};

// Exécution directe
if (require.main === module) {
    const cli = new PVGISCLI();
    cli.run();
}
