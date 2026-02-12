import streamlit as st
import random
import time

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="D20 Arena",
    page_icon="🎲",
    layout="wide"
)

# =====================
# Session State (History with Migration)
# =====================
if "history" not in st.session_state:
    st.session_state.history = []
else:
    # Auto-reset history lama (format lama tidak punya key 'p1')
    if st.session_state.history and "p1" not in st.session_state.history[0]:
        st.session_state.history = []

# =====================
# Custom CSS
# =====================
st.markdown("""
<style>
body {
    background-color: #0e0e1a;
    color: white;
}

.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #9b5cff;
    text-shadow: 0 0 15px #9b5cff;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #cfcfff;
}

.player-card {
    background: linear-gradient(145deg, #1a1a2e, #12121f);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 0 20px rgba(155,92,255,0.4);
}

.roll {
    font-size: 72px;
    font-weight: bold;
    text-align: center;
    color: #00ffd5;
    text-shadow: 0 0 15px #00ffd5;
    animation: pulse 0.3s infinite alternate;
}

.fatal {
    color: #ff3b3b !important;
    text-shadow: 0 0 25px #ff3b3b;
    animation: flash 0.15s infinite alternate, shake 0.15s infinite;
}

.effect {
    margin-top: 10px;
    padding: 12px;
    border-radius: 12px;
    background-color: #26264a;
}

.history-card {
    background-color: #1a1a2e;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}

@keyframes pulse {
    from { transform: scale(1); }
    to { transform: scale(1.15); }
}

@keyframes flash {
    from { opacity: 1; }
    to { opacity: 0.3; }
}

@keyframes shake {
    0% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    50% { transform: translateX(5px); }
    75% { transform: translateX(-5px); }
    100% { transform: translateX(0); }
}
</style>
""", unsafe_allow_html=True)

# =====================
# Helper Functions
# =====================
def animate_d20_roll(placeholder, duration=1.2, fps=25):
    for _ in range(int(duration * fps)):
        placeholder.markdown(
            f"<div class='roll'>{random.randint(1,20)}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1 / fps)

    final = random.randint(1, 20)

    if final == 1:
        placeholder.markdown(
            "<div class='roll fatal'>1</div>",
            unsafe_allow_html=True
        )
    else:
        placeholder.markdown(
            f"<div class='roll'>{final}</div>",
            unsafe_allow_html=True
        )

    return final

def get_effect(value):
    if value == 1:
        return "☠️ Fatal Wound", "Launch dengan tangan non-dominan"
    elif 2 <= value <= 5:
        return "🐢 Slow Start", "-1 poin"
    elif 6 <= value <= 10:
        return "⏳ Time Bending", "Launch 3 detik lebih awal"
    elif 11 <= value <= 15:
        return "🌌 Space Bending", "Bebas pilih sisi launch"
    elif 16 <= value <= 19:
        return "🚀 Head Start", "+1 poin"
    else:
        return "🧠 Mind Control", "+1 poin & atur deck lawan"

# =====================
# Header
# =====================
st.markdown('<div class="title">🎲 D20 ARENA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Player 1 vs Player 2</div>', unsafe_allow_html=True)
st.divider()

# =====================
# Roll Button
# =====================
if st.button("🎲 ROLL D20", use_container_width=True):

    col1, col2 = st.columns(2)

    with col1:
        box1 = st.empty()
    with col2:
        box2 = st.empty()

    roll1 = animate_d20_roll(box1)
    roll2 = animate_d20_roll(box2)

    effect1, desc1 = get_effect(roll1)
    effect2, desc2 = get_effect(roll2)

    st.session_state.history.insert(
        0,
        {
            "round": len(st.session_state.history) + 1,
            "p1": roll1,
            "p2": roll2,
            "e1": effect1,
            "e2": effect2
        }
    )

    st.divider()

    r1, r2 = st.columns(2)

    with r1:
        st.markdown(f"""
        <div class="player-card">
            <h2>Player 1</h2>
            <div class="effect"><b>{effect1}</b><br>{desc1}</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="player-card">
            <h2>Player 2</h2>
            <div class="effect"><b>{effect2}</b><br>{desc2}</div>
        </div>
        """, unsafe_allow_html=True)

# =====================
# History Section
# =====================
st.divider()
st.subheader("📜 Roll History")

if not st.session_state.history:
    st.info("Belum ada roll.")
else:
    for h in st.session_state.history:
        st.markdown(f"""
        <div class="history-card">
            <b>Roll #{h.get('round', '?')}</b><br>
            Player 1: {h.get('p1', '-')} ({h.get('e1', '-')})<br>
            Player 2: {h.get('p2', '-')} ({h.get('e2', '-')})
        </div>
        """, unsafe_allow_html=True)

# =====================
# Clear History
# =====================
if st.button("🗑️ Clear History"):
    st.session_state.history = []
