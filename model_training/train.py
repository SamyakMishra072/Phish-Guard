# model_training/train.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1. Load labeled CSV of features + label
df = pd.read_csv("data/phish_dataset.csv")
X = df.drop('label', axis=1)
y = df['label'].map({'legit':0,'phish':1})

# 2. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Fit model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 4. Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, clf.predict_proba(X_test)[:,1]))

# 5. Save model artifact
joblib.dump(clf, "../inference_engine/model/phish_clf.joblib")
