# pipeline.py

import pandas as pd


def load_file(file):
    """Load CSV or Excel safely"""
    if file.filename.endswith(".csv"):
        return pd.read_csv(file.file)
    elif file.filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(file.file)
    else:
        raise ValueError("Unsupported file format")


def clean_columns(df):
    """Standardize column names"""
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    return df


def clean_data(df):
    """Core data cleaning logic"""

    df = clean_columns(df)

    # Normalize status
    if "status" in df.columns:
        df["status"] = (
            df["status"]
            .astype(str)
            .str.strip()
            .str.title()
        )

    # Fill department
    if "department" in df.columns:
        df["department"] = df["department"].fillna("Unknown")

    # Remove empty rows
    df = df.dropna(how="all")

    return df


def process_file(file):
    """Full pipeline"""
    df = load_file(file)
    df = clean_data(df)
    return df