import re
from typing import List, Dict, Any

class InspectionEngine:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    def evaluate(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        fields = extracted_data.get("fields", {})

        for rule in self.rules:
            target_field = rule["target_field"]
            extracted_val = fields.get(target_field)
            check_type = rule["check_type"]

            status = "Passed"
            evidence = f"Extracted value: '{extracted_val}'"

            if check_type == "regex_match":
                pattern = rule.get("pattern", "")
                if not extracted_val or not re.match(pattern, extracted_val):
                    status = rule.get("severity", "Failed")
                    evidence = f"Expected pattern '{pattern}', got '{extracted_val}'"

            elif check_type == "presence":
                expected = rule.get("expected", "")
                if not extracted_val or expected.lower() not in str(extracted_val).lower():
                    status = rule.get("severity", "Review Required")
                    evidence = f"Expected string containing '{expected}', found '{extracted_val}'"

            results.append({
                "rule_id": rule["rule_id"],
                "category": rule["category"],
                "description": rule["description"],
                "status": status,
                "evidence": evidence
            })

        return results