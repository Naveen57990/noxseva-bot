from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Language and system message mapping
LANGUAGE_MAP = {
    "1": ("en-IN", "You are a helpful assistant."),
    "2": ("hi-IN", "आप एक सहायक सहायक हैं।"),
    "3": ("te-IN", "మీరు సహాయకుడిగా వ్యవహరిస్తారు.")
}


@app.route("/voice", methods=["POST"])
def voice():
    """Initial route: asks user to choose language"""
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/set-language", method="POST", timeout=5)
    gather.say("Welcome to NVSevaBot. Press 1 for English, 2 for Hindi, or 3 for Telugu.")
    response.append(gather)
    response.redirect("/voice")  # Retry if nothing is pressed
    return Response(str(response), mimetype="application/xml")


@app.route("/set-language", methods=["POST"])
def set_language():
    """Handles language selection and prompts for voice input"""
    digit = request.form.get("Digits")
    language, system_msg = LANGUAGE_MAP.get(digit, ("en-IN", "You are a helpful assistant."))

    response = VoiceResponse()
    gather = Gather(
        input="speech",
        timeout=5,
        speech_timeout="auto",
        action=f"/ai-reply?lang={language}&msg={system_msg}",
        method="POST",
        language=language
    )
    gather.say("Please speak now.", language=language)
    response.append(gather)
    response.redirect("/voice")  # Retry on no speech input
    return Response(str(response), mimetype="application/xml")


@app.route("/ai-reply", methods=["POST"])
def ai_reply():
    """Handles user speech and generates AI response"""
    user_input = request.form.get("SpeechResult", "")
    language = request.args.get("lang", "en-IN")
    system_msg = request.args.get("msg", "You are a helpful assistant.")

    try:
        chat_response = client.chat.completions.create(
            model="llama3-8b-8192",  # Use current supported model
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_input}
            ]
        )
        ai_message = chat_response.choices[0].message.content
    except Exception as e:
        ai_message = "Sorry, I had a problem generating a response."

    response = VoiceResponse()
    response.say(ai_message, language=language)
    response.redirect("/voice")
    return Response(str(response), mimetype="application/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)