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

