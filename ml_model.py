import pandas as pd
import joblib
import os

from sklearn.linear_model import LogisticRegression

MODEL_PATH = "models/hr_model.pkl"


# =========================
# TRAIN MODEL
# =========================
def train_model(df: pd.DataFrame):
    df = df.copy()

    if df.empty or "status" not in df.columns:
        return None, None

    df["target"] = df["status"].apply(lambda x: 1 if x == "terminated" else 0)

    features = []

    if "salary" in df.columns:
        features.append("salary")
    if "tenure" in df.columns:
        features.append("tenure")

    if not features:
        return None, None

    X = df[features]
    y = df["target"]

    model = LogisticRegression()
    model.fit(X, y)

    return model, features


# =========================
# SAVE MODEL
# =========================
def save_model(model, features):
    os.makedirs("models", exist_ok=True)
    joblib.dump((model, features), MODEL_PATH)
    print("💾 Model saved")


# =========================
# LOAD MODEL
# =========================
def load_model():
    if os.path.exists(MODEL_PATH):
        print("📦 Loading existing model")
        return joblib.load(MODEL_PATH)
    return None, None


# =========================
# TRAIN + SAVE PIPELINE
# =========================
def train_and_save(df):
    model, features = train_model(df)

    if model:
        save_model(model, features)

    return model, features


# =========================
# PREDICT RISK (SMART)
# =========================
def predict_risk(df: pd.DataFrame):
    df = df.copy()

    # Try loading existing model
    model, features = load_model()

    # If no model → train one
    if model is None:
        print("⚠️ No model found → training new model")
        model, features = train_and_save(df)

    if model is None:
        return df

    X = df[features]

    probs = model.predict_proba(X)[:, 1]

    df["risk_probability"] = probs

    df["risk_level"] = df["risk_probability"].apply(
        lambda p: "HIGH" if p > 0.7 else "MEDIUM" if p > 0.4 else "LOW"
    )

    return df