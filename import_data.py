import pandas as pd
import os
import unicodedata
import re

def normalize_string(s):
    """Normalise une chaîne de caractères (supprime les accents, met en minuscules)"""
    if pd.isna(s):
        return ''
    # Convertit en minuscules et supprime les accents
    s = unicodedata.normalize('NFKD', str(s)).encode('ASCII', 'ignore').decode('ASCII')
    return s.lower().strip()

def clean_string(s):
    if pd.isna(s):
        return ''
    return str(s).replace("'", "''")

def parse_ingredients(ingredients_str):
    """Parse la chaîne d'ingrédients et retourne une liste de tuples (ingrédient, quantité)"""
    if pd.isna(ingredients_str):
        return []
    
    # Dictionnaire des quantités par défaut (en grammes)
    default_quantities = {
        'ail': 2,
        'ananas': 40,
        'artichaut': 20,
        'bacon': 80,
        'base tomate': 200,
        'base creme': 200,
        'champignon': 40,
        'chevre': 50,
        'cresson': 20,
        'emmental': 50,
        'gorgonzola': 50,
        'jambon cuit': 80,
        'jambon fume': 80,
        'mozarella': 50,
        'oignon': 20,
        'olive noire': 20,
        'olive verte': 20,
        'parmesan': 50,
        'piment': 2,
        'poivre': 1,
        'pomme de terre': 80,
        'raclette': 50,
        'salami': 80,
        'tomate cerise': 40,
        'oeuf': 50
    }
    
    # Dictionnaire des corrections de noms d'ingrédients
    ingredient_corrections = {
        'chèvre': 'Chevre',
        'œuf': 'Oeuf',
        'base crème': 'Base crème'
    }
    
    # Extraire la première ligne qui contient les ingrédients
    lines = ingredients_str.split('\n')
    ingredients_line = None
    for line in lines:
        # Ignorer les lignes vides ou qui commencent par des caractères spéciaux
        if not line.strip() or line.strip().startswith(('-', '*', '•', 'Sauf', 'Les quantités')):
            continue
        # Ignorer les lignes qui contiennent " : " car ce sont les quantités par défaut
        if ' : ' in line:
            continue
        ingredients_line = line.strip()
        break
    
    if not ingredients_line:
        return []
    
    result = []
    # Séparer les ingrédients
    ingredients = [ing.strip() for ing in ingredients_line.split(',')]
    
    for ing in ingredients:
        # Ignorer les entrées vides
        if not ing:
            continue
            
        # Vérifier s'il y a une quantité spécifiée entre parenthèses
        match = re.match(r'(.*?)(?:\s*\((\d+)\))?$', ing.strip())
        if match:
            ingredient_name = match.group(1).strip()
            quantity = match.group(2)
            
            # Appliquer les corrections de noms si nécessaire
            ingredient_name = ingredient_corrections.get(ingredient_name, ingredient_name)
            
            # Si pas de quantité spécifiée, utiliser la quantité par défaut
            if not quantity:
                normalized_name = normalize_string(ingredient_name)
                quantity = default_quantities.get(normalized_name, 1)
            else:
                quantity = int(quantity)
                
            result.append((ingredient_name, quantity))
            
    return result

def print_excel_info(df, filename):
    print(f"\nStructure du fichier {filename}:")
    print("Colonnes:", df.columns.tolist())
    print("Premières lignes:")
    print(df.head())
    print("-" * 50)

def create_ingredients_mapping(df_ingredient):
    """Crée un dictionnaire de correspondance pour les ingrédients"""
    mapping = {}
    for _, row in df_ingredient.iterrows():
        nom = row['nom_ingredient']
        normalized = normalize_string(nom)
        # Ajouter la version normalisée
        mapping[normalized] = nom
        # Ajouter la version originale
        mapping[normalize_string(nom)] = nom
        
        # Ajouter des variantes courantes
        if normalized == 'base tomate':
            mapping['base tomate'] = nom
        elif normalized == 'base creme':
            mapping['base creme'] = nom
            mapping['base crème'] = nom
        elif normalized == 'jambon fume':
            mapping['jambon fume'] = nom
            mapping['jambon fumé'] = nom
        elif normalized == 'oeuf':
            mapping['oeuf'] = nom
            mapping['œuf'] = nom
            mapping['uf'] = nom
        elif normalized == 'chevre':
            mapping['chevre'] = nom
            mapping['chèvre'] = nom
            mapping['Chèvre'] = nom
        
        # Ajouter la version avec la première lettre en majuscule
        mapping[normalized.capitalize()] = nom
        
        # Ajouter la version tout en majuscules
        mapping[normalized.upper()] = nom
        
    return mapping

def generate_sql_inserts():
    # Chemin vers le dossier contenant les fichiers Excel
    excel_dir = 'fichiers-à-joindre-au-devoir'
    
    # Fichier de sortie SQL
    with open('data.sql', 'w', encoding='utf-8') as sql_file:
        sql_file.write('USE tifosi;\n\n')
        
        try:
            # Marque
            print("\nLecture du fichier marque.xlsx...")
            df_marque = pd.read_excel(os.path.join(excel_dir, 'marque.xlsx'))
            print_excel_info(df_marque, 'marque.xlsx')
            sql_file.write('-- Insertion des marques\n')
            for _, row in df_marque.iterrows():
                try:
                    sql_file.write(f"INSERT INTO marque (nom) VALUES ('{clean_string(row['nom_marque'])}');\n")
                except KeyError as e:
                    print(f"Erreur: Colonne manquante dans marque.xlsx: {e}")
                    print("Colonnes disponibles:", df_marque.columns.tolist())
                    return
            sql_file.write('\n')
            
            # Boisson
            print("\nLecture du fichier boisson.xlsx...")
            df_boisson = pd.read_excel(os.path.join(excel_dir, 'boisson.xlsx'))
            print_excel_info(df_boisson, 'boisson.xlsx')
            sql_file.write('-- Insertion des boissons\n')
            for _, row in df_boisson.iterrows():
                try:
                    marque_nom = clean_string(row['marque'])
                    sql_file.write(f"INSERT INTO boisson (nom, id_marque) VALUES ('{clean_string(row['nom_boisson'])}', "
                                f"(SELECT id_marque FROM marque WHERE nom = '{marque_nom}'));\n")
                except KeyError as e:
                    print(f"Erreur: Colonne manquante dans boisson.xlsx: {e}")
                    print("Colonnes disponibles:", df_boisson.columns.tolist())
                    return
            sql_file.write('\n')
            
            # Ingredient
            print("\nLecture du fichier ingredient.xlsx...")
            df_ingredient = pd.read_excel(os.path.join(excel_dir, 'ingredient.xlsx'))
            print_excel_info(df_ingredient, 'ingredient.xlsx')
            
            # Créer le mapping des ingrédients
            ingredients_mapping = create_ingredients_mapping(df_ingredient)
            print("\nListe des ingrédients normalisés disponibles:")
            for norm, orig in sorted(ingredients_mapping.items()):
                print(f"'{norm}' -> '{orig}'")
            
            sql_file.write('-- Insertion des ingrédients\n')
            for _, row in df_ingredient.iterrows():
                try:
                    sql_file.write(f"INSERT INTO ingredient (nom) VALUES ('{clean_string(row['nom_ingredient'])}');\n")
                except KeyError as e:
                    print(f"Erreur: Colonne manquante dans ingredient.xlsx: {e}")
                    print("Colonnes disponibles:", df_ingredient.columns.tolist())
                    return
            sql_file.write('\n')
            
            # Focaccia
            print("\nLecture du fichier focaccia.xlsx...")
            df_focaccia = pd.read_excel(os.path.join(excel_dir, 'focaccia.xlsx'))
            print_excel_info(df_focaccia, 'focaccia.xlsx')
            sql_file.write('-- Insertion des focaccias\n')
            
            # Créer un dictionnaire des focaccias uniques
            focaccias_uniques = {}
            for _, row in df_focaccia.iterrows():
                try:
                    # Ignorer les lignes sans nom de focaccia ou sans prix
                    if pd.isna(row['nom_focaccia']) or pd.isna(row['prix']):
                        continue
                        
                    nom = clean_string(row['nom_focaccia'])
                    # Ignorer les lignes avec des noms vides ou qui sont des instructions
                    if not nom or nom.startswith(('-', '*', '•', 'Sauf', 'Les')):
                        continue
                        
                    if nom not in focaccias_uniques:
                        focaccias_uniques[nom] = row['prix']
                        sql_file.write(f"INSERT INTO focaccia (nom, prix) VALUES ('{nom}', {row['prix']});\n")
                except KeyError as e:
                    print(f"Erreur: Colonne manquante dans focaccia.xlsx: {e}")
                    print("Colonnes disponibles:", df_focaccia.columns.tolist())
                    return
            sql_file.write('\n')
            
            # Relations Focaccia-Ingredient (comprend)
            sql_file.write('-- Insertion des relations focaccia-ingredient\n')
            missing_ingredients = set()
            
            for _, row in df_focaccia.iterrows():
                try:
                    # Ignorer les lignes sans nom de focaccia ou sans prix
                    if pd.isna(row['nom_focaccia']) or pd.isna(row['prix']):
                        continue
                        
                    nom_focaccia = clean_string(row['nom_focaccia'])
                    # Ignorer les lignes avec des noms vides ou qui sont des instructions
                    if not nom_focaccia or nom_focaccia.startswith(('-', '*', '•', 'Sauf', 'Les')):
                        continue
                        
                    ingredients_list = parse_ingredients(row['ingrédients'])
                    
                    if ingredients_list:  # Ne pas afficher les focaccias sans ingrédients
                        print(f"\nIngrédients pour {nom_focaccia}:")
                        for ingredient, quantite in ingredients_list:
                            print(f"- {ingredient} ({quantite}g)")
                            ingredient_normalized = normalize_string(ingredient)
                            
                            # Vérifier si l'ingrédient existe dans notre mapping
                            if ingredient_normalized in ingredients_mapping:
                                ingredient_original = clean_string(ingredients_mapping[ingredient_normalized])
                                sql_file.write(f"INSERT INTO comprend (id_focaccia, id_ingredient, quantite) "
                                            f"SELECT f.id_focaccia, i.id_ingredient, {quantite} "
                                            f"FROM focaccia f, ingredient i "
                                            f"WHERE f.nom = '{nom_focaccia}' "
                                            f"AND i.nom = '{ingredient_original}';\n")
                            else:
                                print(f"Ingrédient non trouvé: '{ingredient}' (normalisé: '{ingredient_normalized}')")
                                missing_ingredients.add(ingredient)
                            
                except KeyError as e:
                    print(f"Erreur: Colonne manquante dans focaccia.xlsx pour les relations: {e}")
                    print("Colonnes disponibles:", df_focaccia.columns.tolist())
                    return
            
            if missing_ingredients:
                print("\nATTENTION: Les ingrédients suivants n'ont pas été trouvés dans la table ingredient:")
                for ing in sorted(missing_ingredients):
                    print(f"- {ing}")
                    
        except FileNotFoundError as e:
            print(f"Erreur: Fichier non trouvé: {e}")
        except Exception as e:
            print(f"Erreur inattendue: {e}")

if __name__ == "__main__":
    generate_sql_inserts() 