from fastapi import FastAPI
from pydantic import BaseModel
from policygate.models import Decision, EvaluateResponseV1
import policygate_pep.enforcer as pep
from policygate_pep.mappers import build_evaluate_request_for_summarise

# Simple Pydantic model (recommended) to represent the request body for the summarise endpoint.
class SummariseBody(BaseModel):
    document_id: str
    env_name: str
    user_id: str | None = None
    sensitivity: str
    caller_trust: str | None = None


pep_service_app = FastAPI()


@pep_service_app.get("/health")
async def health():
    return {"status": "OK"}  

# Example endpoint to handle the document summarisation requests. 
@pep_service_app.post("/summarise")
async def summarise(payload: SummariseBody): 
    
    # Build the policy evaluation request based on the incoming summarisation request
    # The result is in the required EvaluateRequestV1 format for the PDP /evaluate endpoint.
    summarise_request = build_evaluate_request_for_summarise(
        document_id=payload.document_id,
        env_name=payload.env_name,
        user_id=payload.user_id,
        sensitivity=payload.sensitivity,
        caller_trust=payload.caller_trust
    )
      
    # Call the PEP enforcer with the evaluation request, PDP URL, and handlers for each possible decision.
    result = pep.enforce(
        evaluate_request=summarise_request.model_dump(),
        pdp_url="http://localhost:8000/evaluate",
        on_allow=handle_allow,
        on_degrade=handle_degrade,
        on_block=handle_block,
        on_require_review=handle_require_review,
        timeout_seconds=5.0
    )
    print(f"PEP Enforcer result: {result['summary']}, Decision: {result['decision']}, Message: {result['message']}")
    return result



# Handlers for each possible decision from the PDP.
# the handler names must match the names passed to the enforce function above. 
def handle_allow(evaluate_response: EvaluateResponseV1):

    #Add ALLOW logic here ...

    result = {
        "summary": evaluate_response.rationale_codes[0],
        "decision": Decision(evaluate_response.decision),
        "message": "Processed action Allowed."
    }
    return result

def handle_block(evaluate_response: EvaluateResponseV1):

    # Add BLOCK logic here ...

    result = {
        "summary": evaluate_response.rationale_codes[0],
        "decision": Decision(evaluate_response.decision),
        "message": "Action blocked. Access denied."
    }
    return result

def handle_require_review(evaluate_response: EvaluateResponseV1):

    # Add REQUIRE_REVIEW logic here ...

    result = {
        "summary": evaluate_response.rationale_codes[0],
        "decision": Decision(evaluate_response.decision),
        "message": "Action requires review. Access pending."
    }
    return result

def handle_degrade(evaluate_response: EvaluateResponseV1):

    # Add DEGRADE logic here ...

    result = {
        "summary": evaluate_response.rationale_codes[0],
        "decision": Decision(evaluate_response.decision),
        "obligations": evaluate_response.obligations,
        "message": "Action degraded. Proceeded with limited functionality..."
    }
    return result
