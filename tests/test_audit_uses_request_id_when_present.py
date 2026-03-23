import uuid
import requests
import policygate.audit as audit
from policygate.audit_models import DecisionAuditEvent
from policygate.config import SERVICE_NAME
from policygate.models import (
    Action, Env, EvaluateRequestV1, 
    Resource, ResourceSensitivity, 
    Subject, EvaluateResponseV1
)


test_url = "http://127.0.0.1:8000/evaluate"

def test_build_decision_audit_event_with_request_id():
    # This test would create a sample EvaluateRequestV1 and EvaluateResponseV1, call build_decision_audit_event, 
    # and assert that the returned DecisionAuditEvent has the expected structure and values.
    request_data = EvaluateRequestV1(
        request_id=str(uuid.uuid4()),
        action=Action.INFER_RUN,
        env=Env(name="dev"),
        resource=Resource(type="document", id="123", sensitivity=ResourceSensitivity.PUBLIC),
        subject=Subject(type="user", id="456"),
        signals=dict({"caller_trust": "low"})
    )
    assert EvaluateRequestV1.model_validate(request_data.model_dump())
    response = requests.post(test_url, json=request_data.model_dump())  
    response_data =  EvaluateResponseV1.model_validate(response.json())

    audit_event = audit.build_decision_audit_event(request_data, response_data, 0.5)

    audit_event =DecisionAuditEvent.model_validate(audit_event.model_dump())

    assert audit_event.event_type == "policygate.decision.evaluated"
    assert audit_event.service_name == SERVICE_NAME
    assert audit_event.environment == request_data.env.name
    assert audit_event.evaluation.action == request_data.action
    assert audit_event.evaluation.resource_type == request_data.resource.type
    assert audit_event.evaluation.decision == response_data.decision
    assert audit_event.evaluation.matched_rule_id == response_data.matched_rule_id
    assert audit_event.decision_context == {
        "resource": request_data.resource.model_dump(),
        "env": request_data.env.model_dump(),
        "signals": request_data.signals,
    }
    assert "action" not in audit_event.decision_context
    assert audit_event.latency_ms == 0.5
    assert audit_event.policy.policy_id == response_data.policy.policy_id
    assert audit_event.policy.policy_version == response_data.policy.policy_version
    assert audit_event.policy.policy_sha256 == response_data.policy.policy_sha256
    if request_data.request_id is not None:
      assert audit_event.request_id == request_data.request_id
   
    

