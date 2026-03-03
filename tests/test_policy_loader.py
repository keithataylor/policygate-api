
import json
from pathlib import Path
import pytest

from jsonschema import validate, ValidationError
from policygate.policy_loader import load_and_validate_policy


def test_load_and_validate_policy_valid():
    policy = load_and_validate_policy(
    "policy/policy.yaml", 
    "contracts/policy.schema.json"
    )
    assert isinstance(policy, dict)
    assert policy["policy_id"]  
    assert "rules" in policy


# Test with a valid policy and schema

def test_policy_schema_rejects_typo_decision():
    schema_path = Path("contracts/policy.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    # Minimal valid-looking policy, with one realistic typo in decision.
    bad_policy = {
        "policy_id": "test",
        "policy_version": "1",
        "default": {"decision": "ALOW", "rationale_codes": ["X"]},  # typo
        "rules": [
            {
                "rule_id": "r1",
                "priority": 1,
                "when": {"action": "infer:run"},
                "then": {"decision": "ALLOW", "rationale_codes": ["OK"]},
            }
        ],
    }

    with pytest.raises(ValidationError):
        validate(instance=bad_policy, schema=schema)
        

