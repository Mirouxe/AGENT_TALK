# 📘 Guide de configuration Notion

Ce guide vous aide à configurer votre base de données Notion pour fonctionner avec l'application.

## 🎯 Étape 1 : Créer une intégration Notion

1. Allez sur [www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Cliquez sur **"+ Nouvelle intégration"**
3. Remplissez les informations :
   - **Nom** : `Vocal to Notion` (ou un nom de votre choix)
   - **Workspace** : Sélectionnez votre workspace
   - **Type** : Internal Integration
4. Sélectionnez les **capacités** suivantes :
   - ✅ **Lire le contenu**
   - ✅ **Mettre à jour le contenu**
   - ✅ **Insérer du contenu**
5. Cliquez sur **"Soumettre"**
6. **Copiez le "Internal Integration Token"** (commence par `secret_`)
   - Collez-le dans votre fichier `.env` comme valeur de `NOTION_API_KEY`

## 📊 Étape 2 : Créer ou configurer une base de données

### Option A : Créer une nouvelle base de données

1. Dans Notion, créez une nouvelle page
2. Tapez `/database` et sélectionnez **"Base de données - Vue tableau"**
3. Nommez votre base de données : `📝 Notes Vocales` (ou un nom de votre choix)

### Option B : Utiliser une base de données existante

Vous pouvez utiliser une base de données existante si elle contient les bonnes propriétés.

## 🔧 Étape 3 : Configurer les propriétés de la base de données

Assurez-vous que votre base de données contient **exactement** ces propriétés :

| Nom de la propriété | Type | Obligatoire | Description |
|---------------------|------|-------------|-------------|
| **Name** | Title | ✅ Oui | Le titre de la note (généré automatiquement) |
| **Date** | Date | ✅ Oui | Date et heure de création |
| **Status** | Select | ✅ Oui | Statut de la note |

### Comment ajouter ces propriétés :

1. Cliquez sur **"+ Nouveau"** dans l'en-tête du tableau pour ajouter une colonne
2. Pour la propriété **Date** :
   - Nom : `Date`
   - Type : `Date`
3. Pour la propriété **Status** :
   - Nom : `Status`
   - Type : `Select`
   - Options à créer :
     - `À classer` (couleur de votre choix)
     - `Classé` (optionnel)
     - `Archivé` (optionnel)

### Exemple de structure :

```
┌───────────────────────────┬──────────────┬──────────────┐
│ Name                      │ Date         │ Status       │
├───────────────────────────┼──────────────┼──────────────┤
│ Ma première note - 25/... │ 25/10/2025   │ À classer    │
│ Idées pour le projet -... │ 24/10/2025   │ Classé       │
└───────────────────────────┴──────────────┴──────────────┘
```

## 🔗 Étape 4 : Partager la base de données avec votre intégration

**C'est l'étape la plus importante !** Sans cela, l'application ne pourra pas créer de pages.

1. Ouvrez votre base de données dans Notion
2. Cliquez sur **"Partager"** en haut à droite
3. Dans le champ de recherche, tapez le nom de votre intégration (`Vocal to Notion`)
4. Sélectionnez votre intégration dans la liste
5. Elle devrait apparaître avec l'icône d'un robot 🤖
6. Assurez-vous que les permissions sont sur **"Peut modifier"**

## 🆔 Étape 5 : Obtenir l'ID de la base de données

1. Ouvrez votre base de données dans Notion
2. Cliquez sur **"⋯"** (trois points) en haut à droite
3. Sélectionnez **"Copier le lien vers la vue"**
4. Collez le lien quelque part, il ressemble à :
   ```
   https://www.notion.so/workspace/1234567890abcdef1234567890abcdef?v=...
   ```
5. L'**ID de la base de données** est la longue chaîne de caractères entre le dernier `/` et le `?`
   ```
   1234567890abcdef1234567890abcdef
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   C'est votre Database ID
   ```
6. Copiez cet ID et collez-le dans votre fichier `.env` comme valeur de `NOTION_DATABASE_ID`

## ✅ Étape 6 : Vérifier la configuration

Votre fichier `.env` devrait maintenant ressembler à :

```env
OPENAI_API_KEY=sk-proj-...
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=1234567890abcdef1234567890abcdef
PORT=5000
```

## 🎨 Personnalisation (optionnel)

### Ajouter des propriétés supplémentaires

Vous pouvez ajouter d'autres propriétés à votre base de données :

- **Tags** (Multi-select) : Pour catégoriser vos notes
- **Priorité** (Select) : Haute, Moyenne, Basse
- **Source** (Select) : Mobile, Bureau, etc.

L'application créera les pages sans toucher à ces propriétés supplémentaires, vous pourrez les remplir manuellement.

### Modifier le template de page

Si vous voulez personnaliser comment les pages sont créées, éditez le fichier `services/notion_service.py`.

## 🧪 Test de la configuration

1. Démarrez l'application : `python app.py`
2. Enregistrez un court message vocal
3. Vérifiez qu'une nouvelle page est créée dans votre base de données Notion
4. La page devrait contenir :
   - Un titre avec la date
   - Le contenu structuré
   - La transcription originale en callout
   - Le statut "À classer"

## ❌ Problèmes courants

### "L'intégration n'a pas accès à cette base de données"

**Solution** : Vous avez oublié l'étape 4 ! Partagez la base de données avec votre intégration.

### "Database ID invalide"

**Solutions** :
- Vérifiez que vous avez bien copié l'ID complet (32 caractères)
- Essayez de copier l'ID depuis l'URL quand vous êtes sur la page de la base de données

### "Propriété manquante"

**Solution** : Assurez-vous que votre base de données contient bien les propriétés `Name` (Title), `Date` (Date), et `Status` (Select) avec l'option "À classer".

### Les pages sont créées mais vides

**Solution** : Vérifiez que l'intégration a les permissions "Insérer du contenu" et "Mettre à jour le contenu".

## 📚 Ressources

- [Documentation officielle Notion API](https://developers.notion.com/)
- [Guide des intégrations Notion](https://www.notion.so/help/create-integrations-with-the-notion-api)
- [Propriétés des bases de données](https://developers.notion.com/reference/property-object)

---

Si vous rencontrez des problèmes, vérifiez les logs de l'application dans le terminal pour plus de détails sur l'erreur.

