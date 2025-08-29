import streamlit as st
from streamlit_chat import message
from leaders import leaders
from PIL import Image
import requests

# -----------------------------
# Hugging Face API setup
# -----------------------------
HF_API_URL = "https://api-inference.huggingface.co/models/TheBloke/gpt4all-lora-quantized"  # small free model
HF_API_TOKEN = ""  # optional for anonymous free usage, but you can add your token if rate-limited

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

def query_llm(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        outputs = response.json()
        # Hugging Face API returns a list of dicts with 'generated_text'
        return outputs[0]["generated_text"]
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"

# -----------------------------
# Streamlit UI setup
# -----------------------------
st.set_page_config(page_title="Her Story", layout="wide")

# Background image
bg_image = Image.open("backgrounds/female_leaders_bg.jpg")
st.image(bg_image, use_column_width=True)

st.title("🌟 Her Story: AI Women's Leadership Platform (Free, Hugging Face API)")

# Sidebar: select leader
st.sidebar.header("Choose a Leader")
selected_leader = st.sidebar.selectbox("Select a historical female leader:", list(leaders.keys()))
leader_info = leaders[selected_leader]

# Show avatar
st.subheader(f"{selected_leader}'s Avatar")
avatar_img = Image.open(leader_info["avatar"])
st.image(avatar_img, width=300)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
st.subheader(f"💬 Chat with {selected_leader}")
user_input = st.text_input("Ask a question or request advice:")

# Query the LLM
if user_input:
    prompt = f"{leader_info['prompt']}\nStudent asks: {user_input}\nRespond as {selected_leader}:"
    answer = query_llm(prompt)

    # Store conversation
    st.session_state.history.append({"user": user_input, "ai": answer})

# Display chat bubbles
for chat in st.session_state.history:
    message(chat["user"], is_user=True)
    message(chat["ai"], is_user=False)

