import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Finance Advisors — Women Leaders", page_icon="💼", layout="wide")

# ---------- Leader data ----------
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

# ---------- Session state ----------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {sender:'user'|'bot', leader, text}
if "selected" not in st.session_state:
    st.session_state.selected = DEFAULT_LEADER
if "input" not in st.session_state:
    st.session_state.input = ""

# ---------- CSS for modern chat ----------
st.markdown(
    """
    <style>
    .chat-container {max-width:800px;}
    .msg-user {
        background: linear-gradient(90deg,#6366f1,#7c3aed);
        color:white; padding:10px 14px; border-radius:14px; max-width:75%; margin-left:auto;
    }
    .msg-bot {
        background: #f3f4f6; padding:10px 14px; border-radius:14px; max-width:75%; margin-right:auto;
        border:1px solid #e5e7eb;
    }
    .leader-card {border-radius:14px; padding:10px; margin-bottom:8px; transition: box-shadow 0.2s ease;}
    .leader-card:hover {box-shadow:0 8px 24px rgba(0,0,0,0.08);}
    .avatar {width:50px; height:50px; border-radius:12px; object-fit:cover;}
    .small {font-size:12px; color:#6b7280;}
    .disclaimer {font-size:13px; color:#374151; background:#fffbf0; padding:8px; border-radius:8px; border:1px solid #fcefc7;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Layout ----------
col1, col2 = st.columns([1.2, 3])

# ---------- Left sidebar ----------
with col1:
    st.markdown("## Finance Advisors")
    st.markdown("Famous leaders — finance & education\n---")

    for idx, (name, meta) in enumerate(LEADERS.items()):
        st.markdown(
            f"<div class='leader-card' style='display:flex;align-items:center;gap:10px'>"
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
            st.session_state.input = q

    st.markdown("---")
    st.markdown(
        "<div class='disclaimer'><b>Disclaimer:</b> Replies are AI-generated simulations and not actual statements by the pictured individuals.</div>",
        unsafe_allow_html=True
    )

# ---------- Right main chat ----------
with col2:
    sel = st.session_state.selected
    st.image(LEADERS[sel]["img"], width=80)
    st.markdown(f"### {sel}")
    st.markdown(f"{LEADERS[sel]['role']} • Finance & Education\n---")

    chat_container = st.container()
    with chat_container:
        if not st.session_state.history:
            st.markdown("Ask anything about finance. Your selected advisor will respond in their voice.")
        else:
            for entry in st.session_state.history:
                if entry["sender"] == "user":
                    st.markdown(f"<div class='msg-user'>{entry['text']}</div>", unsafe_allow_html=True)
                else:
                    leader = entry.get("leader", sel)
                    st.markdown(
                        f"<div class='msg-bot'><b>{leader}:</b> {entry['text']}</div>",
                        unsafe_allow_html=True
                    )

    # ---------- Input ----------
    user_input = st.text_area(" ", value=st.session_state.input, placeholder="Type your question...", key="input_area", height=90)
    if st.button("Send", key="send_button"):
        msg = st.session_state.input.strip()
        if msg:
            st.session_state.history.append({"sender": "user", "text": msg})
            st.session_state.input = ""
            # pick random response
            reply = random.choice(LEADERS[sel]["responses"])
            st.session_state.history.append({"sender": "bot", "text": reply, "leader": sel})
            st.experimental_rerun()
