# Base de données Tifosi

Ce projet contient les scripts nécessaires pour créer et alimenter la base de données du restaurant Tifosi, spécialisé dans la Street-Food italienne.

## Structure du projet

```
.
├── fichiers-à-joindre-au-devoir/
│   ├── boisson.xlsx
│   ├── focaccia.xlsx
│   ├── ingredient.xlsx
│   └── marque.xlsx
├── schema.sql
├── data.sql
├── queries.sql
├── import_data.py
└── README.md
```

## Prérequis

- MySQL Server
- Python 3.x
- Bibliothèques Python requises :
  - pandas
  - openpyxl

## Installation des dépendances Python

```bash
pip install pandas openpyxl
```

## Instructions d'utilisation

1. Créer la base de données et les tables :
```bash
mysql -u root -p < schema.sql
```

2. Générer le fichier d'insertion des données :
```bash
python import_data.py
```

3. Insérer les données dans la base :
```bash
mysql -u root -p < data.sql
```

4. Exécuter les requêtes de test :
```bash
mysql -u root -p < queries.sql
```

## Description des fichiers

- `schema.sql` : Script de création de la base de données et des tables
- `import_data.py` : Script Python pour convertir les fichiers Excel en instructions SQL
- `data.sql` : Script généré contenant les données à insérer (généré par import_data.py)
- `queries.sql` : Script contenant les requêtes de test

## Structure de la base de données

La base de données contient les tables suivantes :

- `marque` : Marques des boissons
- `boisson` : Boissons disponibles
- `ingredient` : Ingrédients utilisés dans les focaccias
- `focaccia` : Focaccias disponibles
- `menu` : Menus proposés
- `client` : Informations des clients
- `comprend` : Relations entre focaccias et ingrédients
- `est_constitue` : Relations entre menus et focaccias
- `contient` : Relations entre menus et boissons
- `achete` : Historique des achats

## Sécurité

- Un utilisateur dédié 'tifosi' est créé avec les droits nécessaires
- Les mots de passe sont stockés de manière sécurisée
- Les contraintes d'intégrité sont appliquées sur toutes les tables

## Maintenance

Pour mettre à jour les données :
1. Modifier les fichiers Excel dans le dossier `fichiers-à-joindre-au-devoir/`
2. Exécuter à nouveau le script Python et le script SQL généré 