
import requests
from policygate.models import Action, Env, EvaluateRequestV1, EvaluateResponseV1, Resource, Subject


request_data = EvaluateRequestV1(
    action=Action.INFER_RUN,
    env=Env(name="development"),
    resource=Resource(type="dataset", id="123", sensitivity="public"),
    subject=Subject(type="user", id="456"),
    signals=dict({"caller_trust": "low"})
)



def test_evaluate_policy() -> EvaluateResponseV1: 
    assert EvaluateRequestV1.model_validate(request_data.model_dump())
    response = requests.post("http://localhost:8000/evaluate", json=request_data.model_dump())  
    #print(f"Response Json: {response.json()}")
    assert EvaluateResponseV1.model_validate(response.json())

    assert response.status_code == 200
    assert response.json().get("decision") == "ALLOW"
    assert response.json().get("rationale_codes")[0] == 'ALLOW_PUBLIC_INFER'

    request_data.resource.sensitivity = "restricted"
    response = requests.post("http://localhost:8000/evaluate", json=request_data.model_dump())
    #print(f"Response Json: {response.json()}")
    assert response.status_code == 200
    assert response.json().get("decision") == "DEGRADE"    
    assert response.json().get("rationale_codes")[0] == 'SENSITIVE_OUTPUT_LIMIT'

    request_data.resource.sensitivity = "restricted"
    #request_data.resource.type = "tool"
    request_data.action = Action.TOOL_INVOKE
    response = requests.post("http://localhost:8000/evaluate", json=request_data.model_dump())
    #print(f"Response Json: {response.json()}")
    assert response.status_code == 200 
    assert response.json().get("decision") == "BLOCK"
    assert response.json().get("rationale_codes")[0] == 'TOOL_CALL_LOW_TRUST'

    return None



