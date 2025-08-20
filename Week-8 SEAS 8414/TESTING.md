# TESTING

Manual test the four scenarios below in the Streamlit UI sidebar. These map to the synthetic feature design.

---

## 1) Benign (Expect: BENIGN)
- URL Length: **Normal**
- SSL: **Trusted**
- Sub-domain: **None**
- Uncheck: **Uses IP**, **Is Shortened**, **Abnormal URL**
- Keep other tri-state inputs at **benign/neutral**

---

## 2) Organized Cybercrime (Expect: MALICIOUS + Organized Cybercrime)
- URL Length: **Long**
- SSL: **Suspicious**
- Sub-domain: **Many**
- Check: **Uses IP**, **Is Shortened**, **Abnormal URL**
- Others: skew toward suspicious

---

## 3) State‑Sponsored (Expect: MALICIOUS + State‑Sponsored)
- SSL: **Trusted**
- Prefix/Suffix: **Checked**
- Low use of IP/shorteners
- Abnormal structure: **Low**
- Sub-domains: **One** / **Many** (moderate)

---

## 4) Hacktivist (Expect: MALICIOUS + Hacktivist)
- Contains political keyword: **Checked**
- Abnormal structure: **Often**
- Others: mixed/variable

---

### Batch Testing
Use the app’s **Batch Test** tab with a CSV matching feature columns
