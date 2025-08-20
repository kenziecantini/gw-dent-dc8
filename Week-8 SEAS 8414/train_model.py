import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  

from pycaret.classification import setup, compare_models, finalize_model, save_model
from pycaret.clustering import setup as clu_setup, create_model as clu_create_model, assign_model as clu_assign_model, save_model as clu_save_model, pull as clu_pull

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


def generate_synthetic_data(num_samples: int = 500) -> pd.DataFrame:
    """
    Generates a synthetic dataset with your original phishing URL features,
    plus a new 'has_political_keyword' feature so Hacktivist behavior is discoverable by clustering.

    Malicious rows are split into three latent profiles:
      - State-Sponsored
      - Organized Cybercrime
      - Hacktivist
    """
    print("Generating synthetic dataset...")

    features = [
        'having_IP_Address',
        'URL_Length',
        'Shortining_Service',
        'having_At_Symbol',
        'double_slash_redirecting',
        'Prefix_Suffix',
        'having_Sub_Domain',
        'SSLfinal_State',
        'URL_of_Anchor',
        'Links_in_tags',
        'SFH',
        'Abnormal_URL',
        'has_political_keyword',
    ]

    # Split BENIGN / MALICIOUS counts
    num_phishing = num_samples // 2
    num_benign = num_samples - num_phishing

    rows = []

    # BENIGN (baseline behaviors)
    for _ in range(num_benign):
        rows.append({
            'having_IP_Address': np.random.choice([1, -1], p=[0.02, 0.98]),
            'URL_Length': np.random.choice([1, 0, -1], p=[0.20, 0.65, 0.15]),
            'Shortining_Service': np.random.choice([1, -1], p=[0.05, 0.95]),
            'having_At_Symbol': np.random.choice([1, -1], p=[0.05, 0.95]),
            'double_slash_redirecting': np.random.choice([1, -1], p=[0.10, 0.90]),
            'Prefix_Suffix': np.random.choice([1, -1], p=[0.10, 0.90]),
            'having_Sub_Domain': np.random.choice([1, 0, -1], p=[0.20, 0.60, 0.20]),
            'SSLfinal_State': np.random.choice([-1, 0, 1], p=[0.10, 0.15, 0.75]),
            'URL_of_Anchor': np.random.choice([-1, 0, 1], p=[0.10, 0.30, 0.60]),
            'Links_in_tags': np.random.choice([-1, 0, 1], p=[0.10, 0.40, 0.50]),
            'SFH': np.random.choice([-1, 0, 1], p=[0.10, 0.20, 0.70]),
            'Abnormal_URL': np.random.choice([1, -1], p=[0.10, 0.90]),
            'has_political_keyword': 0,  # benign rarely has political messaging
            'label': 'BENIGN',
            'actor_profile': None,
        })

    # MALICIOUS (three threat profiles)
    # Split malicious rows evenly across profiles (State, Crime, Hacktivist)
    per_profile = max(1, num_phishing // 3)
    profiles = (
        ('State-Sponsored', per_profile),
        ('Organized Cybercrime', per_profile),
        ('Hacktivist', num_phishing - 2 * per_profile),
    )

    for profile_name, n in profiles:
        for _ in range(n):
            if profile_name == 'State-Sponsored':
                row = {
                    'having_IP_Address': np.random.choice([1, -1], p=[0.05, 0.95]),
                    'URL_Length': np.random.choice([1, 0, -1], p=[0.40, 0.45, 0.15]),
                    'Shortining_Service': np.random.choice([1, -1], p=[0.05, 0.95]),
                    'having_At_Symbol': np.random.choice([1, -1], p=[0.40, 0.60]),
                    'double_slash_redirecting': np.random.choice([1, -1], p=[0.25, 0.75]),
                    'Prefix_Suffix': np.random.choice([1, -1], p=[0.55, 0.45]),
                    'having_Sub_Domain': np.random.choice([1, 0, -1], p=[0.35, 0.45, 0.20]),
                    'SSLfinal_State': np.random.choice([-1, 0, 1], p=[0.10, 0.05, 0.85]),
                    'URL_of_Anchor': np.random.choice([-1, 0, 1], p=[0.35, 0.30, 0.35]),
                    'Links_in_tags': np.random.choice([-1, 0, 1], p=[0.35, 0.40, 0.25]),
                    'SFH': np.random.choice([-1, 0, 1], p=[0.55, 0.25, 0.20]),
                    'Abnormal_URL': np.random.choice([1, -1], p=[0.25, 0.75]),
                    'has_political_keyword': np.random.choice([1, 0], p=[0.10, 0.90]),
                }
            elif profile_name == 'Organized Cybercrime':
                row = {
                    'having_IP_Address': np.random.choice([1, -1], p=[0.60, 0.40]),
                    'URL_Length': np.random.choice([1, 0, -1], p=[0.70, 0.20, 0.10]),
                    'Shortining_Service': np.random.choice([1, -1], p=[0.75, 0.25]),
                    'having_At_Symbol': np.random.choice([1, -1], p=[0.40, 0.60]),
                    'double_slash_redirecting': np.random.choice([1, -1], p=[0.70, 0.30]),
                    'Prefix_Suffix': np.random.choice([1, -1], p=[0.60, 0.40]),
                    'having_Sub_Domain': np.random.choice([1, 0, -1], p=[0.60, 0.30, 0.10]),
                    'SSLfinal_State': np.random.choice([-1, 0, 1], p=[0.45, 0.20, 0.35]),
                    'URL_of_Anchor': np.random.choice([-1, 0, 1], p=[0.45, 0.30, 0.25]),
                    'Links_in_tags': np.random.choice([-1, 0, 1], p=[0.45, 0.35, 0.20]),
                    'SFH': np.random.choice([-1, 0, 1], p=[0.60, 0.25, 0.15]),
                    'Abnormal_URL': np.random.choice([1, -1], p=[0.75, 0.25]),
                    'has_political_keyword': np.random.choice([1, 0], p=[0.05, 0.95]),
                }
            else:  # Hacktivist
                row = {
                    'having_IP_Address': np.random.choice([1, -1], p=[0.25, 0.75]),
                    'URL_Length': np.random.choice([1, 0, -1], p=[0.55, 0.30, 0.15]),
                    'Shortining_Service': np.random.choice([1, -1], p=[0.35, 0.65]),
                    'having_At_Symbol': np.random.choice([1, -1], p=[0.40, 0.60]),
                    'double_slash_redirecting': np.random.choice([1, -1], p=[0.55, 0.45]),
                    'Prefix_Suffix': np.random.choice([1, -1], p=[0.50, 0.50]),
                    'having_Sub_Domain': np.random.choice([1, 0, -1], p=[0.45, 0.35, 0.20]),
                    'SSLfinal_State': np.random.choice([-1, 0, 1], p=[0.35, 0.20, 0.45]),
                    'URL_of_Anchor': np.random.choice([-1, 0, 1], p=[0.40, 0.30, 0.30]),
                    'Links_in_tags': np.random.choice([-1, 0, 1], p=[0.40, 0.40, 0.20]),
                    'SFH': np.random.choice([-1, 0, 1], p=[0.55, 0.25, 0.20]),
                    'Abnormal_URL': np.random.choice([1, -1], p=[0.55, 0.45]),
                    'has_political_keyword': np.random.choice([1, 0], p=[0.55, 0.45]),  # key signal
                }

            row['label'] = 'MALICIOUS'
            row['actor_profile'] = profile_name
            rows.append(row)

    df = pd.DataFrame(rows, columns=features + ['label', 'actor_profile'])
    df = df.sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)
    return df


def train_models(df: pd.DataFrame, out_dir: str = "models") -> None:
    """
    Minimal additions to meet objectives:
    - Train classifier (BENIGN vs MALICIOUS) with PyCaret Classification
    - Train clustering model (K-Means, k=3) with PyCaret Clustering
    - Save both models and a cluster→actor mapping to JSON
    """
    os.makedirs(out_dir, exist_ok=True)

    #Classification
    cls_setup = setup(
        data=df.copy(),
        target="label",
        session_id=RANDOM_STATE,
        train_size=0.8,
        fold=5,
        silent=True,
        verbose=False,
    )
    best_cls = compare_models()
    best_cls = finalize_model(best_cls)
    save_model(best_cls, os.path.join(out_dir, "phishing_url_detector"))

    # Clustering
    # IMPORTANT: clustering uses features-only; keep actor_profile to build mapping
    features_only = df.drop(columns=["label"]).copy()
    actor_series = features_only.pop("actor_profile")

    clu_setup(
        data=features_only.copy(),
        session_id=RANDOM_STATE,
        normalize=True,
        silent=True,
        verbose=False,
    )
    kmeans = clu_create_model("kmeans", num_clusters=3)
    clustered = clu_assign_model(kmeans, transformation=True)

    # Build majority mapping: cluster id -> dominant actor_profile
    mapping = {}
    for cid in sorted(clustered["Cluster"].unique()):
        subset = clustered[clustered["Cluster"] == cid]
        maj = actor_series.loc[subset.index].dropna().value_counts().idxmax()
        mapping[int(cid)] = str(maj)

    clu_save_model(kmeans, os.path.join(out_dir, "threat_actor_profiler"))
    with open(os.path.join(out_dir, "cluster_mapping.json"), "w") as f:
        json.dump(mapping, f, indent=2)

    # Optional: persist data for testing
    df.to_csv(os.path.join(out_dir, "synthetic_urls.csv"), index=False)

    print("Saved classification model   ->", os.path.join(out_dir, "phishing_url_detector.pkl"))
    print("Saved clustering model       ->", os.path.join(out_dir, "threat_actor_profiler.pkl"))
    print("Saved cluster→actor mapping  ->", os.path.join(out_dir, "cluster_mapping.json"))
    print("Mapping:", json.dumps(mapping, indent=2))


if __name__ == "__main__":
    data = generate_synthetic_data(num_samples=1500)  # modestly larger set for better clusters
    train_models(data, out_dir=os.environ.get("MODEL_DIR", "models"))
