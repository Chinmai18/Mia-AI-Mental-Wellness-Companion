import ollama

def generate_journal_prompt(emotion):
    prompt = f"""
    Generate ONE simple journaling question for someone feeling {emotion}.
    Keep it supportive and easy to answer.
    """

    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.5,
            "num_predict": 60
        }
    )

    return response["message"]["content"]
