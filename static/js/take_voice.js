let recordings = []; // Store blobs for all phrases
let currentStream = null;
let mediaRecorder = null;
let chunks = [];

document.querySelectorAll('.mini').forEach((section, index) => {
    const startBtn = section.querySelector('#startBtn');
    const stopBtn = section.querySelector('#stopBtn');
    const audioPlayback = section.querySelector('#audioPlayback');

    startBtn.addEventListener('click', async () => {
        startBtn.disabled = true;
        stopBtn.disabled = false;

        currentStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(currentStream);
        chunks = [];

        mediaRecorder.ondataavailable = e => chunks.push(e.data);

        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/webm' });
            recordings[index] = blob;  // Save this recording
            audioPlayback.src = URL.createObjectURL(blob);
            currentStream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.start();
    });

    stopBtn.addEventListener('click', () => {
        startBtn.disabled = false;
        stopBtn.disabled = true;
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
    });
});
// Expose recordings globally for form submission
window.getRecordings = () => recordings;


document.getElementById('recordForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const recordings = window.getRecordings();
    const formData = new FormData();

    recordings.forEach((blob, idx) => {
        if (blob) {
            formData.append('audio' + idx , blob, `voice_${idx + 1}.mp3`);
        }
    });

    const response = await fetch("/training", {
        method: "POST",
        body: formData
    });

    if (response.redirected) {
        window.location.href = response.url;
    }
});
