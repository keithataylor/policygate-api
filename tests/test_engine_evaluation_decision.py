from tokenize import maybe
from unittest import result

from policygate.models import Decision
from policygate import engine


def test_engine_higher_priority_rule_wins() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "review_public_infer",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "REQUIRE_REVIEW",
                    "rationale_codes": ["PUBLIC_REVIEW"],
                },
            },
            {
                "rule_id": "degrade_public_infer",
                "priority": 20,
                "when": {
                    "action": "infer:run",
                    "resource": {"sensitivity": "public"},
                },
                "then": {
                    "decision": "DEGRADE",
                    "rationale_codes": ["PUBLIC_DEGRADED"],
                },
            },
        ]
    }

    evaluate_request = {
        "action": "infer:run",
        "resource": {"sensitivity": "public"},
    }

    result = engine.evaluate_decision(evaluate_request, policy)

    assert result.decision == Decision.DEGRADE
    assert result.matched_rule_id == "degrade_public_infer"


def test_engine_decision_no_matching_rule() -> None:
    policy = {
        "default": {
            "decision": "BLOCK",
            "rationale_codes": ["POLICY_DEFAULT_DENY"],
        },
        "rules": [
            {
                "rule_id": "allow_internal_infer",
                "priority": 10,
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

    evaluate_request = {
        "action": "infer:run",
        "resource": {"sensitivity": "public"},
    }

    result = engine.evaluate_decision(evaluate_request, policy)

    assert result.decision == Decision.BLOCK # Default decision when no rules match
    assert result.rationale_codes == ["POLICY_DEFAULT_DENY"]
    assert result.matched_rule_id is None


def test_engine_decision_signals() -> None:
    policy = {
        "rules": [
            {
                "rule_id": "block_tool_low_trust",
                "priority": 10,
                "when": {
                    "action": "infer:run",
                    "signals": {"caller_trust": "low"},
                },
                "then": {
                    "decision": "BLOCK",
                    "rationale_codes": ["TOOL_CALL_LOW_TRUST"],
                },
            }
        ]
    }

    evaluate_request = {
        "action": "infer:run",
        "signals": {"caller_trust": "low"},  # This should trigger the rule based on signals
    }

    result = engine.evaluate_decision(evaluate_request, policy)

    assert result.decision == Decision.BLOCK
    assert result.matched_rule_id == "block_tool_low_trust"
    assert result.rationale_codes == ["TOOL_CALL_LOW_TRUST"]