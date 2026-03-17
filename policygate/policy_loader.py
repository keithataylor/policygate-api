import json
from jsonschema import validate, ValidationError
from typing import Any
import yaml

from policygate.exceptions import (
  DuplicateRuleIdError, InvalidPriorityError, InvalidRationaleCodesError,
  ConflictingEqualPriorityOverlapError, RedundantEqualPriorityOverlapError
)

def load_policy_file(policy_path: str) -> dict:
    """
    Load a YAML policy file and return it as a dictionary.
    
    Parameters
    ----------
        policy_path: str
            The file path to the YAML policy file.
    Returns
    -------
        dict
            The policy document loaded as a dictionary.
    Raises
    ------
        ValueError: If the policy file cannot be loaded or parsed.
    """
    with open(policy_path, "r", encoding="utf-8") as f:
        policy = yaml.safe_load(f)
    if not isinstance(policy, dict):
        raise ValueError(f"Policy file '{policy_path}' did not contain a valid YAML dictionary.")
    return policy


def validate_policy_schema(policy: dict, schema_path: str) -> None:
    """
    Validate a policy dictionary against a JSON Schema.
    Parameters
    ----------
        policy: dict 
            The policy document loaded as a dictionary.
        schema_path: str
            The file path to the JSON Schema to validate against.
    Returns
    -------
        None
    
    Raises
    ------
        ValueError: If the policy fails validation against the schema, with details about the validation errors.
    """

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=policy, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Policy validation failed for '{policy}': {e.message}") from e


def validate_policy_semantics(policy: dict[str, Any]) -> None:
    """
    Perform semantic validation checks that sit above JSON Schema validation.

    This function assumes the policy document has already passed structural/schema
    validation. Its role is to catch policy authoring problems that are valid JSON/YAML
    but semantically weak, ambiguous, or unsafe.

    Checks performed
    ----------------
    1. Rule identifiers
       - Every rule must have a non-empty `rule_id`
       - `rule_id` values must be unique

    2. Priority hygiene
       - Every rule must have an integer `priority`
       - Priority must be within the accepted range 0..100

    3. Rationale code hygiene
       - Every rule must define at least one non-empty rationale code
       - Every rationale code must be a non-empty string

    4. Equal-priority overlap detection
       - If two rules have the same priority and their `when` clauses can both match
         the same request, they are considered overlapping
       - If overlapping equal-priority rules produce different decisions, this is
         treated as an error and policy loading fails
       - If overlapping equal-priority rules produce the same decision, this is treated
         as redundant/suspicious and also fails load for now to keep policy behaviour
         explicit and unambiguous

    Notes
    -----
    - This function is intentionally conservative.
    - It does not try to solve full policy satisfiability or reachability.
    - Overlap detection here is based on whether two `when` clauses are mutually
      compatible under exact/subset matching semantics.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If any semantic validation check fails.
    """

    rules = policy.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError("Policy 'rules' must be a list.")

    seen_rule_ids: set[str] = set()

    for index, rule in enumerate(rules):
        rule_id = rule.get("rule_id")
        if not isinstance(rule_id, str) or not rule_id.strip():
            raise ValueError(f"Rule at index {index} has missing or invalid 'rule_id'.")

        if rule_id in seen_rule_ids:
            raise DuplicateRuleIdError(f"Duplicate rule_id found: '{rule_id}'.")
        seen_rule_ids.add(rule_id)

        priority = rule.get("priority")
        if not isinstance(priority, int):
            raise InvalidPriorityError(
                f"Rule '{rule_id}' has invalid priority '{priority}'. "
                "Priority must be an integer."
            )   
        if not (0 <= priority <= 100):
            raise InvalidPriorityError(
                f"Rule '{rule_id}' has invalid priority '{priority}'. "
                "Priority must be between 0 and 100."
            )  
        rationale_codes = rule.get("then", {}).get("rationale_codes", [])
        if not isinstance(rationale_codes, list) or not rationale_codes:
            raise InvalidRationaleCodesError( 
                f"Rule '{rule_id}' must define at least one rationale code."
            )

        if not all(isinstance(code, str) and code.strip() for code in rationale_codes):
            raise InvalidRationaleCodesError(
                f"Rule '{rule_id}' has invalid rationale_codes. "
                "All rationale codes must be non-empty strings."
            )


    for i, left_rule in enumerate(rules):
        for j in range(i + 1, len(rules)):
            right_rule = rules[j]

            if left_rule["priority"] != right_rule["priority"]:
                continue

            left_when = left_rule.get("when", {})
            right_when = right_rule.get("when", {})

            if not _when_clauses_overlap(left_when, right_when):
                continue

            left_id = left_rule["rule_id"]
            right_id = right_rule["rule_id"]
            left_decision = left_rule.get("then", {}).get("decision")
            right_decision = right_rule.get("then", {}).get("decision")

            if left_decision != right_decision:
                raise ConflictingEqualPriorityOverlapError(
                    "Conflicting equal-priority overlapping rules detected: "
                    f"'{left_id}' and '{right_id}' both have priority "
                    f"{left_rule['priority']} but different decisions "
                    f"('{left_decision}' vs '{right_decision}')."
                )

            raise RedundantEqualPriorityOverlapError(
                "Redundant equal-priority overlapping rules detected: "
                f"'{left_id}' and '{right_id}' both have priority "
                f"{left_rule['priority']} and the same decision "
                f"('{left_decision}'). Refine or merge these rules to avoid "
                "ambiguous policy authoring."
            )




def _when_clauses_overlap(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """
    Return True if two `when` clauses are mutually compatible and could both match
    the same request under exact/subset matching semantics.
    """
    if not isinstance(left, dict) or not isinstance(right, dict):
        return False

    shared_keys = set(left.keys()) & set(right.keys())

    for key in shared_keys:
        left_value = left[key]
        right_value = right[key]

        if isinstance(left_value, dict) and isinstance(right_value, dict):
            if not _when_clauses_overlap(left_value, right_value):
                return False
        elif isinstance(left_value, dict) != isinstance(right_value, dict):
            return False
        else:
            if left_value != right_value:
                return False

    return True
    


def load_and_validate_policy(policy_path: str, schema_path: str) -> dict:
    """
    Load a policy from a YAML file, validate it against a JSON Schema, and perform additional semantic checks.
    """
    policy = load_policy_file(policy_path)
    validate_policy_schema(policy, schema_path)
    validate_policy_semantics(policy)

    return policy