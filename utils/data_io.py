
import io
import pandas as pd

def load_csv(file, **read_kwargs) -> pd.DataFrame:
    """Load CSV from file-like or path. Auto-parse dates if possible."""
    if file is None:
        return None
    defaults = dict(encoding=read_kwargs.pop("encoding", "utf-8"),)
    defaults.update(read_kwargs)
    df = pd.read_csv(file, **defaults)
    return df

def load_excel(file, **read_kwargs) -> pd.DataFrame:
    if file is None:
        return None
    return pd.read_excel(file, **read_kwargs)

def coerce_datetimes(df: pd.DataFrame, cols=None):
    if df is None:
        return df
    if cols is None:
        # try all object columns
        cols = [c for c in df.columns if df[c].dtype == "object"]
    for c in cols:
        try:
            df[c] = pd.to_datetime(df[c])
        except Exception:
            pass
    return df
