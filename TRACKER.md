# PolicyGate Implementation Tracker

## Current focus
- [ ] Implement actual PEP `DEGRADE` enforcement for `OUTPUT_CAP` with fail-closed behaviour

## Milestones

### M0 — Contracts & policy validation
- [x] contracts/evaluate_request.schema.json
- [x] contracts/evaluate_response.schema.json
- [x] contracts/policy.schema.json
- [x] contracts/audit_event.schema.json
- [x] policy/policy.yaml
- [x] policy/README.md
- [x] policy/SCHEMA.md
- [x] tools/generate_policy_schema_md.py
- [x] Implement `policygate/policy_loader.py` (load YAML, validate schema)
- [x] Add unit tests for policy validation (valid + invalid cases)

### M1 — Decision engine (deterministic)
- [x] Implement `policygate/engine.py` (match rules, choose by priority, tie = file order, else default)
- [ ] Add golden tests: request + policy -> exact decision response
- [ ] Add explicit overlap/precedence tests for multi-match scenarios

### M2 — API wiring
- [x] Implement FastAPI `POST /evaluate`
- [x] Implement `GET /health`
- [x] Load policy once at startup
- [x] Implement runtime Pydantic request/response models in `policygate/models.py`

### M3 — Reference PEP demo
- [x] Create `pep_demo/pep_service.py` with `/summarise`
- [x] Create `pep_demo/pep_models.py`
- [x] Create `pep_demo/mappers.py` to map request/context -> `EvaluateRequestV1`
- [x] Create `pep_demo/pep_client.py`
- [ ] Implement actual PEP enforcement for `DEGRADE` / `OUTPUT_CAP`
- [ ] Add demo tests covering ALLOW / BLOCK / REQUIRE_REVIEW / DEGRADE flows

### M4 — Audit logging
- [ ] Emit structured audit event per PDP request
- [ ] Validate emitted audit events against `contracts/audit_event.schema.json`

### M5 — Policy visibility / simulation
- [ ] Add fixed scenario matrix file for representative policy cases
- [ ] Add runner to evaluate all scenarios against current policy
- [ ] Return tabulated scenario results: scenario id, description, decision, obligations, matched rule id
- [ ] Later: add simple web-based policy editor + “Run scenarios” simulation view

### M6 — Docker + CI gate
- [ ] Dockerfile builds
- [ ] GitHub Actions: pytest + ruff + mypy/pyright + docker build

### M7 — AWS deploy (Terraform)
- [ ] ECS/Fargate/ALB deploy
- [ ] CloudWatch logs visible