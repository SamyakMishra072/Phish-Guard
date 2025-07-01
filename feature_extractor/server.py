# feature_extractor/server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from .extractor import extract_all

class URLRequest(BaseModel):
    url: HttpUrl

app = FastAPI(title="Feature Extractor")

@app.post("/features/")
async def get_features(req: URLRequest):
    try:
        feats = extract_all(req.url)
        return {"features": feats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# run with: uvicorn feature_extractor.server:app --host 0.0.0.0 --port 8001
