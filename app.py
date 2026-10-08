import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="HearMe — VedaThon 2026",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom minimal CSS to remove default Streamlit margins and padding for full-bleed experience
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

html_path = Path(__file__).parent / "demo" / "index.html"

if html_path.exists():
    with open(html_path, "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=3600, scrolling=True)
else:
    st.error("Demo file not found at demo/index.html")
