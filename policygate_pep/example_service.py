import os
from fastapi import FastAPI
from pydantic import BaseModel
from policygate.models import Action, Decision, EvaluateRequestV1, EvaluateResponseV1
import policygate_pep.enforcer as enforcer
import policygate_pep.mappers as mapper

POLICYGATE_EVAL_HOST = os.getenv("POLICYGATE_EVAL_HOST", "localhost")
POLICYGATE_EVAL_PORT = int(os.getenv("POLICYGATE_EVAL_PORT", "8000"))
PDP_EVALUATE_URL = f"http://{POLICYGATE_EVAL_HOST}:{POLICYGATE_EVAL_PORT}/evaluate"


# Simple Pydantic model (recommended) to represent the request body for the summarise endpoint.
class SummariseBody(BaseModel):
    document_id: str
    env_name: str
    user_id: str | None = None
    sensitivity: str
    caller_trust: str | None = None

# FastAPI app instance for the example service that will call the PEP enforcer.
pep_service_app = FastAPI()

# Example health endpoint to check if the service is running.
@pep_service_app.get("/health")
async def health():
    return {"status": "OK"}  

# Example endpoint to handle a document summarisation ML inference requests. 
# For ML inference, the action in the evaluation request is set to Action.INFER_RUN.
@pep_service_app.post("/summarise")
async def summarise(payload: SummariseBody): 
    
    # Use the mapper helper function to build the policy evaluation request based on 
    # the incoming summarisation request. The result is in the required EvaluateRequestV1 
    # format for the PDP /evaluate endpoint.
    summarise_request = mapper.build_evaluate_request(
        action=Action.INFER_RUN,
        env_name=payload.env_name,
        resource_type="document",
        resource_sensitivity=payload.sensitivity,
        resource_id=payload.document_id,
        subject_id=payload.user_id,
        request_id=None,
        signals={"caller_trust": payload.caller_trust} if payload.caller_trust else {}
    )
      
    # Call the PEP enforcer with the evaluation request, PDP URL, and handlers for each possible decision.
    result = enforcer.enforce(
        evaluate_request=summarise_request.model_dump(),
        pdp_url=PDP_EVALUATE_URL,
        on_allow=handle_allow,
        on_degrade=handle_degrade,
        on_block=handle_block,
        on_require_review=handle_require_review,
        timeout_seconds=5.0
    )
    #print(f"PEP Enforcer result: {result['summary']}, Decision: {result['decision']}, Message: {result['message']}")
    return result



# Handlers for each possible decision from the PDP.
# the handler names must match the names passed to the enforce function above. 
def handle_allow(evaluate_response: EvaluateResponseV1):

    #Add ALLOW logic here ...

    result = {
        "outcome": "success",
        "decision": Decision(evaluate_response.decision),
        "rationale": evaluate_response.rationale_codes[0],
        "summary": "Processed action Allowed."
    }
    return result

def handle_block(evaluate_response: EvaluateResponseV1):

    # Add BLOCK logic here ...

    result = {
        "outcome": "denied",
        "decision": Decision(evaluate_response.decision),
        "rationale": evaluate_response.rationale_codes[0],
        "summary": "Action blocked. Access denied."
    }
    return result

def handle_require_review(evaluate_response: EvaluateResponseV1):

    # Add REQUIRE_REVIEW logic here ...

    result = {
        "outcome": "denied",
        "decision": Decision(evaluate_response.decision),
        "rationale": evaluate_response.rationale_codes[0],
        "summary": "Action requires review. Access pending."
    }
    return result

def handle_degrade(evaluate_response: EvaluateResponseV1):

    # Add DEGRADE logic here ...
    # For this case you would typically check and handle the obligations returned.
    # E.g., 'obligations': [{'type': 'OUTPUT_CAP', 'params': {'max_tokens': 200, 'max_items': None, 'max_bytes': None}} 
    # See customer-defined policy/policy.yaml

    result = {
        "outcome": "success",
        "decision": Decision(evaluate_response.decision),
        "rationale": evaluate_response.rationale_codes[0],
        "obligations": evaluate_response.obligations,
        "summary": "Action degraded. Proceeded with limited functionality..."
    }
    return result
