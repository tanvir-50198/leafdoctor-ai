"""Shared helpers: API calls, result rendering, site constants."""
import os

import requests
import streamlit as st

DEFAULT_API = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

# ---- edit these for your About page ----
AUTHOR_NAME = "Abdur Rahman Tanvir"
AUTHOR_ROLE = "CSE Student"
GITHUB_URL = ""
LINKEDIN_URL = ""
EMAIL = ""

CROPS = [  # (name, emoji, number of classes)
    ("Tomato", "🍅", 10),
    ("Potato", "🥔", 3),
    ("Corn", "🌽", 4),
    ("Pepper", "🫑", 2),
    ("Grape", "🍇", 4),
    ("Apple", "🍎", 4),
]
TONES = {"ok": "Healthy", "bad": "Disease detected", "warn": "Not sure"}


def crop_emoji(name: str) -> str:
    for crop, emoji, _ in CROPS:
        if name.lower().startswith(crop.lower()):
            return emoji
    return "🌱"


def api_url() -> str:
    return st.session_state.get("api_url", DEFAULT_API).rstrip("/")


@st.cache_data(ttl=5, show_spinner=False)
def _alive(url: str) -> bool:
    try:
        return requests.get(f"{url}/health", timeout=2).ok
    except requests.RequestException:
        return False


def api_online() -> bool:
    return _alive(api_url())


def predict(file) -> dict:
    r = requests.post(
        f"{api_url()}/predict",
        files={"file": (file.name, file.getvalue(), file.type or "image/jpeg")},
        timeout=60,
    )
    if not r.ok:
        try:
            detail = r.json().get("detail", r.text)
        except ValueError:
            detail = r.text
        raise RuntimeError(detail)
    return r.json()


@st.cache_data(ttl=300, show_spinner=False)
def _library(url: str) -> list:
    r = requests.get(f"{url}/classes", timeout=10)
    r.raise_for_status()
    return r.json()


def get_library():
    try:
        return _library(api_url())
    except requests.RequestException:
        return None


def tone_of(p: dict) -> str:
    if p["low_confidence"]:
        return "warn"
    return "ok" if p["healthy"] else "bad"


def render_result(res: dict) -> None:
    p = res["prediction"]
    tone = tone_of(p)
    pct = p["confidence"] * 100
    st.markdown(
        '<div class="card">'
        f'<span class="badge {tone}">{TONES[tone]}</span>'
        f'<div class="crop">{crop_emoji(p["crop"])} {p["crop"]}</div>'
        f'<div class="disease">{p["disease"]}</div>'
        f'<div class="conf-row"><span>Confidence</span><b>{pct:.1f}%</b></div>'
        f'<div class="bar-bg"><div class="bar-fill {tone}" style="width:{pct:.1f}%"></div></div>'
        "</div>",
        unsafe_allow_html=True,
    )
    if p["low_confidence"]:
        st.warning(
            "The model is not confident about this photo. Retake it with a single leaf, "
            "good daylight and a plain background."
        )

    rows = "".join(
        f'<div class="top-row"><span>{t["crop"]} · {t["disease"]}</span>'
        f'<b>{t["confidence"] * 100:.1f}%</b></div>'
        f'<div class="bar-bg thin"><div class="bar-fill neutral" style="width:{t["confidence"] * 100:.1f}%"></div></div>'
        for t in res["top3"]
    )
    st.markdown(
        f'<div class="card"><div class="card-title">Top 3 possibilities</div>{rows}</div>',
        unsafe_allow_html=True,
    )

    info = res["info"]
    st.markdown(
        '<div class="card">'
        '<div class="card-title">About this result</div>'
        f'<p class="para">{info["about"]}</p>'
        '<div class="card-title">What to do</div>'
        f'<p class="para">{info["action"]}</p>'
        "</div>",
        unsafe_allow_html=True,
    )
