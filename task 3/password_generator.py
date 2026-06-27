import streamlit as st
import string
import secrets
import math

# ============================================
# DecodeLabs - Project 3: Password Generator
# Modules: string, secrets
# Key: secrets.choice() + ''.join()
# ============================================

def generate_password(length, use_letters, use_digits, use_symbols):
    """PROCESS: Build character pool and generate password"""
    
    # ---------- CHARACTER POOL (string module) ----------
    pool = ""
    if use_letters:
        pool += string.ascii_letters      
    if use_digits:
        pool += string.digits            
    if use_symbols:
        pool += string.punctuation        

    if pool == "":
        return None

    # Guarantee at least one char from each selected type
    password_chars = []
    if use_letters:
        password_chars.append(secrets.choice(string.ascii_letters))
    if use_digits:
        password_chars.append(secrets.choice(string.digits))
    if use_symbols:
        password_chars.append(secrets.choice(string.punctuation))

    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(pool))  

    secrets.SystemRandom().shuffle(password_chars)
    password = ''.join(password_chars)
    return password

def calculate_entropy(length, pool_size):
    """E = L × log2(R)"""
    if pool_size == 0:
        return 0
    return round(length * math.log2(pool_size), 2)

def get_strength(entropy):
    if entropy < 28:
        return "🔴 Very Weak", "red"
    elif entropy < 36:
        return "🟠 Weak", "orange"
    elif entropy < 60:
        return "🟡 Moderate", "yellow"
    elif entropy < 128:
        return "🟢 Strong", "green"
    else:
        return "🔵 Very Strong", "blue"

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Password Generator", page_icon="🔐", layout="centered")

# ---------- HEADER ----------
st.title("🔐 Password Generator")
st.caption("DecodeLabs • Project 3 — Cryptographically Secure")
st.divider()

# ---------- SETTINGS ----------
st.subheader("⚙️ Settings")

length = st.slider(
    "Password Length",
    min_value=8,      
    max_value=64,     
    value=16,
    step=1
)

col1, col2, col3 = st.columns(3)
with col1:
    use_letters = st.checkbox("🔤 Letters (A-Z)", value=True)
with col2:
    use_digits = st.checkbox("🔢 Numbers (0-9)", value=True)
with col3:
    use_symbols = st.checkbox("🔣 Symbols (@#$)", value=True)

st.divider()

# ---------- GENERATE BUTTON ----------
if st.button("⚡ Generate Password", type="primary", use_container_width=True):
    if not use_letters and not use_digits and not use_symbols:
        st.error("Please select at least one character type!")
    else:
        password = generate_password(length, use_letters, use_digits, use_symbols)

        # Pool size for entropy calculation
        pool_size = 0
        if use_letters: pool_size += 52
        if use_digits:  pool_size += 10
        if use_symbols: pool_size += 32

        entropy = calculate_entropy(length, pool_size)
        strength_label, strength_color = get_strength(entropy)

        # Save to session
        st.session_state.password = password
        st.session_state.entropy = entropy
        st.session_state.strength = strength_label
        st.session_state.pool_size = pool_size

# ---------- OUTPUT ----------
if "password" in st.session_state:
    st.subheader("🔑 Generated Password")
    st.code(st.session_state.password, language=None)

    col1, col2, col3 = st.columns(3)
    col1.metric("📏 Length", len(st.session_state.password))
    col2.metric("🔢 Entropy", f"{st.session_state.entropy} bits")
    col3.metric("💪 Strength", st.session_state.strength)

    st.divider()

    # ---------- ENTROPY INFO ----------
    st.subheader("📊 Security Analysis")
    entropy = st.session_state.entropy

    if entropy >= 128:
        st.success("🔵 Very Strong — Secure for millions of years against modern GPUs.")
    elif entropy >= 60:
        st.success("🟢 Strong — Excellent security for everyday use.")
    elif entropy >= 36:
        st.warning("🟡 Moderate — Consider increasing length or adding symbols.")
    elif entropy >= 28:
        st.warning("🟠 Weak — Increase length to at least 12 characters.")
    else:
        st.error("🔴 Very Weak — This password can be cracked quickly!")

    st.caption(f"Entropy Formula: E = L × log₂(R) = {len(st.session_state.password)} × log₂({st.session_state.pool_size}) = {entropy} bits")

    st.divider()

    # ---------- HISTORY ----------
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("💾 Save to History", use_container_width=True):
        st.session_state.history.append({
            "password": st.session_state.password,
            "entropy": st.session_state.entropy,
            "strength": st.session_state.strength
        })
        st.success("Saved!")

if "history" in st.session_state and len(st.session_state.history) > 0:
    st.subheader("📋 Password History")
    for i, item in enumerate(reversed(st.session_state.history), 1):
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        with col1:
            st.code(item["password"], language=None)
        with col2:
            st.write(f"{item['entropy']} bits")
        with col3:
            st.write(item["strength"])

    if st.button("🗑 Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

if __name__ == "__main__":
    pass