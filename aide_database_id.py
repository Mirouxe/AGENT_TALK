"""
Script interactif pour vous aider à trouver le bon Database ID Notion
"""
import os
import re
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("🔍 ASSISTANT DE CONFIGURATION NOTION DATABASE ID")
print("="*70)
print()

print("📋 Problème actuel:")
print("   Vous avez fourni l'ID d'une PAGE au lieu d'une BASE DE DONNÉES")
print()
print("🎯 Ce que vous devez faire:")
print()
print("ÉTAPE 1: Créer ou ouvrir une BASE DE DONNÉES dans Notion")
print("-" * 70)
print()
print("Option A - Créer une NOUVELLE base de données (RECOMMANDÉ):")
print("   1. Dans Notion, créez une nouvelle page")
print("   2. Dans cette page, tapez: /database")
print("   3. Sélectionnez: 'Base de données - Vue tableau'")
print("   4. Une base apparaît avec des colonnes (Name, Tags, etc.)")
print()
print("Option B - Utiliser une base EXISTANTE:")
print("   1. Trouvez une base de données que vous avez déjà")
print("   2. Assurez-vous que c'est bien une base (vous voyez des colonnes)")
print()
print("⚠️  IMPORTANT: Une BASE DE DONNÉES ressemble à un TABLEAU")
print("   avec des colonnes et des lignes, PAS à une page de texte!")
print()

input("Appuyez sur Entrée quand vous avez une base de données prête...")
print()

print("ÉTAPE 2: Configurer les propriétés requises")
print("-" * 70)
print()
print("Votre base DOIT avoir ces 3 propriétés:")
print()
print("   1. Name (Type: Title) ✅ Déjà présent par défaut")
print("   2. Date (Type: Date)  ⚠️  À ajouter si absent")
print("      → Cliquez sur '+' → Choisir 'Date' → Nommer 'Date'")
print()
print("   3. Status (Type: Select) ⚠️  À ajouter si absent")
print("      → Cliquez sur '+' → Choisir 'Select' → Nommer 'Status'")
print("      → Ajouter l'option 'À classer' (Important!)")
print()

input("Appuyez sur Entrée quand les propriétés sont configurées...")
print()

print("ÉTAPE 3: PARTAGER avec votre intégration (NE PAS OUBLIER!)")
print("-" * 70)
print()
print("   1. En haut à droite de la BASE, cliquez sur 'Partager'")
print("   2. Dans le champ de recherche, tapez le nom de votre intégration")
print("   3. Cliquez dessus pour l'ajouter (elle aura une icône 🤖)")
print("   4. Elle devrait apparaître dans la liste des personnes ayant accès")
print()
print("⚠️  Si vous sautez cette étape, l'application ne pourra PAS écrire!")
print()

input("Appuyez sur Entrée quand l'intégration a accès...")
print()

print("ÉTAPE 4: Copier le lien de la BASE DE DONNÉES")
print("-" * 70)
print()
print("ATTENTION - Méthode CORRECTE pour obtenir l'ID:")
print()
print("   1. Cliquez sur le TITRE de la base de données")
print("      (La base s'ouvre en plein écran)")
print()
print("   2. Regardez l'URL dans votre navigateur:")
print("      Elle devrait ressembler à:")
print("      https://notion.so/workspace/[32-CARACTERES]?v=...")
print()
print("   3. Cliquez sur '⋯' (trois points) en haut à droite")
print()
print("   4. Sélectionnez 'Copier le lien'")
print()
print("   5. Collez le lien ci-dessous")
print()
print("❌ ERREUR COMMUNE: Ne copiez PAS le lien de la PAGE qui contient la base!")
print("✅ CORRECT: Copiez le lien de la BASE elle-même (elle est ouverte en plein écran)")
print()

url = input("Collez l'URL de votre base de données ici: ").strip()
print()

# Extraire l'ID de l'URL
database_id = None

# Nettoyer l'URL
url = url.replace('"', '').replace("'", '')

# Patterns possibles
patterns = [
    r'notion\.so/[^/]*/([a-f0-9]{32})',  # Format standard
    r'notion\.so/([a-f0-9]{32})',  # Format court
    r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})',  # Format avec tirets
]

for pattern in patterns:
    match = re.search(pattern, url)
    if match:
        database_id = match.group(1).replace('-', '')
        break

if not database_id:
    print("❌ Je n'ai pas pu extraire l'ID de cette URL")
    print("   Assurez-vous de copier l'URL complète depuis Notion")
    print()
    print("L'URL devrait ressembler à:")
    print("https://www.notion.so/workspace/1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d?v=...")
    print()
    exit(1)

print("✅ ID extrait:", database_id)
print()

# Vérifier avec l'API Notion
print("🔍 Vérification que c'est bien une base de données...")
print()

try:
    from notion_client import Client
    notion_key = os.getenv('NOTION_API_KEY')
    
    if not notion_key:
        print("❌ NOTION_API_KEY non trouvée dans .env")
        exit(1)
    
    notion = Client(auth=notion_key)
    database = notion.databases.retrieve(database_id)
    
    db_title = "Sans titre"
    if database.get('title') and len(database['title']) > 0:
        db_title = database['title'][0].get('plain_text', 'Sans titre')
    
    print(f"✅ C'EST UNE BASE DE DONNÉES!")
    print(f"   Nom: {db_title}")
    print()
    
    # Vérifier les propriétés
    properties = database.get('properties', {})
    print("📋 Propriétés trouvées:")
    
    has_name = 'Name' in properties and properties['Name']['type'] == 'title'
    has_date = 'Date' in properties and properties['Date']['type'] == 'date'
    has_status = 'Status' in properties and properties['Status']['type'] == 'select'
    
    print(f"   {'✅' if has_name else '❌'} Name (Title)")
    print(f"   {'✅' if has_date else '❌'} Date (Date)")
    print(f"   {'✅' if has_status else '❌'} Status (Select)")
    print()
    
    if not (has_name and has_date and has_status):
        print("⚠️  Il manque des propriétés!")
        print("   Retournez dans Notion et ajoutez les propriétés manquantes")
        print()
        exit(1)
    
    print("="*70)
    print("🎉 PARFAIT! Tout est correct!")
    print("="*70)
    print()
    print("✅ Mise à jour automatique de votre fichier .env...")
    
    # Mettre à jour le .env
    with open('.env', 'r') as f:
        content = f.read()
    
    # Remplacer l'ancien ID
    old_id = os.getenv('NOTION_DATABASE_ID', '')
    if old_id:
        content = content.replace(f'NOTION_DATABASE_ID="{old_id}"', f'NOTION_DATABASE_ID="{database_id}"')
        content = content.replace(f'NOTION_DATABASE_ID={old_id}', f'NOTION_DATABASE_ID="{database_id}"')
    else:
        # Ajouter si n'existe pas
        if 'NOTION_DATABASE_ID' not in content:
            content += f'\nNOTION_DATABASE_ID="{database_id}"\n'
    
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ Fichier .env mis à jour!")
    print()
    print("🚀 Maintenant, lancez le test complet:")
    print("   python test_pipeline.py")
    print()
    print("Si tous les tests passent, vous pouvez démarrer l'application:")
    print("   python app.py")
    print()
    
except Exception as e:
    error = str(e)
    print(f"❌ Erreur: {error}")
    print()
    
    if 'page' in error.lower() and 'not a database' in error.lower():
        print("⚠️  C'EST TOUJOURS UNE PAGE, PAS UNE BASE DE DONNÉES!")
        print()
        print("Vous avez probablement:")
        print("   - Copié l'URL de la PAGE qui contient la base")
        print("   - Au lieu de l'URL de la BASE elle-même")
        print()
        print("Solution:")
        print("   1. CLIQUEZ sur le titre de votre base de données")
        print("   2. Elle doit s'ouvrir en PLEIN ÉCRAN")
        print("   3. L'URL doit CHANGER dans la barre d'adresse")
        print("   4. C'est CETTE nouvelle URL qu'il faut copier")
        print()
        print("Relancez ce script et réessayez!")
        
    elif 'object not found' in error.lower():
        print("⚠️  La base de données n'a pas été trouvée!")
        print()
        print("Causes possibles:")
        print("   1. Vous n'avez PAS partagé la base avec votre intégration")
        print("      → Retournez dans Notion → Partager → Inviter l'intégration")
        print()
        print("   2. L'ID est incorrect")
        print("      → Vérifiez que vous avez copié la bonne URL")
        print()
    
    exit(1)

