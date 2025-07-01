from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
import joblib
import numpy as np

app = FastAPI()

class URLRequest(BaseModel):
    url: HttpUrl

# Load the model (already done if you used create_dummy_model.py)
clf = joblib.load("model/phish_clf.joblib")

@app.post("/predict/")
def predict_url(request: URLRequest):
    try:
        # Step 1: Call feature extractor
        res = requests.post("http://feature_extractor:8001/features/", json={"url": str(request.url)})
        res.raise_for_status()

        features = res.json()["features"]
        prediction = clf.predict([features])[0]
        return {"prediction": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
