# 🌿 LeafDoctor AI - Crop Disease Detection

Upload a leaf photo -> get crop, disease, confidence, top-3 and treatment advice.

- **Model:** EfficientNetV2-S (PyTorch), trained on Google Colab GPU
- **Backend:** FastAPI (`backend/`)
- **Frontend:** Streamlit multipage website (`frontend/`) with Light / Night theme
- **Data:** PlantVillage - Tomato, Potato, Corn, Pepper, Grape, Apple (27 classes)

```
crop-disease-ai/
├── training/train_colab.ipynb   # run on Colab (T4 GPU)
├── models/                      # put model.pt + classes.json here
├── backend/                     # main.py, disease_info.py
└── frontend/                    # app.py, utils.py, style.css, views/ (5 pages)
```

## 1. Train (Colab)
1. Open `training/train_colab.ipynb` in Google Colab, set runtime to **T4 GPU**.
2. Run cells top to bottom (you will upload `kaggle.json`). About 20-30 minutes.
3. Download `model.pt` and `classes.json`, put them in `models/`.

## 2. Backend (your laptop, CPU is fine)
```bash
pip install -r requirements-backend.txt
cd backend
uvicorn main:app --reload --port 8000
```
Check: http://localhost:8000/docs

## 3. Frontend
```bash
pip install -r requirements-frontend.txt
cd frontend
streamlit run app.py
```
If the backend is elsewhere: `API_URL=http://host:8000 streamlit run app.py`.

## Website pages
| Page | What it does |
|---|---|
| Home | Landing page, supported crops, how it works |
| Diagnose | Upload / camera, diagnosis, top-3, advice, recent scans |
| Crop Library | Searchable list of all diseases with advice (needs backend running) |
| How it Works | Pipeline, model details, photo tips, limitations |
| About | Project info, your name/links, backend URL setting |

- **Light / Night mode:** toggle at the top right. It is remembered in the URL (`?theme=dark`).
- **Your name and links:** edit `AUTHOR_NAME`, `AUTHOR_ROLE`, `GITHUB_URL`, `LINKEDIN_URL`, `EMAIL` at the top of `frontend/utils.py`.
- Needs **Streamlit >= 1.46** for the top navigation bar (older versions fall back to a sidebar).

## Accuracy notes (read this)
- PlantVillage photos are lab-style (one leaf, plain background). Test accuracy will be ~99%, but **real field photos score lower**. Always test with your own phone photos (last notebook cell).
- Several photos in PlantVillage come from the same leaf, so a random split is optimistic.
- Predictions under 60% confidence are flagged as "Not sure" in the UI.
- The model only knows the 27 classes; any other plant will still get a (wrong) answer.

## Next steps to improve
1. Add a Bangladesh-relevant crop (rice leaf disease datasets on Kaggle) and retrain.
2. Fine-tune on field-condition images (e.g. PlantDoc) for robustness.
3. Add Grad-CAM to show which part of the leaf the model looked at.
4. Export to ONNX for faster inference / deployment.
