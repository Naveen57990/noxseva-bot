from gtts import gTTS
from playsound import playsound
from langdetect import detect

def speak(text):
    try:
        # Detect language of the text
        lang = detect(text)

        # Convert text to speech using Google TTS
        tts = gTTS(text=text, lang=lang)

        # Save the output in the current folder
        output_path = "response.mp3"
        tts.save(output_path)

        # Play the audio response
        playsound(output_path)

    except Exception as e:
        print("❌ Error while speaking:", e)