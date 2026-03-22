
import datetime
import logging
import uuid
from policygate.models import EvaluateRequestV1, EvaluateResponseV1, PolicyRef
from policygate.audit_models import DecisionAuditEvent, EvaluationOutcome

logger = logging.getLogger("policygate.audit")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

def build_decision_audit_event(request: EvaluateRequestV1, response: EvaluateResponseV1) -> DecisionAuditEvent:
    # Build and return a DecisionAuditEvent instance with relevant data 

    audit_event = DecisionAuditEvent(
        event_type="policygate.decision.evaluated",
        event_version="1.0",
        occurred_at=datetime.datetime.now(datetime.UTC),
        environment=request.env.name if request.env else "unknown",
        service_name="request",  # Replace with actual service name
        request_id=request.request_id or str(uuid.uuid4()),
        trace_id=None,
        span_id=None,
        policy=PolicyRef(
            policy_id=response.policy.policy_id,
            policy_version=response.policy.policy_version,
            policy_sha256=response.policy.policy_sha256
        ),  # Include policy reference details
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
            "subject": request.subject,
            "resource": request.resource,
            "env": request.env,
            "signals": request.signals if request.signals else {},
        },
        latency_ms=0,  # Placeholder for actual latency measurement
    )
    return audit_event


def emit_audit_event( request: EvaluateRequestV1, response: EvaluateResponseV1) -> None:
  # Emit the audit event to the desired destination (e.g., log, external system)
  # policygate.decision.evaluated
  # policygate.decision.error
  # policygate.policy.loaded
  # policygate.policy.rejected
  audit_event = build_decision_audit_event(request, response)
  logger.info(f"Emitting audit event: {audit_event.model_dump_json()}")



  