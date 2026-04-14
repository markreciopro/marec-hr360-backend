import pandas as pd

def calculate_risk_score(row):
    score = 0

    # Salary risk
    if "salary" in row and row["salary"] < 45000:
        score += 2

    # Tenure risk
    if "tenure" in row and row["tenure"] < 2:
        score += 2

    # Status risk (historical)
    if "status" in row and row["status"] == "terminated":
        score += 3

    return score


def classify_risk(score):
    if score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    else:
        return "LOW"


def add_risk_scores(df: pd.DataFrame):
    if df.empty:
        return df

    df = df.copy()

    df["risk_score"] = df.apply(calculate_risk_score, axis=1)
    df["risk_level"] = df["risk_score"].apply(classify_risk)

    return df