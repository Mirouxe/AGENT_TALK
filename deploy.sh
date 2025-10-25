#!/bin/bash

# Script de déploiement pour l'application Vocal → Notion
# Ce script vous guide à travers le processus de déploiement

echo "🚀 Script de déploiement - Vocal → Notion"
echo "=========================================="
echo ""

# Vérifier que Git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé"
    echo "   Installez Git depuis: https://git-scm.com/"
    exit 1
fi

echo "✅ Git est installé"
echo ""

# Vérifier si c'est déjà un dépôt Git
if [ ! -d ".git" ]; then
    echo "📦 Initialisation du dépôt Git..."
    git init
    echo "✅ Dépôt Git initialisé"
else
    echo "✅ Dépôt Git existant"
fi
echo ""

# Vérifier que .env n'est pas dans Git
if git ls-files | grep -q "^.env$"; then
    echo "⚠️  ATTENTION: .env est tracké par Git!"
    echo "   Suppression de .env du tracking..."
    git rm --cached .env
    echo "✅ .env retiré du tracking"
fi
echo ""

# Ajouter tous les fichiers
echo "📝 Ajout des fichiers au dépôt..."
git add .
echo "✅ Fichiers ajoutés"
echo ""

# Créer un commit si nécessaire
if git diff --cached --quiet; then
    echo "ℹ️  Aucun changement à commiter"
else
    echo "💾 Création du commit..."
    git commit -m "Préparation pour le déploiement - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "✅ Commit créé"
fi
echo ""

echo "=========================================="
echo "📋 PROCHAINES ÉTAPES"
echo "=========================================="
echo ""
echo "Vous avez 3 options pour déployer :"
echo ""
echo "1️⃣  RENDER (Recommandé - Le plus simple)"
echo "   → Gratuit, facile, HTTPS automatique"
echo "   → render.com"
echo ""
echo "2️⃣  RAILWAY (Rapide)"
echo "   → $5 de crédit/mois gratuit"
echo "   → railway.app"
echo ""
echo "3️⃣  FLY.IO (Performant)"
echo "   → Gratuit avec limites"
echo "   → fly.io"
echo ""
echo "Consultez DEPLOIEMENT.md pour les instructions détaillées"
echo ""

# Proposer de créer un dépôt GitHub
echo "Voulez-vous pousser vers GitHub maintenant? (o/n)"
read -r response

if [[ "$response" == "o" || "$response" == "oui" || "$response" == "y" ]]; then
    echo ""
    echo "🔐 Configuration GitHub avec Personal Access Token"
    echo ""
    
    # Demander le token ou utiliser une variable d'environnement
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "✅ Token GitHub trouvé dans les variables d'environnement"
        github_token="$GITHUB_TOKEN"
    else
        echo "📝 Entrez votre Personal Access Token GitHub:"
        echo "   (Le token ne sera pas affiché pour des raisons de sécurité)"
        read -rs github_token
        echo ""
    fi
    
    if [ -z "$github_token" ]; then
        echo "❌ Token non fourni, abandon du push"
        exit 1
    fi
    
    # Demander username et nom du repo
    echo "📝 Entrez votre username GitHub:"
    read -r github_username
    
    echo "📝 Entrez le nom du dépôt (ex: agent-talk):"
    read -r repo_name
    
    if [ -z "$github_username" ] || [ -z "$repo_name" ]; then
        echo "❌ Username ou nom de dépôt manquant"
        exit 1
    fi
    
    # Construire l'URL avec le token
    github_url="https://${github_token}@github.com/${github_username}/${repo_name}.git"
    
    echo ""
    echo "📍 Dépôt: https://github.com/${github_username}/${repo_name}.git"
    echo ""
    
    # Vérifier si origin existe déjà
    if git remote | grep -q "^origin$"; then
        echo "ℹ️  Remote origin existe déjà, mise à jour..."
        git remote set-url origin "$github_url"
    else
        echo "📎 Ajout du remote origin..."
        git remote add origin "$github_url"
    fi
    
    echo "🚀 Push vers GitHub..."
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Code poussé sur GitHub avec succès!"
        echo ""
        
        # Nettoyer l'URL avec le token des logs pour la sécurité
        git remote set-url origin "https://github.com/${github_username}/${repo_name}.git"
        echo "🔒 Token retiré de la configuration Git (pour la sécurité)"
        echo ""
        
        echo "🎉 Vous pouvez maintenant:"
        echo "   1. Aller sur render.com ou railway.app"
        echo "   2. Créer un nouveau projet"
        echo "   3. Connecter votre dépôt GitHub: ${github_username}/${repo_name}"
        echo "   4. Configurer les variables d'environnement"
        echo "   5. Déployer!"
        echo ""
        echo "📍 Votre dépôt: https://github.com/${github_username}/${repo_name}"
    else
        echo ""
        echo "❌ Erreur lors du push"
        echo ""
        echo "Causes possibles:"
        echo "   - Token GitHub invalide ou expiré"
        echo "   - Dépôt n'existe pas (créez-le sur github.com/new)"
        echo "   - Pas de permissions suffisantes sur le dépôt"
        echo ""
        echo "💡 Vérifiez votre token sur: https://github.com/settings/tokens"
    fi
else
    echo ""
    echo "ℹ️  D'accord! Vous pouvez le faire plus tard avec:"
    echo ""
    echo "   Option 1 - Avec token (sécurisé):"
    echo "   git remote add origin https://TOKEN@github.com/USERNAME/REPO.git"
    echo "   git push -u origin main"
    echo ""
    echo "   Option 2 - Sans token (demandera identifiants):"
    echo "   git remote add origin https://github.com/USERNAME/REPO.git"
    echo "   git push -u origin main"
    echo ""
fi

echo ""
echo "📖 Consultez DEPLOIEMENT.md pour plus de détails"
echo ""

