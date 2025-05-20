import ta
import pandas as pd


def add_technical_indicators(data):
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    close_series = data["Close"]
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.squeeze()

    data["SMA_20"] = ta.trend.sma_indicator(close_series, window=20)
    data["EMA_20"] = ta.trend.ema_indicator(close_series, window=20)

    data["BB_upper"] = ta.volatility.bollinger_hband(close_series, window=20)
    data["BB_middle"] = ta.volatility.bollinger_mavg(close_series, window=20)
    data["BB_lower"] = ta.volatility.bollinger_lband(close_series, window=20)

    typical_price = (data["High"] + data["Low"] + data["Close"]) / 3
    cumulative_tp_vol = (typical_price * data["Volume"]).cumsum()
    cumulative_vol = data["Volume"].cumsum()
    data["VWAP"] = cumulative_tp_vol / cumulative_vol

    return data
