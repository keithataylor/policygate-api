
from pydantic import BaseModel


class SummariseBody(BaseModel):
    document_id: str
    env_name: str
    user_id: str | None = None
    sensitivity: str
    caller_trust: str | None = None

