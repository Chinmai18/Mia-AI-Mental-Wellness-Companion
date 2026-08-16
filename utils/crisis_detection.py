def is_crisis(text):
    words = [
        "die", "kill myself", "suicide",
        "end my life", "i want to die"
    ]
    text = text.lower()
    return any(w in text for w in words)

def crisis_response():
    return """
I'm really sorry you're feeling this overwhelmed 💙

Please reach out immediately:
📞 India Suicide Helpline: 9152987821   

You matter. You're not alone.
"""

