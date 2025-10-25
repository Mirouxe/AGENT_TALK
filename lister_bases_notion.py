"""
Script pour lister toutes les bases de données accessibles à votre intégration Notion
"""
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

print("="*70)
print("📋 LISTE DES BASES DE DONNÉES ACCESSIBLES")
print("="*70)
print()

notion_key = os.getenv('NOTION_API_KEY')

if not notion_key:
    print("❌ NOTION_API_KEY non trouvée dans .env")
    exit(1)

notion = Client(auth=notion_key)

try:
    # Rechercher toutes les bases de données
    print("🔍 Recherche de toutes les bases de données partagées...")
    print()
    
    # Notion API nécessite une recherche
    results = notion.search(filter={"property": "object", "value": "database"})
    
    databases = results.get('results', [])
    
    if not databases:
        print("❌ Aucune base de données trouvée!")
        print()
        print("Cela signifie qu'aucune base n'est connectée à votre intégration.")
        print()
        print("🔧 Solution:")
        print("   1. Ouvrez UNE base de données dans Notion")
        print("   2. Cliquez sur '...' (trois points) en haut à droite")
        print("   3. Cherchez 'Connections' ou 'Connexions'")
        print("   4. Ajoutez votre intégration")
        print("   5. Relancez ce script")
        print()
        exit(1)
    
    print(f"✅ {len(databases)} base(s) de données trouvée(s):")
    print("="*70)
    print()
    
    current_id = os.getenv('NOTION_DATABASE_ID', '')
    
    for i, db in enumerate(databases, 1):
        db_id = db['id'].replace('-', '')
        title = "Sans titre"
        
        if db.get('title') and len(db['title']) > 0:
            title = db['title'][0].get('plain_text', 'Sans titre')
        
        is_current = db_id == current_id
        
        print(f"{'🎯' if is_current else '📊'} Base #{i}: {title}")
        print(f"   ID: {db_id}")
        
        if is_current:
            print("   ✅ C'EST CELLE CONFIGURÉE DANS VOTRE .env")
        
        # Vérifier les propriétés
        properties = db.get('properties', {})
        has_name = 'Name' in properties
        has_date = 'Date' in properties
        has_status = 'Status' in properties
        
        print(f"   Propriétés: ", end="")
        props = []
        if has_name:
            props.append("Name ✅")
        if has_date:
            props.append("Date ✅")
        if has_status:
            props.append("Status ✅")
        
        if has_name and has_date and has_status:
            print(" ".join(props) + " - PARFAIT! ✅")
        else:
            print(" ".join(props))
            missing = []
            if not has_name:
                missing.append("Name")
            if not has_date:
                missing.append("Date")
            if not has_status:
                missing.append("Status")
            if missing:
                print(f"   ⚠️  Manquant: {', '.join(missing)}")
        
        print()
    
    print("="*70)
    print()
    
    # Vérifier si l'ID actuel est dans la liste
    if current_id:
        found = any(db['id'].replace('-', '') == current_id for db in databases)
        if found:
            print("✅ L'ID dans votre .env correspond à une base accessible!")
            print()
            print("🔧 Si vous voyez toujours une erreur, essayez:")
            print("   1. Redémarrez votre terminal")
            print("   2. Relancez: python test_pipeline.py")
            print()
        else:
            print("❌ L'ID dans votre .env ne correspond à AUCUNE base accessible!")
            print()
            print(f"   ID actuel dans .env: {current_id}")
            print()
            print("🔧 Solutions:")
            print()
            print("   Option 1 - Utiliser une base existante:")
            for i, db in enumerate(databases, 1):
                db_id = db['id'].replace('-', '')
                title = db.get('title', [{}])[0].get('plain_text', 'Sans titre') if db.get('title') else 'Sans titre'
                print(f"      Base #{i}: {title}")
                print(f"      → Copiez cet ID dans votre .env: {db_id}")
                print()
            
            print("   Option 2 - Connecter la base que vous voulez:")
            print("      1. Ouvrez LA base que vous voulez utiliser dans Notion")
            print("      2. ... → Connections → Ajouter votre intégration")
            print("      3. Copiez l'URL de cette base")
            print("      4. Extrayez l'ID et mettez-le dans .env")
            print()
    else:
        print("⚠️  NOTION_DATABASE_ID n'est pas défini dans .env")
        print()
        if databases:
            print("💡 Vous pouvez utiliser une de ces bases:")
            for i, db in enumerate(databases, 1):
                db_id = db['id'].replace('-', '')
                title = db.get('title', [{}])[0].get('plain_text', 'Sans titre') if db.get('title') else 'Sans titre'
                print(f"   {i}. {title}")
                print(f"      ID: {db_id}")
                print()
    
except Exception as e:
    print(f"❌ Erreur: {str(e)}")
    print()
    print("Vérifiez que votre NOTION_API_KEY est valide")
    exit(1)

