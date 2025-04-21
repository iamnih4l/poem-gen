import os
import time
from flask import Flask, render_template, request
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import texttospeech

# Load env vars
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\nihal\poem-ai\credentials\get_credentials.json.json"

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# Flask app
app = Flask(__name__)

def generate_poem(prompt):
    poem_response = model.generate_content(f"Write a beautiful poem based on this prompt:\n\n{prompt}")
    time.sleep(2)
    explanation_response = model.generate_content(f"Explain the beautiful philosophy behind the generated poem line by line:\n\n{poem_response.text}")
    return poem_response.text, explanation_response.text

def text_to_audio(text, filename="poem.mp3"):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Wavenet-D")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    audio_path = os.path.join("static", "audio")
    os.makedirs(audio_path, exist_ok=True)
    full_path = os.path.join(audio_path, filename)

    with open(full_path, "wb") as out:
        out.write(response.audio_content)

    return f"/static/audio/{filename}"

@app.route('/', methods=['GET', 'POST'])
def index():
    poem, explanation, audio_url = None, None, None

    if request.method == 'POST':
        prompt = request.form['prompt']
        poem, explanation = generate_poem(prompt)
        audio_url = text_to_audio(poem)

        explanation_lines = explanation.split("\n")
        formatted_explanation = [f"<b>Line {idx + 1}:</b> {line}" for idx, line in enumerate(explanation_lines)]

        return render_template('index.html', poem=poem, explanation=formatted_explanation, audio_url=audio_url)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
