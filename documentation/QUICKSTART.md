# 🚀 Guide de démarrage rapide

Guide ultra-rapide pour mettre en route l'application en moins de 5 minutes.

## ⚡ Installation Express

### 1️⃣ Prérequis

- Python 3.8+ installé
- Compte OpenAI (avec accès API)
- Compte Notion (gratuit)

### 2️⃣ Installation en 4 commandes

```bash
# 1. Créer l'environnement virtuel
python3 -m venv venv

# 2. Activer l'environnement
source venv/bin/activate  # macOS/Linux
# OU
venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer le fichier de configuration
cp .env.example .env
```

### 3️⃣ Configuration (5 minutes)

Éditez le fichier `.env` et ajoutez vos clés :

```env
OPENAI_API_KEY=sk-...              # 👈 Clé depuis platform.openai.com
NOTION_API_KEY=secret_...          # 👈 Clé depuis notion.so/my-integrations
NOTION_DATABASE_ID=...             # 👈 ID de votre base de données
PORT=5000
```

#### 🔑 Où obtenir les clés ?

**OpenAI** :
- 🌐 [platform.openai.com](https://platform.openai.com/) → API Keys → Créer une clé

**Notion** :
- 🌐 [notion.so/my-integrations](https://www.notion.so/my-integrations) → Nouvelle intégration
- ⚠️ **N'oubliez pas** de partager votre base de données avec l'intégration !

**Database ID** :
- Ouvrez votre base de données → ⋯ (trois points) → Copier le lien
- L'ID est la longue chaîne entre le dernier `/` et le `?`

📖 **Guide détaillé** : Voir `GUIDE_NOTION.md` pour les captures d'écran

### 4️⃣ Test de configuration

```bash
python test_api.py
```

Ce script vérifie que toutes vos clés fonctionnent correctement. ✅ = tout est bon !

### 5️⃣ Lancement

```bash
# Option 1 : Script automatique (recommandé)
./start.sh

# Option 2 : Manuelle
python app.py
```

🌐 Ouvrez votre navigateur : **http://localhost:5000**

---

## 🎤 Utilisation

1. **Cliquez** sur "Commencer l'enregistrement"
2. **Autorisez** l'accès au microphone
3. **Parlez** dans votre micro
4. **Cliquez** sur "Arrêter l'enregistrement"
5. **Attendez** quelques secondes (transcription + nettoyage)
6. **Cliquez** sur "Ouvrir dans Notion" pour voir le résultat ! 🎉

---

## 📋 Structure de la base de données Notion

Votre base de données doit contenir ces 3 propriétés :

| Propriété | Type | Valeurs |
|-----------|------|---------|
| **Name** | Title | (auto) |
| **Date** | Date | (auto) |
| **Status** | Select | "À classer" |

➡️ Voir `GUIDE_NOTION.md` pour créer cette structure

---

## 🐛 Problèmes courants

### ❌ "Impossible d'accéder au microphone"
- Utilisez **Chrome** ou **Firefox** (recommandé)
- Vérifiez que vous êtes sur `localhost` ou `https://`
- Autorisez l'accès dans les paramètres du navigateur

### ❌ "Erreur OpenAI"
- Vérifiez votre clé API sur [platform.openai.com](https://platform.openai.com/)
- Assurez-vous d'avoir du **crédit** sur votre compte
- La clé doit commencer par `sk-`

### ❌ "Erreur Notion"
- Avez-vous **partagé** la base de données avec votre intégration ? 👈 Cause #1
- La clé doit commencer par `secret_`
- L'ID de database est-il correct ? (32 caractères)

### ❌ "ModuleNotFoundError"
```bash
# Réinstallez les dépendances
pip install -r requirements.txt
```

---

## 📚 Documentation complète

- 📖 **README.md** : Documentation complète
- 📘 **GUIDE_NOTION.md** : Configuration Notion pas à pas
- 🧪 **test_api.py** : Script de test des APIs

---

## 💡 Conseils

### 🎯 Pour de meilleurs résultats

- Parlez **clairement** et pas trop vite
- Évitez les **bruits de fond**
- Structurez vos idées en phrases complètes
- Utilisez des **pauses** entre les idées

### 💰 Coûts estimés

Les APIs OpenAI sont payantes :

- **Whisper** : ~$0.006 / minute d'audio
- **GPT-4** : ~$0.03 / 1000 tokens (~750 mots)

**Exemple** : Un message vocal de 2 minutes = ~$0.015 (1.5 centime)

### ⚡ Performance

- **Transcription** : ~5-10 secondes pour 1 minute d'audio
- **Nettoyage** : ~3-5 secondes
- **Notion** : ~1-2 secondes

**Total** : ~10-20 secondes pour traiter 1 minute d'audio

---

## 🆘 Besoin d'aide ?

1. Lancez `python test_api.py` pour diagnostiquer
2. Consultez les logs dans le terminal
3. Vérifiez le **README.md** et **GUIDE_NOTION.md**

---

**✅ Vous êtes prêt !** Lancez l'application et commencez à enregistrer vos notes vocales ! 🎙️

