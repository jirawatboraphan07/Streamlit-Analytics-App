
import streamlit as st

st.title("⚙️ Settings")

if "settings" not in st.session_state:
    st.session_state["settings"] = {
        "theme": "light",
        "thousands_sep": ",",
        "decimals": 2,
        "language": "en",
    }

with st.form("settings_form"):
    theme = st.selectbox("Theme", ["light", "dark"], index=0 if st.session_state["settings"]["theme"]=="light" else 1)
    thousands = st.text_input("Thousands separator", value=st.session_state["settings"]["thousands_sep"]
    )
    decimals = st.number_input("Decimal places", min_value=0, max_value=8, value=st.session_state["settings"]["decimals"]
    )
    language = st.selectbox("Language", ["en", "th"], index=0 if st.session_state["settings"]["language"]=="en" else 1)

    submitted = st.form_submit_button("Save settings")
    if submitted:
        st.session_state["settings"].update({
            "theme": theme,
            "thousands_sep": thousands,
            "decimals": decimals,
            "language": language
        })
        st.success("Settings saved (stored in session only). Reload to apply theme.")

st.caption("Note: For a global theme, edit .streamlit/config.toml in the repo.")
