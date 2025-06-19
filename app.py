# ✅ app.py (lightweight version for Render hosting)

from flask import Flask, request, jsonify
from groq import Groq
from gtts import gTTS
from langdetect import detect
import os

app = Flask(__name__)

# Load GROQ API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "NVSevaBot is live!"

@app.route("/voice", methods=["POST"])
def voice():
    try:
        # Simulated input for Render testing (since we can't record)
        text = "Tell me about child nutrition."
        print("User said:", text)

        # Detect language (if needed in future)
        language = detect(text)

        # Generate reply
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions related to health, education, and awareness in a simple voice-friendly way."},
                {"role": "user", "content": text}
            ],
            model="mixtral-8x7b-32768"
        )
        reply = response.choices[0].message.content
        print("Bot reply:", reply)

        # Convert to speech and save
        tts = gTTS(reply, lang='en')
        tts.save("output.mp3")

        return jsonify({"response": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)


   
