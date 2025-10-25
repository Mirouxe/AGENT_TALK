"""
Service d'intégration avec l'API Notion
"""
import logging
from notion_client import Client
from datetime import datetime

logger = logging.getLogger(__name__)


class NotionService:
    """Service pour créer des pages dans Notion"""
    
    def __init__(self, api_key, database_id):
        """
        Initialiser le service Notion
        
        Args:
            api_key (str): Clé API Notion
            database_id (str): ID de la base de données Notion cible
        """
        self.client = Client(auth=api_key)
        self.database_id = database_id
        
        # Récupérer les métadonnées de la base pour connaître le type de Status
        try:
            database = self.client.databases.retrieve(database_id)
            properties = database.get('properties', {})
            self.status_type = properties.get('Status', {}).get('type', 'select')
            logger.info(f"Service Notion initialisé (Status type: {self.status_type})")
        except Exception as e:
            logger.warning(f"Impossible de récupérer les métadonnées: {e}")
            self.status_type = 'select'  # Par défaut
            logger.info("Service Notion initialisé (Status type: select par défaut)")
    
    def create_page(self, cleaned_text, original_transcription=None):
        """
        Créer une nouvelle page dans Notion avec le texte traité
        
        Args:
            cleaned_text (str): Texte nettoyé et structuré
            original_transcription (str, optional): Transcription originale
            
        Returns:
            str: URL de la page Notion créée
        """
        try:
            logger.info("Création d'une nouvelle page Notion")
            
            # Extraire un titre du texte (première ligne ou premiers mots)
            title_text = self._generate_title(cleaned_text)
            
            # Préparer le contenu de la page
            children = self._prepare_page_content(cleaned_text, original_transcription)
            
            # Préparer les propriétés
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title_text
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }
            
            # Ajouter Status selon son type (select ou status)
            # Utiliser "Not started" par défaut (option commune dans Notion)
            if self.status_type == 'status':
                properties["Status"] = {
                    "status": {
                        "name": "Not started"
                    }
                }
            else:  # 'select' par défaut
                properties["Status"] = {
                    "select": {
                        "name": "À classer"
                    }
                }
            
            # Créer la page
            new_page = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )
            
            page_url = new_page.get('url', '')
            logger.info(f"Page créée avec succès: {page_url}")
            return page_url
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la page Notion: {str(e)}")
            raise Exception(f"Erreur Notion: {str(e)}")
    
    def _generate_title(self, text):
        """
        Générer un titre à partir du texte
        
        Args:
            text (str): Texte complet
            
        Returns:
            str: Titre généré
        """
        # Prendre les 50 premiers caractères ou jusqu'au premier point
        lines = text.strip().split('\n')
        first_line = lines[0].strip()
        
        # Nettoyer les titres markdown si présents
        if first_line.startswith('#'):
            first_line = first_line.lstrip('#').strip()
        
        # Limiter la longueur
        if len(first_line) > 50:
            title = first_line[:47] + "..."
        else:
            title = first_line if first_line else "Note vocale"
        
        # Ajouter la date
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        return f"{title} - {date_str}"
    
    def _prepare_page_content(self, cleaned_text, original_transcription=None):
        """
        Préparer le contenu de la page Notion
        
        Args:
            cleaned_text (str): Texte nettoyé
            original_transcription (str, optional): Transcription originale
            
        Returns:
            list: Blocs de contenu pour Notion
        """
        children = []
        
        # Ajouter le texte nettoyé
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📝 Contenu structuré"}}]
            }
        })
        
        # Diviser le texte en paragraphes
        paragraphs = cleaned_text.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                # Vérifier si c'est un titre (commence par #)
                if paragraph.strip().startswith('#'):
                    title_text = paragraph.strip().lstrip('#').strip()
                    children.append({
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"type": "text", "text": {"content": title_text}}]
                        }
                    })
                else:
                    children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": paragraph.strip()}}]
                        }
                    })
        
        # Ajouter la transcription originale en callout si disponible
        if original_transcription:
            children.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "🎤 Transcription originale"}}]
                }
            })
            children.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": original_transcription}}],
                    "icon": {"emoji": "💬"}
                }
            })
        
        return children

