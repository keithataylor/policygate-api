from fastapi import FastAPI
import requests
from pep_demo.mappers import build_evaluate_request_for_summarise
from pep_demo.pep_models import SummariseBody

pep_service_app = FastAPI()

@pep_service_app.get("/health")
async def health():
    return {"status": "OK"}  

@pep_service_app.post("/summarise")
async def summarise(payload: SummariseBody):

    print(f"Received summarise request with payload: {payload}")  # Log the incoming request payload for debugging

    # Build the policy evaluation request based on the incoming summarisation request
    summarise_request = build_evaluate_request_for_summarise(
        document_id=payload.document_id,
        env_name=payload.env_name,
        user_id=payload.user_id,
        sensitivity=payload.sensitivity,
        caller_trust=payload.caller_trust
    )
    
    with requests.Session() as session: 
        evaluate_response = session.post(url="http://localhost:8000/evaluate", json=summarise_request.model_dump())  # Use model_dump() to convert Pydantic model to dict

    return evaluate_response.json()