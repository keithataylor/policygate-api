# PolicyGate Implementation Tracker

## Current focus
- [ ] (fill in the one thing you are doing right now)

## Milestones
### M0 — Contracts & policy validation
- [x] contracts/decision_contract.*
- [x] contracts/evaluate_request.schema.json
- [x] contracts/evaluate_response.schema.json
- [x] contracts/audit_event.schema.json
- [x] policy/policy.yaml
- [x] contracts/policy.schema.json
- [ ] Implement `policygate/policy_loader.py` (load YAML, validate schema)
- [ ] Add unit tests for policy validation (valid + invalid cases)

### M1 — Decision engine (deterministic)
- [ ] Implement `policygate/engine.py` (match rules, choose by priority)
- [ ] Add golden tests: request+policy -> exact decision response

### M2 — API wiring
- [ ] Implement FastAPI `POST /evaluate`
- [ ] Implement `GET /health`

### M3 — Audit logging
- [ ] Emit structured audit event per request

### M4 — Docker + CI gate
- [ ] Dockerfile builds
- [ ] GitHub Actions: pytest + ruff + mypy/pyright + docker build

### M5 — AWS deploy (Terraform)
- [ ] ECS/Fargate/ALB deploy
- [ ] CloudWatch logs visible