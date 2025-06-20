from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(input="speech", timeout=5, speechTimeout="auto", action="/select-language", method="POST")
    gather.say("Welcome to NVSevaBot. Please say English, Hindi, or Telugu to continue.", language="en-IN")
    response.append(gather)
    response.redirect("/voice")
    return Response(str(response), mimetype="application/xml")

@app.route("/select-language", methods=["POST"])
def select_language():
    user_choice = request.form.get("SpeechResult", "").strip().lower()
    
    # Decide language code
    lang_map = {
        "english": "en",
        "hindi": "hi",
        "telugu": "te"
    }
    selected_lang = lang_map.get(user_choice, "en")  # default to English

    response = VoiceResponse()
    gather = Gather(input="speech", timeout=5, speechTimeout="auto", action=f"/ai-reply?lang={selected_lang}", method="POST")
    gather.say("How can I help you today?", language="en-IN")
    response.append(gather)
    response.redirect("/voice")
    return Response(str(response), mimetype="application/xml")

@app.route("/ai-reply", methods=["POST"])
def ai_reply():
    user_input = request.form.get("SpeechResult", "")
    selected_lang = request.args.get("lang", "en")

    try:
        chat_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Reply in {selected_lang}."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_message = chat_response.choices[0].message.content
    except Exception as e:
        ai_message = "Sorry, I had a problem generating a response."

    response = VoiceResponse()
    response.say(ai_message, language="en-IN")  # TTS only supports en-IN for now via Twilio
    response.redirect("/voice")
    return Response(str(response), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)