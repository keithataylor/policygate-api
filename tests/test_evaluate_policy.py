
import requests
from policygate.models import Action, Env, EvaluateRequestV1, EvaluateResponseV1, Resource, Subject


request_data = EvaluateRequestV1(
    action=Action.INFER_RUN,
    env=Env(name="development"),
    resource=Resource(type="dataset", id="123", sensitivity="public"),
    subject=Subject(type="user", id="456"),
    signals=dict({"caller": "low"})
)



def test_evaluate_policy() -> EvaluateResponseV1:
    
    assert EvaluateRequestV1.model_validate(request_data.model_dump())

    response = requests.post("http://localhost:8000/evaluate", json=request_data.model_dump())  

    print(f"Response Json: {response.json()}")
    
    assert EvaluateResponseV1.model_validate(response.json())
    
    return None


