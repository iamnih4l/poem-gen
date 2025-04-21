from flask import Flask, render_template, request
from gemini_poetry import generate_poem  # your Gemini generation function
from text_to_speech import text_to_audio_google_cloud  # your TTS function
from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_url = None
    generated_poem = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        generated_poem = generate_poem(prompt)
        audio_url = text_to_audio_google_cloud(generated_poem, filename="poem.mp3")

    return render_template("index.html", audio_url=audio_url, poem=generated_poem)

if __name__ == "__main__":
    app.run(debug=True)
