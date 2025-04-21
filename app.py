import os
import pyttsx3
from google.cloud import texttospeech

# Set your Google Cloud credentials securely
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\nihal\poem-ai\credentials\get_credentials.json.json"

# Main function to decide between Google Cloud or pyttsx3
def text_to_audio(text, use_google_cloud=True, filename="poem.mp3"):
    if use_google_cloud:
        return get_google_cloud_tts_audio(text, filename)
    else:
        return pyttsx3_audio_to_file(text, filename)

# Fallback: offline TTS using pyttsx3
def pyttsx3_audio_to_file(text, filename):
    engine = pyttsx3.init()
    audio_path = os.path.join("static", "audio")
    os.makedirs(audio_path, exist_ok=True)
    full_path = os.path.join(audio_path, filename)

    engine.save_to_file(text, full_path)
    engine.runAndWait()

    return f"/static/audio/{filename}"

# Google Cloud TTS
def get_google_cloud_tts_audio(text, filename="poem.mp3"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audio_path = os.path.join("static", "audio")
    os.makedirs(audio_path, exist_ok=True)
    full_path = os.path.join(audio_path, filename)

    with open(full_path, "wb") as out:
        out.write(response.audio_content)

    return f"/static/audio/{filename}"
