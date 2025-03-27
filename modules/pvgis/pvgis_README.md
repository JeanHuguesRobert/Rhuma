# PVGIS Client

Client JavaScript pour l'API PVGIS (Photovoltaic Geographical Information System) avec interface CLI.


## Installation

```bash
npm install @acorsica/pvgis
```


## Utilisation


### Géocodage
Obtenir les coordonnées à partir d'une adresse :

```bash
# Format texte (par défaut)
pvgis geocode "Paris, France"

# Format JSON
pvgis geocode "Paris, France" -f json

# Format .env
pvgis geocode "Paris, France" -f env
```


### Simulation PV
Obtenir les données de production PV pour un système :

```bash
# Format texte (par défaut)
pvgis pv 45.0 8.0 -p 1.0 -l 14.0 -a 30.0

# Format JSON
pvgis pv 45.0 8.0 -p 1.0 -l 14.0 -a 30.0 -f json

# Format .env
pvgis pv 45.0 8.0 -p 1.0 -l 14.0 -a 30.0 -f env
```


### Rayonnement Mensuel
Obtenir les données de rayonnement mensuel :

```bash
# Format texte (par défaut)
pvgis radiation 45.0 8.0

# Format JSON
pvgis radiation 45.0 8.0 -f json

# Format .env
pvgis radiation 45.0 8.0 -f env
```


## Options Communes

- `-f, --format <format>` : Format de sortie (json|env|text)


## Formats de Sortie

- `json` : Format JSON indenté
- `env` : Format .env avec préfixe PV_ (ex: PV_LATITUDE=45.0)
- `text` : Format texte simple (par défaut)


## Paramètres de Simulation PV

- `-p, --peak-power <number>` : Puissance crête (kWc)
- `-l, --losses <number>` : Pertes (%)
- `-a, --angle <number>` : Angle d'inclinaison
- `--aspect <number>` : Orientation (0=sud)
- `--tracking` : Utiliser le suivi de soleil
- `--optimal` : Utiliser l'angle optimal


## Implémentations Alternatives

Il existe d'autres implémentations de l'API PVGIS :

- [pvgispy](https://github.com/jannikobenhoff/pvgispy) (Python) : Interface complète avec support de tous les endpoints
- [PVGIS_API](https://github.com/fcfahl/PVGIS_API) (Python) : Interface pour données de points avec gestion des fuseaux horaires
- [pvgis-cli-py](https://github.com/jouniverse/pvgis-cli-py) (Python) : Interface CLI simple


## Publication

Ce module est maintenu par ACORSICA, l'association Corse Organisant la Réunion Sur Internet de Compétences Autonomes, ie C.O.R.S.I.C.A. ; créée à Corte fin 1995 par Jean Hugues Robert, actuel président (2025).

Pour l'installer :

```bash
npm install @acorsica/pvgis
```


## Développement

Pour contribuer au développement du module :

```bash
# Cloner le dépôt
# Installer les dépendances
npm install

# Lancer les tests
npm test

# Construire le package
npm run build
```


## Dépendances

- `axios` : Pour les appels API
- `commander` : Pour l'interface CLI


## Utilisateurs

- Rhuma (2025)
Projet de rhum solaire en Corse. Voir [Rhuma](https://github.com/JeanHuguesRobert/rhuma)
