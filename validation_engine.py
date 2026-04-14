def validate_data(df):
    errors = []

    if df.empty:
        errors.append("Dataset is empty")

    if "salary" in df.columns:
        if df["salary"].max() > 1_000_000:
            errors.append("Unrealistic salary values detected")

    if "tenure" in df.columns:
        if df["tenure"].max() > 60:
            errors.append("Tenure values too high")

    return errors