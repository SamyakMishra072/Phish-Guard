# tests/test_inference.py

import requests

def test_inference_endpoint():
    url_to_test = "https://example.com"  # Replace with any valid URL
    api_url = "http://localhost:8002/predict/"
    
    response = requests.post(api_url, json={"url": url_to_test})

    assert response.status_code == 200, f"Request failed: {response.text}"
    
    data = response.json()
    assert "label" in data and "score" in data, "Missing keys in API response."
    assert data["label"] in ["phish", "legit"], "Invalid label output."
    assert 0.0 <= data["score"] <= 1.0, "Invalid score range."

    print("✅ Inference API test passed.")
