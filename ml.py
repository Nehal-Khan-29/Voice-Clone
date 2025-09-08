import os
import numpy as np
import librosa
import soundfile as sf

UPLOAD_FOLDER = "static/uploads/"
PROCESSED_FOLDER = "static/processed/"
MODEL_PATH = "static/models/"

# -------------------------
# Silence trimming function
# -------------------------
def trim_audio(file_path, top_db=20):
    """Trim leading and trailing silence and return trimmed waveform."""
    y, sr = librosa.load(file_path, sr=16000)
    y_trimmed, _ = librosa.effects.trim(y, top_db=top_db)
    return y_trimmed, sr

# -------------------------
# Join audio function
# -------------------------
def join_audios(file_path):
    """Join multiple audio files into one."""
    combined = []
    for file in os.listdir(file_path):
        if file.endswith(".wav"):
            filepath = os.path.join(file_path, file)
            y, sr = librosa.load(filepath, sr=16000)
            combined.append(y)
    if combined:
        return np.concatenate(combined)
    else:
        return np.array([])

# -------------------------
# Training code
# -------------------------
def trainingcode(username):

    # Clear old processed files
    for f in os.listdir(PROCESSED_FOLDER):
        os.remove(os.path.join(PROCESSED_FOLDER, f))

    # Step 1: Trim all uploads and save in processed folder
    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith(".wav"):
            filepath = os.path.join(UPLOAD_FOLDER, file)
            y_trimmed, sr = trim_audio(filepath)
            processed_path = os.path.join(PROCESSED_FOLDER, file)
            sf.write(processed_path, y_trimmed, sr)

    # Step 2: Join all processed audio files
    combined_audio = join_audios(PROCESSED_FOLDER)

    # Step 3: Save the combined audio as the "model"
    combined_path = os.path.join(MODEL_PATH, f"{username}.wav")
    if os.path.exists(combined_path):  # overwrite if exists
        os.remove(combined_path)
    sf.write(combined_path, combined_audio, 16000)

    print(f"✅ Model for {username} created successfully")
