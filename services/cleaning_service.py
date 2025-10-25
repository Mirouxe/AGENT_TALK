"""
Service de nettoyage et structuration de texte utilisant l'API ChatGPT
"""
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class CleaningService:
    """Service pour nettoyer et structurer le texte transcrit"""
    
    def __init__(self, api_key):
        """
        Initialiser le service de nettoyage
        
        Args:
            api_key (str): Clé API OpenAI
        """
        self.client = OpenAI(api_key=api_key)
        logger.info("Service de nettoyage initialisé")
    
    def clean_and_structure(self, transcription):
        """
        Nettoyer et structurer un texte transcrit
        Supprime les éléments de langage inutiles et améliore la structure
        
        Args:
            transcription (str): Texte transcrit brut
            
        Returns:
            str: Texte nettoyé et structuré
        """
        try:
            logger.info("Nettoyage et structuration du texte")
            
            # Prompt pour ChatGPT
            system_prompt = """Tu es un assistant expert en traitement de texte. 
            Ta mission est de nettoyer et structurer des transcriptions vocales.
            
            Consignes:
            1. Supprime tous les éléments de langage parasites (euh, hum, bah, genre, etc.)
            2. Corrige les fautes de grammaire et d'orthographe
            3. Structure le texte avec des paragraphes logiques
            4. Ajoute de la ponctuation appropriée
            5. Améliore la clarté sans changer le sens
            6. Si le texte contient des idées distinctes, organise-les en sections avec des titres
            7. Garde un ton naturel et fluide
            
            Retourne uniquement le texte nettoyé et structuré, sans commentaires."""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Nettoie et structure ce texte:\n\n{transcription}"}
                ],
                temperature=0.3
            )
            
            cleaned_text = response.choices[0].message.content
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {str(e)}")
            raise Exception(f"Erreur de nettoyage: {str(e)}")

