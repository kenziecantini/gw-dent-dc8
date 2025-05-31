
# Lab: Securing a Vulnerable Web Application

## Overview

The lab walks through seven steps to set up, secure, and analyze a vulnerable web application (Juice Shop). Each step builds on the previous one, showing the transition from an insecure baseline to a defended state, and then verifying the effectiveness of the security measures.

### What the Demo is About

The demo showcases:
- Setting up a vulnerable web application (Juice Shop) and assessing its initial security posture.
- Adding layered security controls (WAF and IDS) to protect the application.
- Measuring the impact of these controls through security scans and analysis.
- Connecting practical security measures to foundational architectures like Zero Trust Architecture (ZTA), Defense in Depth (DiD), and Adaptive Security Architecture (ASA).

## Prerequisites

- **Docker** 20.10 or higher
- **`make`** command-line tool
- **Linux Users**: Either run commands with `sudo` or add yourself to the `docker` group:
  ```bash
  sudo usermod -aG docker $USER && newgrp docker
  ```
- Optional: Python 3 and `beautifulsoup4` (for Step 4 analysis):
  ```bash
  pip install beautifulsoup4
  ```

## Steps Explained

### Step 1: Baseline Setup and Scan
- **Command**: `make step-1`
- **What it Does**:
  - Launches the Juice Shop (a deliberately vulnerable web app) on port 3000 and a ZAP (OWASP Zed Attack Proxy) container for scanning.
  - Runs a baseline ZAP scan against `http://juice:3000` to identify initial vulnerabilities.
  - Saves the scan report to `reports/zap-before.html`.
- **Purpose**: Establishes the insecure starting point for the lab.

### Step 2: Add Security Controls
- **Command**: `make step-2`
- **What it Does**:
  - Deploys a WAF (ModSecurity CRS) and an IDS (Suricata) using Docker Compose.
  - The WAF protects Juice Shop, now accessible only through `http://localhost` (port 80), blocking direct access to port 3000.
  - Suricata monitors network traffic for suspicious activity.
- **Purpose**: Introduces security controls to mitigate vulnerabilities.

### Step 3: Verify with Another Scan
- **Command**: `make step-3`
- **What it Does**:
  - Runs a second ZAP scan, this time against the WAF at `http://waf:8080`.
  - Saves the report to `reports/zap-after.html`.
  - Displays a diff between `zap-before.html` and `zap-after.html` to highlight changes.
- **Purpose**: Verifies the effectiveness of the WAF and IDS by comparing scan results.

### Step 4: Analyze Reports
- **Command**: `make step-4`
- **What it Does**:
  - Executes a Python script (`analyze_reports.py`) to compare the before and after ZAP reports.
  - Provides a detailed summary of how the security posture improved.
- **Purpose**: Offers a deeper analysis of the security controls' impact.

### Step 5: Discuss Security Concepts
- **Command**: `make step-5`
- **What it Does**:
  - Prints talking points linking the lab to ZTA, DiD, and ASA (see "Controls and Security Architectures" below).
- **Purpose**: Connects the practical demo to theoretical security frameworks.

### Step 6: Live Demo Script
- **Command**: `make step-6`
- **What it Does**:
  - Outputs a step-by-step guide for a live demo:
    1. Run `make step-1` to set up the baseline.
    2. Simulate an attack on `http://localhost:3000`.
    3. Run `make step-2` to add defenses.
    4. Attempt the attack on `http://localhost` (WAF blocks it; IDS logs it).
    5. Run `make step-3` to re-scan and diff results.
    6. Run `make step-4` to analyze reports.
    7. Discuss security mappings from Step 5.
- **Purpose**: Provides a script for presenting the lab live.

### Step 7: Cleanup
- **Command**: `make step-7`
- **What it Does**:
  - Stops all containers, removes volumes, and prunes unused Docker resources.
- **Purpose**: Ensures a clean environment after the lab.

## How to Use This Lab

1. **Setup and Baseline**:
   ```bash
   make step-1
   ```
   - Open `reports/zap-before.html` to review initial vulnerabilities.
   - Access Juice Shop at `http://localhost:3000` (initially).

2. **Add Defenses**:
   ```bash
   make step-2
   ```
   - Browse to `http://localhost` (via WAF).
   - Optionally, tail Suricata logs:
     ```bash
     docker compose -p week10 logs -f suricata
     ```

3. **Verify and Analyze**:
   ```bash
   make step-3
   make step-4
   ```
   - Review `reports/zap-after.html` and the analysis output.

4. **Live Demo (Optional)**:
   - Follow the script from `make step-6` for a 15-minute presentation.

5. **Cleanup**:
   ```bash
   make step-7
   ```

## What to Take Home

This lab offers practical insights into:
- **Vulnerability Assessment**: Using ZAP to identify and quantify application weaknesses.
- **Security Controls**: Deploying a WAF and IDS to protect an application.
- **Impact Measurement**: Comparing before-and-after scans to evaluate security improvements.
- **Conceptual Understanding**:
  - How security layers reduce risk.
  - Real-world application of ZTA, DiD, and ASA principles.

## Controls Implemented

1. **Web Application Firewall (WAF)**:
   - **Tool**: ModSecurity CRS (running on NGINX Alpine).
   - **Role**: Filters and blocks malicious HTTP requests at the application layer (Layer 7).
   - **Configuration**: Enforces security policies with `MODSEC_RULE_ENGINE=On`, routing traffic to Juice Shop via `BACKEND=http://juice:3000`.

2. **Intrusion Detection System (IDS)**:
   - **Tool**: Suricata.
   - **Role**: Monitors network traffic (Layers 3/4) and logs suspicious activities.
   - **Configuration**: Runs with network visibility (`-i eth0`) and elevated privileges (`NET_ADMIN`, `NET_RAW`).

3. **Application**:
   - **Tool**: Juice Shop.
   - **Role**: The target application, representing a real-world asset needing protection.

## Mapping to Security Architectures

### Zero Trust Architecture (ZTA)
- **Principle**: "Never trust, always verify."
- **Mapping**: The WAF acts as a **Policy Enforcement Point (PEP)**, inspecting and validating every request to Juice Shop, ensuring no implicit trust is granted.

### Defense in Depth (DiD)
- **Principle**: Multiple layers of security controls.
- **Mapping**:
  - **Layer 7 (Application)**: WAF filters HTTP traffic.
  - **Layers 3/4 (Network/Transport)**: Suricata detects anomalies.
  - **Application Layer**: Juice Shop itself (ideally with internal hardening).

### Adaptive Security Architecture (ASA)
- **Principle**: Dynamic, perimeter-based protection.
- **Mapping**: The WAF serves as an edge defense, akin to a perimeter firewall, adapting to threats by blocking attacks before they reach the application.

## Additional Notes

- **Portability**: Docker ensures consistent setup across systems.
- **Reports**: ZAP HTML reports are human-readable; use a browser to view them.
- **Logs**: Check Suricata logs for IDS alerts during attacks.
- **Dependencies**: Install `beautifulsoup4` for Step 4 if not already present.

This lab bridges theory and practice, making security concepts tangible and actionable.

