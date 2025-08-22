Manual verification for one **legit** domain and one **DGA-like** domain using the end-to-end pipeline.

## Prerequisites

- Python 3.11
- Repo checked out locally
- The following files exist in `model/` (from Colab or local training):
  - `DGA_Leader.zip`
  - `model_meta.json`
  - `leaderboard.csv`

Optional (for GenAI playbook):
```bash
export GEMINI_API_KEY="YOUR_KEY"
```
> If not set, the app falls back to an offline playbook template—still acceptable for testing.

---

## 1) Sanity check

From the project root (e.g., `Week-9 SEAS-8414/`):

```bash
python -V
ls model
```

Expected:
```
DGA_Leader.zip  model_meta.json  leaderboard.csv
```

---

## 2) Legit domain test

Command:
```bash
python 2_analyze_domain.py microsoft.com --model_dir model
```

Expect:
- **Prediction**: `Legit` (or `label=0`)
- **Probability of DGA**: low (typically `< 0.50`)
- **SHAP summary**: contributions show **lower entropy** and **lower digit_ratio** pushing toward Legit
- **Playbook**: a short action list tailored to a legit outcome (e.g., “no action / monitor only”)

Sample (truncated):
```
Prediction: Legit (P[DGA]=0.12)
Top features: entropy (-0.31), digit_ratio (-0.18), vowel_ratio (+0.05)
Playbook:
- No immediate block required.
- Monitor DNS queries for similar lookalike domains.
- Add to allowlist if internal services require it.
```

Pass criteria:
- Final classification clearly indicates **Legit** (and DGA probability is low).
- SHAP mentions key features (entropy, digit_ratio, etc.).
- Playbook rendered without error.

---

## 3) DGA-like domain test

Use a synthetic, high-entropy domain:

```bash
python 2_analyze_domain.py xj2a9k-sd81zq.biz --model_dir model
```

Expect:
- **Prediction**: `DGA` (or `label=1`)
- **Probability of DGA**: high (typically `> 0.50`)
- **SHAP summary**: **higher entropy** and **higher digit_ratio** pushing toward DGA
- **Playbook**: prescriptive actions (block, hunt, pivot)

Sample (truncated):
```
Prediction: DGA (P[DGA]=0.91)
Top features: entropy (+0.42), digit_ratio (+0.25), hyphen_ratio (+0.07)
Playbook:
- Block the domain at DNS/Proxy.
- Search logs for recent connections to xj2a9k-sd81zq.biz and related high-entropy siblings.
- Isolate any host initiating outbound requests.
- Notify SOC; open an incident with priority P2.
```

Pass criteria:
- Final classification clearly indicates **DGA** with high probability.
- SHAP highlights entropy/digit features as primary drivers.
- Playbook contains concrete, incident-response steps.

---

## 4) Troubleshooting

- **“Model not found / MOJO missing”**  
  Ensure `model/DGA_Leader.zip` and `model/model_meta.json` are present. If missing, (re)train in Colab and download into `model/`.

- **“Feature mismatch”**  
  `2_analyze_domain.py` reads `model_meta.json["features"]` and uses that exact set. If you changed features in training, update `model_meta.json` or retrain.

- **No GenAI outputs**  
  If `GEMINI_API_KEY` isn’t set or outbound calls fail, the script prints an offline playbook template. This is acceptable for verification.

- **Environment issues**  
  Use Python 3.11. Install deps:
  ```bash
  pip install h2o shap pandas numpy scipy scikit-learn google-generativeai
  ```

---

## 5) What to submit

- Link to your public GitHub repository containing:
  - `1_train_and_export.py`, `2_analyze_domain.py`, `utils/`, `.github/workflows/lint.yml`
  - `model/DGA_Leader.zip`, `model/model_meta.json`, `model/leaderboard.csv`
  - `README.md` and this `TESTING.md`

✔️ If both tests above produce the expected labels, SHAP summaries, and a playbook, your pipeline is functioning end-to-end.

