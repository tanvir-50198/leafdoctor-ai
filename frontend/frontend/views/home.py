import streamlit as st

from utils import CROPS

with st.container(key="hero"):
    st.markdown(
        '<div class="eyebrow">🌿 AI-POWERED PLANT HEALTH</div>'
        '<div class="hero-title">Spot crop leaf diseases in seconds</div>'
        '<div class="hero-sub">Upload or snap a photo of a leaf. Our deep-learning model identifies the crop, '
        "the disease, and gives you practical next steps.</div>",
        unsafe_allow_html=True,
    )
    col, _ = st.columns([1, 3])
    with col:
        st.page_link("views/diagnose.py", label="Start diagnosis", icon="🔬")

st.markdown(
    '<div class="stats">'
    '<div class="stat"><b>6</b><span>Supported crops</span></div>'
    '<div class="stat"><b>27</b><span>Disease classes</span></div>'
    '<div class="stat"><b>Top-3</b><span>Ranked predictions</span></div>'
    '<div class="stat"><b>Instant</b><span>Treatment guidance</span></div>'
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-head">Why LeafDoctor AI</div>'
    '<div class="section-sub">Built for farmers, students and agronomists who need a quick first opinion.</div>'
    '<div class="grid-3">'
    '<div class="feature"><div class="ico">⚡</div><div class="ft">Fast diagnosis</div>'
    '<div class="fd">A fine-tuned EfficientNetV2 model reads your leaf photo and returns a result in moments.</div></div>'
    '<div class="feature"><div class="ico">🩺</div><div class="ft">Actionable advice</div>'
    '<div class="fd">Every result comes with a short explanation of the problem and what to do about it.</div></div>'
    '<div class="feature"><div class="ico">📱</div><div class="ft">Works with your phone</div>'
    '<div class="fd">Take a photo directly with your camera or upload one from your gallery.</div></div>'
    "</div>",
    unsafe_allow_html=True,
)

cards = "".join(
    f'<div class="crop-card"><div class="emoji">{e}</div><div class="cname">{n}</div>'
    f'<div class="cmeta">{c} classes</div></div>'
    for n, e, c in CROPS
)
st.markdown(
    '<div class="section-head">Supported crops</div>'
    '<div class="section-sub">Browse every disease in the Crop Library page.</div>'
    f'<div class="grid-6">{cards}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-head">How it works</div>'
    '<div class="section-sub">Three simple steps.</div>'
    '<div class="steps">'
    '<div class="step"><div class="num">1</div><div class="ft">Add a photo</div>'
    '<div class="fd">Upload an image or use your camera. One leaf, good light.</div></div>'
    '<div class="step"><div class="num">2</div><div class="ft">AI analyses it</div>'
    '<div class="fd">The model compares it with 27 crop-disease patterns it has learned.</div></div>'
    '<div class="step"><div class="num">3</div><div class="ft">Take action</div>'
    '<div class="fd">Read the diagnosis, confidence and recommended next steps.</div></div>'
    "</div>",
    unsafe_allow_html=True,
)

with st.container(key="cta"):
    st.markdown(
        '<div class="hero-title small">Ready to check a leaf?</div>'
        '<div class="hero-sub">It takes less than a minute. No sign-up needed.</div>',
        unsafe_allow_html=True,
    )
    _, mid, _ = st.columns([2, 1.2, 2])
    with mid:
        st.page_link("views/diagnose.py", label="Diagnose now", icon="🔬")
