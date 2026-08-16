\# AI-Powered Mental Wellness Companion



An AI-powered mental wellness companion that combines \*\*Large Language Model (LLM)-based conversational intelligence, Cognitive Behavioral Therapy (CBT) principles, adaptive habit formation, emotion-aware interaction, and gamification\*\* to provide users with a supportive and engaging mental wellness experience.



\## Project Overview



The AI Mental Wellness Companion, named \*\*Mia\*\*, is designed to provide users with a safe and interactive environment where they can express their thoughts and feelings through natural conversation. The system uses the \*\*Phi-3 Mini Large Language Model through Ollama\*\* to generate empathetic and context-aware responses.



The application goes beyond a conventional chatbot by combining conversational support with daily wellness activities, mood-based task recommendations, journaling, meditation, thought reframing, progress tracking, and a gamified Healing Garden. A crisis detection mechanism is also included to identify critical expressions and provide an appropriate safety response.



> \*\*Disclaimer:\*\* Mia is a wellness-support application and is not a replacement for a qualified mental-health professional, medical diagnosis, emergency service, or professional treatment.



\## Key Features



\### 1. AI Conversational Companion



Mia uses an LLM to provide natural-language conversations with users. The chatbot follows an empathy-focused conversational approach by listening to the user, acknowledging emotions, asking gentle questions, and providing small supportive suggestions.



\### 2. Emotion-Aware Interaction



The system analyzes user conversations to understand emotional states such as sadness, anxiety, stress, and happiness. The detected emotional context can be used to personalize wellness activities and recommendations.



\### 3. Crisis Detection



A dedicated crisis-detection mechanism checks user messages for critical expressions related to self-harm or suicidal thoughts. When a crisis-related message is detected, the normal conversational response is overridden and the application provides an immediate supportive safety response.



\### 4. Adaptive Daily Wellness Tasks



Mia generates a combination of stable core habits and mood-based daily activities. The tasks encourage healthy routines involving mindfulness, physical activity, journaling, hydration, sleep, digital balance, and other wellness practices.



\### 5. Healing Garden – Gamification



The Healing Garden provides a visual representation of the user's progress. As users complete their daily wellness activities, their journey progresses through different plant-growth stages.



The gamification element encourages consistency and engagement by transforming wellness progress into a visual and motivating experience.



\### 6. 12-Day Healing Journey



The application provides a structured 12-day wellness journey. Users complete daily tasks and progress through different stages of the Healing Garden.



\### 7. Meditation Timer



A built-in meditation timer allows users to select a duration and practice guided periods of focused breathing and relaxation.



\### 8. Journal Prompts



The application uses the LLM to generate simple and supportive journaling questions that encourage users to reflect on their thoughts and emotions.



\### 9. Thought Reframing



The Thought Reframing feature applies CBT-inspired principles to help users examine negative thoughts and consider more balanced perspectives.



\### 10. AI Mental Health Analysis



The Analysis Report module uses the LLM to analyze the user's conversation and generate an overview containing:



\* Stress Level

\* Anxiety Level

\* Emotional State

\* Burnout Risk

\* Therapist-style Summary

\* AI-generated Wellness Suggestions



The report is intended for self-reflection and wellness support and is not a clinical diagnosis.



\## System Modules



The project consists of the following major modules:



\* User Login and Registration

\* AI Chat with Mia

\* Emotion Detection

\* Crisis Detection

\* Adaptive Daily Task Generation

\* Mood Detection

\* Healing Garden

\* Progress Tracking

\* Meditation Timer

\* Journal Prompt Generation

\* CBT Thought Reframing

\* AI Mental Health Analysis

\* AI Therapy Advice

\* Data Storage and Memory



\## Technology Stack



\### Programming Language



\* Python



\### Artificial Intelligence



\* Large Language Model (LLM)

\* Phi-3 Mini

\* Ollama

\* Prompt Engineering

\* Natural Language Processing (NLP)



\### Mental Wellness Methodology



\* Cognitive Behavioral Therapy (CBT) principles

\* Emotion-aware interaction

\* Habit formation

\* Gamification



\### Framework



\* Streamlit



\### Database



\* SQLite



\### Data and Utility Libraries



\* Pandas

\* NumPy

\* JSON

\* Datetime

\* Hashlib



\### User Interface



\* Streamlit

\* HTML

\* CSS

\* Custom UI styling

\* Base64 image embedding



\## Project Architecture



The application follows a modular architecture in which the Streamlit interface communicates with different Python modules responsible for conversation, emotion processing, crisis detection, recommendations, wellness tools, and data management.



The LLM is accessed locally through Ollama. SQLite is used for local data persistence, while the assets folder contains the visual resources used by the Healing Garden.



\## Project Structure



```text

MENTAL\_WELLNESS/

│

├── assets/

│   ├── garden\_bg.jpg

│   ├── stage1.png

│   ├── stage2.png

│   ├── stage3.png

│   ├── stage4.png

│   ├── stage5.png

│   └── stage6.png

│

├── utils/

│   ├── cbt\_helper.py

│   ├── crisis\_detection.py

│   ├── emotion\_detection.py

│   ├── garden.py

│   ├── intent\_detection.py

│   ├── journal.py

│   ├── user\_analysis.py

│   └── voice.py

│

├── app.py

├── chatbot.py

├── database.py

├── memory.py

├── recommendations.py

├── requirements.txt

├── README.md

└── .gitignore

```



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/YOUR-USERNAME/AI-Mental-Wellness-Companion.git

cd AI-Mental-Wellness-Companion

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



Activate it on Windows:



```bash

venv\\Scripts\\activate

```



\### 3. Install Python dependencies



```bash

pip install -r requirements.txt

```



\### 4. Install Ollama



Install Ollama on your system and make sure it is running.



Then download the required model:



```bash

ollama pull phi3:mini

```



Verify the model:



```bash

ollama list

```



\### 5. Run the application



```bash

streamlit run app.py

```



The application will open in your browser.



\## User Flow



```text

User

&#x20; ↓

Login / Sign Up

&#x20; ↓

Chat with Mia

&#x20; ↓

Crisis Detection

&#x20; ├── Crisis → Safety Response

&#x20; │

&#x20; └── Normal Conversation

&#x20;         ↓

&#x20;      LLM Response

&#x20;         ↓

&#x20;    Mood / Emotion Context

&#x20;         ↓

&#x20;    Adaptive Wellness Tasks

&#x20;         ↓

&#x20;     Task Completion

&#x20;         ↓

&#x20;    Healing Garden Progress

```



\## Database



The application uses SQLite for local persistence.



The database can store application information such as:



\* User account information

\* Chat records

\* Mood information

\* Journey progress

\* Application state



Local database files are intentionally excluded from the GitHub repository through `.gitignore` to prevent user data from being exposed.



\## Safety



The project includes a basic crisis-detection mechanism designed to identify explicit crisis-related expressions and provide an immediate safety response.



The application should not be considered a substitute for professional mental-health care. Users experiencing serious or immediate danger should contact appropriate emergency services or qualified mental-health professionals.



\## Future Scope



Future development can include more advanced emotion and intent detection, improved long-term conversational memory, voice-based interaction, multilingual support, cloud database integration, wearable-device integration, professional therapist integration, improved personalization, advanced gamification, and more robust safety mechanisms.



\## Project Objective



The primary objective of the project is to demonstrate how modern AI technologies can be combined with CBT-inspired techniques and habit-forming mechanisms to create an interactive mental wellness support platform.



The system aims to encourage self-reflection, healthy routines, emotional awareness, and consistent engagement through a combination of conversational AI and gamified wellness activities.



\## Conclusion



The AI Mental Wellness Companion demonstrates the potential of Large Language Models to support interactive and personalized wellness experiences. By integrating LLM-based conversation, CBT-inspired thought reframing, adaptive daily tasks, crisis detection, wellness tools, progress tracking, and the gamified Healing Garden, the project provides a comprehensive AI-assisted mental wellness platform while maintaining clear limitations regarding professional medical care.



