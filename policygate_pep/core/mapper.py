"""
Mappers to convert incoming request data into the format expected by the PDP /evaluate endpoint.
"""

import uuid
from datetime import datetime
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
    ''' Helper function to build the EvaluateRequestV1 for the PDP /evaluate endpoint
    based on the incoming request data. 
    Args:
        action (Action): The action being performed, e.g. Action.INFER_RUN.
        env_name (str): The name of the environment, e.g. "prod".
        resource_type (str): The type of resource, e.g. "document".
        resource_sensitivity (str): The sensitivity of the resource, e.g. "restricted".
        resource_id (str | None): The unique identifier of the resource, e.g. document ID (optional).
        subject_type (str | None): The type of subject, e.g. "user" (optional).
        subject_id (str | None): The unique identifier of the subject, e.g. user ID (optional).
        request_id (str | None): A unique identifier for the request, e.g. a UUID (optional).
        signals (dict[str, object] | None): Additional contextual signals to include in the evaluation request (optional).
    Returns:
        EvaluateRequestV1: The constructed evaluation request object.
    '''
    
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

