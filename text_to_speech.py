import os
from google.cloud import texttospeech

# Set your credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/get_credentials.json"


def text_to_audio_google_cloud(text, filename="poem.mp3"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    audio_path = os.path.join("static", "audio")
    os.makedirs(audio_path, exist_ok=True)
    full_path = os.path.join(audio_path, filename)

    with open(full_path, "wb") as out:
        out.write(response.audio_content)

    return f"/static/audio/{filename}"
