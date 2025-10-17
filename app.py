
import streamlit as st

st.set_page_config(page_title="Streamlit Analytics App", page_icon="📊", layout="wide")

st.title("📊 Streamlit Analytics App")
st.write("This is the entry point. Use the sidebar to navigate pages.")

st.page_link("pages/1_Dashboard.py", label="Open Dashboard", icon="🏠")
st.page_link("pages/2_Upload_and_Clean.py", label="Upload & Clean", icon="📤")
st.page_link("pages/3_Explore.py", label="Explore", icon="🔎")
st.page_link("pages/4_Charts_Gallery.py", label="Charts Gallery", icon="📊")
st.page_link("pages/5_Settings.py", label="Settings", icon="⚙️")

st.caption("Tip: Once you upload your dataset in Upload & Clean, it will be available across pages via session_state.")
