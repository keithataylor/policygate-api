from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, ConfigDict, field_validator


# ----- Enums (allowed values) -----

class Action(str, Enum):
    INFER_RUN = "infer:run"
    DATA_READ = "data:read"
    DATA_WRITE = "data:write"
    TOOL_INVOKE = "tool:invoke"
    POLICY_ADMIN = "policy:admin"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"
    DEGRADE = "DEGRADE"

class ResourceSensitivity(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"

# ----- Request models -----

class Env(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., min_length=1, max_length=64)


class Resource(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str = Field(..., min_length=1, max_length=64)
    id: Optional[str] = Field(None, min_length=1, max_length=256)
    sensitivity: ResourceSensitivity


class Subject(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Optional[str] = Field(None, min_length=1, max_length=32)
    id: Optional[str] = Field(None, min_length=1, max_length=256)


SignalValue = Union[str, int, float, bool, None]


class EvaluateRequestV1(BaseModel):
    """
    Runtime request model for POST /evaluate.
    (Matches the intent of contracts/evaluate_request.schema.json.)
    """
    model_config = ConfigDict(extra="forbid")

    request_id: Optional[str] = Field(None, min_length=1, max_length=128)
    timestamp: Optional[str] = Field(None, description="ISO-8601 date-time string (optional)")
    action: Action
    env: Env
    resource: Resource
    subject: Optional[Subject] = None
    signals: Dict[str, SignalValue] = Field(default_factory=dict, max_length=50)

    @field_validator("signals")
    @classmethod
    def validate_signal_keys(cls, v: Dict[str, SignalValue]) -> Dict[str, SignalValue]:
        # Enforce the same key discipline as the JSON schema:
        # ^[a-z][a-z0-9_]{0,40}$
        import re
        pat = re.compile(r"^[a-z][a-z0-9_]{0,40}$")
        for k in v.keys():
            if not pat.match(k):
                raise ValueError(f"Invalid signals key '{k}'. Must match ^[a-z][a-z0-9_]{{0,40}}$")
        return v


# ----- Response models -----

class OutputCapParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_tokens: Optional[int] = Field(None, ge=1, le=100000)
    max_items: Optional[int] = Field(None, ge=1, le=1000000)
    max_bytes: Optional[int] = Field(None, ge=1, le=100000000)

    @field_validator("max_bytes", "max_items", "max_tokens")
    @classmethod
    def _noop(cls, v):
        return v

    @field_validator("*")
    @classmethod
    def at_least_one(cls, v, info):  # pydantic v2 runs per-field; keep separate check below
        return v

    def model_post_init(self, __context: Any) -> None:
        if self.max_tokens is None and self.max_items is None and self.max_bytes is None:
            raise ValueError("OUTPUT_CAP.params must set at least one of max_tokens/max_items/max_bytes")


class Obligation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str = Field(..., pattern="^OUTPUT_CAP$")
    params: OutputCapParams


class PolicyRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    policy_id: str = Field(..., min_length=1, max_length=128)
    policy_version: str = Field(..., min_length=1, max_length=128)
    policy_sha256: str = Field(..., min_length=64, max_length=64, pattern="^[a-fA-F0-9]{64}$")


class EvaluateResponseV1(BaseModel):
    """
    Runtime response model for POST /evaluate.
    (Matches the intent of contracts/evaluate_response.schema.json.)
    """
    model_config = ConfigDict(extra="forbid")

    correlation_id: str = Field(..., min_length=1, max_length=128)
    decision: Decision
    rationale_codes: List[str] = Field(..., min_length=1)
    obligations: Optional[List[Obligation]] = None
    policy: PolicyRef
    matched_rule_id: Optional[str] = Field(None, min_length=1, max_length=128)

    def model_post_init(self, __context: Any) -> None:
        # Enforce: obligations required for DEGRADE, absent otherwise.
        if self.decision == Decision.DEGRADE:
            if not self.obligations:
                raise ValueError("obligations are required when decision=DEGRADE")
        else:
            if self.obligations:
                raise ValueError("obligations must be omitted unless decision=DEGRADE")
            

