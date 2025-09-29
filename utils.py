import joblib
import lightgbm as lgb
import pandas as pd

# Load artifacts
def load_artifacts():
    model = lgb.Booster(model_file="models/lgb_sales_model.txt")
    feature_cols = joblib.load("models/feature_cols.pkl")
    return model, feature_cols

# Preprocess new input row into model-ready features
def preprocess_input(promo, holiday, date, past_sales):
    """
    Args:

        promo: int (0/1)
        holiday: int (0/1)
        date: datetime-like
        past_sales: dict with keys ['lag_1','lag_7','mean_3','mean_7']

    Returns:
        pd.DataFrame with a single row ready for prediction
    """
    date = pd.to_datetime(date)

    features = {
        "promo": promo,
        "holiday": holiday,
        "day": date.day,
        "month": date.month,
        "year": date.year,
        "day_of_week": date.weekday(),
        "is_weekend": 1 if date.weekday() >= 5 else 0,
        "sales_lag_1": past_sales.get("lag_1", 0),
        "sales_lag_7": past_sales.get("lag_7", 0),
        "rolling_mean_3": past_sales.get("mean_3", 0),
        "rolling_mean_7": past_sales.get("mean_7", 0),
    }

    return pd.DataFrame([features])

# Prediction
def predict_sales(model, feature_cols, promo, holiday, date, lag_1, lag_7, mean_3, mean_7):
    past_sales = {
        "lag_1": lag_1,
        "lag_7": lag_7,
        "mean_3": mean_3,
        "mean_7": mean_7,
    }
    X = preprocess_input(promo, holiday, date, past_sales)
    X = X[feature_cols]  # ensure correct column order
    prediction = model.predict(X)[0]
    return round(prediction, 2)
