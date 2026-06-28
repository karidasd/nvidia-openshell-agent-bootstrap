import os

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def main():
    print("=================================================================")
    print("🛠️ NVIDIA OpenShell policy-generator Utility")
    print("=================================================================")
    print("Generates secure declarative YAML profiles for local AI agents.\n")

    agent_name = get_input("Enter Agent Profile Name", "custom-security-agent")
    workspace = get_input("Allowed Workspace Directory", "/workspace/my-project")
    
    print("\nSelect Allowed binaries (comma-separated):")
    binaries_raw = get_input("Binaries", "python3,git,curl")
    binaries = [f"/usr/bin/{b.strip()}" for b in binaries_raw.split(",") if b.strip()]
    
    print("\nSelect Network egress domains (comma-separated):")
    domains_raw = get_input("Allowed Egress Domains", "api.anthropic.com,github.com")
    domains = [d.strip() for d in domains_raw.split(",") if d.strip()]

    # Generate YAML Content
    yaml_content = f"""# NVIDIA OpenShell Security Policy
# Target Profile: {agent_name}
# Enforcement Layer: Landlock FS & Granular Egress Whitelists
# Generated via OpenShell Policy Generator CLI

filesystem:
  allow_read:
    - {workspace}/**
    - /usr/lib/**
  allow_write:
    - {workspace}/src/**
    - {workspace}/tests/**
    - /tmp/**
  deny_read:
    - {workspace}/.env
    - {workspace}/secrets/**

process:
  allow_binaries:
"""
    for b in binaries:
        yaml_content += f"    - {b}\n"
        
    yaml_content += """  deny_capabilities:
    - CAP_SYS_ADMIN
    - CAP_NET_RAW

network:
  egress:
"""
    for d in domains:
        yaml_content += f"    - destination: '{d}'\n      ports: [443]\n"
        
    yaml_content += """
inference:
  routes:
    - pattern: '*'
      backend: local/nemotron
"""

    policies_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "policies")
    os.makedirs(policies_dir, exist_ok=True)
    out_path = os.path.join(policies_dir, f"{agent_name}-policy.yaml")

    with open(out_path, "w") as f:
        f.write(yaml_content)

    print(f"\n[OK] Successfully generated custom secure policy file!")
    print(f"👉 Exported to: policies/{agent_name}-policy.yaml")
    print("=================================================================")

if __name__ == "__main__":
    main()
