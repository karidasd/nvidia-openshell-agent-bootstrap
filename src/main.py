import os
from agent import OpenShellAgentSandbox

def main():
    policy_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "policies")
    secure_coder_path = os.path.join(policy_dir, "secure-coder-policy.yaml")
    
    print("=================================================================")
    print("[ACTIVE] NVIDIA OpenShell Agent Sandbox Local Simulator")
    print("=================================================================\n")
    
    if not os.path.exists(secure_coder_path):
        print("[ERROR] Policy file secure-coder-policy.yaml not found!")
        return

    with open(secure_coder_path, "r") as f:
        policy_content = f.read()

    # Ingest sandbox rules
    sandbox = OpenShellAgentSandbox(policy_content)
    print("[LOADED] Policy: secure-coder-policy.yaml")
    print(f"   Allow Binaries: {sandbox.policy['process']['allow_binaries']}")
    print(f"   Egress Whitelists: {sandbox.policy['network']['egress']}\n")

    # Simulation Test Cases
    test_cases = [
        # Binary execution tests
        ("execute", "/usr/bin/python3", None),
        ("execute", "/usr/bin/apt-get", None),
        
        # Filesystem read tests
        ("read", "/usr/bin/python3", "/workspace/my-project/src/app.py"),
        ("read", "/usr/bin/python3", "/workspace/my-project/.env"),
        ("read", "/usr/bin/python3", "/home/user/passwords.txt"),
        
        # Filesystem write tests
        ("write", "/usr/bin/python3", "/workspace/my-project/src/utility.py"),
        ("write", "/usr/bin/python3", "/etc/hosts"),
        
        # Network egress tests
        ("network", "/usr/bin/curl", "api.anthropic.com"),
        ("network", "/usr/bin/curl", "malicious-server.net"),
    ]

    for action, binary, target in test_cases:
        target_str = f" on '{target}'" if target else ""
        print(f"-> Request: Running '{binary}'{target_str}...")
        result = sandbox.validate_action(action, binary, target)
        status_flag = "[OK]" if result["status"] == "ALLOWED" else "[BLOCKED]"
        print(f"   {status_flag} {result['status']}: {result['reason']}\n")

if __name__ == "__main__":
    main()
