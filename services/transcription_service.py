"""
Service de transcription audio utilisant l'API Whisper d'OpenAI
"""
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Service pour transcrire les fichiers audio en texte"""
    
    def __init__(self, api_key):
        """
        Initialiser le service de transcription
        
        Args:
            api_key (str): Clé API OpenAI
        """
        self.client = OpenAI(api_key=api_key)
        logger.info("Service de transcription initialisé")
    
    def transcribe(self, audio_filepath):
        """
        Transcrire un fichier audio en texte
        
        Args:
            audio_filepath (str): Chemin vers le fichier audio
            
        Returns:
            str: Texte transcrit
        """
        try:
            logger.info(f"Transcription du fichier: {audio_filepath}")
            
            with open(audio_filepath, 'rb') as audio_file:
                # Utiliser l'API Whisper d'OpenAI
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="fr"  # Français par défaut
                )
            
            return transcription.text
            
        except Exception as e:
            logger.error(f"Erreur lors de la transcription: {str(e)}")
            raise Exception(f"Erreur de transcription: {str(e)}")

