"""LeafDoctor AI - FastAPI backend.

Run:  uvicorn main:app --reload --port 8000   (from the backend/ folder)
Needs models/model.pt and models/classes.json (created by the Colab notebook).
"""
import io
import json
import os
import urllib.request
from pathlib import Path

import torch
import torch.nn as nn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from torchvision import models
from torchvision import transforms as T

from disease_info import get_info

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
IMG_SIZE = 224
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOW_CONF = 0.60  # below this we tell the user the model is unsure



def ensure_file(name: str, env_var: str) -> Path:
    """Use the local file if present, otherwise download it from the URL in an env var."""
    path = MODEL_DIR / name
    url = os.getenv(env_var)
    if not path.exists() and url:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {name} ...")
        urllib.request.urlretrieve(url, path)
    return path


classes_path = ensure_file("classes.json", "CLASSES_URL")
model_path = ensure_file("model.pt", "MODEL_URL")

classes = json.loads(classes_path.read_text())

model = models.efficientnet_v2_s(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(classes))
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

transform = T.Compose(
    [
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

app = FastAPI(title="LeafDoctor AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


def pretty(text: str) -> str:
    return text.replace("_", " ").strip()


def describe(class_name: str) -> dict:
    crop_raw, disease_raw = class_name.split("___", 1)
    crop, disease = pretty(crop_raw), pretty(disease_raw)
    return {
        "class_name": class_name,
        "crop": crop,
        "disease": disease,
        "healthy": disease.lower() == "healthy",
    }


@app.get("/health")
def health():
    return {"status": "ok", "num_classes": len(classes)}


@app.get("/classes")
def list_classes():
    out = []
    for c in classes:
        d = describe(c)
        d["about"], d["action"] = get_info(d["crop"], d["disease"])
        out.append(d)
    return out


@app.post("/predict")
def predict(file: UploadFile = File(...)):
    data = file.file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Image too large (max 10 MB).")
    try:
        img = Image.open(io.BytesIO(data)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(400, "Could not read this file as an image.")

    x = transform(img).unsqueeze(0)
    with torch.inference_mode():
        probs = torch.softmax(model(x), dim=1)[0]
    conf, idx = probs.topk(3)

    top = []
    for c, i in zip(conf.tolist(), idx.tolist()):
        item = describe(classes[i])
        item["confidence"] = round(c, 4)
        top.append(item)

    best = top[0]
    about, action = get_info(best["crop"], best["disease"])
    return {
        "prediction": {**best, "low_confidence": best["confidence"] < LOW_CONF},
        "top3": top,
        "info": {"about": about, "action": action},
    }
