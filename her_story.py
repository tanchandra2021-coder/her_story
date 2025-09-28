import streamlit as st
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO
import random

st.set_page_config(page_title="Finance Advisors Chat", layout="wide")

# -------------------
# Leader metadata
# -------------------
LEADERS = {
    "Michelle Obama": {
        "personality": "Policy-minded, empathetic mentor",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Michelle_Obama_official_portrait.jpg"
    },
    "Frida Kahlo": {
        "personality": "Reflective, artistic, metaphor-driven",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Frida_Kahlo_1941.jpg"
    },
    "Marie Curie": {
        "personality": "Scientific, evidence-first",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Marie_Curie_c1920.jpg"
    },
    "Rosa Parks": {
        "personality": "Calm, principled, concise",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Rosa_Parks.jpg"
    },
    "Malala Yousafzai": {
        "personality": "Educator, clear, empowering",
        "avatar": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Malala_Yousafzai_at_NYU_2013_cropped.jpg"
    }
}

# -------------------
# Load HF model
# -------------------
@st.cache_resource(show_spinner=False)
def load_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B", device=-1)

model = load_model()

# -------------------
# Helper: Get avatar image
# -------------------
def get_avatar(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img.thumbnail((80, 80))
        return img
    except:
        return Image.new("RGB", (80, 80), color=(200, 200, 200))

# -------------------
# Initialize session state
# -------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# -------------------
# Sidebar
# -------------------
st.sidebar.title("Finance Advisors")
advisor_selected = st.sidebar.selectbox(
    "Choose a leader", list(LEADERS.keys())
)

st.sidebar.markdown(f"**{advisor_selected}** — {LEADERS[advisor_selected]['personality']}")
st.sidebar.markdown("Quick prompts:")
quick_prompts = [
    "How should I start investing?",
    "What's a safe way to learn about crypto?",
    "How do I budget effectively?",
    "Advice for saving for college?",
    "Tips for beginner investors?"
]
for q in quick_prompts:
    if st.sidebar.button(q, key=f"quick_{q[:10]}"):
        st.session_state.input_text = q

st.sidebar.markdown(
    "Disclaimer: Replies are AI-generated simulations and not actual statements by the pictured individuals."
)

# -------------------
# Chat input
# -------------------
st.title("💬 Chat with a Finance Advisor")

user_input = st.text_input("Type your question here:", value=st.session_state.input_text)

# -------------------
# Handle chat
# -------------------
if user_input:
    prompt = f"You are {advisor_selected}, a famous female leader and mentor. Speak cordially and in your personality. You give clear, accurate, concise finance advice (stocks, crypto, investing, saving, budgeting). Answer directly and stay on topic, avoid repetition, avoid unrelated info.\n\nUser: {user_input}\nAdvisor:"
    response = model(prompt, max_new_tokens=256, do_sample=True, temperature=0.7)[0]["generated_text"]
    # Remove prompt from output
    response = response.replace(prompt, "").strip()

    # Append to history
    st.session_state.history.append({"sender": "user", "text": user_input})
    st.session_state.history.append({"sender": "bot", "text": response, "avatar": get_avatar(LEADERS[advisor_selected]['avatar'])})

    st.session_state.input_text = ""  # clear input

# -------------------
# Display chat
# -------------------
for chat in st.session_state.history:
    if chat["sender"] == "user":
        st.markdown(f"**You:** {chat['text']}")
    else:
        cols = st.columns([1, 5])
        with cols[0]:
            st.image(chat["avatar"])
        with cols[1]:
            st.markdown(f"**{advisor_selected}:** {chat['text']}")
