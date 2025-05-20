import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta
def generate_7_day_prediction(data):
    if data is None or data.empty or len(data) < 30:
        return pd.DataFrame()

    df = data[["Datetime", "Close"]].copy().dropna()
    df["ds"] = pd.to_datetime(df["Datetime"]).dt.tz_localize(None)
    df = df.rename(columns={"Close": "y"})

    for i in range(1, 8):
        df[f"y_shift{i}"] = df["y"].shift(i)

    df = df.dropna()

    X = df[[f"y_shift{i}" for i in range(1, 8)]]
    y = df["y"]

    model = LinearRegression()
    model.fit(X, y)

    last_values = list(
        df.iloc[-1][
            [
                "y",
                "y_shift1",
                "y_shift2",
                "y_shift3",
                "y_shift4",
                "y_shift5",
                "y_shift6",
            ]
        ].values
    )

    predictions = []
    dates = [df["ds"].iloc[-1] + timedelta(days=i) for i in range(1, 8)]

    for i in range(7):
        input_features = last_values[-7:]
        next_val = model.predict([input_features])[0]
        next_val = max(0, next_val)
        predictions.append(next_val)
        last_values.append(next_val)

    return pd.DataFrame({"Datetime": dates, "Predicted": predictions})
