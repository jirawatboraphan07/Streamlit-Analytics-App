
import streamlit as st
import pandas as pd
from utils.data_io import load_csv, load_excel, coerce_datetimes
from utils.cleaning import drop_duplicates, handle_missing, cast_numeric, cast_category

st.title("📤 Upload & Clean")

with st.expander("Upload a dataset", expanded=True):
    source = st.radio("File type", ["CSV", "Excel"], horizontal=True)
    file = st.file_uploader("Upload file", type=["csv", "xlsx", "xls"])    

    read_options = {}
    if source == "CSV":
        read_options["encoding"] = st.selectbox("Encoding", ["utf-8", "latin-1", "cp874"], index=0)
        delimiter = st.text_input("Delimiter (CSV)", value=",")
        read_options["sep"] = delimiter or ","

    if st.button("Load") and file is not None:
        try:
            if source == "CSV":
                df = pd.read_csv(file, **read_options)
            else:
                df = load_excel(file)
            st.session_state["df"] = df
            st.success(f"Loaded dataframe with shape {df.shape}.")
        except Exception as e:
            st.error(f"Failed to load: {e}")

df = st.session_state.get("df")
if df is None:
    st.stop()

st.subheader("Preview")
st.dataframe(df.head(50), use_container_width=True)

st.subheader("Basic cleaning")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Drop duplicates"):
        st.session_state["df"] = drop_duplicates(st.session_state["df"])
        st.experimental_rerun()

with c2:
    missing_strategy = st.selectbox("Missing strategy", ["none", "drop", "fill_zero", "fill_value"], index=0)
    if missing_strategy != "none":
        fill_val = st.text_input("Fill value (for 'fill_value')", value="0")
        if st.button("Apply missing strategy"):
            v = pd.to_numeric(fill_val, errors="ignore")
            st.session_state["df"] = handle_missing(st.session_state["df"], strategy=missing_strategy, fill_value=v)
            st.experimental_rerun()

with c3:
    # dtype helpers
    num_cols = st.multiselect("Cast to numeric", options=list(df.columns))
    cat_cols = st.multiselect("Cast to category", options=[c for c in df.columns if c not in num_cols])
    if st.button("Apply dtypes"):
        if num_cols:
            st.session_state["df"] = cast_numeric(st.session_state["df"], num_cols)
        if cat_cols:
            st.session_state["df"] = cast_category(st.session_state["df"], cat_cols)
        st.experimental_rerun()

st.success("Data is stored in session_state as 'df' and is available on other pages.")
