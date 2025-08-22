"""
1_train_and_export.py
Run H2O AutoML on a DGA dataset, save the best SHAP-capable model as a MOJO and BIN,
and persist feature metadata for consistent inference.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import List, Optional

import pandas as pd
import h2o
from h2o.automl import H2OAutoML

from utils.features import compute_features, feature_names

SUPPORTED_SHAP_ALGOS = {"GBM", "XGBoost", "DRF"}


def _infer_label_column(df: pd.DataFrame) -> str:
    """
    Try common label column names.
    """
    candidates = ["label", "class", "is_dga", "target"]
    lower_cols = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lower_cols:
            return lower_cols[c]
    # if not found, raise
    raise ValueError(f"Could not find a label column among {candidates}. Columns present: {list(df.columns)}")


def _ensure_binary(df: pd.DataFrame, label_col: str) -> pd.DataFrame:
    """
    Make sure labels are 0/1 with 1 = DGA, 0 = Legitimate.
    Accepts strings like 'dga', 'legit', etc.
    """
    series = df[label_col]
    if series.dtype == object:
        s = series.str.lower().str.strip()
        mapping = {
            "dga": 1, "dgadomain": 1, "malicious": 1, "1": 1, "true": 1, "yes": 1,
            "legit": 0, "legitimate": 0, "benign": 0, "0": 0, "false": 0, "no": 0
        }
        df[label_col] = s.map(mapping)
    df[label_col] = df[label_col].astype(int)
    return df


def pick_best_shap_model(aml: H2OAutoML) -> str:
    """
    From the AutoML leaderboard, pick the best model whose algorithm is SHAP-capable.
    Returns model_id.
    """
    lb = aml.leaderboard.as_data_frame()
    # model_id format often includes algo, we can also fetch model details for safety
    for model_id in lb["model_id"]:
        algo = str(model_id).split("_")[0].upper()
        if any(a in algo for a in SUPPORTED_SHAP_ALGOS):
            return model_id
    # fallback to leader, but SHAP may be unavailable
    return aml.leader.model_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=str, required=True, help="Path to DGA dataset CSV with at least columns: domain,label")
    ap.add_argument("--domain_col", type=str, default="domain", help="Name of the column with domain strings")
    ap.add_argument("--label_col", type=str, default=None, help="Name of the label column (if omitted, auto-detect)")
    ap.add_argument("--rich_features", action="store_true", help="Use extended feature set (default True)", default=True)
    ap.add_argument("--max_runtime_secs", type=int, default=180, help="AutoML wall clock limit")
    ap.add_argument("--outdir", type=str, default="model", help="Directory to save MOJO/BIN and metadata")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) Load CSV with pandas first so we can compute features identically
    raw = pd.read_csv(args.csv)
    if args.label_col:
        label_col = args.label_col
    else:
        label_col = _infer_label_column(raw)

    if args.domain_col not in raw.columns:
        raise ValueError(f"Domain column '{args.domain_col}' not found. Available: {list(raw.columns)}")

    raw = _ensure_binary(raw, label_col)

    # 2) Compute features
    feats = compute_features(raw[args.domain_col].tolist(), rich=args.rich_features)
    feats[label_col] = raw[label_col].values

    # 3) Spin up H2O and prepare frames
    h2o.init()
    hf = h2o.H2OFrame(feats)
    hf[label_col] = hf[label_col].asfactor()
    x = feature_names(args.rich_features)
    y = label_col

    # 4) Train AutoML, restrict to SHAP-capable algos to guarantee predict_contributions support
    aml = H2OAutoML(
        max_runtime_secs=args.max_runtime_secs,
        seed=42,
        include_algos=list(SUPPORTED_SHAP_ALGOS),
        sort_metric="AUC"
    )
    aml.train(x=x, y=y, training_frame=hf)

    leader_id = pick_best_shap_model(aml)
    model = h2o.get_model(leader_id)

    # 5) Save leaderboard and model artifacts
    lb_path = outdir / "leaderboard.csv"
    aml.leaderboard.as_data_frame().to_csv(lb_path, index=False)

    # BIN model (fallback for local explanations if MOJO import isn't available)
    bin_path = h2o.save_model(model=model, path=str(outdir), force=True)

    # MOJO
    mojo_zip = model.download_mojo(path=str(outdir), get_genmodel_jar=False)

    # 6) Save metadata for inference
    meta = {
        "features": x,
        "label": y,
        "positive_class": "1",
        "mojo_path": os.path.basename(mojo_zip),
        "bin_path": os.path.basename(bin_path),
        "trained_at": pd.Timestamp.utcnow().isoformat(),
        "automl_leader": leader_id,
    }
    with open(outdir / "model_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("Saved artifacts:")
    print(f"- Leaderboard: {lb_path}")
    print(f"- BIN model:   {bin_path}")
    print(f"- MOJO:        {mojo_zip}")
    print(f"- Metadata:    {outdir / 'model_meta.json'}")

    h2o.shutdown(prompt=False)


if __name__ == "__main__":
    main()
