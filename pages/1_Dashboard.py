
import streamlit as st
import pandas as pd
from utils.data_io import load_csv, coerce_datetimes
from utils.transforms import summarize_basic
from utils.charts import line, bar

st.title("🏠 Dashboard")

# Load data from session or sample
df = st.session_state.get("df", None)
if df is None:
    df = pd.read_csv("data/sample.csv")
    df = coerce_datetimes(df, cols=["date"])
    st.info("Using sample dataset (data/sample.csv). Upload your own in 'Upload & Clean'.")
else:
    st.success("Using dataset from session.")

# KPIs
summary = summarize_basic(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{summary['rows']:,}")
c2.metric("Columns", f"{summary['cols']:,}")
c3.metric("Missing %", f"{summary['missing_pct']:.2f}%")
if summary["date_range"]:
    dmin, dmax = summary["date_range"]
    c4.metric("Date Range", f"{dmin.date()} → {dmax.date()}")
else:
    c4.metric("Date Range", "—")


# Charts
st.subheader("Quick Charts")
left, right = st.columns(2)

with left:
    # If have a date column and numeric, plot a line
    candidates_num = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if "date" in df.columns and candidates_num:
        st.plotly_chart(line(df, x="date", y=candidates_num[0], color=None, title=f"{candidates_num[0]} over time"), use_container_width=True)
    else:
        st.write("No time series candidate found.")

with right:
    # bar by category if exists
    cat_cols = [c for c in df.columns if df[c].dtype.name in ("object", "category")]
    if cat_cols and candidates_num:
        top = df.groupby(cat_cols[0])[candidates_num[0]].sum().reset_index().sort_values(candidates_num[0], ascending=False).head(10)
        st.plotly_chart(bar(top, x=cat_cols[0], y=candidates_num[0], title=f"Top {cat_cols[0]} by {candidates_num[0]}"), use_container_width=True)
    else:
        st.write("No categorical/metric pair for bar chart.")
