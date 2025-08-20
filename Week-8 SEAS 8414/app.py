import os
import json
import time
import streamlit as st
import pandas as pd

from pycaret.classification import load_model as load_cls_model, predict_model as predict_cls
from pycaret.clustering import load_model as load_clu_model, predict_model as predict_clu

# Page config
st.set_page_config(page_title="GenAI-Powered Phishing SOAR", layout="wide")
st.title("GenAI Powered SOAR for Phishing URL Analysis")

# Cached loader (models + optional plot)
@st.cache_resource
def load_assets():
    # Classification model
    cls = load_cls_model('models/phishing_url_detector') if os.path.exists('models/phishing_url_detector.pkl') else None

    # Clustering model + mapping
    clu = load_clu_model('models/threat_actor_profiler') if os.path.exists('models/threat_actor_profiler.pkl') else None
    mapping_path = 'models/cluster_mapping.json'
    mapping = None
    if os.path.exists(mapping_path):
        with open(mapping_path, 'r') as f:
            mapping = {int(k): v for k, v in json.load(f).items()}

    #feature importance image
    feat_plot = 'models/feature_importance.png' if os.path.exists('models/feature_importance.png') else None
    return cls, clu, mapping, feat_plot

cls_model, clu_model, cluster_map, feature_plot = load_assets()

if not cls_model:
    st.error("Model not found. Make sure you've trained first (python train_model.py).")
    st.stop()

# Sidebar: URL Feature Input (UI)
with st.sidebar:
    st
