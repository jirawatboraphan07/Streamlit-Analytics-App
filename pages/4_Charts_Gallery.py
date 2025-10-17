
import streamlit as st
import pandas as pd
from utils.charts import line, bar, scatter, heatmap_from_corr
from utils.transforms import correlation

st.title("📊 Charts Gallery")

df = st.session_state.get("df")
if df is None:
    df = pd.read_csv("data/sample.csv")
    st.info("Using sample dataset (data/sample.csv). Upload your own in 'Upload & Clean'.")

st.caption("Prebuilt chart templates using the current dataframe.")

with st.expander("Line template", expanded=True):
    if "date" in df.columns:
        y_candidates = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if y_candidates:
            st.plotly_chart(line(df, x="date", y=y_candidates[0], title=f"{y_candidates[0]} over time"), use_container_width=True)
        else:
            st.write("No numeric column found.")
    else:
        st.write("No 'date' column found.")

with st.expander("Bar template", expanded=True):
    cats = [c for c in df.columns if df[c].dtype.name in ("object", "category")]
    nums = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if cats and nums:
        st.plotly_chart(bar(df, x=cats[0], y=nums[0], title=f"{nums[0]} by {cats[0]}"), use_container_width=True)
    else:
        st.write("Need one categorical and one numeric column.")

with st.expander("Scatter template", expanded=True):
    nums = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if len(nums) >= 2:
        st.plotly_chart(scatter(df, x=nums[0], y=nums[1], title=f"{nums[1]} vs {nums[0]}"), use_container_width=True)
    else:
        st.write("Need at least two numeric columns.")

with st.expander("Correlation heatmap", expanded=True):
    corr = correlation(df, numeric_only=True)
    st.plotly_chart(heatmap_from_corr(corr), use_container_width=True)
