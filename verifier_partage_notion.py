"""
Vérification du partage de la base de données Notion avec votre intégration
"""
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

print("="*70)
print("🔍 VÉRIFICATION DU PARTAGE NOTION")
print("="*70)
print()

notion_key = os.getenv('NOTION_API_KEY')
database_id = os.getenv('NOTION_DATABASE_ID')

if not notion_key or not database_id:
    print("❌ Variables manquantes dans .env")
    exit(1)

print(f"📋 Database ID: {database_id}")
print()

notion = Client(auth=notion_key)

try:
    database = notion.databases.retrieve(database_id)
    
    db_title = "Sans titre"
    if database.get('title') and len(database['title']) > 0:
        db_title = database['title'][0].get('plain_text', 'Sans titre')
    
    print("✅✅✅ SUCCÈS! ✅✅✅")
    print()
    print(f"🎉 Base de données trouvée: {db_title}")
    print("✅ Elle EST partagée avec votre intégration!")
    print()
    
    # Vérifier les propriétés
    properties = database.get('properties', {})
    print("📋 Propriétés de la base:")
    
    required = {
        'Name': 'title',
        'Date': 'date',
        'Status': 'select'
    }
    
    all_good = True
    for prop_name, expected_type in required.items():
        if prop_name in properties:
            actual_type = properties[prop_name].get('type')
            if actual_type == expected_type:
                print(f"   ✅ {prop_name} ({expected_type})")
            else:
                print(f"   ❌ {prop_name} - Type incorrect: {actual_type} (attendu: {expected_type})")
                all_good = False
        else:
            print(f"   ❌ {prop_name} - MANQUANTE!")
            all_good = False
    
    print()
    
    if all_good:
        print("="*70)
        print("🎉 CONFIGURATION PARFAITE!")
        print("="*70)
        print()
        print("✅ Base de données accessible")
        print("✅ Toutes les propriétés présentes")
        print()
        print("🚀 Vous pouvez maintenant:")
        print("   1. Démarrer le serveur: python app.py")
        print("   2. Ouvrir http://localhost:8500")
        print("   3. Enregistrer un message vocal")
        print("   4. Le voir apparaître dans Notion!")
        print()
    else:
        print("⚠️  Certaines propriétés manquent ou sont incorrectes")
        print("   Ajoutez-les dans votre base Notion puis relancez ce test")
        print()
    
except Exception as e:
    error_str = str(e)
    print("❌ ERREUR!")
    print()
    print(f"Message d'erreur: {error_str}")
    print()
    
    if 'Could not find database' in error_str or 'object not found' in error_str:
        print("="*70)
        print("⚠️  PROBLÈME: La base n'est PAS partagée avec votre intégration")
        print("="*70)
        print()
        print("🔧 SOLUTION:")
        print()
        print("1️⃣ Ouvrez votre base de données dans Notion")
        print("   (Cliquez dessus pour l'ouvrir en plein écran)")
        print()
        print("2️⃣ Cliquez sur 'Partager' en haut à droite")
        print()
        print("3️⃣ Dans le champ de recherche, tapez le nom de votre intégration")
        print("   (Celui que vous avez créé sur notion.so/my-integrations)")
        print()
        print("4️⃣ Cliquez sur votre intégration pour l'ajouter")
        print("   Elle devrait apparaître avec une icône 🤖")
        print()
        print("5️⃣ Relancez ce script: python verifier_partage_notion.py")
        print()
        print("="*70)
        print()
        print("💡 ASTUCE: Votre intégration s'appelle probablement:")
        print("   'Vocal to Notion' ou un nom similaire")
        print()
        print("   Si vous ne la trouvez pas, allez sur:")
        print("   https://www.notion.so/my-integrations")
        print("   pour voir le nom exact de votre intégration")
        print()
        
    elif 'page' in error_str.lower() and 'not a database' in error_str.lower():
        print("⚠️  C'est encore une PAGE, pas une BASE DE DONNÉES")
        print()
        print("Vous devez:")
        print("   1. Ouvrir la BASE en cliquant sur son titre")
        print("   2. Copier l'URL qui change (elle doit contenir un nouvel ID)")
        print("   3. Extraire l'ID de cette URL")
        print("   4. Mettre à jour NOTION_DATABASE_ID dans .env")
        print()
    
    else:
        print("⚠️  Erreur inattendue. Vérifiez:")
        print("   - Que votre clé Notion est valide")
        print("   - Que l'ID de la base est correct")
        print("   - Que la base existe toujours")
        print()

