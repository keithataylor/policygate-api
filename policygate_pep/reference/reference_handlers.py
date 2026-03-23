"""
Reference handlers for enforcing PDP decisions in the PEP.
This module defines handler functions that the PEP will call based on the decision returned by the PDP.
The handlers contain the logic to enforce the decision, e.g., by allowing the action, blocking it, degrading it, or marking it for review. 
The handlers receive the EvaluateResponseV1 from the PDP, which contains the decision, rationale codes, and any obligations, and can use 
this information to determine how to enforce the decision.
"""

from policygate.models import EvaluateResponseV1


def handle_allow(evaluate_response: EvaluateResponseV1) -> dict:
    """
    Handler logic to enforce the PDP decision ALLOW. 
    """

    #Add ALLOW logic here ...

    result = {
        "outcome": "success",
        "decision": evaluate_response.decision,
        "rationale": evaluate_response.rationale_codes[0],
        "summary": "Processed action Allowed."
    }

    return result


def handle_block(evaluate_response: EvaluateResponseV1) -> dict:
    """ 
    Handler logic to enforce the PDP decision BLOCK. 
    """

    # Add BLOCK logic here ...

    result = {
        "outcome": "denied",
        "decision": evaluate_response.decision,
        "rationale": evaluate_response.rationale_codes[0],
        "summary": "Action blocked. Access denied."
    }
  
    return result


def handle_require_review(evaluate_response: EvaluateResponseV1) -> dict:
    """ 
    Handler logic to enforce the PDP decision REQUIRE_REVIEW. 
    """

    # Add REQUIRE_REVIEW logic here ...

    result = {
        "outcome": "denied",
        "decision": evaluate_response.decision,
        "rationale": evaluate_response.rationale_codes[0],
        "summary": "Action requires review. Access pending."
    }

    return result


def handle_degrade(evaluate_response: EvaluateResponseV1) -> dict:
    """ 
    Handler logic to enforce the PDP decision DEGRADE. 
    """

    # Add DEGRADE logic here ...

    # For the DEGRADE case you would typically check and handle the obligations returned.
    # E.g., 'obligations': [{'type': 'OUTPUT_CAP', 'params': {'max_tokens': 200, 'max_items': None, 'max_bytes': None}} 
    # See customer-defined policy/policy.yaml

    result = {
        "outcome": "success",
        "decision": evaluate_response.decision,
        "rationale": evaluate_response.rationale_codes[0],
        "obligations": evaluate_response.obligations,
        "summary": "Action degraded. Proceeded with limited functionality..."
    }

    return result
