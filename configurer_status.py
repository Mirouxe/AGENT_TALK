"""
Script pour configurer l'option Status de Notion
"""
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

print("="*70)
print("⚙️  CONFIGURATION DE LA PROPRIÉTÉ STATUS")
print("="*70)
print()

notion_key = os.getenv('NOTION_API_KEY')
database_id = os.getenv('NOTION_DATABASE_ID')

notion = Client(auth=notion_key)

try:
    database = notion.databases.retrieve(database_id)
    properties = database.get('properties', {})
    status_prop = properties.get('Status', {})
    status_type = status_prop.get('type')
    
    print(f"📋 Type de la propriété Status: {status_type}")
    print()
    
    # Récupérer les options disponibles
    if status_type == 'status':
        options = status_prop.get('status', {}).get('options', [])
    elif status_type == 'select':
        options = status_prop.get('select', {}).get('options', [])
    else:
        print("❌ Type de Status non reconnu")
        exit(1)
    
    print(f"📌 Options actuellement disponibles dans votre base:")
    print()
    
    if not options:
        print("   ❌ Aucune option trouvée!")
        print()
        print("🔧 Solution:")
        print("   1. Ouvrez votre base de données dans Notion")
        print("   2. Cliquez sur la colonne 'Status'")
        print("   3. Ajoutez une option nommée: 'À classer'")
        print("   4. Relancez ce script")
        print()
        exit(1)
    
    for i, opt in enumerate(options, 1):
        option_name = opt.get('name', 'Sans nom')
        option_color = opt.get('color', '')
        print(f"   {i}. {option_name} ({option_color})")
    
    print()
    
    # Vérifier si "À classer" existe
    has_a_classer = any(opt.get('name') == 'À classer' for opt in options)
    
    if has_a_classer:
        print("✅ L'option 'À classer' existe déjà!")
        print("   Votre configuration est parfaite!")
        print()
        print("🚀 Lancez maintenant: python test_pipeline.py")
        print()
    else:
        print("⚠️  L'option 'À classer' n'existe pas.")
        print()
        print("🔧 SOLUTIONS:")
        print()
        print("Option 1 - Ajouter 'À classer' dans Notion (RECOMMANDÉ):")
        print("   1. Ouvrez votre base de données dans Notion")
        print("   2. Cliquez sur l'en-tête de la colonne 'Status'")
        print("   3. En bas du menu, cliquez sur '+ Nouvelle option'")
        print("   4. Tapez: À classer")
        print("   5. Choisissez une couleur (ex: orange)")
        print("   6. Relancez: python test_pipeline.py")
        print()
        print("Option 2 - Utiliser une option existante:")
        print("   Je peux configurer l'application pour utiliser une de vos")
        print("   options existantes au lieu de 'À classer'")
        print()
        
        choix = input("Voulez-vous utiliser une option existante? (o/n): ").strip().lower()
        
        if choix == 'o' or choix == 'oui' or choix == 'y' or choix == 'yes':
            print()
            print("Quelle option voulez-vous utiliser?")
            for i, opt in enumerate(options, 1):
                print(f"   {i}. {opt.get('name')}")
            
            while True:
                try:
                    choix_num = int(input(f"\nChoisissez un numéro (1-{len(options)}): "))
                    if 1 <= choix_num <= len(options):
                        selected_option = options[choix_num - 1]['name']
                        print()
                        print(f"✅ Option sélectionnée: {selected_option}")
                        print()
                        print("⚠️  ATTENTION: Cette fonctionnalité nécessiterait de modifier")
                        print("   le code source. Pour le moment, je recommande plutôt:")
                        print()
                        print(f"   1. D'ajouter l'option 'À classer' dans Notion")
                        print(f"   2. OU de laisser la propriété Status vide")
                        print()
                        break
                    else:
                        print("Numéro invalide, réessayez.")
                except ValueError:
                    print("Entrée invalide, réessayez.")
        else:
            print()
            print("D'accord! Ajoutez l'option 'À classer' dans Notion")
            print("puis relancez: python test_pipeline.py")
            print()

except Exception as e:
    print(f"❌ Erreur: {str(e)}")
    exit(1)

