import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Finance Advisors", layout="wide")

# ---------- Leader data ----------
LEADERS = {
    "Michelle Obama": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Michelle_Obama_official_portrait.jpg",
        "role": "Policy-minded, empathetic mentor",
    },
    "Frida Kahlo": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Frida_Kahlo_1941.jpg",
        "role": "Reflective, artistic, metaphor-driven",
    },
    "Marie Curie": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Marie_Curie_c1920.jpg",
        "role": "Scientific, evidence-first",
    },
    "Rosa Parks": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Rosa_Parks.jpg",
        "role": "Calm, principled, concise",
    },
    "Malala Yousafzai": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Malala_Yousafzai_at_NYU_2013_cropped.jpg",
        "role": "Educator, clear, empowering",
    },
}

DEFAULT_LEADER = "Michelle Obama"

# ---------- Load GPT-Neo 1.3B ----------
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B", device=-1)

chatbot_model = load_model()

# ---------- Session state ----------
if "history" not in st.session_state:
    st.session_state.history = []
if "selected" not in st.session_state:
    st.session_state.selected = DEFAULT_LEADER
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------- CSS ----------
st.markdown("""
<style>
.msg-user {
    background: linear-gradient(90deg,#6366f1,#7c3aed);
    color:white; padding:10px 14px; border-radius:14px; max-width:75%; margin-left:auto; margin-bottom:6px;
}
.msg-bot {
    background: #f3f4f6; padding:10px 14px; border-radius:14px; max-width:75%; margin-right:auto; margin-bottom:6px;
    border:1px solid #e5e7eb;
}
.leader-card {border-radius:14px; padding:10px; margin-bottom:8px; transition: box-shadow 0.2s ease; display:flex; align-items:center; gap:10px;}
.leader-card:hover {box-shadow:0 8px 24px rgba(0,0,0,0.08);}
.avatar {width:50px; height:50px; border-radius:12px; object-fit:cover;}
.small {font-size:12px; color:#6b7280;}
.disclaimer {font-size:13px; color:#374151; background:#fffbf0; padding:8px; border-radius:8px; border:1px solid #fcefc7;}
</style>
""", unsafe_allow_html=True)

# ---------- Layout ----------
col1, col2 = st.columns([1.2, 3])

# ---------- Sidebar ----------
with col1:
    st.markdown("## Finance Advisors")
    st.markdown("Famous leaders — finance & education\n---")

    for idx, (name, meta) in enumerate(LEADERS.items()):
        st.markdown(
            f"<div class='leader-card'>"
            f"<img class='avatar' src='{meta['img']}'/>"
            f"<div><b>{name}</b><br><span class='small'>{meta['role']}</span></div>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button(f"Select {name}", key=f"select_{idx}"):
            st.session_state.selected = name

    st.markdown("---")
    st.markdown("**Quick prompts**")
    quicks = [
        "How should a beginner start investing $1,000?",
        "What is dollar-cost averaging and why is it useful?",
        "How should I think about risk with equities vs bonds?",
        "Is crypto a good hedge for inflation?",
    ]
    for i, q in enumerate(quicks):
        if st.button(q, key=f"quick_{i}"):
            st.session_state.input_text = q

    st.markdown("---")
    st.markdown("<div class='disclaimer'><b>Disclaimer:</b> Replies are AI-generated simulations and not actual statements by the pictured individuals.</div>", unsafe_allow_html=True)

# ---------- Chat ----------
with col2:
    sel = st.session_state.selected
    st.image(LEADERS[sel]["img"], width=80)
    st.subheader(sel)
    st.write(LEADERS[sel]["role"])

    # Display chat history
    for msg in st.session_state.history:
        if msg["sender"] == "user":
            st.markdown(f"<div class='msg-user'>{msg['text']}</div>", unsafe_allow_html=True)
        else:
            leader = msg.get("leader", sel)
            st.markdown(f"<div class='msg-bot'><b>{leader}:</b> {msg['text']}</div>", unsafe_allow_html=True)

    # Input
    user_input = st.text_area("Type your question here", value=st.session_state.get("input_text", ""), height=100)
    if st.button("Send"):
        if user_input.strip() != "":
            # Append user message
            st.session_state.history.append({"sender": "user", "text": user_input.strip()})

            # Personality-driven prompt
            prompt = f"""
You are {sel}, a famous female leader and mentor. Speak cordially and in your personality.
You give clear, accurate, concise finance advice (stocks, crypto, investing, saving, budgeting).
Answer directly and stay on topic, avoid repetition, avoid unrelated info.

User asks: {user_input.strip()}
Answer:"""

            # Generate response safely
            try:
                output = chatbot_model(prompt, max_length=200, do_sample=True, temperature=0.7)[0]["generated_text"]
                reply = output.replace(prompt, "").strip()
            except Exception:
                reply = "Sorry, I couldn't generate a response right now."

            # Append bot reply
            st.session_state.history.append({"sender": "bot", "text": reply, "leader": sel})

            # Clear input field
            st.session_state.input_text = ""

