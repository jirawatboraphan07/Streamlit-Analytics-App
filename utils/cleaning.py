
import pandas as pd

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()

def handle_missing(df: pd.DataFrame, strategy="drop", fill_value=0):
    if strategy == "drop":
        return df.dropna()
    if strategy == "fill_zero":
        return df.fillna(0)
    if strategy == "fill_value":
        return df.fillna(fill_value)
    return df

def cast_numeric(df: pd.DataFrame, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def cast_category(df: pd.DataFrame, cols):
    for c in cols:
        df[c] = df[c].astype("category")
    return df
