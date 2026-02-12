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
# Session State (History)
# =====================
if "history" not in st.session_state:
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

.history-card {
    background-color: #1a1a2e;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 16px;
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
    frames = int(duration * fps)
    for _ in range(frames):
        placeholder.markdown(
            f"<div class='roll'>{random.randint(1,20)}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1 / fps)

    final = random.randint(1, 20)

    if final == 1:
        placeholder.markdown("<div class='roll fatal'>1</div>", unsafe_allow_html=True)
    else:
        placeholder.markdown(f"<div class='roll'>{final}</div>", unsafe_allow_html=True)

    return final

# =====================
# Header
# =====================
st.markdown('<div class="title">🎲 D20 ARENA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Klik roll sebanyak yang kamu mau</div>', unsafe_allow_html=True)
st.divider()

# =====================
# Roll Button
# =====================
if st.button("🎲 ROLL D20", use_container_width=True):

    col1, col2 = st.columns(2)

    with col1:
        roll_box_1 = st.empty()
    with col2:
        roll_box_2 = st.empty()

    roll1 = animate_d20_roll(roll_box_1)
    roll2 = animate_d20_roll(roll_box_2)

    # Save history
    st.session_state.history.insert(
        0,
        {
            "round": len(st.session_state.history) + 1,
            "roll1": roll1,
            "roll2": roll2
        }
    )

st.divider()

# =====================
# History Section
# =====================
st.subheader("📜 Roll History")

if not st.session_state.history:
    st.info("Belum ada roll.")
else:
    for h in st.session_state.history:
        st.markdown(
            f"""
            <div class="history-card">
                <b>Roll #{h['round']}</b> — 
                Roll 1: <b>{h['roll1']}</b> | 
                Roll 2: <b>{h['roll2']}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================
# Clear History
# =====================
if st.button("🗑️ Clear History"):
    st.session_state.history = []
