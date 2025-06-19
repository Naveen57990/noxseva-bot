# ai_reply.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_reply(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # You can also try "llama3-70b-8192"
            messages=[
                {"role": "system", "content": "You are a helpful assistant that gives simple and clear voice responses related to health, education, and general awareness."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Bot Error: {str(e)}"
