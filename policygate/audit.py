

from policygate.models import Decision, EvaluateRequestV1, EvaluateResponseV1
from policygate.audit_models import DecisionAuditEvent


def build_decision_audit_event(request: EvaluateRequestV1, response: EvaluateResponseV1) -> DecisionAuditEvent:
    # Build and return a DecisionAuditEvent instance with relevant data
    pass

def emit_audit_event() -> None:
  # Emit the audit event to the desired destination (e.g., log, external system)
  # policygate.decision.evaluated
  # policygate.decision.error
  # policygate.policy.loaded
  # policygate.policy.rejected

    pass