"""
Audit event functions for PolicyGate.
"""

import datetime, uuid
from policygate.models import EvaluateRequestV1, EvaluateResponseV1, PolicyRef
from policygate.audit_models import DecisionAuditEvent, EvaluationOutcome
from policygate.config import SERVICE_NAME
from policygate.logging_config import audit_logger


def build_decision_audit_event(request: EvaluateRequestV1, response: EvaluateResponseV1, latency_ms: float) -> DecisionAuditEvent:
    """
    Builds a DecisionAuditEvent based on the evaluation request and response.
    Args:
        request (EvaluateRequestV1): The original evaluation request.
        response (EvaluateResponseV1): The response from the policy evaluation.
        latency_ms (float): The latency of the evaluation in milliseconds.
    Returns:
        DecisionAuditEvent: The constructed audit event with all relevant details.
    """
    audit_event = DecisionAuditEvent(
        event_type="policygate.decision.evaluated",
        event_version="1.0",
        occurred_at=datetime.datetime.now(datetime.timezone.utc),
        environment=request.env.name if request.env else "unknown",
        service_name=SERVICE_NAME,
        request_id=request.request_id or str(uuid.uuid4()),
        trace_id=None,
        span_id=None,
        policy=PolicyRef(
            policy_id=response.policy.policy_id,
            policy_version=response.policy.policy_version,
            policy_sha256=response.policy.policy_sha256
        ), 
        tenant_id=None,
        caller_id=None,
        evaluation=EvaluationOutcome(
            action=request.action,  
            resource_type=request.resource.type,
            decision=response.decision, 
            matched_rule_id=response.matched_rule_id,
            default_applied="POLICY_DEFAULT_DENY" in response.rationale_codes,
            rationale_codes=response.rationale_codes,
        ),
        decision_context={
            "resource": request.resource.model_dump() if request.resource else {},
            "env": request.env.model_dump() if request.env else {},
            "signals": request.signals,
        },
        latency_ms=latency_ms,  # Placeholder for actual latency measurement
    )
    return audit_event


def emit_audit_event( request: EvaluateRequestV1, response: EvaluateResponseV1, latency_ms: float) -> None:
  """
  Emits an audit event for a policy evaluation decision.
  Args:      
    request (EvaluateRequestV1): The original evaluation request.
    response (EvaluateResponseV1): The response from the policy evaluation.
    latency_ms (float): The latency of the evaluation in milliseconds.
  """
  audit_event = build_decision_audit_event(request, response, latency_ms)
  audit_logger.info(audit_event.model_dump_json())
 