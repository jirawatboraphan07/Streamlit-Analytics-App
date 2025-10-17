
import streamlit as st
import pandas as pd
from utils.transforms import groupby_agg, correlation
from utils.charts import line, bar, scatter, heatmap_from_corr

st.title("🔎 Explore")

df = st.session_state.get("df")
if df is None:
    st.warning("No dataset in session. Go to 'Upload & Clean' first.")
    st.stop()

st.subheader("Filters")
with st.expander("Basic filters", expanded=True):
    cols = list(df.columns)
    # Simple row filter on a selected categorical column
    cat_cols = [c for c in cols if df[c].dtype.name in ("object", "category")]
    if cat_cols:
        sel = st.selectbox("Filter column (categorical)", cat_cols)
        choices = ["(all)"] + sorted(list(map(str, df[sel].dropna().unique())))
        choice = st.selectbox("Value", choices)
        if choice != "(all)":
            df = df[df[sel].astype(str) == choice]

st.subheader("Group & Aggregate")
with st.expander("Aggregation", expanded=True):
    by_cols = st.multiselect("Group by", options=list(df.columns))
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    value_col = st.selectbox("Value column", options=[None] + numeric_cols, index=0)
    agg = st.selectbox("Aggregation", ["sum", "mean", "min", "max", "count"], index=0)
    if st.button("Run aggregation"):
        g = groupby_agg(df, by_cols, value_col, agg)
        if g is not None:
            st.dataframe(g, use_container_width=True)
        else:
            st.info("Please select 'group by' and a value column.")

st.subheader("Charts")
chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs(["Line", "Bar", "Scatter", "Correlation"])

with chart_tab1:
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    x = st.selectbox("X (usually date)", options=list(df.columns))
    y = st.selectbox("Y (numeric)", options=num_cols)
    color = st.selectbox("Color (optional)", options=[None] + list(df.columns), index=0)
    if st.button("Plot line"):
        st.plotly_chart(line(df, x=x, y=y, color=color, title=f"{y} vs {x}"), use_container_width=True)

with chart_tab2:
    x = st.selectbox("X (category)", options=list(df.columns), key="bar_x")
    y = st.selectbox("Y (numeric)", options=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])], key="bar_y")
    color = st.selectbox("Color (optional)", options=[None] + list(df.columns), index=0, key="bar_color")
    if st.button("Plot bar"):
        st.plotly_chart(bar(df, x=x, y=y, color=color, title=f"{y} by {x}"), use_container_width=True)

with chart_tab3:
    x = st.selectbox("X (numeric)", options=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])], key="sc_x")
    y = st.selectbox("Y (numeric)", options=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])], key="sc_y")
    color = st.selectbox("Color (optional)", options=[None] + list(df.columns), index=0, key="sc_color")
    size = st.selectbox("Size (optional numeric)", options=[None] + [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])], index=0, key="sc_size")
    if st.button("Plot scatter"):
        st.plotly_chart(scatter(df, x=x, y=y, color=color, size=size, title=f"{y} vs {x}"), use_container_width=True)

with chart_tab4:
    corr = correlation(df, numeric_only=True)
    st.plotly_chart(heatmap_from_corr(corr), use_container_width=True)
