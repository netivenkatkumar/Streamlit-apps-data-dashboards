import streamlit as st
import json
import pandas as pd
import numpy as np
from PIL import Image
import zipfile
import io
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Attendance Chatbox",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
.stChatMessage {
    background-color: #020617;
}
.metric-card {
    background: linear-gradient(135deg, #1e293b, #020617);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 20px rgba(56,189,248,0.15);
}
.title {
    font-size: 42px;
    font-weight: 800;
    color: #38bdf8;
}
.subtitle {
    color: #94a3b8;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🧠 AI Attendance Chatbox</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Face Recognition • Biometrics • Smart Attendance</div>', unsafe_allow_html=True)
st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Configuration")

attendance_mode = st.sidebar.selectbox(
    "Attendance Mode",
    ["Face Recognition", "Biometric", "Manual + AI Verification"]
)

enable_ai = st.sidebar.toggle("Enable AI Assistant", True)
st.sidebar.divider()

# ---------------- KPI DASHBOARD ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">👥<h2>128</h2><p>Employees</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">✅<h2>94%</h2><p>Today Attendance</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">⏱️<h2>09:18</h2><p>Avg Check-In</p></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">🚨<h2>3</h2><p>Anomalies</p></div>', unsafe_allow_html=True)

st.divider()

# ---------------- PROFILE JSON UPLOAD ----------------
st.subheader("📂 Employee Profile (JSON)")

profile_file = st.file_uploader("Upload Office Profile JSON", type=["json"])

profile_data = None
if profile_file:
    profile_data = json.load(profile_file)
    st.success("Profile Loaded Successfully")
    st.json(profile_data)

# ---------------- PORTFOLIO ZIP ----------------
st.subheader("📦 Employee Portfolio ZIP")

zip_file = st.file_uploader("Upload Portfolio ZIP", type=["zip"])

if zip_file:
    z = zipfile.ZipFile(io.BytesIO(zip_file.read()))
    st.success(f"{len(z.namelist())} files found in portfolio")
    st.write(z.namelist())

st.divider()

# ---------------- CHATBOT ----------------
st.subheader("💬 Attendance AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about attendance, anomalies, or employees...")

def ai_response(prompt):
    """Mock AI logic (replace with LLM later)"""
    prompt = prompt.lower()

    if "attendance" in prompt:
        return "✅ Today's attendance is **94%**, with most employees checked in before 9:30 AM."
    if "late" in prompt:
        return "⏰ 7 employees checked in late today. Would you like a detailed list?"
    if "anomaly" in prompt:
        return "🚨 Detected **3 anomalies** related to unusual check-in locations."
    if "employee" in prompt:
        return "👤 Employee profiles are loaded. Ask me by name or ID."
    return "🤖 I'm monitoring attendance in real-time. How can I help?"

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response = ai_response(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------- FOOTER ----------------
st.divider()
st.caption("© 2026 • AI Attendance System • Streamlit + Open Models")
