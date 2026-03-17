import pytest
from policygate.exceptions import (
    DuplicateRuleIdError, 
    InvalidPriorityError, 
    InvalidRationaleCodesError,
    ConflictingEqualPriorityOverlapError, 
    RedundantEqualPriorityOverlapError
)
from policygate.policy_loader import validate_policy_semantics


def test_validate_policy_semantics_accepts_valid_policy() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["PUBLIC_OK"],
                },
            }
        ]
    }
    validate_policy_semantics(policy)


def test_validate_policy_semantics_duplicate_rule_id() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["PUBLIC_OK"],
                },
            },
            {
                "rule_id": "allow_public_infer",
                "priority": 50,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "internal"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["INTERNAL_OK"],
                },
            }
        ]
    }
    with pytest.raises(DuplicateRuleIdError):
        validate_policy_semantics(policy)


def test_validate_policy_semantics_invalid_priority() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 150,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["PUBLIC_OK"],
                },
            }
        ]
    }
    with pytest.raises(InvalidPriorityError):
        validate_policy_semantics(policy)


def test_validate_policy_semantics_invalid_rationale_codes_list() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": {},  # Invalid: should be a list, not a dict               
                },
            }
        ]
    }
    with pytest.raises(InvalidRationaleCodesError):
        validate_policy_semantics(policy)

def test_validate_policy_semantics_invalid_rationale_codes_empty_id() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": [""],  # Invalid: empty string in list               
                },
            }
        ]
    }
    with pytest.raises(InvalidRationaleCodesError):
        validate_policy_semantics(policy)    


def test_validate_policy_semantics_invalid_rationale_codes_empty_value() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["SOME_CODE", ""],  # Invalid: empty string in list               
                },
            }
        ]
    }
    with pytest.raises(InvalidRationaleCodesError):
        validate_policy_semantics(policy)    


def test_validate_policy_semantics_invalid_rationale_codes_non_string() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["SOME_CODE", 100],  # Invalid: non-string in list               
                },
            }
        ]
    }
    with pytest.raises(InvalidRationaleCodesError):
        validate_policy_semantics(policy)


#conflicting equal-priority overlap
def test_validate_policy_semantics_conflicting_equal_priority_overlap() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 50,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["PUBLIC_OK"],
                },
            },
            {
                "rule_id": "block_public_infer",
                "priority": 50,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "BLOCK",
                    "rationale_codes": ["PUBLIC_BLOCKED"],
                },
            }
        ]
    }
    with pytest.raises(ConflictingEqualPriorityOverlapError):
        validate_policy_semantics(policy)

#redundant equal-priority overlap
def test_validate_policy_semantics_redundant_equal_priority_overlap() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "allow_public_infer",
                "priority": 50,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["PUBLIC_OK"],
                },
            },
            {
                "rule_id": "allow_public_infer_duplicate",
                "priority": 50,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "ALLOW",
                    "rationale_codes": ["PUBLIC_OK"],
                },
            }
        ]
    }
    with pytest.raises(RedundantEqualPriorityOverlapError):
        validate_policy_semantics(policy)
