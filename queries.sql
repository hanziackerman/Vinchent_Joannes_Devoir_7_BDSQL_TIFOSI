USE tifosi;

-- 1. Afficher la liste des noms des focaccias par ordre alphabétique croissant
-- But : Obtenir une liste triée de toutes les focaccias
SELECT nom 
FROM focaccia 
ORDER BY nom ASC;

-- 2. Afficher le nombre total d'ingrédients
-- But : Compter le nombre total d'ingrédients disponibles
SELECT COUNT(*) as nombre_ingredients 
FROM ingredient;

-- 3. Afficher le prix moyen des focaccias
-- But : Calculer le prix moyen de toutes les focaccias
SELECT ROUND(AVG(prix), 2) as prix_moyen 
FROM focaccia;

-- 4. Afficher la liste des boissons avec leur marque, triée par nom de boisson
-- But : Obtenir la liste des boissons avec leurs marques respectives
SELECT b.nom as boisson, m.nom as marque 
FROM boisson b 
JOIN marque m ON b.id_marque = m.id_marque 
ORDER BY b.nom;

-- 5. Afficher la liste des ingrédients pour une Raclaccia
-- But : Obtenir tous les ingrédients utilisés dans la Raclaccia
SELECT i.nom as ingredient 
FROM ingredient i 
JOIN comprend c ON i.id_ingredient = c.id_ingredient 
JOIN focaccia f ON c.id_focaccia = f.id_focaccia 
WHERE f.nom = 'Raclaccia';

-- 6. Afficher le nom et le nombre d'ingrédients pour chaque foccacia
-- But : Compter le nombre d'ingrédients par focaccia
SELECT f.nom, COUNT(c.id_ingredient) as nombre_ingredients 
FROM focaccia f 
LEFT JOIN comprend c ON f.id_focaccia = c.id_focaccia 
GROUP BY f.nom;

-- 7. Afficher le nom de la focaccia qui a le plus d'ingrédients
-- But : Identifier la focaccia avec le plus grand nombre d'ingrédients
SELECT f.nom, COUNT(c.id_ingredient) as nombre_ingredients 
FROM focaccia f 
JOIN comprend c ON f.id_focaccia = c.id_focaccia 
GROUP BY f.nom 
ORDER BY nombre_ingredients DESC 
LIMIT 1;

-- 8. Afficher la liste des focaccia qui contiennent de l'ail
-- But : Trouver toutes les focaccias contenant de l'ail
SELECT DISTINCT f.nom 
FROM focaccia f 
JOIN comprend c ON f.id_focaccia = c.id_focaccia 
JOIN ingredient i ON c.id_ingredient = i.id_ingredient 
WHERE i.nom LIKE '%ail%';

-- 9. Afficher la liste des ingrédients inutilisés
-- But : Identifier les ingrédients qui ne sont utilisés dans aucune focaccia
SELECT i.nom 
FROM ingredient i 
LEFT JOIN comprend c ON i.id_ingredient = c.id_ingredient 
WHERE c.id_focaccia IS NULL;

-- 10. Afficher la liste des focaccia qui n'ont pas de champignons
-- But : Trouver les focaccias ne contenant pas de champignons
SELECT f.nom 
FROM focaccia f 
WHERE f.id_focaccia NOT IN (
    SELECT DISTINCT c.id_focaccia 
    FROM comprend c 
    JOIN ingredient i ON c.id_ingredient = i.id_ingredient 
    WHERE i.nom LIKE '%champignon%'
); 