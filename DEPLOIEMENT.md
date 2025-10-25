# 🚀 Guide de Déploiement

Ce guide vous explique comment déployer votre application **Vocal → Notion** pour la rendre accessible en ligne.

## 📋 Table des matières

1. [Préparation](#préparation)
2. [Option 1 : Render (Recommandé - Gratuit)](#option-1--render-recommandé---gratuit)
3. [Option 2 : Railway (Gratuit)](#option-2--railway-gratuit)
4. [Option 3 : Fly.io (Gratuit)](#option-3--flyio-gratuit)
5. [Vérification du déploiement](#vérification-du-déploiement)

---

## Préparation

Avant de déployer, nous devons préparer quelques fichiers.

### 1. Créer un fichier Procfile

Ce fichier indique comment démarrer l'application.

### 2. Créer un fichier runtime.txt

Spécifie la version de Python à utiliser.

### 3. Mettre à jour requirements.txt

Ajouter Gunicorn (serveur de production).

### 4. Initialiser Git

Sauvegarder votre code dans un dépôt Git.

---

## Option 1 : Render (Recommandé - Gratuit)

**Avantages** :
- ✅ Gratuit (750 heures/mois)
- ✅ Très simple à configurer
- ✅ Support HTTPS automatique
- ✅ Redémarrage automatique

### Étape 1 : Créer un compte

1. Allez sur [render.com](https://render.com)
2. Créez un compte (gratuit)
3. Connectez votre compte GitHub

### Étape 2 : Préparer le dépôt Git

```bash
# Initialiser Git si ce n'est pas déjà fait
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Application Vocal to Notion"

# Créer un dépôt sur GitHub
# Puis connectez-le
git remote add origin https://github.com/VOTRE-USERNAME/agent-talk.git
git branch -M main
git push -u origin main
```

### Étape 3 : Créer un nouveau Web Service sur Render

1. Sur Render, cliquez sur **"New +"** → **"Web Service"**
2. Connectez votre dépôt GitHub
3. Configurez :
   - **Name** : `vocal-to-notion`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app`
   - **Instance Type** : `Free`

### Étape 4 : Ajouter les variables d'environnement

Dans l'onglet **"Environment"**, ajoutez :

```
OPENAI_API_KEY=votre_clé_openai
NOTION_API_KEY=votre_clé_notion
NOTION_DATABASE_ID=votre_database_id
PORT=10000
```

### Étape 5 : Déployer

Cliquez sur **"Create Web Service"**. Render va :
- Installer les dépendances
- Démarrer l'application
- Vous donner une URL : `https://vocal-to-notion.onrender.com`

⚠️ **Note** : Les instances gratuites s'endorment après 15 min d'inactivité. Le premier chargement peut prendre 30 secondes.

---

## Option 2 : Railway (Gratuit)

**Avantages** :
- ✅ Gratuit ($5 de crédit/mois)
- ✅ Très rapide
- ✅ Interface moderne

### Étape 1 : Créer un compte

1. Allez sur [railway.app](https://railway.app)
2. Créez un compte avec GitHub

### Étape 2 : Nouveau projet

1. Cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez votre dépôt

### Étape 3 : Configuration

Railway détecte automatiquement Python. Ajoutez les variables d'environnement :

1. Allez dans **"Variables"**
2. Ajoutez :
   ```
   OPENAI_API_KEY=...
   NOTION_API_KEY=...
   NOTION_DATABASE_ID=...
   PORT=8500
   ```

### Étape 4 : Générer un domaine

1. Allez dans **"Settings"**
2. Cliquez sur **"Generate Domain"**
3. Votre app sera accessible sur : `https://xxx.railway.app`

---

## Option 3 : Fly.io (Gratuit)

**Avantages** :
- ✅ Gratuit (avec limites)
- ✅ Très performant
- ✅ Déploiement mondial

### Étape 1 : Installer Fly CLI

```bash
# Sur macOS
brew install flyctl

# Ou avec curl
curl -L https://fly.io/install.sh | sh
```

### Étape 2 : Se connecter

```bash
flyctl auth signup
# ou
flyctl auth login
```

### Étape 3 : Lancer l'application

```bash
flyctl launch
```

Répondez aux questions :
- **App name** : `vocal-to-notion`
- **Region** : Choisissez le plus proche
- **PostgreSQL** : Non
- **Redis** : Non

### Étape 4 : Configurer les secrets

```bash
flyctl secrets set OPENAI_API_KEY="votre_clé"
flyctl secrets set NOTION_API_KEY="votre_clé"
flyctl secrets set NOTION_DATABASE_ID="votre_id"
```

### Étape 5 : Déployer

```bash
flyctl deploy
```

Votre app sera sur : `https://vocal-to-notion.fly.dev`

---

## 📝 Fichiers nécessaires pour le déploiement

### Procfile

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```

### runtime.txt

```
python-3.11.0
```

### requirements.txt (mis à jour)

Ajouter :
```
gunicorn==21.2.0
```

### .dockerignore (optionnel)

```
venv/
__pycache__/
*.pyc
.env
.git/
uploads/*
!uploads/.gitkeep
```

---

## 🔒 Sécurité

### Ne JAMAIS commiter les secrets

Assurez-vous que `.env` est dans `.gitignore` :

```bash
# Vérifier
cat .gitignore | grep .env

# Si absent, ajoutez-le
echo ".env" >> .gitignore
```

### Variables d'environnement

Toujours configurer les clés API via les variables d'environnement de la plateforme, JAMAIS dans le code.

---

## 🐛 Dépannage

### Erreur "Application failed to start"

- Vérifiez les logs : `flyctl logs` ou dans l'interface Render/Railway
- Vérifiez que toutes les variables d'environnement sont définies
- Vérifiez que Gunicorn est dans requirements.txt

### Erreur "ModuleNotFoundError"

- Vérifiez que requirements.txt contient toutes les dépendances
- Relancez le build

### Erreur "Port already in use"

- Sur Render/Railway/Fly, utilisez `$PORT` (variable fournie par la plateforme)
- Modifiez `app.py` pour utiliser `os.getenv('PORT', 8500)`

### L'enregistrement audio ne fonctionne pas

- ⚠️ Le microphone nécessite HTTPS ou localhost
- Les plateformes gratuites fournissent automatiquement HTTPS
- Si problème, vérifiez les permissions dans les paramètres du navigateur

---

## 📊 Comparaison des plateformes

| Plateforme | Prix | Facilité | Performance | Limites |
|------------|------|----------|-------------|---------|
| **Render** | Gratuit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 750h/mois, sleep après 15min |
| **Railway** | $5 crédit/mois | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $5/mois en crédit |
| **Fly.io** | Gratuit | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 3 VMs gratuites |

**Recommandation** : Commencez avec **Render** pour sa simplicité, puis passez à Railway ou Fly.io si vous avez besoin de plus de performances.

---

## ✅ Vérification du déploiement

Une fois déployé :

1. **Ouvrez l'URL** de votre application
2. **Autorisez le microphone** (votre navigateur demandera la permission)
3. **Enregistrez un test** vocal
4. **Vérifiez dans Notion** que la page est créée

---

## 🎯 Prochaines étapes

Après le déploiement :

1. **Domaine personnalisé** : Configurez un nom de domaine custom
2. **Monitoring** : Configurez des alertes (UptimeRobot, etc.)
3. **Analytics** : Ajoutez Google Analytics si nécessaire
4. **Backup** : Sauvegardez régulièrement votre base Notion

---

## 📞 Support

Si vous rencontrez des problèmes :
- Consultez les logs de la plateforme
- Vérifiez que toutes les variables d'environnement sont définies
- Testez localement d'abord avec `gunicorn app:app`

---

Bon déploiement ! 🚀

