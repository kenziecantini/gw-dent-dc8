"""
Feature computation utilities for domain analysis.
"""
from __future__ import annotations
import math
import re
from typing import Dict, List
import pandas as pd


_ALLOWED_CHARS_RE = re.compile(r"[a-z0-9.-]")

def _clean_domain(domain: str) -> str:
    if not isinstance(domain, str):
        return ""
    d = domain.strip().lower()
    # remove scheme and path fragments just in case
    d = re.sub(r"^https?://", "", d)
    d = d.split("/")[0]
    # keep only allowed characters
    d = "".join(ch for ch in d if _ALLOWED_CHARS_RE.match(ch))
    return d

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    # Count frequency of each character
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    n = float(len(s))
    return -sum((c/n) * math.log(c/n, 2) for c in freq.values())

def domain_length(s: str) -> int:
    return len(s or "")

def digit_ratio(s: str) -> float:
    if not s:
        return 0.0
    digits = sum(ch.isdigit() for ch in s)
    return digits / len(s)

def hyphen_ratio(s: str) -> float:
    if not s:
        return 0.0
    hyphens = s.count("-")
    return hyphens / len(s)

def vowel_ratio(s: str) -> float:
    if not s:
        return 0.0
    vowels = set("aeiou")
    v = sum(ch in vowels for ch in s)
    return v / len(s)

BASIC_FEATURES = ["length", "entropy"]
RICH_FEATURES = ["length", "entropy", "digit_ratio", "hyphen_ratio", "vowel_ratio"]

def compute_features(domains: List[str], rich: bool = True) -> pd.DataFrame:
    """
    Compute features for a list of domain strings.
    Returns a pandas DataFrame with consistent column order.
    """
    rows = []
    for d in domains:
        cd = _clean_domain(d)
        base = {
            "length": domain_length(cd),
            "entropy": shannon_entropy(cd.replace(".", "")),  # entropy without dots
        }
        if rich:
            base.update({
                "digit_ratio": digit_ratio(cd),
                "hyphen_ratio": hyphen_ratio(cd),
                "vowel_ratio": vowel_ratio(cd),
            })
        rows.append(base)
    cols = RICH_FEATURES if rich else BASIC_FEATURES
    return pd.DataFrame(rows, columns=cols)

def feature_names(rich: bool = True) -> List[str]:
    return RICH_FEATURES if rich else BASIC_FEATURES