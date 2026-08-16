def get_cbt_prompt(emotion):

    prompts = {
        "stress": "Help user slow down and focus on one thing at a time.",
        "anxiety": "Gently reassure and bring attention to present moment.",
        "sadness": "Validate feelings and encourage small positive steps.",
        "depression": "Encourage small actions and remind they are not alone.",
        "fear": "Help question the fear and bring logical perspective.",
        "burnout": "Encourage rest and self-care without guilt.",
        "neutral": "Keep conversation open and exploratory.",
        "happy": "Encourage gratitude and reflection."
    }

    return prompts.get(emotion, "Be supportive and understanding.")