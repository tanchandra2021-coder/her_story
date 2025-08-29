import streamlit as st
from streamlit_chat import message
from leaders import leaders
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# -----------------------------
# Initialize local LLM (GPT4All-J)
# -----------------------------
model_name = "nomic-ai/gpt4all-j"  # or a locally downloaded LLaMA 2 model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# -----------------------------
# Streamlit config
# -----------------------------
st.set_page_config(page_title="Her Story", layout="wide")

# Background image
bg_image = Image.open("backgrounds/female_leaders_bg.jpg")
st.image(bg_image, use_column_width=True)

st.title("🌟 Her Story: AI Women's Leadership Platform (Fully Free)")

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

def query_local_llm(prompt_text):
    inputs = tokenizer(prompt_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=300)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if user_input:
    prompt = f"{leader_info['prompt']}\nStudent asks: {user_input}\nRespond as {selected_leader}:"
    answer = query_local_llm(prompt)
    
    # Store conversation
    st.session_state.history.append({"user": user_input, "ai": answer})

# Display chat bubbles
for chat in st.session_state.history:
    message(chat["user"], is_user=True)
    message(chat["ai"], is_user=False)
