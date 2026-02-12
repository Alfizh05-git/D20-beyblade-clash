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
    transition: 0.3s;
}

.winner {
    border: 2px solid #00ffd5;
    box-shadow: 0 0 30px #00ffd5;
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
def animate_d20_roll(placeholder, duration=1.3, fps=25):
    frames = int(duration * fps)
    for _ in range(frames):
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
        return "⏳ Time Bending", "Launch 1 detik lebih awal"
    elif 11 <= value <= 15:
        return "🌌 Space Bending", "Bebas pilih sisi launch"
    elif 16 <= value <= 19:
        return "🚀 Head Start", "+1 poin"
    else:
        return "🧠 Mind Control", "+1 poin & atur deck lawan"

def suit_winner(s1, s2):
    rules = {"Batu": "Gunting", "Gunting": "Kertas", "Kertas": "Batu"}
    if s1 == s2:
        return None
    return 1 if rules[s1] == s2 else 2

# =====================
# Header
# =====================
st.markdown('<div class="title">🎲 D20 ARENA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Roll the dice. Bend reality.</div>', unsafe_allow_html=True)
st.divider()

# =====================
# Player Setup
# =====================
c1, c2 = st.columns(2)

with c1:
    p1_name = st.text_input("Nama Pemain 1", "Pemain 1")
    p1_point = st.number_input("Poin Awal", value=0)
    suit1 = st.selectbox("Suit", ["Batu", "Gunting", "Kertas"], key="s1")

with c2:
    p2_name = st.text_input("Nama Pemain 2", "Pemain 2")
    p2_point = st.number_input("Poin Awal ", value=0)
    suit2 = st.selectbox("Suit ", ["Batu", "Gunting", "Kertas"], key="s2")

st.divider()

# =====================
# Roll Button
# =====================
if st.button("🎲 ROLL D20", use_container_width=True):

    rcol1, rcol2 = st.columns(2)

    with rcol1:
        roll_box_1 = st.empty()
    with rcol2:
        roll_box_2 = st.empty()

    roll1 = animate_d20_roll(roll_box_1)
    roll2 = animate_d20_roll(roll_box_2)

    effect1, desc1 = get_effect(roll1)
    effect2, desc2 = get_effect(roll2)

    affected = []

    # Conflict rules
    if effect1 == effect2:
        if "Time Bending" in effect1:
            if p1_point != p2_point:
                affected.append(p1_name if p1_point < p2_point else p2_name)
            else:
                affected.append(p1_name if suit_winner(suit1, suit2) == 1 else p2_name)

        elif "Space Bending" in effect1:
            if p1_point != p2_point:
                affected.append(p1_name if p1_point > p2_point else p2_name)
            else:
                affected.append(p1_name if suit_winner(suit1, suit2) == 1 else p2_name)

    # Point changes
    if 2 <= roll1 <= 5:
        p1_point -= 1
    if 2 <= roll2 <= 5:
        p2_point -= 1
    if roll1 >= 16:
        p1_point += 1
    if roll2 >= 16:
        p2_point += 1

    # =====================
    # Result Cards
    # =====================
    rc1, rc2 = st.columns(2)

    with rc1:
        cls = "player-card winner" if p1_name in affected else "player-card"
        st.markdown(f"""
        <div class="{cls}">
            <h2>{p1_name}</h2>
            <div class="effect"><b>{effect1}</b><br>{desc1}</div>
            <h3>🏁 Poin: {p1_point}</h3>
        </div>
        """, unsafe_allow_html=True)

    with rc2:
        cls = "player-card winner" if p2_name in affected else "player-card"
        st.markdown(f"""
        <div class="{cls}">
            <h2>{p2_name}</h2>
            <div class="effect"><b>{effect2}</b><br>{desc2}</div>
            <h3>🏁 Poin: {p2_point}</h3>
        </div>
        """, unsafe_allow_html=True)

    if affected:
        st.success(f"⚡ Efek khusus berlaku untuk **{affected[0]}**")
