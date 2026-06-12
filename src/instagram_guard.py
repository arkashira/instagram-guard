import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SecurityRule:
    name: str
    description: str
    enabled: bool

class InstagramGuard:
    def __init__(self):
        self.rules = {
            "geo-restriction": SecurityRule("Geo-Restriction", "Restrict access based on location", False),
            "device-fingerprinting": SecurityRule("Device Fingerprinting", "Restrict access based on device fingerprint", False)
        }

    def get_rules(self) -> Dict[str, SecurityRule]:
        return self.rules

    def toggle_rule(self, rule_name: str) -> None:
        if rule_name in self.rules:
            self.rules[rule_name].enabled = not self.rules[rule_name].enabled
        else:
            raise ValueError("Rule not found")

    def save_preferences(self) -> None:
        # In a real implementation, this would save to a database or file
        # For this example, we'll just print the current state
        print(json.dumps({rule_name: rule.enabled for rule_name, rule in self.rules.items()}))
