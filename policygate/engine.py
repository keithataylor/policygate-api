
"""
Policy evaluation engine for PolicyGate.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from policygate.logging_config import app_logger


@dataclass(frozen=True)
class DecisionResult:
    decision: str
    rationale_codes: List[str]
    obligations: Optional[List[Dict[str, Any]]] = None
    matched_rule_id: Optional[str] = None


def _match_when(request: Dict[str, Any], when: Dict[str, Any]) -> bool:
    """
    Exact-match rule:
    - Only keys present in `when` are checked.
    - Nested dicts are matched recursively.
    - For signals: key/value exact equality.
    """
    for key, expected in when.items():
        actual = request.get(key)

        if isinstance(expected, dict):
            if not isinstance(actual, dict):
                return False
            if not _match_when(actual, expected):
                return False
        else:
            if actual != expected:
                return False

    return True


def evaluate_decision(request_dict: Dict[str, Any], policy: Dict[str, Any]) -> DecisionResult:
    """
    Deterministic evaluation:
    - Find all matching rules.
    - Pick highest priority.
    - Tie-breaker: first in file order.
    - If none match: use policy['default'].
    """
    rules = policy["rules"]
    matches: List[Dict[str, Any]] = []

    for rule in rules:
        when = rule["when"]
        if _match_when(request_dict, when):
            matches.append(rule)

    if matches:
        # highest priority wins; stable sort keeps file-order for ties
        matches.sort(key=lambda r: r["priority"], reverse=True)
        chosen = matches[0]
        then = chosen["then"]
        return DecisionResult(
            decision=then["decision"],
            rationale_codes=then["rationale_codes"],
            obligations=then.get("obligations"),
            matched_rule_id=chosen["rule_id"],
        )

    app_logger.info(f"Policy Default Applied: {policy}")
    default = policy["default"]
    return DecisionResult(
        decision=default["decision"],
        rationale_codes=default["rationale_codes"],
        obligations=None,
        matched_rule_id=None,
    )