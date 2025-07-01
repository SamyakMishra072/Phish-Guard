# create_dummy_model.py
import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Create dummy features (say, 10 features) and labels
X = np.random.rand(100, 10)
y = np.random.randint(2, size=100)

# Train a dummy model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model in the correct path
import os
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/phish_clf.joblib")

print("✅ Dummy model created and saved at model/phish_clf.joblib")
