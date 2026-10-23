import html

import streamlit as st

from utils import CROPS, crop_emoji, get_library

st.markdown(
    '<div class="page-title">Crop Library</div>'
    '<div class="page-sub">Browse every disease the model can recognise, with a short description '
    "and general guidance.</div>",
    unsafe_allow_html=True,
)

data = get_library()
if data is None:
    st.warning("The library loads from the backend, which is not reachable right now. Start the API and refresh.")
    st.stop()

crop_names = [c[0] for c in CROPS]
choice = st.segmented_control("Crop", ["All"] + crop_names, default="All", label_visibility="collapsed")
choice = choice or "All"
query = st.text_input("Search", placeholder="Search a disease, e.g. blight, rust, virus...", label_visibility="collapsed")

items = [d for d in data if not d["healthy"]]
if choice != "All":
    items = [d for d in items if d["crop"].lower().startswith(choice.lower())]
if query:
    q = query.lower()
    items = [d for d in items if q in d["disease"].lower() or q in d.get("about", "").lower()]

st.markdown(
    f'<div class="section-sub" style="margin-top:1rem">{len(items)} disease(s) found</div>',
    unsafe_allow_html=True,
)

if not items:
    st.info("No match. Try a different crop or keyword.")
else:
    esc = html.escape
    cards = "".join(
        '<div class="dcard"><div class="dcard-head">'
        f'<div class="emoji">{crop_emoji(d["crop"])}</div>'
        f'<div><div class="crop" style="margin:0">{esc(d["crop"])}</div>'
        f'<div class="dname">{esc(d["disease"])}</div></div></div>'
        f'<p class="para">{esc(d.get("about", ""))}</p>'
        f'<div class="action"><b>What to do:</b> {esc(d.get("action", ""))}</div></div>'
        for d in items
    )
    st.markdown(f'<div class="grid-2">{cards}</div>', unsafe_allow_html=True)
