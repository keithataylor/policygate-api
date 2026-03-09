from datetime import datetime
import uuid
from policygate.models import Action, Env, EvaluateRequestV1, Resource, Subject

def build_evaluate_request( 
        *,
        action: Action,
        env_name: str,
        resource_type: str,
        resource_sensitivity: str,
        resource_id: str | None = None,
        subject_type: str | None = None,
        subject_id: str | None = None,
        request_id: str | None = None,
        signals: dict[str, object] | None = None
    ) -> EvaluateRequestV1:
    
    eval_request = EvaluateRequestV1(
        request_id=request_id or str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),      
        action=action,
        env=Env(name=env_name),
        resource=Resource(type=resource_type, id=resource_id, sensitivity=resource_sensitivity),
        subject=Subject(type=subject_type, id=subject_id) if subject_type or subject_id else None,
        signals=signals or {}
    )
    return eval_request


def build_evaluate_request_for_summarise(
        *,
        document_id: str,
        env_name: str,
        user_id: str | None,
        sensitivity: str,
        request_id: str | None = None,
        caller_trust: str | None = None,
    ) -> EvaluateRequestV1:

    eval_request = build_evaluate_request(
        action=Action.INFER_RUN,
        env_name=env_name,
        resource_type="document",
        resource_sensitivity=sensitivity,
        resource_id=document_id,
        subject_type="user" if user_id else None,
        subject_id=user_id,
        request_id=request_id,
        signals={"caller_trust": caller_trust} if caller_trust else {}
    )
    return eval_request