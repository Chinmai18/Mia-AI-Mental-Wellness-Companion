
import streamlit as st
import ollama
import json
import time
import base64
import os
import datetime
from utils.emotion_detection import analyze_emotion
from utils.crisis_detection import is_crisis, crisis_response
from recommendations import*
from memory import*
from memory import save_app_state, load_app_state
from utils.journal import generate_journal_prompt
from database import conn, cursor


st.set_page_config(page_title="Mia 🌸", layout="wide")
st.markdown("""
<style>
/* ============================= */
/* 🌿 MODERN MESH BACKGROUND */
/* ============================= */
.stApp {
    /* A soft, animated mesh gradient of mint, sky blue, and lavender */
    background: radial-gradient(at 0% 0%, #e0f2f1 0, transparent 50%), 
                radial-gradient(at 50% 0%, #e3f2fd 0, transparent 50%), 
                radial-gradient(at 100% 0%, #f3e5f5 0, transparent 50%),
                radial-gradient(at 50% 50%, #f1f8e9 0, transparent 100%),
                #ffffff;
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
}
/* ============================= */
/* ✨ GLASSMORPHISM CARD EFFECT */
/* ============================= */
.card {
    background: rgba(255, 255, 255, 0.7); /* Translucent white */
    backdrop-filter: blur(10px);          /* Frosted glass effect */
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 25px;
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
    margin-bottom: 20px;
}

/* ============================= */
/* 🌿 LAYOUT WIDTH */
/* ============================= */
.block-container {
    max-width: 1200px;   /* 🔥 wider app */
    margin: auto;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ============================= */
/* 🌿 TABS (APP STYLE) */
/* ============================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    justify-content: center;
}

.stTabs [data-baseweb="tab"] {
    background: #ffffff;
    padding: 10px 20px;
    border-radius: 12px;
    border: none;
    color: #555;
    font-weight: 500;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

/* ACTIVE TAB */
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c8f7dc, #e6fff4);  /* 🌿 light green */
    color: #2e7d6b !important;
    font-weight: 600;
    transform: scale(1.05);
}

/* HOVER */
.stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-2px);
}

/* ============================= */
/* 🌿 BUTTONS (LIGHT GREEN) */
/* ============================= */
.stButton>button {
    background: #d4f5e9;
    color: #2e7d6b;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 500;
}
.stButton>button:hover {
    background: #bff0dd;
    color: #1b5e50;
}
/* ============================= */
/* 🌿 INPUT BOX */
/* ============================= */
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
}

.stTextArea textarea {
    border-radius: 10px;
}
/* ============================= */
/* 🌿 CHAT INPUT */
/* ============================= */
[data-testid="stChatInput"] {
    border-radius: 12px;
}
/* ============================= */
/* 🌿 CHECKBOX */
/* ============================= */
.stCheckbox {
    padding: 5px;
}
/* ============================= */
/* 🌿 PROGRESS BAR */
/* ============================= */
.stProgress > div > div > div {
    background-color: #8be0c3;
}
/* ============================= */
/* 🌿 SCROLLBAR */
/* ============================= */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD SAVED STATE ----------------

from memory import load_app_state, save_app_state
saved = load_app_state()
if saved:
    st.session_state.day_count = saved["day_count"]
    st.session_state.chat_ready = saved["chat_ready"]

SYSTEM_PROMPT = """
You are Mia, a caring AI mental wellness companion like Wysa.

Be empathetic, calm, and human-like. Do not sound robotic.
Be supportive and non-judgmental.

Your goal:
- Understand user emotions deeply over multiple messages
- Identify feelings like stress, anxiety, overthinking, sadness, etc (internally only)
- Do NOT diagnose

Conversation flow:
1. Listen first (no quick advice)
2. Validate feelings naturally
3. Ask gentle question if they want to share what is bothering them
4. After understanding, give ONE small helpful suggestion

Use light CBT:
- Help user reflect on thoughts

Rules:
- Keep response SHORT (2–3 lines)
-each response should be completed within 2 to 3 lines
-STRICT: Complete your entire thought in 2 sentences maximum.
- No long paragraphs
- No bullet points
- STRICT LIMIT: Your total response MUST be 2 sentences only.
- Never start a sentence you cannot finish.
- Be natural and complete your thoughts clearly.
- Do not use any HTML, tags, or special formatting.

Special cases:
- If venting → just listen + validate
- If asking help → understand then suggest
- If distress → calm and reassure
- If crisis → support + suggest contacting help

Goal:
Make user feel safe, understood, and open to sharing.
"""

# ---------------- LOGIN / SIGNUP ----------------

if "username" not in st.session_state:

    st.title("🔐 Mia your wellness companion")

    mode = st.radio("Select", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Continue"):

        if username.strip() == "" or password.strip() == "":
            st.warning("Enter both fields")
            st.stop()

        if mode == "Sign Up":

            if user_exists(username):
                st.error("User already exists")
            else:
                create_user(username, password)
                st.success("Account created! Now login.")

        else:
            user = get_user(username, password)

            if user:
                st.session_state.username = username
                st.session_state.day_count = user["day_count"]
                st.session_state.chat_ready = user["chat_ready"]

                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()
# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "✅Daily Tasks", "🌱Healing Garden", "🧘 Wellness Tools", "Analysis Report"])

# =====================================================
# 💬 CHAT
# =====================================================
with tab1:

    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.markdown(f"""
            <div style="
                background:#d1f5d3;
                padding:12px 16px;
                border-radius:16px;
                margin:8px 0;
                max-width:70%;
                margin-left:auto;
                box-shadow:0px 2px 8px rgba(0,0,0,0.05);
            ">
            {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="
                background:#ffffff;
                padding:12px 16px;
                border-radius:16px;
                margin:8px 0;
                max-width:70%;
                box-shadow:0px 2px 8px rgba(0,0,0,0.05);
            ">
            {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

    user_input = st.chat_input("Talk to Mia...")

    if user_input:
        # 1. Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        save_chat("user", user_input)
        
        # 2. Show user bubble immediately (Custom HTML, no icons)
        st.markdown(f"""
            <div style="background:#d1f5d3; padding:12px 16px; border-radius:16px; margin:8px 0; max-width:70%; margin-left:auto; box-shadow:0px 2px 8px rgba(0,0,0,0.05);">
                {user_input}
            </div>
        """, unsafe_allow_html=True)

        mia_placeholder = st.empty()
        import re

        # 4. CHECK CRISIS FIRST
        if is_crisis(user_input):
            bot_reply = crisis_response().strip()
            mia_placeholder.markdown(f"""
                <div style="
                    background:#ffffff;
                    padding:12px 16px;
                    border-radius:16px;
                    margin:8px 0;
                    max-width:70%;
                    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
                ">
                {bot_reply}
                </div>
            """, unsafe_allow_html=True)

        else:
            full_response = ""

            stream = ollama.chat(
                model="phi3:mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages[-4:]   # ✅ FIX: no duplicate user input
                ],
                stream=True,
                options={"temperature": 0.6, "num_predict": 80}
            )

            for chunk in stream:
                if "message" in chunk:
                    content = chunk["message"]["content"]
                    full_response += content

                    # ✅ CLEAN RESPONSE (removes </div> etc)
                    clean_response = re.sub(r"<.*?>", "", full_response)

                    mia_placeholder.markdown(f"""
                        <div style="
                            background:#ffffff;
                            padding:12px 16px;
                            border-radius:16px;
                            margin:8px 0;
                            max-width:70%;
                            box-shadow:0px 2px 8px rgba(0,0,0,0.05);
                        ">
                        {clean_response}
                        </div>
                    """, unsafe_allow_html=True)

            bot_reply = re.sub(r"<.*?>", "", full_response).strip()


        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        save_chat("assistant", bot_reply)
        st.rerun()
# =====================================================
# ✅ TASKS
# =====================================================
import datetime
from recommendations import generate_core_tasks, generate_daily_tasks, detect_mood

with tab2:

    st.subheader("🌿 Healing Garden – AI Therapy Plan")

    today = str(datetime.date.today())

    # ---------------- INIT ----------------
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if "checked" not in st.session_state:
        st.session_state.checked = {}

    if "task_date" not in st.session_state:
        st.session_state.task_date = None

    if "day_count" not in st.session_state:
        st.session_state.day_count = 1

    if "completed_today" not in st.session_state:
        st.session_state.completed_today = False


    # ---------------- CHAT GATE (10 MESSAGES RULE) ----------------
    user_msgs = [
        m["content"] for m in st.session_state.messages if m["role"] == "user"
    ]

    # NEW USER → 15 messages
    if not st.session_state.chat_ready:

        if len(user_msgs) < 15:
            st.info(f"💙 Talk to Mia ({len(user_msgs)}/15) to unlock your Healing Garden 🌿")
        
        else:
            st.session_state.chat_ready = True

            # 🔥 SAVE PERMANENTLY
            update_user(
                st.session_state.username,
                st.session_state.day_count,
                True
            )

            save_app_state(
                st.session_state.day_count,
                True
            )

            st.success("🌿 Healing Garden Unlocked!")
            st.rerun()


    # ---------------- GENERATE TASKS (ONCE DAILY) ----------------
    if st.session_state.task_date != today:

        chat_text = " ".join(user_msgs)

        mood = detect_mood(chat_text)

        core_tasks = generate_core_tasks(chat_text)
        daily_tasks = generate_daily_tasks(chat_text, mood, "")

        st.session_state.tasks = core_tasks + daily_tasks

        st.session_state.task_date = today
        st.session_state.checked = {}
        st.session_state.completed_today = False


    tasks = st.session_state.tasks


    # ---------------- DAY DISPLAY ----------------
    st.write(f"### 🌿 Day {st.session_state.day_count}")
    st.info(f"💭 Mood: {detect_mood(' '.join(user_msgs))}")

    # ---------------- TASK UI ----------------
    completed = 0

    for task in tasks:

        if task not in st.session_state.checked:
            st.session_state.checked[task] = False

        st.session_state.checked[task] = st.checkbox(
            task,
            value=st.session_state.checked[task],
            key=f"{today}_{task}"
        )

        if st.session_state.checked[task]:
            completed += 1


    # ---------------- PROGRESS ----------------
    st.progress(completed / len(tasks))
    st.write(f"🌿 {completed}/{len(tasks)} completed")


    # ---------------- COMPLETE DAY LOGIC ----------------
    if completed == len(tasks) and len(tasks) > 0:

        if not st.session_state.completed_today:

            st.session_state.completed_today = True
            st.session_state.day_count += 1
                
            save_app_state(
                st.session_state.day_count,
                st.session_state.chat_ready
            )
            update_user(
                st.session_state.username,
                st.session_state.day_count,
                st.session_state.chat_ready
            )
            st.success(f"🌱 Day {st.session_state.day_count - 1} completed successfully!")
            st.info(f"🌿 Welcome to Day {st.session_state.day_count}")
                
    if st.session_state.day_count > 12:

        st.success("🌸 You completed the 12-Day Healing Journey!")

        if st.button("🔄 Restart Journey"):
            st.session_state.day_count = 1
            st.session_state.chat_ready = False

            update_user(
                st.session_state.username,
                1,
                False
            )
            st.rerun()

    # ---------------- RESET BUTTON ----------------
    
    if st.button("🔄 Reset Healing Garden"):

        st.session_state.tasks = []
        st.session_state.checked = {}
        st.session_state.task_date = None
        st.session_state.day_count = 1
        st.session_state.completed_today = False
        st.session_state.chat_ready = False

        save_app_state(1, False)

        update_user(
            st.session_state.username,
            1,
            False
        )
        st.rerun()
        
# =====================================================
# 🌱 GARDEN
# ====================================================
with tab3:
    import base64
    import os
    import streamlit as st

    # ---------------- HELPER ----------------
    def get_base64(path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        return None

    # ---------------- LOGIC ----------------
    day = st.session_state.get("day_count", 8)
    completed_days = day - 1

    stages = {
        2: ("🌱 Seed Stage", "assets/stage1.png"),
        4: ("🌿 Sprout Stage", "assets/stage2.png"),
        6: ("🌾 Growing Strong", "assets/stage3.png"),
        8: ("🌾 Growing Strong", "assets/stage4.png"),
        10: ("🌾 Growing Strong", "assets/stage5.png"),
        12: ("🌸 Full Bloom", "assets/stage6.png")
    }

    text, img_path = "🌸 Full Bloom", "assets/stage6.png"
    for limit in sorted(stages.keys()):
        if completed_days <= limit:
            text, img_path = stages[limit]
            break

    bg_path = "assets/garden_bg.jpg"
    bg_base64 = get_base64(bg_path)

    # ---------------- CSS ----------------
    if bg_base64:
        st.markdown(f"""
        <style>
        /* THE MAIN CONTAINER */
        /* THE MAIN CONTAINER */
        .garden-container {{
            position: relative;
            width: 100%;
            height: 650px; /* ⬆️ Increased height slightly */
            background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)),
                            url("data:image/jpg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            border-radius: 25px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start; /* 🌿 Keeps header at the top */
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}

        /* FLOATING HEADER */
        .garden-header {{
            margin-top: 30px; /* ⬇️ Moves it slightly down from the top edge */
            text-align: center;
            background: rgba(255, 255, 255, 0.2); /* 🌫️ Slightly more visible */
            backdrop-filter: blur(15px);
            padding: 12px 40px;
            border-radius: 50px;
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            z-index: 10;
        }}

                /* THE PLANT FIX */
        .plant-anchor {{
            position: absolute;
            bottom: 20px; /* ⬇️ Decreased from 140px to bring it back down */
            left: 50%;
            transform: translateX(-50%);
            z-index: 5;
        }}

        .plant-anchor img {{
            width: 320px; /* Keeps the nice large size */
            border-radius: 50%;
            -webkit-mask-image: radial-gradient(circle, black 45%, rgba(0,0,0,0) 80%);
            mask-image: radial-gradient(circle, black 45%, rgba(0,0,0,0) 80%);
            filter: drop-shadow(0px 0px 40px rgba(255,255,255,0.7));
        
        }}
        </style>
        """, unsafe_allow_html=True)

    if bg_base64 and os.path.exists(img_path):
        plant_base64 = get_base64(img_path)
        
        # We use a single string with NO extra spaces inside the tags
        html_code = f"""
        <div class="garden-container">
            <div class="garden-header">
                <h2 style="margin:0; font-family: 'Segoe UI'; font-size: 24px; color: white;">{text}</h2>
                <p style="margin:0; font-weight: bold; opacity: 0.9; font-size: 14px; color: white;">Day {day}</p>
            </div>
            <div class="plant-anchor">
                <img src="data:image/png;base64,{plant_base64}" />
            </div>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
    else:
        st.error("Assets missing. Check your folders!")

# =====================================================
# 🧘 TOOLS
# =====================================================
with tab4:    

    # =============================
    # 🧘 MEDITATION TIMER
    # =============================
    st.markdown("### 🧘 Meditation Timer")

    import time

    if "meditating" not in st.session_state:
        st.session_state.meditating = False
        st.session_state.start_time = 0
        st.session_state.duration = 0

    minutes = st.slider("Set Time (minutes)", 1, 20, 5)

    col1, col2 = st.columns(2)

    if col1.button("▶ Start Meditation"):
        st.session_state.meditating = True
        st.session_state.start_time = time.time()
        st.session_state.duration = minutes * 60

    if col2.button("⏹ Stop Meditation"):
        st.session_state.meditating = False
        st.info("Meditation stopped.")

    if st.session_state.meditating:

        elapsed = int(time.time() - st.session_state.start_time)
        remaining = st.session_state.duration - elapsed

        if remaining <= 0:
            st.session_state.meditating = False

            st.markdown("""
            <audio autoplay>
                <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
            </audio>
            """, unsafe_allow_html=True)

            st.success("✨ Time completed. Relax and breathe 💙")

        else:
            mins = remaining // 60
            secs = remaining % 60

            st.info(f"⏳ Time left: {mins:02d}:{secs:02d}")

            progress = (st.session_state.duration - remaining) / st.session_state.duration
            st.progress(progress)

            time.sleep(1)
            st.rerun()

    st.divider()

    # =============================
    # 📖 JOURNAL PROMPT (LLM)
    # =============================
    st.markdown("### 📖 Journal Prompt")

    if st.button("Get Journal Prompt"):

        with st.spinner("Thinking..."):
            

            prompt = generate_journal_prompt("emotion")  # you can improve later using emotion

            st.info(prompt)

    st.divider()

    # =============================
    # 🧠 THOUGHT REFRAMING (LLM)
    # =============================
    st.markdown("### 🧠 Thought Reframing")

    thought = st.text_input("What’s bothering you?")

    if st.button("Reframe Thought") and thought:

        import ollama

        with st.spinner("Reframing..."):
            
            response = ollama.chat(
                model="phi3:mini",
                messages=[{
                    "role": "user",
                    "content": f"""
Reframe this negative thought using CBT.
Give a balanced positive perspective in 2–5 lines.
"""
                }],
                options={"temperature": 0.6, "num_predict": 60}
            )

            st.success(response["message"]["content"])

    st.divider()

# --------------------------------------------------------
import datetime
import ollama
from collections import Counter

# ---------------------------
# SAFETY CHECK
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# DATA PREPARATION
# ---------------------------
chat_text = " ".join(
    [m["content"] for m in st.session_state.messages if m["role"] == "user"]
)

today = str(datetime.date.today())

# ---------------------------
# HEADER
# ---------------------------
with tab5:
    st.subheader("🧠 AI Therapy Engine")


    if len(st.session_state.messages) < 15:
        st.info("Chat a bit more so I can understand you better 💙")
    else:
        chat_text = " ".join(
            [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        )

        analysis = analyze_user_state(chat_text)

        st.write("🧠 Your current state:")
        st.write(analysis)


    if not chat_text:
        st.info("Start chatting to generate your mental health report 🌿")
        st.stop()

    # ---------------------------
    # 1. MOOD + PSYCHOLOGICAL ANALYSIS
    # ---------------------------
    analysis_prompt = f"""
You are a clinical-style CBT AI therapist (NOT medical).

Analyze user chat and return STRICT JSON:

{{
"stress_level": "low/medium/high",
"anxiety_level": "low/medium/high",
"emotional_state": "stable/unstable/overwhelmed",
"burnout_risk": "low/medium/high",
"summary": "short 2 line psychological summary"
}}

Chat:
{chat_text}
"""

    analysis = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": analysis_prompt}],
        options={"temperature": 0.3}
    )

    raw_analysis = analysis["message"]["content"]

    import json

    try:
        start = raw_analysis.find("{")
        end = raw_analysis.rfind("}") + 1
        report = json.loads(raw_analysis[start:end])
    except:
        report = {
            "stress_level": "medium",
            "anxiety_level": "medium",
            "emotional_state": "unstable",
            "burnout_risk": "low",
            "summary": "Unable to generate full report. Keep chatting for better insights."
        }

    # ---------------------------
    # 2. DISPLAY DASHBOARD
    # ---------------------------
    st.markdown("### 📊 Mental Health Report")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Stress Level", report["stress_level"])
        st.metric("Anxiety Level", report["anxiety_level"])

    with col2:
        st.metric("Emotional State", report["emotional_state"])
        st.metric("Burnout Risk", report["burnout_risk"])


    st.markdown("### 🧠 Therapist Summary")
    st.info(report["summary"])
    # ---------------------------
    # 3. AI THERAPIST ADVICE
    # ---------------------------
    advice_prompt = f"""
You are an expert CBT therapist.

Based on this psychological report:

{report}

Give:
- 3 emotional healing suggestions
- 2 behavioral changes
- 1 motivational line

Keep it simple, supportive, non-medical.
"""

    advice = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": advice_prompt}],
        options={"temperature": 0.5}
    )

    st.markdown("### 🌿 AI Therapy Advice")
    st.write(advice["message"]["content"])

    # ---------------------------
    # 5. SAFETY MESSAGE
    # ---------------------------
    st.markdown("---")
    st.caption("⚠️ This is not medical advice. If you're feeling severe distress, please consult a professional.")