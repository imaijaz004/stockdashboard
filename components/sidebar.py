import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def sidebar_content():
    with st.sidebar:
        # Logo
        img = Image.open("assets/dashboard.png")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()

        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{img_b64}" width="70" style="margin-right: 15px;margin:10px;">
                <h1 style="margin: 0;"><strong>TickrView</strong></h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Styled sidebar navigation
        st.sidebar.markdown(
            """
            <div style="padding: 0px; font-size: 18px;">
                <strong style="font-size: 26px;">Navigate</strong>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Page navigation
        return st.sidebar.radio("Navigate", ["Home", "About"])