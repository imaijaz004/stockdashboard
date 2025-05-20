import yfinance as yf
from datetime import datetime, timedelta


def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    if period == "1wk":
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data


def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize("UTC")
    data.index = data.index.tz_convert("US/Eastern")
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "Datetime"}, inplace=True)
    return data


def calculate_metrics(data):
    last_close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data["High"].max()
    low = data["Low"].min()
    volume = data["Volume"].sum()
    return last_close, change, pct_change, high, low, volume
