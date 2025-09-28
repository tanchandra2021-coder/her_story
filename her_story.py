import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Leader personalities
LEADERS = {
    "Michelle Obama": "You are Michelle Obama, empathetic mentor. Give cordial finance advice.",
    "Frida Kahlo": "You are Frida Kahlo, reflective and artistic. Give finance advice using metaphors."
}

# Leader selection
leader = st.selectbox("Select a leader:", list(LEADERS.keys()))

# Input
st.text_input("Ask a question:", key="input_text")

# Lazy load model only on first generate
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
    model.eval()
    return tokenizer, model

def generate_response(prompt):
    tokenizer, model = load_model()
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7
        )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text.replace(prompt, "").strip()

# Generate response
if st.button("Ask") and st.session_state.input_text.strip() != "":
    user_input = st.session_state.input_text.strip()
    prompt = f"{LEADERS[leader]}\nUser: {user_input}\n{leader}:"
    response = generate_response(prompt)
    st.session_state.history.append({"sender": "user", "text": user_input})
    st.session_state.history.append({"sender": "bot", "text": response})
    st.session_state.input_text = ""

# Show chat history
for chat in st.session_state.history:
    if chat["sender"] == "user":
        st.markdown(f"**You:** {chat['text']}")
    else:
        st.markdown(f"**{leader}:** {chat['text']}")
