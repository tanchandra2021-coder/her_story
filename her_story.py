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
# Leader personalities (rest of the dictionary remains the same)
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
# Load model - ***MODEL CHANGE HERE***
# -------------------------
@st.cache_resource(show_spinner=True)
def load_model():
    # 125M parameter model is far more manageable than the 6B model
    model_name = "EleutherAI/gpt-neo-125M"  
    
    # You can also try "openai-community/gpt2" which is also 124M parameters.
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Load the model. You can optionally add a torch.dtype for half-precision to save a little more memory:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 # Use half-precision for lower memory footprint
    )
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# -------------------------
# Generate response (rest of the function remains the same)
# -------------------------
def generate_response(leader, user_input):
    prompt_intro = LEADERS[leader]["prompt_intro"]
    prompt = f"{prompt_intro}\n\nUser: {user_input}\n{leader}:"
    try:
        # NOTE: Using 'cuda' or a specific device is not necessary unless a GPU is guaranteed.
        # The model will run on the CPU, which is the only option on the free tier.
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
        response = response.replace(prompt, "").strip()
    except Exception as e:
        response = f"Sorry, something went wrong: {e}"
    return response

# -------------------------
# Streamlit UI (rest of the UI code remains the same)
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

# Chat form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here:", st.session_state.input_text)
    submit_button = st.form_submit_button(label="Ask")

if submit_button and user_input.strip():
    st.session_state.history.append({"sender": "user", "text": user_input})
    response = generate_response(leader, user_input)
    st.session_state.history.append({"sender": "bot", "text": response})

# Display history
for chat in st.session_state.history:
    if chat["sender"] == "user":
        st.markdown(f"**You:** {chat['text']}")
    else:
        st.markdown(f"**{leader}:** {chat['text']}")
