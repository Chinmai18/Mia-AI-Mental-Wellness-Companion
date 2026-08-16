import ollama

def analyze_user_state(chat_history):
    prompt = f"""
You are a mental health analysis assistant.

Analyze the user's overall mental state from the conversation.

Identify:

1. Main issue (ONE word only):
   stress / anxiety / depression / fear / burnout / neutral /ptsd / other mental health psycological issues

2. Severity:
   low / medium / high

3. Pattern:
   temporary / recurring / worsening

Conversation:
{chat_history}

Output STRICTLY in this format:
issue: <type>
severity: <level>
pattern: <type>
"""

    response = ollama.chat(
      model="phi3",
      messages=[
         {"role": "user", "content": prompt}
      ],
      options={
         "temperature": 0.7,
         "num_predict": 120
      }
   )

    return response["message"]["content"]