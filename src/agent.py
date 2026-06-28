import re
import fnmatch

class OpenShellAgentSandbox:
    def __init__(self, policy_content=None):
        self.policy = {
            "filesystem": {"allow_read": [], "allow_write": [], "deny_read": []},
            "process": {"allow_binaries": [], "deny_capabilities": []},
            "network": {"egress": []},
            "inference": {"routes": []}
        }
        if policy_content:
            self.parse_yaml(policy_content)

    def parse_yaml(self, content):
        """Lighweight, zero-dependency YAML parser for OpenShell policies."""
        current_section = None
        current_subsection = None
        
        for line in content.splitlines():
            # Remove comments and whitespace
            line = line.split('#')[0].strip()
            if not line:
                continue
            
            # Check if line is a list item
            is_list_item = False
            if line.startswith('-'):
                is_list_item = True
                line = line[1:].strip()
                
            # Detect section declarations ending with colon (and no value)
            if line.endswith(':') and not is_list_item:
                section_name = line[:-1].strip()
                if section_name in ["filesystem", "process", "network", "inference"]:
                    current_section = section_name
                    current_subsection = None
                elif current_section in ["filesystem", "process"] and section_name in ["allow_read", "allow_write", "deny_read", "allow_binaries", "deny_capabilities"]:
                    current_subsection = section_name
                elif current_section == "network" and section_name == "egress":
                    current_subsection = section_name
                continue
            
            # Key-value pairs
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip()
                v = v.strip().replace('"', '').replace("'", "")
                
                # Check for properties or subsection settings
                if not is_list_item:
                    if current_section == "filesystem" and k in ["allow_read", "allow_write", "deny_read"]:
                        current_subsection = k
                    elif current_section == "process" and k in ["allow_binaries", "deny_capabilities"]:
                        current_subsection = k
                else:
                    # Inside a list, e.g. - destination: api.anthropic.com
                    if current_section == "network" and k == "destination":
                        self.policy["network"]["egress"].append(v)
            else:
                # Simple list value (e.g. - /usr/bin/python3)
                if is_list_item and current_section and current_subsection:
                    val = line.replace('"', '').replace("'", "")
                    if current_section == "filesystem":
                        self.policy["filesystem"][current_subsection].append(val)
                    elif current_section == "process":
                        self.policy["process"][current_subsection].append(val)

    def is_path_matched(self, path, patterns):
        for pattern in patterns:
            # Convert glob stars to fnmatch format
            clean_pattern = pattern.replace('**', '*')
            if fnmatch.fnmatch(path, clean_pattern):
                return True
        return False

    def validate_action(self, action_type, binary, target=None):
        """Audits actions against the parsed policy rules.
        
        Returns:
            dict: { "status": "ALLOWED"|"BLOCKED", "reason": str }
        """
        # 1. Process validation
        if binary not in self.policy["process"]["allow_binaries"]:
            return {
                "status": "BLOCKED",
                "reason": f"Binary '{binary}' is not listed in allow_binaries configuration."
            }

        # 2. Filesystem operations
        if action_type == "read" and target:
            # Check explicit denies first
            if self.is_path_matched(target, self.policy["filesystem"]["deny_read"]):
                return {
                    "status": "BLOCKED",
                    "reason": f"Read access to '{target}' explicitly denied by deny_read rules."
                }
            # Check allow rules
            if not self.is_path_matched(target, self.policy["filesystem"]["allow_read"]):
                return {
                    "status": "BLOCKED",
                    "reason": f"Read access to '{target}' blocked (not matched in allow_read)."
                }
            return {"status": "ALLOWED", "reason": f"Matched filesystem allow_read rule."}

        if action_type == "write" and target:
            if not self.is_path_matched(target, self.policy["filesystem"]["allow_write"]):
                return {
                    "status": "BLOCKED",
                    "reason": f"Write access to '{target}' blocked (not matched in allow_write)."
                }
            return {"status": "ALLOWED", "reason": f"Matched filesystem allow_write rule."}

        # 3. Network operations
        if action_type == "network" and target:
            # Check if domain matches any whitelist patterns
            allowed = False
            for rule in self.policy["network"]["egress"]:
                clean_rule = rule.replace('*.', '')
                if clean_rule in target or fnmatch.fnmatch(target, rule):
                    allowed = True
                    break
            if not allowed:
                return {
                    "status": "BLOCKED",
                    "reason": f"Outbound connection to '{target}' blocked (domain not whitelisted in network.egress)."
                }
            return {"status": "ALLOWED", "reason": f"Network egress to '{target}' allowed."}

        return {"status": "ALLOWED", "reason": "No policy constraint matched."}
