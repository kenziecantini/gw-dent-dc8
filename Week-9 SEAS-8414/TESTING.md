Manual verification for one **DGA** and one **Legitimate** domain.

## Setup

```bash
pip install -r requirements.txt
python 1_train_and_export.py --csv data/dga_sample.csv --max_runtime_secs 120
```

> Replace `data/dga_sample.csv` with your real dataset. Required columns: `domain,label` (1=DGA, 0=Legit).

---

## Test 1: DGA Domain

**Domain**: `xj2a9k-sd81zq.biz` (synthetic example with high entropy/digits)

```bash
python 2_analyze_domain.py xj2a9k-sd81zq.biz
```

**Expected**:
- P(DGA) ≥ 0.5
- SHAP lists `entropy` and `digit_ratio` as positive contributors
- Playbook renders with concrete DNS/SIEM/EDR steps

---

## Test 2: Legitimate Domain

**Domain**: `microsoft.com`

```bash
python 2_analyze_domain.py microsoft.com
```

**Expected**:
- P(DGA) < 0.5
- SHAP shows factors like `vowel_ratio` or lower `entropy` decreasing DGA risk
- Playbook still prints (with "Legitimate" classification) for completeness

---

## Edge Cases

- Subdomains with many labels: `cdn.assets.example.com` → entropy excludes dots but length includes them.
- Short domains: `x.co` → low length may marginally increase risk depending on training.
- Non-ASCII: such characters are stripped during cleaning; ensure your dataset uses ASCII domains.

---
