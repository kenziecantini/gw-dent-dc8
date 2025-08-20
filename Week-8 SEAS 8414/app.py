import os
import json
import streamlit as st
import pandas as pd

# PyCaret helpers
from pycaret.classification import load_model as load_cls_model, predict_model as predict_cls
from pycaret.clustering import load_model as load_clu_model, predict_model as predict_clu

st.set_page_config(page_title="Mini-SOAR: Prediction → Attribution", layout="wide")
st.title("🧠 Mini-SOAR: From Prediction to Attribution")

MODEL_DIR = os.environ.get("MODEL_DIR", "models")
CLS_PATH = os.path.join(MODEL_DIR, "phishing_url_detector")
CLU_PATH = os.path.join(MODEL_DIR, "threat_actor_profiler")
MAP_PATH = os.path.join(MODEL_DIR, "cluster_mapping.json")

@st.cache_resource
def _load_artifacts():
    cls = load_cls_model(CLS_PATH) if os.path.exists(CLS_PATH + ".pkl") else None
    clu = load_clu_model(CLU_PATH) if os.path.exists(CLU_PATH + ".pkl") else None
    mapping = None
    if os.path.exists(MAP_PATH):
        with open(MAP_PATH, "r") as f:
            mapping = {int(k): v for k, v in json.load(f).items()}
    return cls, clu, mapping

cls_model, clu_model, cluster_map = _load_artifacts()

if not cls_model:
    st.error("Classifier not found. Run `python train_model.py` first (or `docker compose up --build`).")
    st.stop()

# Sidebar: feature entry
with st.sidebar:
    st.header("URL Feature Input")

    def tri(x, mapping):
        return mapping[x]

    url_length = st.select_slider("URL Length", ["Short", "Normal", "Long"], value="Normal")
    ssl_state = st.select_slider("SSL/TLS Status", ["Trusted", "None", "Suspicious"], value="Trusted")
    subdomains = st.select_slider("Sub-domains", ["None", "One", "Many"], value="One")

    prefix_suffix = st.checkbox("Has Prefix/Suffix (hyphen)", value=False)
    has_at_symbol = st.checkbox("Has '@' symbol", value=False)
    abnormal_url = st.checkbox("Abnormal URL structure", value=False)
    uses_ip = st.checkbox("Uses IP Address", value=False)
    shortened = st.checkbox("Uses URL Shortener", value=False)
    double_slash_redirect = st.checkbox("Double-slash redirecting ('//')", value=False)

    url_of_anchor = st.select_slider("URL of Anchor", ["Low/Benign", "Neutral", "High/Suspicious"], value="Neutral")
    links_in_tags = st.select_slider("Links in <tags>", ["Low/Benign", "Neutral", "High/Suspicious"], value="Neutral")
    sfh = st.select_slider("SFH (Server Form Handler)", ["Low/Benign", "Neutral", "High/Suspicious"], value="High/Suspicious")

    has_political_keyword = st.checkbox("Contains political keyword", value=False)

    submitted = st.button("Analyze", type="primary", use_container_width=True)

# Map UI → model feature values (match train_model.py encoding)
def build_feature_row():
    return pd.DataFrame([{
        "having_IP_Address": 1 if uses_ip else -1,
        "URL_Length": {"Short": -1, "Normal": 0, "Long": 1}[url_length],
        "Shortining_Service": 1 if shortened else -1,
        "having_At_Symbol": 1 if has_at_symbol else -1,
        "double_slash_redirecting": 1 if double_slash_redirect else -1,
        "Prefix_Suffix": 1 if prefix_suffix else -1,
        "having_Sub_Domain": {"None": -1, "One": 0, "Many": 1}[subdomains],
        "SSLfinal_State": {"Trusted": 1, "None": 0, "Suspicious": -1}[ssl_state],
        "URL_of_Anchor": {"Low/Benign": 1, "Neutral": 0, "High/Suspicious": -1}[url_of_anchor],
        "Links_in_tags": {"Low/Benign": 1, "Neutral": 0, "High/Suspicious": -1}[links_in_tags],
        "SFH": {"Low/Benign": 1, "Neutral": 0, "High/Suspicious": -1}[sfh],
        "Abnormal_URL": 1 if abnormal_url else -1,
        "has_political_keyword": 1 if has_political_keyword else 0,
    }])

# Tabs
tab_analyze, tab_attr = st.tabs(["Analyze URL", "Threat Attribution"])

with tab_analyze:
    st.subheader("Step 1: Predict MALICIOUS vs BENIGN")
    if submitted:
        feats = build_feature_row()
        pred = predict_cls(cls_model, data=feats)
        verdict = pred["prediction_label"].iloc[0]
        st.markdown(f"### Verdict: **{verdict}**")

        # keep for attribution tab
        st.session_state["last_features"] = feats
        st.session_state["last_verdict"] = verdict

        # Optional confidence if scores exist
        score_cols = [c for c in pred.columns if c.lower().startswith("score")]
        if score_cols:
            try:
                conf = float(pred[score_cols].max(axis=1).iloc[0])
                st.caption(f"Model confidence: {conf:.3f}")
            except Exception:
                pass

with tab_attr:
    st.subheader("Step 2: Threat Attribution (runs only if verdict is MALICIOUS)")
    if st.session_state.get("last_verdict") == "MALICIOUS":
        if (clu_model is None) or (cluster_map is None):
            st.info("Attribution model or mapping not found. Re-run `train_model.py` to enable attribution.")
        else:
            feats = st.session_state["last_features"]
            clu_pred = predict_clu(clu_model, data=feats)
            cluster_id = int(clu_pred["Cluster"].iloc[0])
            actor = cluster_map.get(cluster_id, "Unknown")

            st.markdown(f"### Predicted Actor: **{actor}** (Cluster {cluster_id})")

            with st.expander("About this actor profile"):
                blurbs = {
                    "State-Sponsored": "Well-resourced, stealthy operations; often valid SSL and subtle deception.",
                    "Organized Cybercrime": "High-volume monetization campaigns; shorteners, IP-based links, noisy structure.",
                    "Hacktivist": "Opportunistic, message-driven; mixed tactics with political themes."
                }
                st.write(blurbs.get(actor, "No description available."))
            st.json({"cluster_id": cluster_id, "mapped_actor": actor})
    else:
        st.info("Run an analysis and ensure the verdict is **MALICIOUS** to see attribution here.")
