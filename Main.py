# main.py – Full AI Voice Bot (Multilingual)
from speak import speak
from transcribe import transcribe_audio
from ai_reply import get_ai_reply
import sounddevice as sd
import scipy.io.wavfile as wav

def record_voice(filename="input.wav", duration=5, fs=44100):
    print("🎙️ Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, recording)
    print("✅ Voice recorded and saved.")

def run_voice_bot():
    record_voice()
    text = transcribe_audio("input.wav")
    print(f"📝 You said: {text}")
    reply = get_ai_reply(text)
    print(f"🤖 Bot says: {reply}")
    speak(reply)

if __name__ == "__main__":
    run_voice_bot()