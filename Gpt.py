import openai

openai.api_key = "YOUR_OPENAI_API_KEY"  # 🔁 Replace this with your actual API key

def ask_bot(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for health, education, and awareness."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print(ask_bot("How can I stay healthy?"))