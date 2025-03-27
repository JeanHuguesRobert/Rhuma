# 🏅 Kudos - Système de Monnaie Complémentaire pour l'Autoconsommation Collective

## 🎯 Objectif

Le système Kudos est conçu pour faciliter les échanges d'énergie dans le cadre de l'autoconsommation collective tout en minimisant la charge fiscale. Il s'inspire de l'économie du don et du contre-don décrite par Marcel Mauss, permettant aux usagers de s'échanger de l'énergie sous forme de dons plutôt que de ventes.

## 📋 Principe

### 1. Mécanisme de Base

- Les usagers reçoivent des Kudos pour l'énergie qu'ils économisent ou produisent et partagent
- Les Kudos peuvent être utilisés pour recevoir de l'énergie d'autres producteurs
- Les échanges de Kudos sont considérés comme des dons, non soumis à la TVA

### 2. Fonctionnalités Uniques

#### Échanges Publics et Nominatifs

- **Transparence** : Tous les échanges sont publics et visibles par la communauté
- **Nominativité** : Les Kudos sont liés à l'identité de chaque usager
- **Réputation** : Système de notation mutuelle entre usagers

#### Types d'Échanges

- **Production d'énergie** : Les producteurs reçoivent des Kudos pour leur production, y compris quand il s'agit d'effacement, c'est à dire d'économies d'énergie
- **Consommation d'énergie** : Les consommateurs peuvent recevoir des Kudos selon leur réputation, laquelle se mesure en Kudos
- **Échanges avec la distillerie** : La distillerie solaire participe au système
- **Échanges entre usagers** : Possibilité d'échanger entre particuliers possédant des panneaux solaires par exemple, sur la base de dons libres

### 3. Gestion de la Réputation

- **Notation mutuelle** : Les usagers peuvent noter leurs pairs après chaque échange, le montant de Kudos donnés indique la note
- **Score de réputation** : Impact sur la capacité à recevoir des Kudos. Les acteurs dotés d'une bonne réputation vont naturellement attirer des dons, tant qu'ils maintiennent leur bonne réputation
- **Historique public** : Tous les échanges et notations sont visibles
- **Modération communautaire** : Possibilité de signaler des comportements inappropriés, avec des blâmes, qui sont des anti-bon-point et donc anti-dons et donc des anti-Kudos !

### 4. Fonctionnalités

#### Création et Attribution

- **Attribution automatique** : Les Kudos sont attribués automatiquement en fonction de la production d'énergie et de la redistribution périodique d'une cagnotte alimentée par des dons
- **Attribution manuelle** : Les usagers peuvent recevoir des Kudos selon leur réputation, par exemple à l'occasion de contributions à la communauté des usagers considéré comme bénéfiques
- **Valeur des Kudos** : 1 Kudo = 1 kWh d'énergie, approximativement. A noter : toutes les formes d'énergie ne se valent pas et l'énergie sous forme d'électricité à plus de valeur que l'énergie sous forme de chaleur. Quand à l'énergie sous forme de rhum, c'est valeur "premium" ;)
- **Plafond** : Plafond mensuel d'attribution de Kudos (défaut : 5000 Kudos)

#### Utilisation

- **Échange d'énergie** : Les usagers peuvent utiliser leurs Kudos pour recevoir de l'énergie d'autres producteurs
- **Valeur d'échange** : 1 Kudo = 1 kWh d'énergie reçue
- **Expiration** : Les Kudos expirent après 12 mois pour encourager les échanges réguliers, comme pour les monnaies dites "fondantes".

#### Gestion des Comptes

- **Solde Kudos** : Suivi du solde Kudos de chaque usager
- **Historique des échanges** : Conservation de l'historique des échanges de Kudos
- **Score de réputation** : Suivi de la réputation de chaque usager
- **Rapports mensuels** : Génération de rapports sur l'activité Kudos

## 📊 Avantages

### Fiscal

- **Exemption TVA** : Les échanges de Kudos sont considérés comme des dons, non soumis à la TVA
- **Réduction de la charge fiscale** : Les usagers peuvent échanger de l'énergie sans payer de TVA sur une partie des échanges
- **Incertitude sur la réciprocité** : Les échanges sont considérés comme des dons en raison de l'incertitude sur la réciprocité

### Communautaire

- **Soutien mutuel** : Encouragement à l'entraide et au partage au sein de la communauté
- **Inclusion** : Accès à l'énergie pour les usagers qui ne peuvent pas investir dans des panneaux solaires
- **Sensibilisation** : Promotion de la production d'énergie renouvelable
- **Réputation** : Système de notation mutuelle pour encourager les bonnes pratiques

## 📋 Configuration

### Variables d'Environnement

- `KUDOS_PLAFOND_MENSUEL` : Plafond mensuel d'attribution de Kudos (défaut : 5000 Kudos)
- `KUDOS_VALEUR` : Valeur d'un Kudo en kWh (défaut : 1 kWh)
- `KUDOS_EXPIRATION` : Durée de validité des Kudos en mois (défaut : 12 mois)
- `KUDOS_NOTATION_MIN` : Note minimale pour recevoir des Kudos (défaut : 3/5)

### Paramètres de Simulation

- **Attribution**
  - Pourcentage de production converti en Kudos (défaut : 100%)
  - Plafond mensuel d'attribution
  - Période d'attribution (mensuelle)

- **Utilisation**
  - Pourcentage maximum de Kudos utilisables par mois
  - Durée de validité des Kudos
  - Frais de transaction (défaut : 0%)

- **Réputation**
  - Poids de la réputation dans l'attribution des Kudos
  - Nombre minimum de notations pour valider un score
  - Période de conservation des notations

## 📊 Métriques

### Échanges

- Nombre total de Kudos émis
- Nombre total de Kudos utilisés
- Taux d'utilisation des Kudos
- Montant d'énergie échangée via Kudos

### Impact Fiscal

- Économies de TVA réalisées
- Montant d'énergie échangée sans TVA
- Répartition des échanges entre usagers
- Impact sur la consommation d'énergie

### Réputation

- Distribution des scores de réputation
- Évolution des scores au fil du temps
- Corrélation entre réputation et échanges
- Impact de la réputation sur l'attribution des Kudos

## 🔄 Maintenance

### Logs

- Création et attribution de Kudos
- Utilisation des Kudos
- Échanges d'énergie via Kudos
- Notations et scores de réputation
- Erreurs et exceptions

### Sauvegarde

- Historique des transactions
- Solde des comptes Kudos
- Scores de réputation
- Rapports mensuels

## 📈 Monitoring

### Métriques

- Volume d'échanges Kudos
- Répartition des Kudos par usager
- Évolution des échanges
- Impact sur la consommation d'énergie
- Évolution des scores de réputation

## 📋 Exemple d'Utilisation

```
# Exemple de configuration
KUDOS_PLAFOND_MENSUEL=5000
KUDOS_VALEUR=1
KUDOS_EXPIRATION=12
KUDOS_NOTATION_MIN=3

# Exemple d'échange
- Producteur A produit 500 kWh
- Reçoit 500 Kudos (limite du plafond mensuel)
- Consommateur B utilise 200 Kudos pour recevoir 200 kWh
- Échange considéré comme un don, non soumis à la TVA
- Consommateur B note Producteur A (4/5)
- Producteur A note Consommateur B (5/5)
