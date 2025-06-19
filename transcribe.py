import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path="input.wav"):
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == "__main__":
    print(transcribe_audio())