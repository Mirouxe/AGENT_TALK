#!/bin/bash

# Script de démarrage rapide pour l'application Vocal → Notion

echo "🎙️  Démarrage de l'application Vocal → Notion"
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "⚠️  Environnement virtuel non trouvé. Création en cours..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
fi

# Activer l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer/Mettre à jour les dépendances
echo "📦 Installation des dépendances..."
pip install -q -r requirements.txt

# Vérifier que le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé !"
    echo "📝 Création du fichier .env à partir du template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT : Éditez le fichier .env avec vos clés API avant de continuer"
    echo "   - OPENAI_API_KEY"
    echo "   - NOTION_API_KEY"
    echo "   - NOTION_DATABASE_ID"
    echo ""
    read -p "Appuyez sur Entrée une fois les clés configurées..."
fi

# Créer le dossier uploads s'il n'existe pas
mkdir -p uploads

echo ""
echo "✅ Configuration terminée !"
echo "🚀 Démarrage du serveur..."
echo ""
echo "📍 L'application sera accessible sur : http://localhost:5000"
echo "❌ Pour arrêter le serveur : Ctrl+C"
echo ""

# Démarrer l'application
python app.py

