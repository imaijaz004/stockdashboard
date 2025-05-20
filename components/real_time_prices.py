import streamlit as st
from utils.fetch_data import fetch_stock_data, process_data
import pandas as pd


def show_real_time_prices():
    st.subheader("Real-Time Prices")
    stock_symbols = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NVDA", "NFLX"]
    cols = st.columns(2)

    for idx, symbol in enumerate(stock_symbols):
        try:
            real_time_data = fetch_stock_data(symbol, "1d", "1m")
            if not real_time_data.empty:
                if isinstance(real_time_data.columns, pd.MultiIndex):
                    real_time_data.columns = [col[0] for col in real_time_data.columns]
                real_time_data = process_data(real_time_data)

                if "Close" in real_time_data.columns:
                    last_price = real_time_data["Close"].iloc[-1]
                    open_price = real_time_data["Open"].iloc[0]

                    last_price = float(last_price) if pd.notna(last_price) else 0.0
                    open_price = float(open_price) if pd.notna(open_price) else 0.0

                    change = last_price - open_price
                    pct_change = (change / open_price) * 100 if open_price != 0 else 0

                    with cols[idx % 2]:  # Alternate between the 2 columns
                        st.metric(
                            label=f"{symbol}",
                            value=f"{last_price:.2f} USD",
                            delta=f"{change:.2f} ({pct_change:.2f}%)",
                        )
                else:
                    with cols[idx % 2]:
                        st.warning(f"⚠️ No 'Close' data for {symbol}.")
        except Exception as e:
            with cols[idx % 2]:
                st.warning(f"⚠️ Error for {symbol}: {e}")

