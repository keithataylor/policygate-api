# PolicyGate Implementation Tracker

## Current focus
- [ ] Implement actual reference-service enforcement for `DEGRADE` / `OUTPUT_CAP`
- [ ] Dockerise PolicyGate and prove the local container run path
- [ ] Tighten reference integration code and docs around the customer-owned PEP/service pattern

## Positioning guardrails
PolicyGate is being built as a **deployable inference policy gate** for internal AI services and gateways.

This tracker should prioritise:
- deterministic policy evaluation
- audit-ready decision evidence
- clean customer-side integration
- AWS-oriented deployability
- concrete reference use cases

This tracker should avoid drift into:
- broad MLOps platform features
- policy authoring UI
- model hosting
- general workflow orchestration
- abstract “AI governance platform” sprawl

## Milestones

### M0 — Contracts & policy validation
- [x] `contracts/evaluate_request.schema.json`
- [x] `contracts/evaluate_response.schema.json`
- [x] `contracts/policy.schema.json`
- [x] `contracts/audit_event.schema.json`
- [x] `policy/policy.yaml`
- [x] `policy/README.md`
- [x] `policy/SCHEMA.md`
- [x] `tools/generate_policy_schema_md.py`
- [x] Implement `policygate/policy_loader.py` (load YAML, validate schema)
- [x] Add unit tests for policy validation (valid + invalid cases)
- [x] Add semantic validation phase for:
  - duplicate `rule_id`
  - invalid priority
  - invalid rationale codes
  - conflicting equal-priority overlaps
  - redundant equal-priority overlaps

### M1 — Decision engine (deterministic PDP core)
- [x] Implement `policygate/engine.py`
- [x] Higher priority matching rule wins
- [x] No matching rule falls back to default decision/rationale
- [x] Reject invalid equal-priority overlap at semantic validation stage
- [ ] Add golden tests: request + policy -> exact decision response
- [ ] Add a compact scenario matrix for representative inference-gate cases
- [ ] Confirm policy fingerprint / identity is surfaced cleanly to downstream audit/event building

### M2 — API wiring (stable PDP boundary)
- [x] Implement FastAPI `POST /evaluate`
- [x] Implement `GET /health`
- [x] Load policy once at startup
- [x] Implement runtime Pydantic request/response models in `policygate/models.py`
- [ ] Add `GET /version` or equivalent lightweight policy/app identity endpoint if useful
- [ ] Ensure `/evaluate` response shape remains narrow and decision-focused

### M3 — Reference integration pattern
- [x] Rename demo-style files toward reference naming
- [x] Implement `policygate_pep/core/` and `policygate_pep/reference/` split
- [x] Finalise `policygate_pep/reference/reference_service.py`
- [x] Finalise `policygate_pep/reference/reference_client.py`
- [x] Keep customer/business payloads business-shaped
- [x] Keep mapping from business request -> `EvaluateRequestV1` inside the reference service
- [x] Keep policy-relevant context derivation honest and explicit
- [x] Document the reference service as customer-side integration code, not core PDP code

### M4 — Reference enforcement behaviour
- [ ] Implement actual reference-service enforcement for:
  - `ALLOW`
  - `BLOCK`
  - `REQUIRE_REVIEW`
  - `DEGRADE`
- [ ] Implement `OUTPUT_CAP` handling with fail-closed behaviour where appropriate
- [ ] Add end-to-end reference tests covering the full decision/enforcement path
- [ ] Ensure reference handlers return business responses directly and consistently

### M5 — Audit events and evidence quality
- [x] Implement `policygate/audit_models.py`
- [x] Implement `policygate/audit.py`
- [x] Define frozen structured audit event models
- [x] Emit one structured decision audit event per completed PDP evaluation
- [ ] Emit policy load / policy rejection audit events
- [x] Include in decision audit event:
  - occurrence timestamp
  - request correlation ID
  - decision
  - matched rule ID
  - rationale codes
  - policy identity
  - policy fingerprint
  - minimal decision-relevant context
- [ ] Validate emitted audit events against `contracts/audit_event.schema.json`
- [x] Add unit tests for audit event construction, request ID handling, and logger emission
- [ ] Keep PolicyGate inputs and audit records limited to policy-relevant, audit-safe attributes

### M6 — Concrete policy packs / use-case examples
- [ ] Replace overly generic sample policy examples with concrete reference scenarios
- [ ] Add at least one strong internal AI service example such as:
  - document summarisation gate
  - sensitive-document review gate
  - human-review-required gate
- [ ] Make example policies visibly relevant to real inference-control use cases

### M7 — Docker + CI gate
- [ ] Dockerfile builds
- [ ] Docker Compose or equivalent local run path is clear
- [ ] GitHub Actions: `pytest` + `ruff` + `mypy`/`pyright` + `docker build`
- [ ] Ensure reference service can be exercised locally alongside PolicyGate

### M8 — AWS implementation-first deploy path
- [ ] ECS / Fargate / IAM / ALB deployment path
- [ ] CloudWatch logs visible
- [ ] Clear environment variable configuration for PDP host/port and service integration
- [ ] Document the initial recommended deployment pattern as central PDP in customer AWS environment
- [ ] Later: evaluate sidecar/service-adjacent deployment pattern where latency or topology justifies it

## Deferred / later only
- [ ] Kubernetes deployment pattern
- [ ] Fleet/policy management control plane
- [ ] Rich simulation UI
- [ ] Policy authoring UI
- [ ] Multi-tenant SaaS control plane
- [ ] Broader governance workflow features

## Current priority order
1. Docker + CI
2. Reference enforcement completeness
3. Concrete reference policy/use-case examples
4. Policy load/rejection audit events and audit schema validation
5. AWS deployment path

## Definition of near-term success
PolicyGate should be able to demonstrate, end to end:

- a customer-owned reference service receives a business request
- the service derives policy-relevant facts
- the service calls `POST /evaluate`
- PolicyGate returns a deterministic decision
- the service enforces that decision
- a structured audit event is emitted showing what was decided, why, and under which policy artifact

That is the current target shape.