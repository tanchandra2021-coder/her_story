import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# -------------------------
# Session state
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "selected_leader" not in st.session_state:
    st.session_state.selected_leader = "Michelle Obama"

# -------------------------
# Leader personalities
# -------------------------
LEADERS = {
    "Michelle Obama": {
        "description": "Policy-minded, empathetic mentor",
        "prompt_intro": "You are Michelle Obama, a policy-minded and empathetic mentor. Speak cordially and give clear, accurate finance advice. Answer directly and stay on topic."
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
# Load model
# -------------------------
@st.cache_resource(show_spinner=True)
def load_model():
    model_name = "EleutherAI/gpt-j-6B"  # Or use smaller model for testing
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# -------------------------
# Generate response


