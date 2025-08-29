import streamlit as st
from streamlit_chat import message
from leaders import leaders
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# -----------------------------
# CPU-friendly LLM setup
# -----------------------------
# Small free model compatible with CPU
model_name = "nomic-ai/gpt4all-lora-quantized"  # lightweight model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Use text-generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # device=-1 => CPU

def query_llm(prompt):
    outputs = generator(prompt, max_new_tokens=200)
    return outputs[0]["generated_text"]

# -----------------------------
# Streamlit UI setup
# -----------------------------
st.set_page_config(page_title="Her Story", layout="wide")

# Background image
bg_image = Image.open("backgrounds/female_leaders_bg.jpg")
st.image(bg_image, use_column_width=True)

st.title("🌟 Her Story: AI Women's Leadership Platform (Free, CPU)")

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
    try:
        answer = query_llm(prompt)
    except Exception as e:
        answer = f"⚠️ Error generating response: {str(e)}"

    # Store conversation
    st.session_state.history.append({"user": user_input, "ai": answer})

# Display chat bubbles
for chat in st.session_state.history:
    message(chat["user"], is_user=True)
    message(chat["ai"], is_user=False)
