#kaleido chrome update 
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

    # ------------------ Normal Q&A ------------------
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

    # ------------------ Chart Analysis ------------------
    if run_analysis:
        if "chart_image" not in st.session_state or st.session_state["chart_image"] is None:
            st.warning("⚠️ Please generate stock data first, then I can analyze it for you.")
        else:
            try:

                data_tail = st.session_state["chart_image"].tail(20).to_string(index=False)

                ticker = st.session_state.get("selected_ticker", "[Symbol]")
                timeframe = st.session_state.get("selected_timeframe", "1-month")
                price = st.session_state.get("last_price", "[Current Price]")

                prompt = f"""
You are a Stock Trader specializing in Technical Analysis at a top financial institution.

Perform a detailed analysis of the following stock data for the company with ticker symbol {ticker}.
The chart represents approximately a {timeframe} period, and the stock is currently trading around {price}.

Here is the most recent stock data:
{data_tail}

**Please generate output in the following structure:**

1. Chart Overview: Trend, volume, support/resistance levels.
2. Technical Trends: Indicators like SMA/EMA, MACD, RSI, patterns.
3. Recommendation: Buy / Hold / Sell, and why.
4. Notes: Any warning signs or unique insights.
"""

                response = client.chat.completions.create(
                    model="shisa-ai/shisa-v2-llama3.3-70b:free",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                )

                reply = response.choices[0].message.content
                st.chat_message("assistant").markdown(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                st.error(f"❌ Failed to analyze chart data: {e}")



#original code
# import streamlit as st
# from openai import OpenAI
# import base64

# def ai_chatbot():
#     st.header("💬 AI Stock Analyst Chatbot")

#     client = OpenAI(
#         base_url="https://openrouter.ai/api/v1",
#         api_key=st.secrets["openai"]["api_key"],
#     )

#     if "messages" not in st.session_state:
#         st.session_state["messages"] = []

#     for msg in st.session_state.messages:
#         st.chat_message(msg["role"]).markdown(msg["content"])

#     col1, col2 = st.columns([2, 1])
#     with col1:
#         user_input = st.chat_input("Ask me anything about stocks...")

#     with col2:
#         run_analysis = st.button("📊 Analyze Chart")

#     if user_input:
#         st.chat_message("user").markdown(user_input)
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         try:
#             response = client.chat.completions.create(
#                 model="shisa-ai/shisa-v2-llama3.3-70b:free",
#                 messages=st.session_state.messages,
#             )
#             reply = response.choices[0].message.content
#             st.chat_message("assistant").markdown(reply)
#             st.session_state.messages.append({"role": "assistant", "content": reply})
#         except Exception as e:
#             st.error(f"❌ Failed to get response: {e}")

#     if run_analysis:
#         if "chart_image" not in st.session_state:
#             st.warning("⚠️ Please generate a stock chart first.")
#         else:
#             try:
#                 image_bytes = st.session_state["chart_image"].getvalue()
#                 image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#                 ticker = st.session_state.get("selected_ticker", "[Symbol]")
#                 timeframe = st.session_state.get("selected_timeframe", "1-month")
#                 price = st.session_state.get("last_price", "[Current Price]")

#                 prompt = f"""
# You are a Stock Trader specializing in Technical Analysis at a top financial institution.

# Perform a detailed analysis of the attached stock chart image for the company with ticker symbol {ticker}.
# The chart represents approximately a {timeframe} period, and the stock is currently trading around {price}.

# **Please generate output in the following structure:**

# 1. Chart Overview: Trend, volume, support/resistance levels.
# 2. Technical Trends: Indicators like SMA/EMA, MACD, RSI, patterns.
# 3. Recommendation: Buy / Hold / Sell, and why.
# 4. Notes: Any warning signs or unique insights.
# """

#                 response = client.chat.completions.create(
#                     model="shisa-ai/shisa-v2-llama3.3-70b:free",
#                     messages=[
#                         {
#                             "role": "user",
#                             "content": [
#                                 {"type": "text", "text": prompt},
#                                 {"type": "image", "image": image_base64},
#                             ],
#                         }
#                     ],
#                 )

#                 reply = response.choices[0].message.content
#                 st.chat_message("assistant").markdown(reply)
#                 st.session_state.messages.append(
#                     {"role": "assistant", "content": reply}
#                 )

#             except Exception as e:
#                 st.error(f"❌ Failed to analyze image: {e}")

