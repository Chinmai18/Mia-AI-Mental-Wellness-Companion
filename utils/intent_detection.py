import ollama

def detect_intent(user_input):
    prompt = f"""
    Identify the user's intent from this message.

    Possible intents:
    - venting (just expressing feelings)
    - advice (seeking help or solution)
    - emotional_distress (sad, anxious, overwhelmed)
    - crisis (self-harm, suicidal thoughts)

    Message:
    {user_input}

    Return only ONE word:
    venting / advice / emotional_distress / crisis
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

    return response["message"]["content"].strip().lower()

    