# app.py
import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Finance Advisors — Women Leaders", page_icon="💼", layout="wide")

# -------- Leader data and persona responses --------
LEADERS = {
    "Michelle Obama": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Michelle_Obama_official_portrait.jpg",
        "role": "Policy-minded, empathetic mentor",
        "responses": [
            "Start small, invest in yourself first. Budget wisely, then explore low-cost index funds.",
            "Financial literacy is key — track spending, save consistently, and think long-term.",
            "Empowerment in finance starts with education. Ask questions, stay informed, and plan ahead."
        ],
    },
    "Frida Kahlo": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Frida_Kahlo_1941.jpg",
        "role": "Reflective, artistic, metaphor-driven",
        "responses": [
            "Investing is like painting a canvas — start with bold strokes and refine over time.",
            "Your financial journey should tell a story; diversify your palette of investments.",
            "Think of your savings as seeds in a garden — nurture them patiently for growth."
        ],
    },
    "Marie Curie": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Marie_Curie_c1920.jpg",
        "role": "Scientific, evidence-first",
        "responses": [
            "Always analyze data before investing — understand risk vs reward clearly.",
            "Use precise calculations: compound interest works best over time with consistent contributions.",
            "Diversify methodically. Scientific approach reduces surprises and uncertainty."
        ],
    },
    "Rosa Parks": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Rosa_Parks.jpg",
        "role": "Calm, principled, concise",
        "responses": [
            "Stand firm on your financial principles, start with disciplined budgeting.",
            "Focus on practical, small steps: save, invest, and stay consistent.",
            "Calm and deliberate action is more powerful than chasing trends."
        ],
    },
    "Malala Yousafzai": {
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Malala_Yousafzai_at_NYU_2013_cropped.jpg",
        "role": "Educator, clear, empowering",
        "responses": [
            "Education is the foundation — learn finance basics before investing.",
            "Empower yourself: track expenses, understand investments, and ask questions.",
            "Small, consistent actions today will lead to greater financial independence tomorrow."
        ],
    },
}

DEFAULT_LEADER = list(LEADERS.keys())[0]

# -------- Session state setup --------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {sender:'user'|'bot', leader, text}
if "selected" not in st.session_state:
    st.session_state.selected = DEFAULT_LEADER
if "input" not in st.session_state:
    st.session_state.input = ""

# -------- Layout: left sidebar (advisors) and main chat --------
col1, col2 = st.columns([1.2, 3])

with col1:
    st.markdown("## Finance Advisors")
    st.markdown("Famous leaders — finance & education\n---")

    for name, meta in LEADERS.items():
        is_selected = (st.session_state.selected == name)
        st.image(meta["img"], width=60)
        st.markdown(f"**{name}**\n{meta['role']}")
        if st.button(f"Select {name}", key="select_" + name):
            st.session_state.selected = name
        st.markdown("---")

    st.markdown("**Quick prompts**")
    quicks = [
        "How should a beginner start investing $1,000?",
        "What is dollar-cost averaging and why is it useful?",
        "How should I think about risk with equities vs bonds?",
        "Is crypto a good hedge for inflation?",
    ]
    for q in quicks:
        if st.button(q, key="quick_" + q[:10]):
            st.session_state.input = q

    st.markdown(
        "⚠️ **Disclaimer:** Replies are AI-generated simulations and not actual statements by the pictured individuals."
    )

with col2:
    # header
    sel = st.session_state.selected
    st.image(LEADERS[sel]["img"], width=80)
    st.markdown(f"### {sel}")
    st.markdown(f"{LEADERS[sel]['role']} • Finance & Education\n---")

    # Chat area
    chat_container = st.container()
    with chat_container:
        if len(st.session_state.history) == 0:
            st.markdown("Ask anything about finance. Your selected advisor will respond in their voice.")
        else:
            for entry in st.session_state.history:
                if entry["sender"] == "user":
                    st.markdown(f"**You:** {entry['text']}")
                else:
                    leader = entry.get("leader", st.session_state.selected)
                    st.markdown(f"**{leader}:** {entry['text']}")

    st.markdown("---")
    # Input
    user_input = st.text_area(" ", value=st.session_state.input, placeholder="Type your question...", key="input_area", height=90)
    if st.button("Send", key="send_button"):
        msg = st.session_state.input.strip()
        if msg:
            st.session_state.history.append({"sender": "user", "text": msg})
            st.session_state.input = ""
            # pick a random response from the selected leader
            reply = random.choice(LEADERS[st.session_state.selected]["responses"])
            st.session_state.history.append({"sender": "bot", "text": reply, "leader": st.session_state.selected})
            st.experimental_rerun()
