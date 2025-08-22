This project integrates three powerful AI components into one workflow:
AutoML (H2O) – Automatically train a high-performance classifier to detect algorithmically generated domains (DGAs).
Explainable AI (SHAP) – Provide human-understandable feature attributions for each prediction.
Generative AI (Google GenAI) – Convert model explanations into an actionable, context-aware incident response playbook.
The final result is an end-to-end analyst tool that classifies a domain, explains the decision, and generates a prescriptive response plan.

            ┌───────────────────────────┐
            │   Input: Domain Name       │
            └──────────────┬────────────┘
                           │
                           ▼
                 [Feature Engineering]
       length • entropy • digit_ratio • hyphen_ratio • vowel_ratio
                           │
                           ▼
                   [H2O AutoML Model]
                           │
                 Prediction: Legit / DGA
                           │
                           ▼
                  [Explainable AI (SHAP)]
            Per-feature contribution scores
                           │
                           ▼
         [Generative AI – Google GenAI API]
 Structured SHAP summary → Analyst playbook
                           │
                           ▼
                   Output: Playbook


### Repository Contents
1_train_and_export.py – Train AutoML model and export MOJO + metadata
2_analyze_domain.py – Main application: classify, explain, and generate playbook
utils/ – Feature engineering functions
model/ – Trained artifacts (DGA_Leader.zip, model_meta.json, leaderboard.csv)
README.md – Project documentation
TESTING.md – Manual test steps for verification
.github/workflows/lint.yml – GitHub Actions workflow (Flake8/Ruff)

### Testing
Manual verification is documented in TESTING.md, covering:
One known DGA domain → prediction = DGA, explanation & playbook
One known legit domain → prediction = Legitimate, explanation & playbook

### Requirements
Python 3.11
Packages: h2o, pandas, numpy, shap, google-generativeai

### Usage

### 1. Train Model (if needed)
```bash
python 1_train_and_export.py --csv data/dga_dataset_train.csv --label_col class --max_runtime_secs 120
```
- Produces:
  - `model/DGA_Leader.zip`
  - `model/model_meta.json`
  - `model/leaderboard.csv`

### 2. Analyze a Domain
```bash
python 2_analyze_domain.py exampledomain.com --model_dir model
```

**Example Output:**
```
Prediction: DGA
Top features: entropy (+0.42), digit_ratio (+0.27)
Generated Playbook:
- Block the domain in DNS
- Pivot on related high-entropy domains
- Alert SOC team for follow-up