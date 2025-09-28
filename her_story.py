import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# -------------------------------
# App configuration
# -------------------------------
st.set_page_config(page_title="Her Story Chat", page_icon="💬")

st.title("Her Story Chatbot 💬")

# -------------------------------
# Session state initialization
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# -------------------------------
# Model loading
# -------------------------------
MODEL_NAME = "EleutherAI/gpt-neo-125M"  # Small, safe for free-tier

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# -------------------------------
# Chat input
# -------------------------------
st.session_state.input_text = st.text_input(
    "You:", value=st.session_state.input_text, key="input_box"
)

if st.session_state.input_text:
    user_text = st.session_state.input_text.strip()
    st.session_state.history.append({"sender": "user", "text": user_text})

    # ---------------------------
    # Generate bot response
    # ---------------------------
    input_ids = tokenizer.encode(user_text + tokenizer.eos_token, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=100,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_p=0.9,
            temperature=0.8
        )
    bot_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    bot_text = bot_text[len(user_text):].strip()  # Remove user input

    st.session_state.history.append({"sender": "bot", "text": bot_text})
    st.session_state.input_text = ""  # Clear input box

# -------------------------------
# Display chat history
# -------------------------------
for message in st.session_state.history:
    if message["sender"] == "user":
        st.markdown(f"**You:** {message['text']}")
    else:
        st.markdown(f"**Bot:** {message['text']}")

