import pyrebase
import streamlit as st

firebase_config = st.secrets["firebase"]

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def clear_chart_state():
    keys_to_clear = [
        "chart_image", "stock_fig", "stock_data", "prediction", "metrics"
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        user_email = user["email"]
        st.session_state["user"] = user_email
        st.session_state["messages"] = []  #deletes any previous prompts
        st.query_params.update({"user": user_email})  # NEW SYNTAX
        clear_chart_state()
        return True
    except:
        return False


def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        user_email = user["email"]
        st.session_state["user"] = user_email
        st.session_state["messages"] = []  #deletes any previous prompts by the previous user logged or signed
        st.query_params.update({"user": user_email})  # NEW SYNTAX
        clear_chart_state()
        return True
    except Exception as e:
        st.error(f"Signup error: {extract_error_message(e)}")
        return False

def logout():
    st.session_state.pop("user", None)  # Clear user
    clear_chart_state()
    st.session_state["logout_triggered"] = True


def extract_error_message(e):
    try:
        return e.args[1]["error"]["message"]
    except:
        return str(e)
