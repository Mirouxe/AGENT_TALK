"""
Application Flask pour la chaîne de traitement vocal -> transcription -> nettoyage -> Notion
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import logging

from services.transcription_service import TranscriptionService
from services.cleaning_service import CleaningService
from services.notion_service import NotionService

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Obtenir le chemin absolu du dossier de l'application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialiser Flask avec les chemins absolus
app = Flask(__name__, 
            static_folder=os.path.join(BASE_DIR, 'static'),
            static_url_path='/static')
CORS(app)

# Dossier pour stocker temporairement les fichiers audio
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialiser les services
transcription_service = TranscriptionService(os.getenv('OPENAI_API_KEY'))
cleaning_service = CleaningService(os.getenv('OPENAI_API_KEY'))
notion_service = NotionService(
    os.getenv('NOTION_API_KEY'),
    os.getenv('NOTION_DATABASE_ID')
)


@app.route('/')
def index():
    """Page d'accueil avec l'interface d'enregistrement"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    """
    Endpoint principal pour traiter un fichier audio
    Pipeline: Audio -> Transcription -> Nettoyage -> Notion
    """
    try:
        # Vérifier qu'un fichier a été envoyé
        if 'audio' not in request.files:
            return jsonify({'error': 'Aucun fichier audio fourni'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'Nom de fichier vide'}), 400
        
        # Sauvegarder temporairement le fichier
        filename = f"audio_{os.urandom(8).hex()}.webm"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(filepath)
        
        logger.info(f"Fichier audio reçu: {filename}")
        
        # Étape 1: Transcription
        logger.info("Étape 1: Transcription en cours...")
        transcription = transcription_service.transcribe(filepath)
        logger.info(f"Transcription terminée: {transcription[:100]}...")
        
        # Étape 2: Nettoyage et structuration
        logger.info("Étape 2: Nettoyage et structuration...")
        cleaned_text = cleaning_service.clean_and_structure(transcription)
        logger.info(f"Nettoyage terminé: {cleaned_text[:100]}...")
        
        # Étape 3: Envoi vers Notion
        logger.info("Étape 3: Création de la page Notion...")
        notion_url = notion_service.create_page(cleaned_text, transcription)
        logger.info(f"Page Notion créée: {notion_url}")
        
        # Nettoyer le fichier temporaire
        os.remove(filepath)
        logger.info(f"Fichier temporaire supprimé: {filename}")
        
        return jsonify({
            'success': True,
            'transcription': transcription,
            'cleaned_text': cleaned_text,
            'notion_url': notion_url,
            'message': 'Traitement terminé avec succès!'
        })
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")
        # Nettoyer le fichier en cas d'erreur
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        # Messages d'erreur plus explicites
        error_message = str(e)
        
        if 'api_key' in error_message.lower() or 'authentication' in error_message.lower():
            error_message = "❌ Clés API non configurées ou invalides. Veuillez vérifier votre fichier .env avec vos vraies clés OpenAI et Notion."
        elif 'openai' in error_message.lower():
            error_message = f"❌ Erreur OpenAI: {error_message}. Vérifiez que votre clé OpenAI est valide et que vous avez du crédit."
        elif 'notion' in error_message.lower():
            error_message = f"❌ Erreur Notion: {error_message}. Vérifiez que votre intégration a accès à la base de données."
        else:
            error_message = f"❌ Erreur: {error_message}"
        
        return jsonify({'error': error_message}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifier que l'API fonctionne"""
    return jsonify({'status': 'ok', 'message': 'API opérationnelle'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8500))
    app.run(debug=True, host='0.0.0.0', port=port)

