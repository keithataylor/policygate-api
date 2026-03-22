from pydantic import BaseModel, ConfigDict
import datetime
from typing import Any, Literal
from policygate.models import PolicyRef


class AuditEventBase(BaseModel):
    """ 
    Base model for all audit events emitted by the system. 
    """
    model_config = ConfigDict(extra="forbid")
    event_type: str
    event_version: str = "1.0"
    occurred_at: datetime.datetime
    environment: str
    service_name: str
    request_id: str | None = None
    trace_id: str | None = None
    span_id: str | None = None


class EvaluationOutcome(BaseModel):
    """
    Details about the outcome of a policy evaluation, for audit events.
    """
    action: str
    resource_type: str
    decision: str
    matched_rule_id: str | None = None
    default_applied: bool
    rationale_codes: list[str]


class DecisionAuditEvent(AuditEventBase):
  """
  Audit event emitted when a policy evaluation decision is made.
  """
  model_config = ConfigDict(extra="forbid")
  event_type: Literal["policygate.decision.evaluated"]
  policy: PolicyRef
  tenant_id: str | None = None
  caller_id: str | None = None
  evaluation: EvaluationOutcome
  decision_context: dict[str, Any]
  latency_ms: int | None = None
  