import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ---------------------
# Initialize session state
# ---------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Trigger for rerendering
if "rerun" not in st.session_state:
    st.session_state.rerun = False

# ---------------------
# Load model and tokenizer
# ---------------------
@st.cache_resource(show_spinner=False)
def load_model():
    model_name = "gpt2"  # replace with your desired model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# ---------------------
# Female leaders dataset (replace/add as needed)
# ---------------------
female_leaders = [
    "Ada Lovelace",
    "Marie Curie",
    "Malala Yousafzai",
    "Kamala Harris",
    "Jacinda Ardern",
    "Ruth Bader Ginsburg",
    "Angela Merkel",
]

# ---------------------
# Generate bot response
# ---------------------
def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_new_tokens=150,
            pad_token_id=tokenizer.eos_token_id
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only new part
    response_text = response[len(prompt):].strip()
    return response_text

# ---------------------
# Sidebar
# ---------------------
st.sidebar.title("Her Story Chatbot 💬")
st.sidebar.markdown(
    """
    This chatbot tells stories of **female leaders** throughout history.
    You can type anything and explore the stories!
    """
)

# ---------------------
# Main UI
# ---------------------
st.title("Her Story Chatbot 💬")

# Display chat history
for entry in st.session_state.history:
    if entry["sender"] == "user":
        st.markdown(f"**You:** {entry['text']}")
    else:
        st.markdown(f"**Bot:** {entry['text']}")

# Input form
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("You:", st.session_state.input_text)
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input.strip():
    # Echo user message
    st.session_state.history.append({"sender": "user", "text": user_input})

    # Prepare prompt with context
    context = "\n".join(
        [f"{entry['sender']}: {entry['text']}" for entry in st.session_state.history]
    )
    prompt = f"{context}\nBot:"

    # Generate response
    bot_response = generate_response(prompt)

    # Append bot response
    st.session_state.history.append({"sender": "bot", "text": bot_response})

    # Trigger rerun
    st.session_state.input_text = ""
    st.session_state.rerun = not st.session_state.rerun
    st.experimental_rerun() if hasattr(st, "experimental_rerun") else None

