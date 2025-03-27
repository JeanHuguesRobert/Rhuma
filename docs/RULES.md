# Règles de Développement

## Structure des Modules

1. **Principe de Simplicité**
   - Éviter la création d'entités au-delà du nécessaire
   - Ne pas créer de sous-répertoires sauf si absolument nécessaire
   - Préférer une structure plate et simple

2. **Organisation des Modules**
   - Chaque module doit être le plus autonome possible
   - Les dépendances externes doivent être minimales
   - L'interface avec le reste du système doit être claire et limitée

3. **Implémentation**
   - Choisir l'implémentation la plus simple qui fonctionne
   - Éviter la sur-ingénierie
   - Privilégier la maintenabilité et la lisibilité du code

4. **Langage et Typage**
   - Préférer JavaScript simple à TypeScript
   - Éviter le typage fort sauf si absolument nécessaire
   - Maintenir le code le plus simple possible

5. **Nomenclature des Fichiers**
   - Éviter les noms génériques comme `index.js` sauf si absolument nécessaire
   - Préférer des noms descriptifs qui reflètent la fonction du fichier
   - Utiliser le nom du répertoire ou un préfixe spécifique pour les fichiers principaux
   - Pour les fichiers `index`, utiliser un suffixe descriptif (ex: `index_pvgis.js`)
