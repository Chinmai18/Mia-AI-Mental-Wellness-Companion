import ollama
import json
import datetime


# ---------------------------
# 1. MOOD DETECTION
# ---------------------------
def detect_mood(chat_history):
    prompt = f"""
Classify mood into ONLY one word:
happy / sad / stressed / neutral

Chat:
{chat_history}
"""

    res = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0}
    )

    return res["message"]["content"].strip().lower()


# ---------------------------
# 2. CORE TASKS (LLM BASED - STABLE HABITS)
# ---------------------------
def generate_core_tasks(chat_history):

    prompt = f"""
You are a CBT therapist.

Based on user chat:
{chat_history}

Generate EXACTLY 6 DAILY CORE HABIT TASKS.

Rules:
- same structure every day (habits)
- focus on: sleep, hydration, exercise, mindfulness, journaling, digital detox
- MUST be short tasks
- return ONLY Python list of 6 strings
- no explanation

example------
analyze the chat **identify user issues, problems such as stress, anxiety, depression, overthinking, pressure, types of depressions as ptsd, etc... and other psycological mental health issues **according to the type of issue they are facing  assign tasks which are atleast 8  that could help user overcome the issues and improve mental health, the tasks should be for 10 to 15 days(for example the identified issue is stress according analysis of user chat then recommend tart with 5–10 Minutes of Morning Mindfulness
Before checking your phone, spend time meditating, doing deep breathing (such as the 4-7-8 technique), or simply sitting in silence to set a calm tone for the day.
Exercise for at Least 20–30 Minutes
Engage in physical activity—brisk walking, yoga, or running—to release endorphins, which act as natural mood lifters and reduce stress hormones.
Journal Three Daily Gratitudes
Write down three specific things you are grateful for each day to rewire your brain to focus on positives rather than ruminating on stressors.
Prioritize "One Thing" and Set Boundaries
Identify your most important task for the day, complete it first, and practice saying "no" to non-essential demands to avoid becoming overwhelmed.
Unplug for a Digital Break
Get Outside for Natural Light
Spend at least 10–15 minutes outside to boost mood, reduce cortisol levels, and ground your senses.
Practice Mindful Eating
Take at least one meal away from your desk, savoring the food slowly without distractions to turn eating into a relaxing, nurturing experience rather than a rushed task.
Establish a Bedtime Relaxation Routine
Create a consistent, screen-free routine (e.g., reading, stretching, or warm bath) to ensure 7-9 hours of quality sleep, which is essential for emotional regulation.
in this way give user tasks and for other issues also identify and give


-like the above exampples suggest the tasks to user 
"""
    res = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.4}
    )

    raw = res["message"]["content"]

    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        return json.loads(raw[start:end].replace("'", '"'))
    except:
        return [
            "Drink enough water today",
            "Do 5 min breathing exercise",
            "Write 3 gratitude points",
            "Take a short walk",
            "Avoid excessive screen time",
            "Sleep on time"
        ]


# ---------------------------
# 3. DAILY TASKS (MOOD BASED)
# ---------------------------
def generate_daily_tasks(chat_history, mood, memory):

    prompt = f"""
You are a CBT-based AI therapist.

User mood: {mood}

User memory:
{memory}

Chat:
{chat_history}

Generate EXACTLY 4 DAILY VARIATION TASKS.

Rules:
- mood sensitive
- motivational + emotional support
- return ONLY Python list of 4 strings
- no explanation
"""

    res = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.6}
    )

    raw = res["message"]["content"]

    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        return json.loads(raw[start:end].replace("'", '"'))
    except:
        return [
            "Take a short peaceful walk",
            "Write your feelings",
            "Practice deep breathing",
            "Listen to calming music"
        ]


# ---------------------------
# 4. MEMORY ENGINE (7-DAY INSIGHT)
# ---------------------------
def generate_memory(log_data):

    prompt = f"""
You are an AI therapist memory system.

Analyze last 7 days task behavior:
{log_data}

Return ONLY:
- mood trend
- discipline level
- improvement suggestion
"""

    res = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.3}
    )

    return res["message"]["content"]