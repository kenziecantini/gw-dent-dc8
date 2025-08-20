# Mini-SOAR → Cognitive SOAR (Prediction ➜ Attribution)

This app upgrades a Mini-SOAR URL classifier with **threat attribution**:
1) **Predict** MALICIOUS vs BENIGN (PyCaret classification).
2) If MALICIOUS, **attribute** to a likely actor cluster (K-Means, k=3) → **State-Sponsored / Organized Cybercrime / Hacktivist**.
3) (Optional) Show a **GenAI prescription** based on the predicted actor.

## Quickstart (Local)
```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
