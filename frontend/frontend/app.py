"""LeafDoctor AI - multipage Streamlit website.  Run: streamlit run app.py"""
from pathlib import Path

import streamlit as st

from utils import api_online

st.set_page_config(
    page_title="LeafDoctor AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed"
)

HERE = Path(__file__).parent

# Night-mode design tokens (light tokens live in style.css)
DARK_TOKENS = """
:root {
  --bg: #09130e; --surface: #101e17; --surface-2: #172a21;
  --text: #e6f2ea; --muted: #8fa89a; --border: #1f362a;
  --primary: #3ecf8e; --primary-hover: #2fb67a; --on-primary: #04210f;
  --ok: #5be39b; --ok-bg: #12382a;
  --bad: #ff8a80; --bad-bg: #3a1a1a;
  --warn: #ffcf70; --warn-bg: #3a2e12;
  --track: #1b3226;
  --hero: linear-gradient(135deg, #0b2a1c 0%, #11553a 55%, #1b8059 100%);
  --shadow: 0 14px 34px -20px rgba(0, 0, 0, .8);
}
"""

# ---- theme state (persisted in the URL as ?theme=dark) ----
if "dark" not in st.session_state:
    st.session_state["dark"] = st.query_params.get("theme") == "dark"

css = (HERE / "style.css").read_text()
st.markdown(
    f"<style>{css}{DARK_TOKENS if st.session_state['dark'] else ''}</style>",
    unsafe_allow_html=True,
)

# ---- navigation (top bar on Streamlit >= 1.46, sidebar fallback otherwise) ----
pages = [
    st.Page("views/home.py", title="Home", icon="🏠", default=True),
    st.Page("views/diagnose.py", title="Diagnose", icon="🔬"),
    st.Page("views/library.py", title="Crop Library", icon="📚"),
    st.Page("views/how_it_works.py", title="How it Works", icon="⚙️"),
    st.Page("views/about.py", title="About", icon="ℹ️"),
]
try:
    nav = st.navigation(pages, position="top")
except TypeError:
    nav = st.navigation(pages)

# ---- brand row ----
c_brand, c_status, c_toggle = st.columns([5, 2.2, 1.8], vertical_alignment="center")
with c_brand:
    st.markdown(
        '<div class="brand"><span class="logo">🌿</span><span>LeafDoctor <span class="ai">AI</span></span></div>',
        unsafe_allow_html=True,
    )
with c_status:
    online = api_online()
    state, label = ("on", "API online") if online else ("off", "API offline")
    st.markdown(
        f'<div style="text-align:right"><span class="pill {state}">● {label}</span></div>',
        unsafe_allow_html=True,
    )
with c_toggle:
    dark = st.toggle("🌙 Night mode", key="dark")

wanted = "dark" if dark else "light"
if st.query_params.get("theme") != wanted:
    st.query_params["theme"] = wanted

# ---- current page ----
nav.run()

st.markdown(
    '<div class="footer">🌿 LeafDoctor AI · Built with PyTorch, FastAPI and Streamlit<br>'
    "AI results are a first screening, not a final diagnosis. Confirm with a local agriculture officer.</div>",
    unsafe_allow_html=True,
)
