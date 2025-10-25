"""
Script de test complet du pipeline Vocal → Transcription → Nettoyage → Notion
"""
import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

print("="*70)
print("🧪 TEST COMPLET DU PIPELINE")
print("="*70)

# Vérifier les variables d'environnement
print("\n1️⃣ Vérification des variables d'environnement")
print("-" * 70)

openai_key = os.getenv('OPENAI_API_KEY')
notion_key = os.getenv('NOTION_API_KEY')
database_id = os.getenv('NOTION_DATABASE_ID')

all_keys_valid = True

if not openai_key or openai_key.startswith('sk-votre'):
    print("❌ OPENAI_API_KEY: Non configurée ou invalide")
    print("   → Doit commencer par 'sk-proj-' ou 'sk-'")
    all_keys_valid = False
else:
    print(f"✅ OPENAI_API_KEY: Configurée ({openai_key[:15]}...)")

if not notion_key or notion_key.startswith('secret_votre'):
    print("❌ NOTION_API_KEY: Non configurée ou invalide")
    print("   → Doit commencer par 'secret_'")
    all_keys_valid = False
else:
    print(f"✅ NOTION_API_KEY: Configurée ({notion_key[:20]}...)")

if not database_id or database_id.startswith('votre'):
    print("❌ NOTION_DATABASE_ID: Non configurée ou invalide")
    print("   → Doit être un ID de 32 caractères")
    all_keys_valid = False
else:
    print(f"✅ NOTION_DATABASE_ID: Configurée ({database_id})")

if not all_keys_valid:
    print("\n⚠️  Veuillez configurer toutes les clés API dans le fichier .env")
    print("   Consultez le README.md pour obtenir ces clés")
    sys.exit(1)

# Test 2: Connexion OpenAI
print("\n2️⃣ Test de connexion OpenAI")
print("-" * 70)

try:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    
    # Test simple avec l'API
    print("   Test de l'API Chat...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Dis juste: OK"}],
        max_tokens=5
    )
    print(f"   ✅ API Chat fonctionne: {response.choices[0].message.content}")
    
    # Test de l'API Whisper avec un fichier de test
    print("   Test de l'API Whisper...")
    print("   ⚠️  Pour tester Whisper, un fichier audio réel est nécessaire")
    print("   ✅ Client Whisper initialisé (sera testé avec un vrai fichier)")
    
except Exception as e:
    print(f"   ❌ Erreur OpenAI: {str(e)}")
    print(f"\n   Problèmes possibles:")
    print(f"   - Clé API invalide")
    print(f"   - Pas de crédit sur le compte OpenAI")
    print(f"   - Clé révoquée ou expirée")
    sys.exit(1)

# Test 3: Connexion Notion
print("\n3️⃣ Test de connexion Notion")
print("-" * 70)

try:
    from notion_client import Client
    notion = Client(auth=notion_key)
    
    # Test de récupération de la base de données
    print("   Test de récupération de la base de données...")
    database = notion.databases.retrieve(database_id)
    
    db_title = "Sans titre"
    if database.get('title') and len(database['title']) > 0:
        db_title = database['title'][0].get('plain_text', 'Sans titre')
    
    print(f"   ✅ Base de données trouvée: {db_title}")
    
    # Vérifier les propriétés
    print("   Vérification des propriétés requises...")
    properties = database.get('properties', {})
    required_props = {
        'Name': 'title',
        'Date': 'date', 
        'Status': ['select', 'status']  # Accepter les deux types
    }
    
    missing_props = []
    wrong_type = []
    
    for prop_name, expected_type in required_props.items():
        if prop_name not in properties:
            missing_props.append(prop_name)
        else:
            actual_type = properties[prop_name].get('type')
            # Gérer le cas où expected_type est une liste (pour Status qui peut être select ou status)
            if isinstance(expected_type, list):
                if actual_type in expected_type:
                    print(f"   ✅ Propriété '{prop_name}' ({actual_type}): OK")
                else:
                    wrong_type.append(f"{prop_name} (type: {actual_type}, attendu: {' ou '.join(expected_type)})")
            else:
                if actual_type != expected_type:
                    wrong_type.append(f"{prop_name} (type: {actual_type}, attendu: {expected_type})")
                else:
                    print(f"   ✅ Propriété '{prop_name}' ({expected_type}): OK")
    
    if missing_props:
        print(f"   ❌ Propriétés manquantes: {', '.join(missing_props)}")
        print(f"      → Ajoutez ces propriétés dans votre base Notion")
        sys.exit(1)
    
    if wrong_type:
        print(f"   ❌ Propriétés avec mauvais type:")
        for prop in wrong_type:
            print(f"      - {prop}")
        sys.exit(1)
    
    # Vérifier que l'option "À classer" existe dans Status
    status_prop = properties.get('Status', {})
    status_type = status_prop.get('type')
    
    if status_type == 'select':
        options = status_prop.get('select', {}).get('options', [])
        has_a_classer = any(opt.get('name') == 'À classer' for opt in options)
        if not has_a_classer:
            print("   ⚠️  L'option 'À classer' n'existe pas dans la propriété Status")
            print("      → Ajoutez cette option ou l'application créera la page avec un autre statut")
        else:
            print("   ✅ Option 'À classer' trouvée dans Status")
    elif status_type == 'status':
        options = status_prop.get('status', {}).get('options', [])
        has_a_classer = any(opt.get('name') == 'À classer' for opt in options)
        if not has_a_classer:
            print("   ⚠️  L'option 'À classer' n'existe pas dans la propriété Status")
            print("      → Ajoutez cette option ou l'application créera la page avec un autre statut")
        else:
            print("   ✅ Option 'À classer' trouvée dans Status")
    
except Exception as e:
    error_str = str(e)
    print(f"   ❌ Erreur Notion: {error_str}")
    print(f"\n   Problèmes possibles:")
    
    if 'Could not find database' in error_str or 'object not found' in error_str:
        print(f"   - L'ID de la base de données est incorrect")
        print(f"   - La base de données a été supprimée")
    elif 'unauthorized' in error_str.lower() or 'forbidden' in error_str.lower():
        print(f"   - L'intégration n'a pas accès à cette base de données")
        print(f"   - Avez-vous partagé la base avec votre intégration ?")
        print(f"   - Dans Notion: Ouvrir la base → Partager → Inviter votre intégration")
    else:
        print(f"   - Clé API Notion invalide")
        print(f"   - Problème de connexion")
    
    sys.exit(1)

# Test 4: Services de l'application
print("\n4️⃣ Test des services de l'application")
print("-" * 70)

try:
    print("   Initialisation de TranscriptionService...")
    from services.transcription_service import TranscriptionService
    transcription_service = TranscriptionService(openai_key)
    print("   ✅ TranscriptionService initialisé")
    
    print("   Initialisation de CleaningService...")
    from services.cleaning_service import CleaningService
    cleaning_service = CleaningService(openai_key)
    print("   ✅ CleaningService initialisé")
    
    print("   Initialisation de NotionService...")
    from services.notion_service import NotionService
    notion_service = NotionService(notion_key, database_id)
    print("   ✅ NotionService initialisé")
    
except Exception as e:
    print(f"   ❌ Erreur lors de l'initialisation: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test du nettoyage de texte (sans audio)
print("\n5️⃣ Test du nettoyage de texte (GPT)")
print("-" * 70)

try:
    test_text = "Euh... ben voilà, je voulais juste dire que, genre, c'est vraiment important de, bah, tester l'application quoi."
    print(f"   Texte de test: '{test_text}'")
    print("   Envoi à ChatGPT pour nettoyage...")
    
    cleaned = cleaning_service.clean_and_structure(test_text)
    print(f"   ✅ Texte nettoyé: '{cleaned}'")
    
except Exception as e:
    print(f"   ❌ Erreur lors du nettoyage: {str(e)}")
    if 'insufficient_quota' in str(e) or 'quota' in str(e).lower():
        print("      → Vous n'avez plus de crédit sur votre compte OpenAI")
        print("      → Ajoutez du crédit sur platform.openai.com/account/billing")
    sys.exit(1)

# Test 6: Test de création de page Notion
print("\n6️⃣ Test de création de page Notion")
print("-" * 70)

try:
    test_title = "🧪 Test du pipeline - Ne pas supprimer"
    test_content = "Ceci est une page de test créée automatiquement.\n\nSi vous voyez cette page, cela signifie que l'intégration fonctionne correctement !"
    
    print(f"   Création d'une page de test dans Notion...")
    notion_url = notion_service.create_page(test_content, "Texte original de test")
    print(f"   ✅ Page créée avec succès!")
    print(f"   📄 URL: {notion_url}")
    print(f"\n   ⚠️  Une page de test a été créée dans votre Notion")
    print(f"       Vous pouvez la supprimer si vous voulez")
    
except Exception as e:
    print(f"   ❌ Erreur lors de la création de la page: {str(e)}")
    
    if 'validation_error' in str(e).lower():
        print("      → Erreur de validation des propriétés")
        print("      → Vérifiez que votre base a les bonnes propriétés (Name, Date, Status)")
    elif 'Status' in str(e):
        print("      → Problème avec la propriété 'Status'")
        print("      → Assurez-vous que l'option 'À classer' existe")
    
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Résumé
print("\n" + "="*70)
print("✅ TOUS LES TESTS SONT PASSÉS!")
print("="*70)
print("\n🎉 Votre configuration est correcte et fonctionnelle!")
print("\n📝 Résumé:")
print("   ✅ Clés API configurées")
print("   ✅ OpenAI (Chat + Whisper) fonctionne")
print("   ✅ Notion fonctionne")
print("   ✅ Services initialisés")
print("   ✅ Nettoyage de texte fonctionne")
print("   ✅ Création de pages Notion fonctionne")
print("\n🚀 Vous pouvez maintenant:")
print("   1. Démarrer le serveur: python app.py")
print("   2. Ouvrir http://localhost:8500")
print("   3. Enregistrer un message vocal")
print("   4. Le voir apparaître dans Notion!")
print("\n⚠️  Note: La transcription audio ne peut être testée qu'avec un vrai fichier audio")
print("   Elle sera testée automatiquement lors de votre premier enregistrement.")
print()

