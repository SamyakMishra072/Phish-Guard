# tests/test_model.py

import os
import joblib
import numpy as np

def test_model_load_and_predict():
    model_path = os.path.abspath("inference_engine/model/phish_clf.joblib")
    assert os.path.exists(model_path), "Model file does not exist."

    model = joblib.load(model_path)
    assert hasattr(model, "predict_proba"), "Loaded model is not a classifier."

    # Dummy feature input (match number and order of features used in training)
    # Update with the actual order of features if needed
    sample_input = np.array([[85, 3, 0, 1200, 10, 5000]])  # Example shape: (1, N_features)
    proba = model.predict_proba(sample_input)[0]

    assert 0 <= proba[1] <= 1, "Invalid probability from model."

    print("✅ Model prediction test passed.")
