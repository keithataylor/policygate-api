from time import perf_counter

from fastapi import FastAPI
from policygate.models import EvaluateRequestV1, EvaluateResponseV1, PolicyRef
import uuid
import policygate.engine as engine
from policygate.policy_loader import load_and_validate_policy  

POLICY = load_and_validate_policy("policy/policy.yaml", "contracts/policy.schema.json") 
    
app = FastAPI(title="PolicyGate API")

@app.get("/")
async def root():
    return {"message": "Welcome to the PolicyGat API!"}

@app.get("/health")
async def health_check():    
    return {"status": "healthy"} 

@app.post("/evaluate")
async def evaluate_policy(request: EvaluateRequestV1) -> EvaluateResponseV1:

    start = perf_counter()

    correlation_id = request.request_id or str(uuid.uuid4())

    decision_result = engine.evaluate_decision(request.model_dump(), POLICY)  # Placeholder for actual policy evaluation logic

    print(f"Decision: {decision_result}")

    response = EvaluateResponseV1(
        correlation_id=correlation_id,
        decision=decision_result.decision, 
        rationale_codes=decision_result.rationale_codes,  
        policy=PolicyRef(policy_id=POLICY['policy_id'], policy_version=POLICY["policy_version"]),
        obligations=decision_result.obligations,
        matched_rule_id=decision_result.matched_rule_id,
    )

    end = perf_counter()
    print(f"Evaluate endpoint took: {end - start:.2f} seconds")

    # Placeholder for policy evaluation logic
    print(f"Request action: {request.action}, resource: {request.resource}, subject: {request.subject}")
    return response
