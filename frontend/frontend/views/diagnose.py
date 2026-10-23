import requests
import streamlit as st

from utils import crop_emoji, predict, render_result, tone_of

st.markdown(
    '<div class="page-title">Diagnose a leaf</div>'
    '<div class="page-sub">Upload a clear photo of a single leaf, or take one with your camera. '
    "The closer and sharper the photo, the better the result.</div>",
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="step-label"><span>1</span> Add a leaf photo</div>', unsafe_allow_html=True)
    tab_up, tab_cam = st.tabs(["📁 Upload", "📷 Camera"])
    with tab_up:
        uploaded = st.file_uploader(
            "Leaf image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed"
        )
    with tab_cam:
        captured = st.camera_input("Take a photo", label_visibility="collapsed")
    image_file = uploaded or captured

    if image_file:
        st.image(image_file, use_container_width=True)
    analyze = st.button(
        "🔍 Diagnose leaf", type="primary", use_container_width=True, disabled=image_file is None
    )
    with st.expander("📸 Tips for an accurate result"):
        st.markdown(
            "- One leaf, filling most of the frame\n"
            "- Natural daylight, no harsh shadows\n"
            "- Plain background if possible\n"
            "- Sharp focus on the affected area"
        )

with right:
    st.markdown('<div class="step-label"><span>2</span> Diagnosis</div>', unsafe_allow_html=True)
    if analyze and image_file:
        try:
            with st.spinner("Analysing leaf..."):
                res = predict(image_file)
            st.session_state["result"] = res
            p = res["prediction"]
            history = st.session_state.setdefault("history", [])
            history.insert(
                0,
                {
                    "crop": p["crop"],
                    "disease": p["disease"],
                    "conf": p["confidence"],
                    "tone": tone_of(p),
                },
            )
            del history[6:]
        except requests.ConnectionError:
            st.session_state.pop("result", None)
            st.error("Cannot reach the backend. Start it with `uvicorn main:app --port 8000`.")
        except Exception as e:  # noqa: BLE001
            st.session_state.pop("result", None)
            st.error(f"Diagnosis failed: {e}")

    if "result" in st.session_state:
        render_result(st.session_state["result"])
    else:
        st.markdown(
            '<div class="card empty">🌱<br>Your diagnosis will appear here.<br>'
            "Add a photo and press <b>Diagnose leaf</b>.</div>",
            unsafe_allow_html=True,
        )

history = st.session_state.get("history", [])
if history:
    chips = "".join(
        f'<span class="chip"><i class="{h["tone"]}"></i>{crop_emoji(h["crop"])} {h["crop"]} · '
        f'{h["disease"]} · {h["conf"] * 100:.0f}%</span>'
        for h in history
    )
    st.markdown(
        f'<div class="section-head">Recent scans</div>'
        f'<div class="section-sub">Kept for this browser session only.</div>{chips}',
        unsafe_allow_html=True,
    )
