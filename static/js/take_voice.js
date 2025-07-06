let recordings = [];
let currentStream = null;
let mediaRecorder = null;
let chunks = [];

function encodeWAV(audioBuffer) {
    let sampleRate = audioBuffer.sampleRate;
    let numChannels = audioBuffer.numberOfChannels;
    let samples = audioBuffer.getChannelData(0);

    let buffer = new ArrayBuffer(44 + samples.length * 2);
    let view = new DataView(buffer);

    function writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }

    let offset = 0;

    writeString(view, offset, 'RIFF'); offset += 4;
    view.setUint32(offset, 36 + samples.length * 2, true); offset += 4;
    writeString(view, offset, 'WAVE'); offset += 4;
    writeString(view, offset, 'fmt '); offset += 4;
    view.setUint32(offset, 16, true); offset += 4;
    view.setUint16(offset, 1, true); offset += 2;
    view.setUint16(offset, numChannels, true); offset += 2;
    view.setUint32(offset, sampleRate, true); offset += 4;
    view.setUint32(offset, sampleRate * numChannels * 2, true); offset += 4;
    view.setUint16(offset, numChannels * 2, true); offset += 2;
    view.setUint16(offset, 16, true); offset += 2;
    writeString(view, offset, 'data'); offset += 4;
    view.setUint32(offset, samples.length * 2, true); offset += 4;

    for (let i = 0; i < samples.length; i++, offset += 2) {
        let s = Math.max(-1, Math.min(1, samples[i]));
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    return new Blob([view], { type: 'audio/wav' });
}

document.querySelectorAll('.mini').forEach((section, index) => {
    const startBtn = section.querySelector('#startBtn');
    const stopBtn = section.querySelector('#stopBtn');
    const audioPlayback = section.querySelector('#audioPlayback');

    let audioContext;
    let input;
    let processor;

    startBtn.addEventListener('click', async () => {
        startBtn.disabled = true;
        stopBtn.disabled = false;

        currentStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new AudioContext();
        input = audioContext.createMediaStreamSource(currentStream);
        processor = audioContext.createScriptProcessor(4096, 1, 1);

        let audioData = [];

        processor.onaudioprocess = e => {
            audioData.push(new Float32Array(e.inputBuffer.getChannelData(0)));
        };

        input.connect(processor);
        processor.connect(audioContext.destination);

        stopBtn.addEventListener('click', () => {
            processor.disconnect();
            input.disconnect();
            currentStream.getTracks().forEach(track => track.stop());
            stopBtn.disabled = true;
            startBtn.disabled = false;

            let flat = Float32Array.from(audioData.reduce((acc, val) => [...acc, ...val], []));
            let buffer = audioContext.createBuffer(1, flat.length, audioContext.sampleRate);
            buffer.copyToChannel(flat, 0);

            let wavBlob = encodeWAV(buffer);
            recordings[index] = wavBlob;
            audioPlayback.src = URL.createObjectURL(wavBlob);
        }, { once: true });
    });
});

window.getRecordings = () => recordings;

document.getElementById('recordForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const recordings = window.getRecordings();
    const formData = new FormData();

    recordings.forEach((blob, idx) => {
        if (blob) {
            formData.append('audio' + idx , blob, `voice_${idx}.wav`);
        }
    });

    const response = await fetch("/training", {
    method: "POST",
    body: formData
    });

    const data = await response.json();
    if (data.redirect) {
        window.location.href = data.redirect;
    }

});
