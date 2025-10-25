"""
Script de test pour vérifier la configuration des APIs
Lance ce script pour vérifier que vos clés API fonctionnent correctement
"""
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans le terminal
try:
    init(autoreset=True)
except:
    pass

def print_success(message):
    """Afficher un message de succès"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    """Afficher un message d'erreur"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    """Afficher un message d'information"""
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def test_env_file():
    """Tester la présence du fichier .env"""
    print_info("Vérification du fichier .env...")
    if not os.path.exists('.env'):
        print_error("Fichier .env non trouvé !")
        print_info("Créez un fichier .env à partir de .env.example")
        return False
    print_success("Fichier .env trouvé")
    return True

def test_openai():
    """Tester la connexion à l'API OpenAI"""
    print_info("Test de la connexion OpenAI...")
    try:
        from openai import OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print_error("OPENAI_API_KEY non défini dans .env")
            return False
        
        if not api_key.startswith('sk-'):
            print_error("OPENAI_API_KEY semble invalide (devrait commencer par 'sk-')")
            return False
        
        client = OpenAI(api_key=api_key)
        
        # Test simple avec l'API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print_success("Connexion OpenAI réussie !")
        print_info(f"Modèle utilisé : {response.model}")
        return True
        
    except Exception as e:
        print_error(f"Erreur OpenAI : {str(e)}")
        return False

def test_notion():
    """Tester la connexion à l'API Notion"""
    print_info("Test de la connexion Notion...")
    try:
        from notion_client import Client
        
        api_key = os.getenv('NOTION_API_KEY')
        database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not api_key:
            print_error("NOTION_API_KEY non défini dans .env")
            return False
        
        if not api_key.startswith('secret_'):
            print_error("NOTION_API_KEY semble invalide (devrait commencer par 'secret_')")
            return False
        
        if not database_id:
            print_error("NOTION_DATABASE_ID non défini dans .env")
            return False
        
        client = Client(auth=api_key)
        
        # Tester l'accès à la base de données
        database = client.databases.retrieve(database_id)
        
        print_success("Connexion Notion réussie !")
        print_info(f"Base de données : {database.get('title', [{}])[0].get('plain_text', 'Sans titre')}")
        
        # Vérifier les propriétés requises
        properties = database.get('properties', {})
        required_props = ['Name', 'Date', 'Status']
        missing_props = []
        
        for prop in required_props:
            if prop not in properties:
                missing_props.append(prop)
        
        if missing_props:
            print_error(f"Propriétés manquantes dans la base de données : {', '.join(missing_props)}")
            print_info("Consultez GUIDE_NOTION.md pour configurer votre base de données")
            return False
        
        print_success("Toutes les propriétés requises sont présentes !")
        return True
        
    except Exception as e:
        print_error(f"Erreur Notion : {str(e)}")
        print_info("Vérifiez que :")
        print_info("  1. Votre intégration a accès à la base de données")
        print_info("  2. L'ID de la base de données est correct")
        print_info("Consultez GUIDE_NOTION.md pour plus d'aide")
        return False

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🧪 Test de configuration - Vocal → Notion")
    print("="*60 + "\n")
    
    # Charger les variables d'environnement
    load_dotenv()
    
    results = []
    
    # Test 1 : Fichier .env
    results.append(("Fichier .env", test_env_file()))
    
    if results[0][1]:  # Si le fichier .env existe
        # Test 2 : OpenAI
        print()
        results.append(("OpenAI API", test_openai()))
        
        # Test 3 : Notion
        print()
        results.append(("Notion API", test_notion()))
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    for name, success in results:
        if success:
            print_success(f"{name} : OK")
        else:
            print_error(f"{name} : ÉCHEC")
    
    print()
    
    all_success = all(result[1] for result in results)
    
    if all_success:
        print_success("Tous les tests sont passés ! 🎉")
        print_info("Vous pouvez démarrer l'application avec : python app.py")
    else:
        print_error("Certains tests ont échoué")
        print_info("Consultez les messages d'erreur ci-dessus et le README.md")
    
    print()

if __name__ == '__main__':
    main()

