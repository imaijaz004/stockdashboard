import streamlit as st
from components.sidebar import sidebar_content
from components.real_time_prices import show_real_time_prices
from components.chatbot import ai_chatbot
from utils.fetch_data import fetch_stock_data, process_data, calculate_metrics
from utils.indicators import add_technical_indicators
from utils.prediction import generate_7_day_prediction
import plotly.graph_objects as go
from components.login import login_page
from utils.firebase_auth import logout
import io

# Setting page config
st.set_page_config(layout="wide")

#  Clear query params and show logout message
if st.session_state.get("logout_triggered"):
    st.session_state.pop("logout_triggered", None)
    st.query_params.clear()  # replaces deprecated experimental_set_query_params
    st.success("Logged out successfully")
    login_page()  # Renders login page immediately after logout
    st.stop()

#  Restore user from query params 
query_params = st.query_params
if "user" in query_params and "user" not in st.session_state:
    st.session_state["user"] = query_params["user"][0]

# Check if user is logged in
if "user" not in st.session_state:
    # If not logged in, show login page
    login_page()
else:
    # User is logged in, show main dashboard
    page = sidebar_content()

    if page == "Home":

        available_tickers = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "NVDA",
            "TSLA",
            "BRK-B",
            "UNH",
            "JNJ",
            "V",
            "PG",
            "XOM",
            "JPM",
            "MA",
            "AVGO",
            "CVX",
            "HD",
            "MRK",
            "PEP",
            "ABBV",
            "LLY",
            "KO",
            "PFE",
            "ADBE",
            "NFLX",
            "T",
            "VZ",
            "CRM",
            "DIS",
            "ABT",
            "CSCO",
            "WMT",
            "INTC",
            "COST",
            "ORCL",
            "ACN",
            "DHR",
            "MCD",
            "TXN",
            "NKE",
            "LIN",
            "QCOM",
            "AMD",
            "BMY",
            "LOW",
            "NEE",
            "MS",
            "PM",
            "UPS",
            "AMGN",
            "BA",
            "HON",
            "RTX",
            "IBM",
            "SBUX",
            "CAT",
            "GE",
            "SPGI",
            "BLK",
            "TMO",
            "MDT",
        ]

        st.sidebar.button("Logout", on_click=logout)

        st.title("Stock Dashboard")
        st.markdown("---")

        col_left, col_right = st.columns([2, 2])

        # Left column for chart parameters
        with col_left:
            st.header("Chart Parameters")
            ticker = st.selectbox("Select Ticker", available_tickers)
            time_period = st.selectbox("Time Period", ["1d", "1wk", "1mo", "1y", "max"])
            chart_type = st.selectbox("Chart Type", ["Candlestick", "Line"])
            indicators = st.multiselect(
                "Technical Indicators", ["SMA 20", "EMA 20", "Bollinger Bands", "VWAP"]
            )
            update = st.button("Update Chart")

        # Right column for real-time prices
        with col_right:
            show_real_time_prices()

        # update button functionality
        if update:
            interval_mapping = {
                "1d": "1m",
                "1wk": "30m",
                "1mo": "1d",
                "1y": "1wk",
                "max": "1wk",
            }
            data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
            data = process_data(data)
            data = add_technical_indicators(data)

            last_close, change, pct_change, high, low, volume = calculate_metrics(data)
            
            #metric into buffer
            st.session_state["selected_ticker"] = ticker
            st.session_state["selected_timeframe"] = time_period
            st.session_state["last_price"] = f"${last_close:.2f}"

            st.markdown("---")
            st.metric(
                label=f'"{ticker}" Last Price',
                value=f"{last_close:.2f} USD",
                delta=f"{change:.2f} ({pct_change:.2f}%)",
            )

            fig = go.Figure()
            if chart_type == "Candlestick":
                fig.add_trace(
                    go.Candlestick(
                        x=data["Datetime"],
                        open=data["Open"],
                        high=data["High"],
                        low=data["Low"],
                        close=data["Close"],
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(x=data["Datetime"], y=data["Close"], mode="lines")
                )

            # Adding technical indicators to the plot
            for indicator in indicators:
                if indicator == "SMA 20":
                    fig.add_trace(
                        go.Scatter(
                            x=data["Datetime"],
                            y=data["SMA_20"],
                            name="SMA 20",
                            line=dict(color="blue"),
                        )
                    )
                elif indicator == "EMA 20":
                    fig.add_trace(
                        go.Scatter(x=data["Datetime"], y=data["EMA_20"], name="EMA 20")
                    )
                elif indicator == "Bollinger Bands":
                    fig.add_trace(
                        go.Scatter(
                            x=data["Datetime"],
                            y=data["BB_upper"],
                            fill=None,
                            mode="lines",
                            name="Upper Bollinger Band",
                            line=dict(color="red"),
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=data["Datetime"],
                            y=data["BB_middle"],
                            fill=None,
                            mode="lines",
                            name="Middle Bollinger Band(\"SMA_20\")",
                            line=dict(color="orange"),
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=data["Datetime"],
                            y=data["BB_lower"],
                            fill="tonexty",
                            mode="lines",
                            name="Lower Bollinger Band",
                            line=dict(color="green"),
                        )
                    )
                elif indicator == "VWAP":
                    fig.add_trace(
                        go.Scatter(x=data["Datetime"], y=data["VWAP"], name="VWAP")
                    )

            fig.update_layout(
                title=f'"{ticker}" {time_period.upper()} Chart', height=750
            )
            st.plotly_chart(fig, use_container_width=True)

            #download chart
            # buf = io.BytesIO()
            # fig.write_image(buf, format="png")
            # buf.seek(0)
            # st.session_state["chart_image"] = buf
            
            buf = io.StringIO()
            fig.write_html(buf,include_plotlyjs='cdn')
            html_bytes=buf.getvalue().encode("utf-8")
            
            #saving into
            st.session_state["chart_image"] = buf
            st.download_button(
                label="📊 Download Chart",
                data=html_bytes,
                file_name="chart.html",
                mime="text/html"
            )
            # historical table
            st.markdown("---")
            st.subheader("Historical Data")
            st.dataframe(data[["Datetime", "Open", "High", "Low", "Close", "Volume"]])

            # Displaying 7-day prediction graph
            st.markdown("---")
            st.markdown("### 7-Day Price Prediction")
            prediction_df = generate_7_day_prediction(data)
            if not prediction_df.empty:
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=prediction_df["Datetime"],
                        y=prediction_df["Predicted"],
                        mode="lines+markers",
                    )
                )
                fig.update_layout(
                    template="plotly_dark",
                    xaxis_title="Date",
                    yaxis_title="Predicted Close Price (USD)",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough data for prediction.")

        # Chatbot section
        st.markdown("---")
        ai_chatbot()

    elif page == "About":
        # About section content
        st.sidebar.button("Logout", on_click=logout)
        st.title("About This Dashboard")
        st.markdown(
            """
        This is a real-time stock market dashboard built with Streamlit and Firebase authentication. It provides the following features:
        - View live stock data with candlestick and line charts.
        - Add technical indicators like SMA, EMA, VWAP, and Bollinger Bands.
        - Analyze historical data and view 7-day stock predictions.
        - Chat with an AI-powered assistant for stock analysis.

        Created with 💡 Streamlit, Firebase, Plotly, and yFinance.
        """
        )
