const axios = require('axios');
const commander = require('commander');
const jsPDF = require('jspdf');
const { JSDOM } = require('jsdom');

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
                outputformat: 'json',
                raddatabase: 'PVGIS-SARAH',
                mountingplace: 'free',
                angle: system.angle,
                aspect: system.aspect,
                components: 1,
                usehorizon: 1,
                optimalangles: 1,
                optimalinclination: 1
            };

            if (system.isTracking) {
                params.trackingtype = 1;
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

            return this.processResults(response.data);
        } catch (error) {
            throw error;
        }
    }

    processResults(data) {
        return {
            monthly_production: data.outputs.pv.monthly,
            annual_production: data.outputs.pv.year,
            optimal_angle: this.calculateOptimalAngle(data.inputs.lat),
            financial_analysis: this.calculateFinancialAnalysis(data),
            comparison: this.generateComparison(data)
        };
    }

    calculateOptimalAngle(latitude) {
        // Formule simplifiée pour l'angle optimal
        return Math.round(latitude * 0.9 + 2.3);
    }

    calculateFinancialAnalysis(data) {
        const annualProduction = data.outputs.pv.year;
        const systemCost = this.calculateSystemCost(data.inputs.peakpower);
        const maintenanceCost = this.calculateMaintenanceCost(data.inputs.peakpower);
        const revenue = this.calculateRevenue(annualProduction);
        
        return {
            system_cost: systemCost,
            maintenance_cost: maintenanceCost,
            revenue: revenue,
            roi: this.calculateROI(systemCost, revenue),
            payback_period: this.calculatePaybackPeriod(systemCost, revenue)
        };
    }

    calculateSystemCost(peakPower) {
        // Prix moyen par kWc (2025) - à ajuster selon la région
        return peakPower * 1500; // €/kWc
    }

    calculateMaintenanceCost(peakPower) {
        // Coût annuel de maintenance - 1% du coût du système
        return this.calculateSystemCost(peakPower) * 0.01;
    }

    calculateRevenue(annualProduction) {
        // Prix moyen de l'électricité - à ajuster selon le tarif
        return annualProduction * 0.12; // €/kWh
    }

    calculateROI(systemCost, annualRevenue) {
        return (annualRevenue / systemCost) * 100;
    }

    calculatePaybackPeriod(systemCost, annualRevenue) {
        return systemCost / annualRevenue;
    }

    generateComparison(data) {
        const fixedData = this.getFixedSystemData(data);
        const trackingData = this.getTrackingSystemData(data);
        
        return {
            fixed: fixedData,
            tracking: trackingData,
            gain_percentage: this.calculateGainPercentage(fixedData, trackingData)
        };
    }

    getFixedSystemData(data) {
        return {
            production: data.outputs.pv.year,
            cost: this.calculateSystemCost(data.inputs.peakpower),
            roi: this.calculateROI(
                this.calculateSystemCost(data.inputs.peakpower),
                this.calculateRevenue(data.outputs.pv.year)
            )
        };
    }

    getTrackingSystemData(data) {
        // Simulation avec tracking
        const trackingFactor = 1.3; // Facteur moyen de gain avec tracking
        const trackingProduction = data.outputs.pv.year * trackingFactor;
        
        return {
            production: trackingProduction,
            cost: this.calculateSystemCost(data.inputs.peakpower) * 1.2, // Coût +20% avec tracking
            roi: this.calculateROI(
                this.calculateSystemCost(data.inputs.peakpower) * 1.2,
                this.calculateRevenue(trackingProduction)
            )
        };
    }

    calculateGainPercentage(fixed, tracking) {
        return ((tracking.production - fixed.production) / fixed.production) * 100;
    }

    async generateReport(data) {
        const doc = new jsPDF();
        
        // Ajouter les données du rapport
        doc.text("Analyse PVGIS - Rapport d'Optimisation", 10, 10);
        
        // Ajouter les graphiques
        await this.addChartsToPDF(doc, data);
        
        // Ajouter l'analyse financière
        await this.addFinancialAnalysis(doc, data);
        
        // Sauvegarder le PDF
        const pdfBuffer = doc.output('arraybuffer');
        return Buffer.from(pdfBuffer);
    }

    async addChartsToPDF(doc, data) {
        // Créer un graphique de production mensuelle
        const chart = await this.createMonthlyProductionChart(data);
        doc.addImage(chart, 'PNG', 15, 40, 180, 90);
    }

    async createMonthlyProductionChart(data) {
        // À implémenter avec une bibliothèque de graphiques
        return Promise.resolve('chart.png');
    }

    async addFinancialAnalysis(doc, data) {
        // Ajouter un tableau d'analyse financière
        const table = await this.createFinancialTable(data);
        doc.addImage(table, 'PNG', 15, 140, 180, 90);
    }

    async createFinancialTable(data) {
        // À implémenter avec une bibliothèque de tableaux
        return Promise.resolve('table.png');
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
