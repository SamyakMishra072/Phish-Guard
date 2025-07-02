# inference_engine/app.py

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
import requests
import joblib
import os

# --- Prometheus Metrics ---
from prometheus_client import Counter, start_http_server

phish_counter = Counter("phish_detected_total", "Total phishing URLs detected")
legit_counter = Counter("legit_detected_total", "Total legitimate URLs detected")

# Start Prometheus metrics endpoint on port 8003
start_http_server(8003)

# --- FastAPI Setup ---
app = FastAPI(title="PhishGuard Inference")

# --- Input Schema ---
class URLRequest(BaseModel):
    url: HttpUrl

# --- Load Model ---
model_path = "model/phish_clf.joblib"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")
clf = joblib.load(model_path)

# --- Prediction Endpoint ---
@app.post("/predict/")
async def predict(req: URLRequest):
    try:
        # Call feature extractor service
        r = requests.post("http://feature_extractor:8001/features/", json={"url": str(req.url)})
        r.raise_for_status()
        feats = r.json()["features"]

        # Already in correct order (list)
        X = feats

        # Predict
        prob = clf.predict_proba([X])[0, 1]
        label = "phish" if prob > 0.5 else "legit"

        # Increment Prometheus counters
        if label == "phish":
            phish_counter.inc()
        else:
            legit_counter.inc()

        return {"label": label, "score": prob}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
