
import os
from TTS.api import TTS

def testingcode(text, model_path):
    
    # Path to your voice sample
    voice_sample_path = model_path

    # Text you want to synthesize
    text_to_speak = text
    
    username = os.path.splitext(os.path.basename(model_path))[0]

    # Output file (use /kaggle/working/ in Kaggle)
    output_path = f"static/output/{username}_clone.wav"

    # Initialize TTS model
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True, gpu=False)

    # Synthesize speech using your sample
    tts.tts_to_file(
        text=text_to_speak,
        speaker_wav=voice_sample_path,
        file_path=output_path,
        language="en"
    )

    print(f"✅ Voice generated successfully")
    
    return output_path