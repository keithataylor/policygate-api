# PolicyGate Implementation Tracker

## Current focus
- [ ] Tighten reference integration code and docs around the customer-owned PEP/service pattern
- [ ] Implement actual reference-service enforcement for `DEGRADE` / `OUTPUT_CAP`
- [ ] Add CI quality gate around tests, linting, and Docker build

## Positioning guardrails
PolicyGate is being built as a **deployable inference policy gate** for internal AI services and gateways.

This tracker should prioritise:
- deterministic policy evaluation
- audit-ready decision evidence
- clean customer-side integration
- AWS-oriented deployability
- concrete reference use cases
- proof of a standalone audited PDP service in a credible customer-environment AWS shape

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
- [x] Confirm policy fingerprint / identity is surfaced cleanly to downstream audit/event building

### M2 — API wiring (stable PDP boundary)
- [x] Implement FastAPI `POST /evaluate`
- [x] Implement `GET /health`
- [x] Load policy once at startup
- [x] Implement runtime Pydantic request/response models in `policygate/models.py`
- [ ] Add `GET /version` or equivalent lightweight policy/app identity endpoint if useful
- [x] Ensure `/evaluate` response shape remains narrow and decision-focused

### M3 — Reference integration pattern
- [x] Rename demo-style files toward reference naming
- [ ] Finalise `policygate_pep/reference_service.py`
- [ ] Finalise `policygate_pep/reference_client.py`
- [ ] Keep customer/business payloads business-shaped
- [ ] Keep mapping from business request -> `EvaluateRequestV1` inside the reference service
- [ ] Keep policy-relevant context derivation honest and explicit
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
- [ ] Add tests proving sensitive/raw business payload is not emitted into audit records

### M6 — Concrete policy packs / use-case examples
- [ ] Replace overly generic sample policy examples with concrete reference scenarios
- [ ] Add at least one strong internal AI service example such as:
  - document summarisation gate
  - sensitive-document review gate
  - human-review-required gate
- [ ] Make example policies visibly relevant to real inference-control use cases

### M7 — Docker + CI gate
- [x] Dockerfile builds
- [x] Local container run path is proven
- [x] Ensure reference service can be exercised locally alongside containerised PolicyGate
- [ ] Docker Compose or equivalent local run path is clear
- [ ] GitHub Actions: `pytest` + `ruff` + `mypy`/`pyright` + `docker build`

### M8 — AWS implementation-first deploy path
- [x] ECR image push path
- [x] ECS / Fargate / IAM / ALB deployment path
- [x] CloudWatch logs visible for both operational and audit output
- [ ] Clear environment variable configuration for PDP host/port and service integration
- [x] Prove the preferred AWS shape: standalone PDP service, customer-side reference caller flow, controlled ALB-backed access
- [ ] Document the initial recommended deployment pattern as central PDP in customer AWS environment
- [ ] Later: evaluate service-adjacent deployment pattern where latency or topology justifies it

## Deferred / later only
- [ ] Kubernetes deployment pattern
- [ ] Fleet/policy management control plane
- [ ] Rich simulation UI
- [ ] Policy authoring UI
- [ ] Multi-tenant SaaS control plane
- [ ] Broader governance workflow features

## Current priority order
1. Reference enforcement completeness
2. Concrete reference policy/use-case examples
3. Docker + CI
4. Deployment documentation tightening
5. Later AWS hardening

## Definition of near-term success
PolicyGate should be able to demonstrate, end to end:

- a customer-owned reference service receives a business request
- the service derives policy-relevant facts
- the service calls `POST /evaluate`
- PolicyGate returns a deterministic decision
- the service enforces that decision
- a structured audit event is emitted showing what was decided, why, and under which policy artifact

That is the current target shape.

## AWS proof checklist
- [x] Build and publish PolicyGate container image to ECR
- [x] Provision minimal networking/security required for runtime access
- [x] Deploy PolicyGate PDP to ECS Fargate
- [x] Expose PDP via ALB with working route to `/evaluate`
- [x] Send app logs and structured audit logs to CloudWatch
- [x] Configure runtime to load policy and start cleanly in AWS
- [x] Prove reference service can call deployed PDP successfully
- [x] Prove end-to-end deterministic evaluation flow with expected decision output
- [x] Confirm deployed service/audit boundary matches current architecture and README

## Later hardening / productionisation
- [ ] Replace default VPC/subnets lookup with fully Terraform-managed VPC networking
- [ ] Move Terraform state from local to remote backend (S3, with locking if used)
- [ ] Tighten container image versioning/tagging strategy beyond mutable proof tags
- [ ] Revisit ECR tag immutability policy
- [ ] Revisit CloudWatch log retention period based on operational/audit needs
- [ ] Consider longer-term log archival/export strategy if evidence retention requires it
- [ ] Harden IAM permissions to least-privilege for task execution and runtime access
- [ ] Review whether ALB/public exposure should later move to more restricted private topology
