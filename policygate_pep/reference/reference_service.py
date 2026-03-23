"""
Reference implementation of a Policy Enforcement Point (PEP) service that calls the PDP /evaluate endpoint
to get a decision and routes to the correct handler based on the decision.

This reference service is implemented using FastAPI and includes:
- A /summarise endpoint that simulates a document summarisation ML inference operation, which is protected by the PEP.
- The PEP enforcer function is called within the /summarise endpoint, which sends the evaluation request to the PDP 
  and routes to the appropriate handler based on the decision.
"""
import os
from fastapi import FastAPI
from pydantic import BaseModel
from policygate.models import Action
import policygate_pep.core.enforcer as pep
import policygate_pep.core.mappers as mapper
import policygate_pep.reference.reference_handlers as handlers

# Configuration for PDP URL, using environment variables with defaults for local testing.
POLICYGATE_EVAL_HOST = os.getenv("POLICYGATE_EVAL_HOST", "127.0.0.1")
POLICYGATE_EVAL_PORT = int(os.getenv("POLICYGATE_EVAL_PORT", "8000"))
PDP_EVALUATE_URL = f"http://{POLICYGATE_EVAL_HOST}:{POLICYGATE_EVAL_PORT}/evaluate"

# Simulated business data that would typically be derived from the service's runtime context,
# authenticated user/session, and/or resource metadata/store.
SIMULATED_BUSINESS_CONTEXT = {
    "env_name": "dev",          # system/runtime derived, not normally posted by the end user
    "user_id": "257",           # derived from auth/session/token, not normally posted in body
    "sensitivity": "public",    # derived from document metadata/store, not normally trusted from client body
    "caller_trust": "low",      # derived internally from trust/risk/auth context, not normally user-supplied. Omit signal if not available
    "request_id": "222",        # optional correlation/request ID, usually generated upstream or by service middleware
    "subject_type": "user",     # derived from authenticated caller context
}

# Simple Pydantic model (recommended) to represent the input to the /summarise endpoint of the reference service.
class SummarisePayload(BaseModel):
    document_id: str

# FastAPI app instance for the reference service that will call the PEP enforcer.
pep_app = FastAPI(title="PEP API")

@pep_app.get("/")
async def root():
    return {"message": "Welcome to the PEP API for document summarisation!"}

# Health endpoint to check if the service is running.
@pep_app.get("/health")
async def health():
    return {"status": "OK"}  

# Endpoint to handle a document summarisation ML inference requests. 
# For ML inference, the action in the evaluation request is set to Action.INFER_RUN.
@pep_app.post("/summarise")
async def summarise(payload: SummarisePayload): 
    """ Endpoint to handle document summarisation requests, with PEP enforcement. """
    
    sim = SIMULATED_BUSINESS_CONTEXT

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
        on_allow=handlers.handle_allow,
        on_degrade=handlers.handle_degrade,
        on_block=handlers.handle_block,
        on_require_review=handlers.handle_require_review,
        timeout_seconds=5.0
    )

    return result



