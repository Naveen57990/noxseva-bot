from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def index():
    return "NOXSevaBot is live and waiting for Twilio calls."

@app.route("/voice", methods=["POST"])
def voice():
    """Initial voice handler"""
    response = VoiceResponse()

    # Let user press a key to interrupt
    gather = Gather(
        input="speech dtmf",
        timeout=5,
        num_digits=1,
        speechTimeout="auto",
        action="/ai-reply",
        method="POST"
    )
    gather.say("Hello! This is NOXSevaBot. How can I help you today?", language="en-IN")
    response.append(gather)

    # If nothing is said or pressed, repeat
    response.redirect("/voice")
    return Response(str(response), mimetype="application/xml")

@app.route("/ai-reply", methods=["POST"])
def ai_reply():
    """Handles user speech and gives AI response"""
    speech_input = request.form.get("SpeechResult", "")
    digits_pressed = request.form.get("Digits", "")

    response = VoiceResponse()

    if digits_pressed:
        # If user pressed a key, restart
        response.say("Restarting the conversation.", language="en-IN")
        response.redirect("/voice")
        return Response(str(response), mimetype="application/xml")

    # Call Groq API for reply
    try:
        chat_response = client.chat.completions.create(
            model="llama3-8b-8192",  # or mixtral if supported
            messages=[
                {"role": "system", "content": "You are a friendly, respectful, and helpful assistant that gives short, clear answers in a calm tone. Avoid long explanations. Speak in simple, easy-to-understand language."},
                {"role": "user", "content": speech_input}
            ]
        )
        ai_text = chat_response.choices[0].message.content
    except Exception as e:
        ai_text = "Sorry, I couldn't generate a response."

    response.say(ai_text, language="en-IN")
    response.redirect("/voice")  # Continue the conversation
    return Response(str(response), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)