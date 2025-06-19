from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import requests
import whisper
from groq import Groq
import speak
from langdetect import detect

app = Flask(__name__)
model = whisper.load_model("base")

@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    resp.say("Hello! Please ask your question after the beep.", language="en-IN")
    resp.record(timeout=3, max_length=10, action="/process", transcribe=False)
    return str(resp)

@app.route("/process", methods=["POST"])
def process():
    recording_url = request.form['RecordingUrl'] + ".wav"
    r = requests.get(recording_url)
    with open("input.wav", "wb") as f:
        f.write(r.content)

    result = model.transcribe("input.wav")
    query = result["text"]
    lang = detect(query)
    print("User said:", query)
    print("Detected language:", lang)

    answer = gpt.ask_bot(query)
    speak.speak(answer, lang)

    resp = VoiceResponse()
    resp.play("response.mp3")
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)
