# ⚡ Déploiement Rapide (5 minutes)

Guide ultra-rapide pour déployer votre application en ligne.

## 🎯 Option recommandée : Render

### Étape 1 : Créer un compte GitHub (si vous n'en avez pas)

1. Allez sur [github.com](https://github.com)
2. Créez un compte gratuit

### Étape 2 : Pousser votre code sur GitHub

```bash
# Dans le dossier de votre application
./deploy.sh
```

Ce script va :
- ✅ Initialiser Git
- ✅ Créer un commit
- ✅ Vous demander l'URL de votre dépôt GitHub

**Créer le dépôt sur GitHub** :
1. Allez sur [github.com/new](https://github.com/new)
2. Nom : `agent-talk` (ou autre)
3. Public ou Privé : votre choix
4. Cliquez sur **"Create repository"**
5. Copiez l'URL (format: `https://github.com/USERNAME/agent-talk.git`)
6. Collez-la quand le script vous le demande

### Étape 3 : Déployer sur Render

1. **Allez sur** [render.com](https://render.com)

2. **Créez un compte** (utilisez votre compte GitHub pour plus de facilité)

3. **Cliquez sur "New +"** → **"Web Service"**

4. **Connectez votre dépôt GitHub**
   - Autorisez Render à accéder à vos dépôts
   - Sélectionnez `agent-talk`

5. **Configuration** :
   - **Name** : `vocal-to-notion` (ou un nom de votre choix)
   - **Region** : Oregon (US West) ou Frankfurt (Europe) selon votre localisation
   - **Branch** : `main`
   - **Runtime** : Python 3
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type** : **Free** ✅

6. **Variables d'environnement** :
   
   Descendez jusqu'à **"Environment Variables"** et ajoutez :
   
   | Key | Value |
   |-----|-------|
   | `OPENAI_API_KEY` | Votre clé OpenAI (commence par `sk-`) |
   | `NOTION_API_KEY` | Votre clé Notion (commence par `secret_` ou `ntn_`) |
   | `NOTION_DATABASE_ID` | L'ID de votre base Notion (32 caractères) |
   | `PORT` | `10000` |

7. **Cliquez sur "Create Web Service"**

### Étape 4 : Attendre le déploiement

Render va :
- 📦 Cloner votre code
- 📥 Installer les dépendances
- 🚀 Démarrer l'application

Cela prend environ **2-3 minutes**.

### Étape 5 : Accéder à votre application

Une fois déployée, vous verrez :
```
🎉 Live at https://vocal-to-notion.onrender.com
```

Cliquez sur le lien pour accéder à votre application !

---

## ✅ C'est tout !

Votre application est maintenant en ligne ! 🎉

### 📱 Utilisation

1. Ouvrez l'URL de votre application
2. Autorisez le microphone (votre navigateur demandera)
3. Enregistrez un message vocal
4. Vérifiez dans Notion !

---

## ⚠️ Points importants

### Mise en veille automatique (Plan gratuit)

Les instances gratuites Render s'endorment après **15 minutes** d'inactivité.

**Ce que ça signifie** :
- La première visite après 15 min prendra ~30 secondes à charger
- Les visites suivantes seront rapides

**Solution si vous voulez éviter ça** :
- Passer au plan payant ($7/mois)
- Ou utiliser un service de "keep-alive" (UptimeRobot)

### Logs et monitoring

Pour voir ce qui se passe :
1. Allez sur votre dashboard Render
2. Cliquez sur votre service
3. Onglet **"Logs"**

### Mettre à jour votre application

Quand vous modifiez votre code :

```bash
git add .
git commit -m "Mise à jour de l'application"
git push origin main
```

Render détectera automatiquement les changements et redéploiera ! 🔄

---

## 🐛 Problèmes courants

### "Build failed"

- Vérifiez que `requirements.txt` contient toutes les dépendances
- Regardez les logs pour voir l'erreur exacte

### "Application error"

- Vérifiez que toutes les **variables d'environnement** sont définies
- Vérifiez les logs pour voir l'erreur

### "Can't access microphone"

- C'est normal : le microphone nécessite HTTPS
- Render fournit automatiquement HTTPS ✅
- Autorisez le microphone dans les paramètres de votre navigateur

### "Notion error"

- Vérifiez que votre base Notion est **connectée** à votre intégration
- Vérifiez que le `NOTION_DATABASE_ID` est correct

---

## 🎓 Prochaines étapes

### 1. Domaine personnalisé (optionnel)

Au lieu de `xxx.onrender.com`, vous pouvez utiliser votre propre domaine :
- Achetez un domaine (ex: Namecheap, Google Domains)
- Dans Render : Settings → Custom Domain
- Suivez les instructions

### 2. Keep-Alive (optionnel)

Pour éviter la mise en veille :
1. Allez sur [uptimerobot.com](https://uptimerobot.com) (gratuit)
2. Créez un monitor HTTP(s)
3. URL : votre URL Render
4. Interval : 5 minutes
5. UptimeRobot va "pinger" votre app toutes les 5 min

### 3. Améliorations

Idées pour améliorer votre app :
- Ajouter une authentification
- Permettre plusieurs bases Notion
- Ajouter des catégories automatiques
- Extraire des tâches du texte
- Support multi-langues

---

## 📖 Documentation complète

Pour plus de détails et d'autres options de déploiement :
- **DEPLOIEMENT.md** : Guide complet
- **README.md** : Documentation générale

---

## 🆘 Besoin d'aide ?

Si vous bloquez :
1. Vérifiez les logs sur Render
2. Consultez DEPLOIEMENT.md
3. Testez localement d'abord : `python app.py`

---

**Félicitations pour avoir déployé votre application ! 🎉**

