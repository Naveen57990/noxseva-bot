from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Load your Groq API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=groq_api_key)

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult")
    response = VoiceResponse()

    if user_input:
        try:
            chat_response = client.chat.completions.create(
                messages=[{"role": "user", "content": user_input}],
                model="mixtral-8x7b-32768",
            )
            bot_reply = chat_response.choices[0].message.content.strip()
        except Exception as e:
            bot_reply = "Sorry, there was a problem. Please try again later."
            print(f"Error getting AI reply: {e}")
    else:
        bot_reply = "I didn't catch that. Please say it again."

    response.say(bot_reply, voice='Polly.Aditi')  # Optional: Customize voice
    response.pause(length=1)
    response.redirect("/voice")  # Loop back for next input

    return str(response)

@app.route("/")
def home():
    return "NVSevaBot is live and ready to talk on phone!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
