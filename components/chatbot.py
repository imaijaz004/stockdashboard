import streamlit as st
from openai import OpenAI

def ai_chatbot():
    st.header("💬 AI Stock Analyst Chatbot")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["openai"]["api_key"],
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.chat_input("Ask me anything about stocks...")

    with col2:
        run_analysis = st.button("📊 Analyze Chart")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="shisa-ai/shisa-v2-llama3.3-70b:free",
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.chat_message("assistant").markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"❌ Failed to get response: {e}")

    if run_analysis:
        if "chart_image" not in st.session_state:
            st.warning("⚠️ Please generate a stock chart first.")
        else:
            try:
                image_bytes = st.session_state["chart_image"].getvalue()

                response = client.chat.completions.create(
                    model="shisa-ai/shisa-v2-llama3.3-70b:free",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "You are a professional stock analyst. Thoroughly analyze the stock chart image and give insights such as trend, patterns, support/resistance levels, and predictions.",
                                },
                                {
                                    "type": "image",
                                    "image": image_bytes,
                                },
                            ],
                        }
                    ],
                )
                analysis_reply = response.choices[0].message.content
                st.chat_message("assistant").markdown(analysis_reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": analysis_reply}
                )
            except Exception as e:
                st.error(f"❌ Failed to analyze image: {e}")

# import streamlit as st
# from openai import OpenAI

# def ai_chatbot():
#     st.header("💬 AI Stock Analyst Chatbot")

#     # ✅ Use Streamlit secrets for the API key
#     client = OpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=st.secrets["openai"]["api_key"],
#     )

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for msg in st.session_state.messages:
#         st.chat_message(msg["role"]).markdown(msg["content"])

#     user_input = st.chat_input("Ask me anything...")

#     if user_input:
#         st.chat_message("user").markdown(user_input)
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         try:
#             response = client.chat.completions.create(
#                 model="shisa-ai/shisa-v2-llama3.3-70b:free",
#                 messages=st.session_state.messages,
#             )
#             bot_reply = response.choices[0].message.content
#             st.chat_message("assistant").markdown(bot_reply)
#             st.session_state.messages.append(
#                 {"role": "assistant", "content": bot_reply}
#             )
#         except Exception as e:
#             st.error(f"❌ Failed to get response: {e}")

