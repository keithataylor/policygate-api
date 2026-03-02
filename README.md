# Implementation-first: 
PolicyGate is delivered primarily as an implementation package: we deploy and integrate it into your environment.

PolicyGate is designed for complex environments by separating fact collection (client-specific mapping) from policy decisioning (generic rules). Customers adapt behavior by changing policy rules and the facts they send (signals), not by changing PolicyGate code.

## What PolicyGate is
PolicyGate is a deployable **Policy Decision Point (PDP)** service. Client systems call `POST /evaluate` to receive a deterministic decision:
ALLOW / BLOCK / REQUIRE_REVIEW / DEGRADE + rationale codes (+ obligations).

## What PolicyGate is not
- Not a full MLOps platform
- Not a compliance certification product
- Not a policy management UI

## How it’s used in real systems (PDP vs PEP)
- PolicyGate (PDP) decides.
- Your service/gateway (PEP) enforces the decision.
- This repo includes a reference PEP demo to show enforcement end-to-end.
- PolicyGate is called by trusted services (PEPs), not by end-users or LLMs directly; the PEP is the enforcement boundary.

## API
- `POST /evaluate` (core product)
- `GET /health`
- Optional demo: `POST /infer` (shows “gate in front of inference”)

## Policy configuration
- Policy lives in `policy/policy.yaml` (rules-only).
- Guide: `policy/README.md`.

## Contracts (frozen interfaces)
- `contracts/decision_contract.*`
- `contracts/evaluate_request.schema.json`
- `contracts/evaluate_response.schema.json`
- `contracts/audit_event.schema.json`

## Run locally
(Exact commands go here)

## Run with Docker
(Exact commands go here)

## Deploy to AWS (Terraform)
(Exact commands go here)

## Evidence / auditability
- Every request emits a structured audit event with correlation id + policy_version + decision + rationale codes.

## Repo layout
(Short tree)

## Implementation package deliverables
(Short bullet list: deploy + integrate + policy baseline + handover + 30-day email support)