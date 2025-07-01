from prometheus_client import Counter, start_http_server

phish_counter = Counter("phish_detected_total", "Total phishing URLs detected")
legit_counter = Counter("legit_detected_total", "Total legitimate URLs detected")

# Start Prometheus metrics endpoint on port 8003
start_http_server(8003)



# inference_engine/app.py
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import requests, joblib

class URLRequest(BaseModel):
    url: HttpUrl

app = FastAPI(title="PhishGuard Inference")

# load model
clf = joblib.load("model/phish_clf.joblib")

@app.post("/predict/")
async def predict(req: URLRequest):
    # call feature‐extractor service
    r = requests.post("http://feature_extractor:8001/features/", json={"url": req.url})
    feats = r.json()["features"]
    # ensure feature order
    X = [feats[k] for k in sorted(feats.keys())]
    prob = clf.predict_proba([X])[0,1]
    label = "phish" if prob>0.5 else "legit"
    return {"label": label, "score": prob}

# run with: uvicorn inference_engine.app:app --host 0.0.0.0 --port 8002
