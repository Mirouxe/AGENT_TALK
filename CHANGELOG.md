# 📝 Changelog - Vocal → Notion

## Version 1.1 - Optimisation pour longs enregistrements (25/10/2025)

### ✅ Améliorations majeures

#### Backend
- **Timeout serveur augmenté** : 300s → 900s (15 minutes)
- Support des enregistrements jusqu'à **15 minutes**
- Ajout de `--max-requests` pour meilleure stabilité
- Worker class `sync` pour traiter les longues requêtes

#### Frontend
- **Timeout fetch augmenté** : 15 minutes côté client
- **Avertissements automatiques** dans la console :
  - À 10 minutes : recommandation de découper
  - À 15 minutes : limite maximale recommandée
- **Message informatif** dans l'interface : "Optimisé pour les longues réflexions (jusqu'à 15 minutes)"
- **AbortController** pour gérer proprement les timeouts

#### Enregistrement audio
- **Timeslice 100ms** : capture audio toutes les 100ms (pas de perte)
- **Meilleure gestion des formats** : fallback automatique (webm → ogg)
- **Logs de debug** : taille des chunks dans la console
- **Vérification des chunks** : ignore les chunks vides

### 📊 Nouvelles limites

| Paramètre | Avant | Maintenant |
|-----------|-------|------------|
| Timeout serveur | 120s (2 min) | 900s (15 min) |
| Timeout client | Aucun | 900s (15 min) |
| Durée recommandée | 2-5 min | Jusqu'à 15 min |
| Taille fichier max | 25 MB (Whisper) | 25 MB (Whisper) |

### 🎯 Cas d'usage optimisés

- ✅ **Notes rapides** (< 2 min) : Très rapide
- ✅ **Réflexions moyennes** (2-5 min) : Rapide
- ✅ **Longues pensées** (5-10 min) : Optimisé ⭐
- ✅ **Très longs enregistrements** (10-15 min) : Supporté
- ⚠️ **> 15 minutes** : Recommandé de découper

### 🔧 Détails techniques

**Procfile**
```bash
gunicorn app:app 
  --timeout 900          # 15 minutes
  --workers 2            # 2 workers
  --worker-class sync    # Synchrone pour longues requêtes
  --max-requests 1000    # Redémarre après 1000 requêtes
```

**MediaRecorder (JavaScript)**
```javascript
mediaRecorder.start(100); // Timeslice 100ms
```

### 📈 Temps de traitement estimés

| Durée audio | Transcription | Nettoyage | Total |
|-------------|---------------|-----------|-------|
| 1 minute | ~10-15s | ~5s | ~15-20s |
| 5 minutes | ~40-60s | ~15s | ~55s-1min15 |
| 10 minutes | ~1min20-2min | ~25s | ~1min45-2min25 |
| 15 minutes | ~2min-3min | ~35s | ~2min35-3min35 |

---

## Version 1.0 - Version initiale (25/10/2025)

### ✅ Fonctionnalités

- Enregistrement audio via MediaRecorder API
- Transcription avec Whisper API (OpenAI)
- Nettoyage et structuration avec GPT-4
- Création automatique de pages Notion
- Interface web moderne et responsive
- Support HTTPS pour microphone
- Gestion des erreurs avec messages clairs

### 🏗️ Architecture

- **Backend** : Flask + Gunicorn
- **APIs** : OpenAI (Whisper + GPT-4) + Notion
- **Frontend** : HTML5 + CSS3 + JavaScript vanilla
- **Déploiement** : Render / Railway / Fly.io

### 📦 Services

1. **TranscriptionService** : Whisper API
2. **CleaningService** : GPT-4 API
3. **NotionService** : Notion API avec support type `status`

---

## 🔜 Prochaines améliorations possibles

- [ ] Découpage automatique des très longs enregistrements (> 15 min)
- [ ] Indicateur de progression pendant la transcription
- [ ] Sauvegarde locale en cas d'échec
- [ ] Support de plusieurs langues
- [ ] Catégorisation automatique dans Notion
- [ ] Extraction automatique de tâches et dates
- [ ] Mode hors-ligne avec synchronisation
- [ ] Application mobile (PWA)

