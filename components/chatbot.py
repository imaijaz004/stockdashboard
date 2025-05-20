import streamlit as st
from openai import OpenAI

def ai_chatbot():
    st.header("💬 AI Stock Analyst Chatbot")

    # ✅ Use Streamlit secrets for the API key
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["openai"]["api_key"],
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Ask me anything...")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="shisa-ai/shisa-v2-llama3.3-70b:free",
                messages=st.session_state.messages,
            )
            bot_reply = response.choices[0].message.content
            st.chat_message("assistant").markdown(bot_reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": bot_reply}
            )
        except Exception as e:
            st.error(f"❌ Failed to get response: {e}")

