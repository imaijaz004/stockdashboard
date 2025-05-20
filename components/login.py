import streamlit as st
from utils.firebase_auth import login, signup
import base64
from pathlib import Path

def login_page():
    # Load logo image and encode to base64
    logo_path = Path("assets/dashboard.png")  # You can change this path
    if logo_path.exists():
        img_b64 = base64.b64encode(logo_path.read_bytes()).decode()
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{img_b64}" width="70" style="margin-right: 10px;">
                <h2 style="margin: 0;">TickrView</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.title("TickrView")  # fallback if logo not found

    st.markdown("## Welcome! Please log in or sign up")

    choice = st.selectbox("Login/Signup", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if login(email, password):
                st.success("Logged in successfully")
                # After login, rerun the app to load the dashboard
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        if st.button("Signup"):
            if signup(email, password):
                st.success("Account created successfully")
                # After signup, rerun the app to load the dashboard
                st.rerun()
            else:
                st.error("Error creating account")
