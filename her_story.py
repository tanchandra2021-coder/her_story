# her_story.py

import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# -------------------------
# Initialize session state
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "selected_leader" not in st.session_state:
    st.session_state.selected_leader = "Michelle Obama"

# -------------------------
# Define leader personalities
# -------------------------
LEADERS = {
    "Michelle Obama": {
        "description": "Policy-minded, empathetic mentor",
        "prompt_intro": "You are Michelle Obama, a policy-minded and empathetic mentor. Speak cordially and give clear, accurate finance advice. Answer directly and stay on topic, avoid repetition, avoid unrelated info."
    },
    "Frida Kahlo": {
        "description": "Reflective, artistic, metaphor-driven",
        "prompt_intro": "You are Frida Kahlo, a reflective, artistic mentor. Speak cordially, use metaphors, and give clear finance advice."
    },
    "Marie Curie": {
        "description": "Scientific, evidence-first",
        "prompt_intro": "You are Marie Curie, scientific and evidence-first. Speak cordially and give clear, data-backed finance advice."
    },
    "Rosa Parks": {
        "description": "Calm, principled, concise",
        "prompt_intro": "You are Rosa Parks, calm, principled, and concise. Give direct finance advice in a cordial tone."
    },
    "Malala Yousafzai": {
        "description": "Educator, clear, empowering",
        "prompt_intro": "You are Malala Yousafzai, a clear and empowering educator. Give cordial, actionable finance advice."
    }
}

# -------------------------
# Load Hugging Face model
# -------------------------
@st.cache_resource(show_spinner=True)
def load_model():
    model_name = "EleutherAI/gpt-j-6B"  # Free, capable model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# -------------------------
# Helper: Generate response
# -------------------------
def generate_response(leader, user_input):
    prompt_intro = LEADERS[leader]["prompt_intro"]
    prompt = f"{prompt_intro}\n\nUser: {user_input}\n{leader}:"
    
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove the prompt from response
        response = response.replace(prompt, "").strip()
    except Exception as e:
        response = f"Sorry, something went wrong: {e}"

    return response

# -------------------------
# Streamlit UI
# -------------------------
st.title("Famous Leaders — Finance & Education Chatbot")

# Leader selection
leader = st.selectbox(
    "Select a leader:",
    list(LEADERS.keys()),
    index=list(LEADERS.keys()).index(st.session_state.selected_leader)
)
st.session_state.selected_leader = leader

st.markdown(f"**{leader}** — {LEADERS[leader]['description']}")

# Chat input
st.text_input(
    "Type your question here:",
    key="input_text"
)

# Quick prompts
QUICK_PROMPTS = [
    "How do I start investing?",
    "What is financial literacy?",
    "How should I budget my money?",
    "Advice on stocks vs crypto?",
]

st.markdown("**Quick prompts:**")
cols = st.columns(len(QUICK_PROMPTS))
for i, prompt in enumerate(QUICK_PROMPTS):
    if cols[i].button(prompt, key=f"quick_{i}"):
        st.session_state.input_text = prompt

# Generate response button
if st.button("Ask"):
    user_input = st.session_state.input_text.strip()
    if user_input != "":
        response = generate_response(leader, user_input)
        st.session_state.history.append({"sender": "user", "text": user_input})
        st.session_state.history.append({"sender": "bot", "text": response})
        st.session_state.input_text = ""  # clear input
    else:
        st.warning("Please type a question.")

# Display chat history
for chat in st.session_state.history:
    if chat["sender"] == "user":
        st.markdown(f"**You:** {chat['text']}")
    else:
        st.markdown(f"**{leader}:** {chat['text']}")

