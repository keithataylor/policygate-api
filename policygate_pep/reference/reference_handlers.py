# Reference handlers for PEP to enforce the PDP decisions. 
# Parameters: evaluate_response (EvaluateResponseV1): The response from the PDP /evaluate endpoint, parsed
#   into the EvaluateResponseV1 model. This contains the decision, rationale codes, and any obligations returned by the PDP. 
# Returns: (customer defined) E.g., dict : dictionary containing the outcome of enforcing the decision, which can be customized based on the service's needs.

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
