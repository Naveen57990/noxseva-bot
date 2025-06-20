from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from groq import Groq  # Make sure this is in your requirements.txt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/voice", methods=["POST"])
def voice():
    # Ask the user to say something
    response = VoiceResponse()
    gather = Gather(input="speech", timeout=5, speechTimeout="auto", action="/ai-reply", method="POST")
    gather.say("Hello! This is NVSevaBot. How can I help you today?")
    response.append(gather)
    response.redirect("/voice")  # If no speech input, repeat
    return Response(str(response), mimetype="application/xml")

@app.route("/ai-reply", methods=["POST"])
def ai_reply():
    user_input = request.form.get("SpeechResult", "")
    
    # Call Groq API to generate a reply
    try:
        chat_response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Or llama3 or any model supported
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_message = chat_response.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")  
        ai_message = "Sorry, I had a problem generating a response."

    # Respond to user
    response = VoiceResponse()
    response.say(ai_message)
    response.redirect("/voice")
    return Response(str(response), mimetype="application/xml")
@app.route("/", methods=["GET"])
def home():
    return "✅ NVSevaBot is live!"

@app.route("/test", methods=["GET"])
def test_groq():
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of India?"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq test error: {e}"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
