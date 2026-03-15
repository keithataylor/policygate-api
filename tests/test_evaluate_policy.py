
import requests
from policygate.models import (
    Env,
    Action, 
    Decision,  
    EvaluateRequestV1, 
    EvaluateResponseV1, 
    Resource,
    ResourceSensitivity, 
    Subject
)

test_url = "http://127.0.0.1:8000/evaluate"

def test_evaluate_policy() -> None: 

    request_data = EvaluateRequestV1(
        action=Action.INFER_RUN,
        env=Env(name="dev"),
        resource=Resource(type="document", id="123", sensitivity=ResourceSensitivity.PUBLIC),
        subject=Subject(type="user", id="456"),
        signals=dict({"caller_trust": "low"})
    )
    assert EvaluateRequestV1.model_validate(request_data.model_dump())
    response = requests.post(test_url, json=request_data.model_dump())  
    assert EvaluateResponseV1.model_validate(response.json())
    assert response.status_code == 200
    assert response.json().get("decision") == Decision.ALLOW
    assert response.json().get("rationale_codes")[0] == 'ALLOW_PUBLIC_INFER'

    request_data = EvaluateRequestV1(
        action=Action.INFER_RUN,
        env=Env(name="dev"),
        resource=Resource(type="document", id="123", sensitivity=ResourceSensitivity.RESTRICTED),
        subject=Subject(type="user", id="456"),
        signals=dict({"caller_trust": "low"})
    )
    response = requests.post(test_url, json=request_data.model_dump())
    assert response.status_code == 200
    assert response.json().get("decision") == Decision.DEGRADE    
    assert response.json().get("rationale_codes")[0] == 'SENSITIVE_OUTPUT_LIMIT'
    
    request_data = EvaluateRequestV1(
        action=Action.TOOL_INVOKE,
        env=Env(name="dev"),
        resource=Resource(type="document", id="123", sensitivity=ResourceSensitivity.RESTRICTED),
        subject=Subject(type="user", id="456"),
        signals=dict({"caller_trust": "low"})
    )
    response = requests.post(test_url, json=request_data.model_dump())
    assert response.status_code == 200 
    assert response.json().get("decision") == Decision.BLOCK
    assert response.json().get("rationale_codes")[0] == 'TOOL_CALL_LOW_TRUST'

    request_data = EvaluateRequestV1(
        action=Action.POLICY_ADMIN,
        env=Env(name="prod"),
        resource=Resource(type="document", id="123", sensitivity=ResourceSensitivity.RESTRICTED),
        subject=Subject(type="user", id="456"),
        signals=dict({"caller_trust": "low"})
    )
    response = requests.post(test_url, json=request_data.model_dump())
    assert response.status_code == 200
    assert response.json().get("decision") == Decision.REQUIRE_REVIEW
    assert response.json().get("rationale_codes")[0] == 'ADMIN_CHANGE_REQUIRES_APPROVAL'

    return None



