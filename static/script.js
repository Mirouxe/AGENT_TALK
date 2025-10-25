// État de l'application
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let recordingStartTime;
let timerInterval;

// Éléments du DOM
const recordBtn = document.getElementById('record-btn');
const statusText = document.getElementById('status-text');
const statusIndicator = document.getElementById('status-indicator');
const recordingInfo = document.getElementById('recording-info');
const timerElement = document.getElementById('timer');
const audioPlayback = document.getElementById('audio-playback');
const processCard = document.getElementById('process-card');
const resultCard = document.getElementById('result-card');
const errorCard = document.getElementById('error-card');

/**
 * Basculer entre démarrer et arrêter l'enregistrement
 */
async function toggleRecording() {
    if (!isRecording) {
        await startRecording();
    } else {
        stopRecording();
    }
}

/**
 * Démarrer l'enregistrement audio
 */
async function startRecording() {
    try {
        // Demander l'accès au microphone
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Créer le MediaRecorder
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        // Collecter les données audio
        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });
        
        // Traiter l'audio quand l'enregistrement s'arrête
        mediaRecorder.addEventListener('stop', handleRecordingComplete);
        
        // Démarrer l'enregistrement
        mediaRecorder.start();
        isRecording = true;
        recordingStartTime = Date.now();
        
        // Mettre à jour l'interface
        updateUIForRecording();
        
        // Démarrer le timer
        startTimer();
        
    } catch (error) {
        console.error('Erreur lors du démarrage de l\'enregistrement:', error);
        showError('Impossible d\'accéder au microphone. Veuillez autoriser l\'accès.');
    }
}

/**
 * Arrêter l'enregistrement audio
 */
function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        // Arrêter le timer
        clearInterval(timerInterval);
        
        // Arrêter le stream
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        
        // Mettre à jour l'interface
        updateUIForStopped();
    }
}

/**
 * Traiter l'enregistrement terminé
 */
async function handleRecordingComplete() {
    // Créer un blob audio
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    
    // Créer une URL pour la lecture
    const audioUrl = URL.createObjectURL(audioBlob);
    audioPlayback.src = audioUrl;
    audioPlayback.style.display = 'block';
    
    // Envoyer l'audio au serveur pour traitement
    await processAudio(audioBlob);
}

/**
 * Envoyer l'audio au serveur pour traitement
 */
async function processAudio(audioBlob) {
    // Afficher la carte de traitement
    processCard.style.display = 'block';
    resultCard.style.display = 'none';
    errorCard.style.display = 'none';
    
    try {
        // Créer un FormData
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        
        // Mettre à jour l'interface - Transcription
        updateStepStatus('step-transcription', 'active', 'En cours...');
        
        // Envoyer au serveur
        const response = await fetch('/api/process-audio', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Erreur lors du traitement de l\'audio');
        }
        
        const result = await response.json();
        
        // Mettre à jour l'interface - Transcription terminée
        updateStepStatus('step-transcription', 'completed', 'Terminé ✓');
        
        // Nettoyage
        updateStepStatus('step-cleaning', 'active', 'En cours...');
        
        // Simuler un délai pour l'affichage
        await new Promise(resolve => setTimeout(resolve, 500));
        updateStepStatus('step-cleaning', 'completed', 'Terminé ✓');
        
        // Notion
        updateStepStatus('step-notion', 'active', 'En cours...');
        await new Promise(resolve => setTimeout(resolve, 500));
        updateStepStatus('step-notion', 'completed', 'Terminé ✓');
        
        // Afficher les résultats
        showResults(result);
        
    } catch (error) {
        console.error('Erreur lors du traitement:', error);
        showError(error.message || 'Une erreur est survenue lors du traitement de votre enregistrement.');
    }
}

/**
 * Mettre à jour le statut d'une étape
 */
function updateStepStatus(stepId, status, text) {
    const step = document.getElementById(stepId);
    const statusElement = step.querySelector('.step-status');
    
    step.className = 'step ' + status;
    statusElement.textContent = text;
}

/**
 * Afficher les résultats
 */
function showResults(result) {
    processCard.style.display = 'none';
    resultCard.style.display = 'block';
    
    document.getElementById('transcription-text').textContent = result.transcription;
    document.getElementById('cleaned-text').textContent = result.cleaned_text;
    document.getElementById('notion-link').href = result.notion_url;
}

/**
 * Afficher une erreur
 */
function showError(message) {
    processCard.style.display = 'none';
    resultCard.style.display = 'none';
    errorCard.style.display = 'block';
    document.getElementById('error-message').textContent = message;
}

/**
 * Réinitialiser l'application
 */
function resetApp() {
    processCard.style.display = 'none';
    resultCard.style.display = 'none';
    errorCard.style.display = 'none';
    audioPlayback.style.display = 'none';
    recordingInfo.style.display = 'none';
    
    // Réinitialiser les étapes
    ['step-transcription', 'step-cleaning', 'step-notion'].forEach(stepId => {
        updateStepStatus(stepId, '', 'En attente...');
    });
    
    // Réinitialiser l'interface d'enregistrement
    recordBtn.innerHTML = '<span class="btn-icon">🎤</span><span class="btn-text">Commencer l\'enregistrement</span>';
    recordBtn.className = 'btn btn-record';
    statusText.textContent = 'Prêt à enregistrer';
    statusIndicator.className = 'status-indicator';
}

/**
 * Démarrer le timer
 */
function startTimer() {
    timerInterval = setInterval(() => {
        const elapsed = Date.now() - recordingStartTime;
        const minutes = Math.floor(elapsed / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
}

/**
 * Mettre à jour l'interface pour l'enregistrement
 */
function updateUIForRecording() {
    recordBtn.innerHTML = '<span class="btn-icon">⏹</span><span class="btn-text">Arrêter l\'enregistrement</span>';
    recordBtn.className = 'btn btn-record recording';
    statusText.textContent = 'Enregistrement en cours...';
    statusIndicator.className = 'status-indicator recording';
    recordingInfo.style.display = 'flex';
    audioPlayback.style.display = 'none';
}

/**
 * Mettre à jour l'interface pour l'arrêt
 */
function updateUIForStopped() {
    recordBtn.innerHTML = '<span class="btn-icon">🎤</span><span class="btn-text">Nouvel enregistrement</span>';
    recordBtn.className = 'btn btn-record';
    statusText.textContent = 'Traitement en cours...';
    statusIndicator.className = 'status-indicator';
    recordingInfo.style.display = 'none';
}

// Vérifier que le navigateur supporte l'API MediaRecorder
if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showError('Votre navigateur ne supporte pas l\'enregistrement audio. Veuillez utiliser un navigateur moderne.');
}

