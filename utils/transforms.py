
import pandas as pd

AGG_FUNCS = {
    "sum": "sum",
    "mean": "mean",
    "min": "min",
    "max": "max",
    "count": "count",
}

def summarize_basic(df: pd.DataFrame):
    n_rows = len(df)
    n_cols = len(df.columns)
    missing_pct = float(df.isna().sum().sum()) / (n_rows * n_cols) * 100 if n_rows and n_cols else 0.0
    date_cols = [c for c in df.columns if str(df[c].dtype).startswith("datetime64") and df[c].notna().any()]
    date_range = None
    if date_cols:
        c = date_cols[0]
        date_range = (pd.to_datetime(df[c]).min(), pd.to_datetime(df[c]).max())
    return {
        "rows": n_rows,
        "cols": n_cols,
        "missing_pct": missing_pct,
        "date_range": date_range,
    }

def groupby_agg(df: pd.DataFrame, by_cols, value_col, agg_name: str):
    if not by_cols or value_col is None:
        return None
    agg = AGG_FUNCS.get(agg_name, "sum")
    g = df.groupby(by_cols, dropna=False)[value_col].agg(agg).reset_index()
    g = g.sort_values(by=value_col, ascending=False)
    return g

def correlation(df: pd.DataFrame, numeric_only=True):
    return df.corr(numeric_only=numeric_only)
