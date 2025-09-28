import streamlit as st
import random

st.set_page_config(page_title="Finance Advisors", layout="wide")

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

# ---------- Main Chat ----------
with col2:
    sel = st.session_state.selected
    st.image(LEADERS[sel]["img"], width=80)
    st.subheader(sel)
    st.write(LEADERS[sel]["role"])

    # Chat display
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
            st.session_state.history.append({"sender": "user", "text": user_input.strip()})
            reply = random.choice(LEADERS[sel]["responses"])
            st.session_state.history.append({"sender": "bot", "text": reply, "leader": sel})
            st.session_state.input_text = ""  # clear quick prompt
            st.experimental_rerun()
