# Mini‑SOAR → Cognitive SOAR (Prediction ➜ Attribution)

This project evolves a Mini‑SOAR URL classifier into a Cognitive SOAR that adds threat attribution after detection.

- Step 1 — Prediction (Supervised): Classify a URL as MALICIOUS or BENIGN using a PyCaret classification model.
- Step 2 — Attribution (Unsupervised): If MALICIOUS, infer a likely actor profile with a clustering model (**K‑Means, k=3**) and map the cluster to:
  - State‑Sponsored
  - Organized Cybercrime
  - Hacktivist

This extra context helps analysts route incidents, pick the right playbooks, and communicate impact quickly.

---

## Key Features
- Dual‑model pipeline (two separate PyCaret `setup()` runs)
- Stable cluster→actor mapping persisted to `models/cluster_mapping.json`
- Streamlit UI with tabs: single analysis, threat attribution (shown only when malicious), batch CSV
- Dockerized for easy run, plus GitHub Actions linting

---

## Architecture (Dual‑Model)
```
[User Features] → [Classifier] ── MALICIOUS? ──► [Clusterer (K=3)] ─► [Actor Mapping] ─► “State | Crime | Hacktivist”
                         │
                         └────────────── BENIGN ────────────────────────────────────────────────────────────────┘
```

- Classifier (supervised): Trained on synthetic labels `BENIGN` vs `MALICIOUS`.
- Clusterer (unsupervised): Trained on features only; its numeric cluster IDs are mapped to actor labels via majority vote on the training set and saved to JSON.

Artifacts (after training):
- `models/phishing_url_detector.pkl`
- `models/threat_actor_profiler.pkl`
- `models/cluster_mapping.json`

---

## Tech Stack
- Python, PyCaret, scikit‑learn
- Streamlit** (UI)
- Docker / Compose** (containerized dev)
- Optional: OpenAI / Gemini for prescriptive text (via `genai_prescriptions.py`)

---

## Repository Layout
```
mini-soar/
├── .github/workflows/lint.yml
├── README.md
├── INSTALL.md
├── TESTING.md
├── Makefile
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── train_model.py
├── genai_prescriptions.py
└── app.py
```

---

##Usage

### Local
```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
# open http://localhost:8501
```

### Docker
```bash
docker compose up --build
# open http://localhost:8501
```

---

## 🧪 Models & Data
Training writes artifacts to `models/`:
- `phishing_url_detector.pkl` (classifier)
- `threat_actor_profiler.pkl` (clusterer)
- `cluster_mapping.json` (cluster ID → actor label)
- `synthetic_urls.csv` (generated dataset for inspection)

---

## CI / Automation
A GitHub Actions workflow runs flake8 lint on every push/PR: `.github/workflows/lint.yml`.

---

##  Notes
- Attribution is heuristic context, not proof. Use it to guide triage and playbooks.
- Clustering runs only when the verdict is MALICIOUS.