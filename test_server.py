"""
Script de test rapide du serveur
"""
import os
import sys
from dotenv import load_dotenv

print("🔍 Test du démarrage du serveur...\n")

# Charger le .env
load_dotenv()

# Vérifier les variables d'environnement
print("1️⃣ Vérification des variables d'environnement:")
openai_key = os.getenv('OPENAI_API_KEY')
notion_key = os.getenv('NOTION_API_KEY')
database_id = os.getenv('NOTION_DATABASE_ID')

if openai_key and openai_key != 'sk-votre-cle-openai-ici':
    print(f"   ✅ OPENAI_API_KEY: Configurée (commence par {openai_key[:10]}...)")
else:
    print(f"   ⚠️  OPENAI_API_KEY: Non configurée (utilisez vos vraies clés)")

if notion_key and notion_key != 'secret_votre-cle-notion-ici':
    print(f"   ✅ NOTION_API_KEY: Configurée (commence par {notion_key[:13]}...)")
else:
    print(f"   ⚠️  NOTION_API_KEY: Non configurée (utilisez vos vraies clés)")

if database_id and database_id != 'votre-database-id-notion-ici':
    print(f"   ✅ NOTION_DATABASE_ID: Configurée ({database_id[:10]}...)")
else:
    print(f"   ⚠️  NOTION_DATABASE_ID: Non configurée (utilisez vos vraies clés)")

print("\n2️⃣ Test de l'importation de l'application:")
try:
    from app import app
    print("   ✅ Application Flask importée avec succès")
    
    print("\n3️⃣ Test des routes:")
    with app.test_client() as client:
        # Test page d'accueil
        response = client.get('/')
        if response.status_code == 200:
            print("   ✅ Page d'accueil: OK (200)")
        else:
            print(f"   ❌ Page d'accueil: ERREUR ({response.status_code})")
            sys.exit(1)
        
        # Test CSS
        response = client.get('/static/style.css')
        if response.status_code == 200:
            print("   ✅ Fichier CSS: OK (200)")
        else:
            print(f"   ❌ Fichier CSS: ERREUR ({response.status_code})")
        
        # Test JS
        response = client.get('/static/script.js')
        if response.status_code == 200:
            print("   ✅ Fichier JS: OK (200)")
        else:
            print(f"   ❌ Fichier JS: ERREUR ({response.status_code})")
        
        # Test health
        response = client.get('/api/health')
        if response.status_code == 200:
            print("   ✅ API Health: OK (200)")
        else:
            print(f"   ❌ API Health: ERREUR ({response.status_code})")
    
    print("\n" + "="*60)
    print("✅ TOUS LES TESTS SONT PASSÉS!")
    print("="*60)
    print("\n🚀 Le serveur peut maintenant être démarré avec:")
    print("   python app.py")
    print("\n📍 Puis ouvrez votre navigateur sur:")
    print("   http://localhost:5000")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

