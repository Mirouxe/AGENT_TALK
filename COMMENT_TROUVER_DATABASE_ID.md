# 🔍 Comment trouver votre Database ID Notion

## ❌ Problème détecté

Vous avez fourni l'ID d'une **page** Notion au lieu d'une **base de données**.

**Votre ID actuel** : `29721d786acc800ab175c698fae0a027`  
→ C'est l'ID d'une **page**, pas d'une **base de données** !

---

## ✅ Solution : Créer ou trouver une base de données

### Option 1 : Créer une NOUVELLE base de données (RECOMMANDÉ)

1. **Ouvrez Notion**

2. **Créez une nouvelle page**
   - Cliquez sur "+ Nouvelle page" dans la barre latérale

3. **Ajoutez une base de données**
   - Dans la page, tapez `/database`
   - Sélectionnez **"Base de données - Vue tableau"** (ou "Table database")
   - Nommez-la : `📝 Notes Vocales`

4. **Configurez les propriétés**
   
   Assurez-vous que votre base contient **exactement** ces 3 propriétés :
   
   | Nom | Type | Comment l'ajouter |
   |-----|------|-------------------|
   | **Name** | Title | (Déjà présent par défaut) |
   | **Date** | Date | Cliquez sur "+", choisissez "Date" |
   | **Status** | Select | Cliquez sur "+", choisissez "Select", ajoutez l'option "À classer" |

5. **Partagez avec votre intégration** ⚠️ IMPORTANT !
   - Cliquez sur **"Partager"** en haut à droite
   - Recherchez votre intégration (le nom que vous avez donné lors de la création)
   - Cliquez dessus pour l'inviter
   - Elle devrait apparaître avec un icône 🤖

6. **Copiez l'ID de la base de données**
   - Cliquez sur **"⋯"** (trois points) en haut à droite de la base
   - Sélectionnez **"Copier le lien"**
   - Le lien ressemble à :
     ```
     https://www.notion.so/workspace/DATABASE_ID?v=...
     ```
   - L'ID est entre le dernier `/` et le `?`

### Option 2 : Utiliser une base de données existante

Si vous avez déjà une base de données :

1. **Ouvrez la base de données** (pas la page qui la contient !)
   - Cliquez directement sur le titre de la base de données
   - L'URL devrait changer

2. **Vérifiez que c'est bien une base de données**
   - Vous devez voir des colonnes et des lignes (comme un tableau)
   - Si vous voyez juste du texte, c'est une page, pas une base !

3. **Ajoutez les propriétés manquantes** (si nécessaire)
   - Name (Title) - déjà présent
   - Date (Date)
   - Status (Select) avec l'option "À classer"

4. **Partagez avec votre intégration**
   - Partager → Inviter votre intégration

5. **Copiez l'ID**
   - ⋯ → Copier le lien
   - Extrayez l'ID

---

## 🔧 Comment mettre à jour votre configuration

Une fois que vous avez le **bon** ID de base de données :

1. **Ouvrez le fichier `.env`** dans votre éditeur
   ```bash
   # Sur macOS/Linux
   nano .env
   # ou utilisez votre éditeur préféré
   ```

2. **Remplacez la ligne NOTION_DATABASE_ID**
   ```env
   NOTION_DATABASE_ID=VOTRE_NOUVEL_ID_ICI
   ```

3. **Sauvegardez** le fichier

4. **Relancez le test**
   ```bash
   python test_pipeline.py
   ```

---

## 📸 Indices visuels

### ✅ C'est une BASE DE DONNÉES si vous voyez :
- Des **colonnes** avec des noms (Name, Date, Status, etc.)
- Des **lignes** pour ajouter des entrées
- Un bouton **"Nouveau"** pour ajouter une ligne
- Des options de **tri** et **filtre** en haut

### ❌ C'est une PAGE si vous voyez :
- Du texte normal, des titres, des paragraphes
- Pas de structure de tableau
- Une base de données **intégrée** dans la page (mais ce n'est pas la page elle-même)

---

## 🆘 Toujours des problèmes ?

### Astuce pour être sûr d'avoir le bon ID :

Quand vous êtes sur votre base de données et que vous copiez le lien, il devrait ressembler à :

```
https://www.notion.so/workspace/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p?v=...
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                C'est ça votre Database ID
                                (32 caractères hexadécimaux)
```

**Nettoyez les tirets** si vous en avez :
- ❌ Mauvais : `1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p`
- ✅ Bon : `1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p`

---

## 🎯 Récapitulatif rapide

1. Créez une **base de données** (pas une page !)
2. Ajoutez les propriétés : Name, Date, Status
3. **Partagez** avec votre intégration ← NE PAS OUBLIER !
4. Copiez l'ID depuis le lien de la base
5. Mettez à jour votre fichier `.env`
6. Relancez `python test_pipeline.py`

Vous devriez voir ✅ sur tous les tests !

