import os
from time import perf_counter
from fastapi import FastAPI
from pydantic import BaseModel
from policygate.models import Action, Decision, EvaluateRequestV1, EvaluateResponseV1
import policygate_pep.enforcer as pep
import policygate_pep.mappers as mapper

POLICYGATE_EVAL_HOST = os.getenv("POLICYGATE_EVAL_HOST", "127.0.0.1")
POLICYGATE_EVAL_PORT = int(os.getenv("POLICYGATE_EVAL_PORT", "8000"))
PDP_EVALUATE_URL = f"http://{POLICYGATE_EVAL_HOST}:{POLICYGATE_EVAL_PORT}/evaluate"

# Simulated business data that would typically be derived from the service's runtime context,
# authenticated user/session, and/or resource metadata/store.
SIMULATED_BUSINESS_CONTEXT = {
    "env_name": "dev",          # system/runtime derived, not normally posted by the end user
    "user_id": "789",           # derived from auth/session/token, not normally posted in body
    "sensitivity": "internal",  # derived from document metadata/store, not normally trusted from client body
    "caller_trust": "low",      # derived internally from trust/risk/auth context, not normally user-supplied. Omit signal if not available
    "request_id": "247",        # optional correlation/request ID, usually generated upstream or by service middleware
    "subject_type": "user",     # derived from authenticated caller context
}

# Example simple Pydantic model (recommended) to represent the input to the /summarise endpoint of the example service.
class SummarisePayload(BaseModel):
    document_id: str


# FastAPI app instance for the example service that will call the PEP enforcer.
pep_service_app = FastAPI()

# Example health endpoint to check if the service is running.
@pep_service_app.get("/health")
async def health():
    return {"status": "OK"}  

# Example endpoint to handle a document summarisation ML inference requests. 
# For ML inference, the action in the evaluation request is set to Action.INFER_RUN.
@pep_service_app.post("/summarise")
async def summarise(payload: SummarisePayload): 
    """ Example endpoint to handle document summarisation requests, with PEP enforcement. """
    
    sim = SIMULATED_BUSINESS_CONTEXT

    print(f"Sim: {sim}")

    # Use the mapper helper function to build the policy evaluation 
    # EvaluateRequestV1 request object required by the PDP /evaluate endpoint.
    eval_request = mapper.build_evaluate_request(
        action=Action.INFER_RUN,                    # fixed by this endpoint: /summarise is treated as an inference operation
        resource_id=payload.document_id,            # business input posted by caller
        resource_type="document",                   # fixed by this endpoint: it summarises documents
        env_name=sim["env_name"],                   # system/runtime derived, not normally posted by the end user       
        resource_sensitivity=sim["sensitivity"],    # derived from document metadata/store, not normally trusted from client body
        subject_type=sim["subject_type"],           # derived from authenticated caller context             
        subject_id=sim["user_id"],                  # derived from auth/session/token, not normally posted in body
        request_id=sim["request_id"],               # optional correlation/request ID, usually generated upstream or by service middleware       
        signals={
            "caller_trust": sim["caller_trust"],    # derived internally from trust/risk/auth context, not normally user-supplied. Omit signal if not available   
        } if sim["caller_trust"] else {},             
    )
      
    # Call the PEP enforcer with the evaluation request, PDP URL, and handlers for each possible decision.
    result = pep.enforce(
        evaluate_request=eval_request.model_dump(),
        pdp_url=PDP_EVALUATE_URL,
        on_allow=handle_allow,
        on_degrade=handle_degrade,
        on_block=handle_block,
        on_require_review=handle_require_review,
        timeout_seconds=5.0
    )

    return result



# Example handlers for PEP to enforce the PDP decisions. 
# Parameters: evaluate_response (EvaluateResponseV1): The response from the PDP /evaluate endpoint, parsed
#   into the EvaluateResponseV1 model. This contains the decision, rationale codes, and any obligations returned by the PDP. 
# Returns: (customer defined) E.g., dict : dictionary containing the outcome of enforcing the decision, which can be customized based on the service's needs.

def handle_allow(evaluate_response: EvaluateResponseV1) -> dict:
    """
    Example handler logic to enforce the PDP decision ALLOW. 
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
    Example handler logic to enforce the PDP decision BLOCK. 
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
    Example handler logic to enforce the PDP decision REQUIRE_REVIEW. 
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
    Example handler logic to enforce the PDP decision DEGRADE. 
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
