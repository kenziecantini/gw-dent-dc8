# Threat Model: Secure Containerized Microservices

## 1. Overview
This document outlines the threat modeling exercise performed on the initial insecure application, following STRIDE and MITRE ATT&CK methodologies.

---
# Threat Model: Flask App Container

## 2. STRIDE Threat Analysis

| Threat      | Description | Location | Mitigation |
|-------------|-------------|----------|------------|
| **Spoofing** | No auth on API requests | All endpoints | Introduced API key via `.env` |
| **Tampering** | Use of `eval()` | `/calculate` | Replaced with `ast.literal_eval()` |
| **Repudiation** | No logging/tracking | Entire app | Logging could be improved |
| **Information Disclosure** | Hardcoded secrets | `app.py` | Secrets moved to `.env` |
| **Denial of Service** | Unvalidated inputs | `/calculate`, `/ping` | Input validation added |
| **Elevation of Privilege** | Runs as root | Docker container | Now runs as non-root user |

---

#3. MITRE ATT&CK for Containers

| Technique ID | Name | Affected Area | Mitigation |
|--------------|------|----------------|------------|
| T1059 | Command & Scripting Interpreter | `eval()`, `subprocess()` | Removed eval, validated IP input |
| T1203 | Exploitation for Client Execution | Open endpoints | Input validation |
| T1086 | PowerShell (generic) | Use of `eval()` | Removed |
| T1611 | Escape to Host | Root in container | Runs as non-root |
| T1526 | Cloud Service Discovery | Ping to any IP | IP validation added |

---

#4. Vulnerabilities Mapped to NIST 800-53 Controls

| Vulnerability | NIST ID | Description | Mitigation |
|---------------|---------|-------------|------------|
| Hardcoded secrets | SC-12, IA-5 | Credential and key management | Use of `.env` |
| Insecure `eval()` | SI-10, SI-7 | Input handling & code integrity | `ast.literal_eval()` |
| Insecure base image | CM-6, SI-2 | Config & software integrity | Slim image + multi-stage |
| Running as root | AC-6, CM-2 | Least privilege | Added non-root user |
| Lack of input validation | SI-10 | Input validation | Checks for IPs, math exprs |


## 1. STRIDE Analysis

| Threat Category | Example | Impact | Mitigation |
|----------------|---------|--------|------------|
| Spoofing        | Lack of auth on `/calculate` | Unauthorized access | Add auth/token check |
| Tampering       | Unsafe IP input to `ping` | Command injection | Input validation |
| Repudiation     | No logging | Difficult to audit usage | Implement access logs |
| Information Disclosure | Hardcoded passwords | Credential leak | Use env variables |
| Denial of Service | Unrestricted `ping` or `eval` | Resource exhaustion | Rate limiting |
| Elevation of Privilege | Runs as root | Full system compromise | Use non-root user |

---

## 2. MITRE ATT&CK Mapping (Containers)

| Tactic         | Technique ID | Technique Name | Application Relevance |
|----------------|--------------|----------------|------------------------|
| Initial Access | T1190         | Exploit Public-Facing Application | Command injection in `/ping` |
| Execution      | T1059         | Command and Scripting Interpreter | Use of `eval()` |
| Persistence    | T1525         | Implant Container Image | No image signing or validation |
| Privilege Escalation | T1611  | Escape to Host | Root container user |
| Defense Evasion | T1211        | Exploitation for Defense Evasion | Lack of file system isolation |

---

## 3. Controls Mapping

| Issue | Recommended Control | Framework Reference |
|-------|---------------------|---------------------|
| Hardcoded secrets | Environment secrets | NIST 800-53: SC-12, SC-28 |
| Root container user | Add `USER appuser` | NIST 800-53: AC-6, CM-6 |
| No network restrictions | Isolate with Docker networks | NIST 800-53: SC-7 |
| Missing health check | Add `HEALTHCHECK` | CIS Docker Benchmark |
| Unvalidated inputs | Strict input validation | OWASP Top 10: A1-Injection |

---

## 4. Risk Rating Summary

| Threat | Risk | Likelihood | Impact | Mitigation Priority |
|--------|------|------------|--------|----------------------|
| Command Injection | High | High | Critical | Immediate |
| Credential Exposure | Medium | High | Medium | High |
| Eval-based execution | High | Medium | High | Immediate |
| Root user in container | High | Medium | Critical | Immediate |

---

## 5. Conclusion

This threat model identifies the major flaws in the system and informs the remediation and architecture redesign. The final implementation significantly reduces the attack surface and enforces least privilege, defense in depth, and secure defaults.

