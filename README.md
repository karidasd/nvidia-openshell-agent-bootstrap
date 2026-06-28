# NVIDIA DGX Spark & OpenShell Agent Bootstrap Kit

🚀 **The Zero-Token Desktop AI & Data Science Supercomputer Setup.**

This repository is a developer-focused bootstrap kit for building, testing, and deploying secure, autonomous AI agents locally on **NVIDIA DGX Spark** workstations utilizing the **NVIDIA OpenShell** sandboxed runtime.

👉 **[Launch the Interactive OpenShell Sandbox & Telemetry Portal Live!](https://karidasd.github.io/nvidia-openshell-agent-bootstrap/)**

---

## 💡 The Problem: Cloud Token Costs & Data Exfiltration Risks

When deploying autonomous coding or analytics agent loops (such as CrewAI, LangGraph, or custom self-correcting prompt scripts) using cloud APIs (like GPT-4o or Claude 3.5 Sonnet):
1. **Exponential API Billing**: A single complex coding task can require 50–100 prompt iterations. For a development team, this translates to **thousands of euros per month in API token bills**.
2. **Data Leaks**: Private enterprise code repositories, database schemas, and proprietary CSV tables are sent over the wire to external cloud vendors.
3. **Execution Risks**: If you allow an autonomous agent to execute shell commands locally to test code, it has full access to your PC. A rogue agent could accidentally delete files, leak `.env` keys, or download malicious dependencies.

---

## 🟢 The Solution: NVIDIA DGX Spark + OpenShell

By running open-source models (like Llama-3.1-70B, DeepSeek-Coder-V2, or Nemotron-4-340B) locally on the **NVIDIA DGX Spark** desktop workstation:
1. **Unlimited Agent Loops for €0**: Run recursive debug loops and data analysis workflows infinitely with zero API token charges or subscriptions.
2. **128GB Unified System Memory**: Powered by the **NVIDIA GB10 Grace Blackwell Superchip**, enabling execution of high-parameter models locally.
3. **Hardware-Level Sandboxing**: **NVIDIA OpenShell** wraps local agents in kernel-level Linux Landlock sandboxes, preventing them from accessing ssh keys, editing systems configs, or initiating unauthorized outbound network connections.

---

## 📁 Repository Structure

*   `policies/`: Declarative YAML security policies governing system access boundaries.
    *   [secure-coder-policy.yaml](policies/secure-coder-policy.yaml): Strict read/write limits for software engineering tasks.
    *   [data-auditor-policy.yaml](policies/data-auditor-policy.yaml): A fully air-gapped security profile for local data science.
    *   [autonomous-scraper-policy.yaml](policies/autonomous-scraper-policy.yaml): restircts network egress solely to HuggingFace or arXiv.
*   `src/`: Python sandbox verification engine.
    *   [agent.py](src/agent.py): Parsers and validators mapping actions to the YAML definitions.
    *   [main.py](src/main.py): Local CLI test simulation.
*   `index.html`: Interactive developer dashboard showing Blackwell telemetry, policy selectors, and a real-time guardrail shell validator.

---

## 🛡️ Example Policy Specification: `secure-coder-policy.yaml`

```yaml
# Static Landlock boundaries applied at sandbox container creation
filesystem:
  allow_read:
    - /workspace/my-project/**
    - /usr/lib/**
  allow_write:
    - /workspace/my-project/src/**
    - /workspace/my-project/tests/**
    - /tmp/**
  deny_read:
    - /workspace/my-project/.env
    - /workspace/my-project/secrets/**

process:
  allow_binaries:
    - /usr/bin/python3
    - /usr/bin/node
    - /usr/bin/git
    - /usr/bin/npm

network:
  egress:
    - destination: api.anthropic.com
      ports: [443]
      binary: /usr/bin/curl
    - destination: '*.github.com'
      ports: [443]
      binary: /usr/bin/git
```

---

## ⚡ Running the Local Simulation

A zero-dependency Python mock sandbox is included to test agent actions against policies:

```bash
# Clone the repository
git clone https://github.com/karidasd/nvidia-openshell-agent-bootstrap.git
cd nvidia-openshell-agent-bootstrap

# Run the test simulation
python src/main.py
```

### Expected Output:
```text
=================================================================
🟢 NVIDIA OpenShell Agent Sandbox Local Simulator
=================================================================

✅ Loaded policy: secure-coder-policy.yaml
   Allow Binaries: ['/usr/bin/python3', '/usr/bin/node', '/usr/bin/git', '/usr/bin/npm']

👉 Request: Running '/usr/bin/python3'...
   [🟢 ALLOWED] Binary '/usr/bin/python3' is allowed.

👉 Request: Running '/usr/bin/python3' on '/workspace/my-project/.env'...
   [🔴 BLOCKED] Read access to '/workspace/my-project/.env' explicitly denied by deny_read rules.

👉 Request: Running '/usr/bin/curl' on 'api.anthropic.com'...
   [🔴 BLOCKED] Binary '/usr/bin/curl' is not listed in allow_binaries configuration.
```
