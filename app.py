"""
Main application file for the PolicyGate API.
"""
from time import perf_counter
from fastapi import FastAPI
from policygate.models import EvaluateRequestV1, EvaluateResponseV1, PolicyRef
import uuid
import policygate.engine as engine
from policygate.policy_loader import load_and_validate_policy  
from policygate.audit import emit_audit_event
from policygate.logging_config import app_logger

POLICY = load_and_validate_policy("policy/policy.yaml", "contracts/policy.schema.json") 

pdp_app = FastAPI(title="PolicyGate API")

@pdp_app.get("/")
async def root():
    return {"message": "Welcome to the PolicyGate API!"}

@pdp_app.get("/health")
async def health_check():    
    return {"status": "healthy"} 

@pdp_app.post("/evaluate")
async def evaluate_policy(request: EvaluateRequestV1) -> EvaluateResponseV1:

    start = perf_counter()

    correlation_id = request.request_id or str(uuid.uuid4())

    decision_result = engine.evaluate_decision(request.model_dump(), POLICY) 

    print(f"Decision: {decision_result}")

    response = EvaluateResponseV1(
        correlation_id=correlation_id,
        decision=decision_result.decision, 
        rationale_codes=decision_result.rationale_codes,  
        policy=PolicyRef(policy_id=POLICY['policy_id'], 
                         policy_version=POLICY["policy_version"],
                         policy_sha256=POLICY["policy_sha256"]),
        obligations=decision_result.obligations,
        matched_rule_id=decision_result.matched_rule_id,
    )

    end = perf_counter()
    elapsed_time = end - start
    app_logger.info(f"Evaluate endpoint took: {elapsed_time} seconds")

    # Emit audit event for the evaluated decision
    emit_audit_event(request, response, latency_ms=(elapsed_time * 1000))

    app_logger.info(f"Request action: {request.action}, resource: {request.resource}, subject: {request.subject}")
    
    return response
