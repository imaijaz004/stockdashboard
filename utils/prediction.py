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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on test set and evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mean_actual = y_test.mean()
    accuracy = 100 - (mae / mean_actual * 100)
    # Print evaluation metrics to terminal (or log if needed)
    print(f" Prediction Evaluation:")
    print(f" - Mean Squared Error (MSE): {mse:.2f}")
    print(f" - Mean Absolute Error (MAE): {mae:.2f}")
    print(f" - Percentage Accuracy: {accuracy:.2f}%")
    # Generate prediction for next 7 days
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