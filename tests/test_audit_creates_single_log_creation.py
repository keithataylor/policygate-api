import requests
import policygate.audit as audit
from policygate.audit_models import DecisionAuditEvent
from policygate.config import SERVICE_NAME
from policygate.models import (
    Action, Env, EvaluateRequestV1, 
    Resource, ResourceSensitivity, 
    Subject, EvaluateResponseV1
)
from unittest.mock import patch


test_url = "http://127.0.0.1:8000/evaluate"

def test_build_decision_audit_event_single_log_creation():
    # This test would create a sample EvaluateRequestV1 and EvaluateResponseV1, call build_decision_audit_event, 
    # and assert that the returned DecisionAuditEvent has the expected structure and values.
    request_data = EvaluateRequestV1(
        request_id=None,  # Simulate missing request_id to test auto-generation in audit event`,
        action=Action.INFER_RUN,
        env=Env(name="dev"),
        resource=Resource(type="document", id="123", sensitivity=ResourceSensitivity.PUBLIC),
        subject=Subject(type="user", id="456"),
        signals=dict({"caller_trust": "low"})
    )
    assert EvaluateRequestV1.model_validate(request_data.model_dump())
    response = requests.post(test_url, json=request_data.model_dump())  
    response_data = EvaluateResponseV1.model_validate(response.json())

    audit_event = audit.build_decision_audit_event(request_data, response_data, 0.5)

    audit_event = DecisionAuditEvent.model_validate(audit_event.model_dump())

    assert len(audit.audit_logger.handlers)  == 1

    with patch.object(audit.audit_logger, "info") as mock_info:
        audit.emit_audit_event(request_data, response_data, 0.5)
        mock_info.assert_called_once()
        #assert mock_info.call_args[0][0] == audit_event.model_dump_json()
        logged_message = mock_info.call_args[0][0]
        assert logged_message.startswith("{")
        assert '"event_type":"policygate.decision.evaluated"' in logged_message
        assert f'"service_name":"{SERVICE_NAME}"' in logged_message

    

