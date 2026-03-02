# Scope
 
## Goal
Deliver a portfolio-grade, production-shaped **PolicyGate** service: a deployable **Policy Decision Point (PDP)** that provides deterministic **ALLOW / BLOCK / REQUIRE_REVIEW / DEGRADE** decisions (with rationale codes) for ML-adjacent APIs and tool/inference calls, plus audit-ready evidence and an operator story.

PolicyGate demonstrates:
- A working **decision API** (`POST /evaluate`) with strict input validation.
- A deterministic governance/control layer that returns **decisions + rationale codes** (no free-text reasons).
- Traceability: **policy version**, **decision trace**, and **request correlation** in every decision and log event.
- Cloud-native ops basics: Docker + AWS deploy (ECS/Fargate + ALB) with CloudWatch visibility and documented operations.

## Non-goals
- Building a “full ML platform” (no orchestration, feature store, training automation, multi-tenant SaaS, or UI).
- Novel model performance work (no deep learning, no SOTA benchmarking).
- Full compliance programme or certification (we implement **technical controls**, not legal sign-off).
- Multi-cloud support (AWS first; portability can be documented, not implemented).
- Complex enterprise auth (SSO/OIDC) in MVP.

## MVP demo scenario (one request end-to-end)
A single request demonstrates the whole system:

1. Client calls `POST /evaluate` with a JSON payload describing the request context (actor, action, resource, environment, optional risk signals).
2. Service validates input schema (fail fast).
3. PolicyGate loads the **versioned policy config** (strict schema) and evaluates deterministically.
4. PolicyGate returns a decision (**ALLOW / BLOCK / REQUIRE_REVIEW / DEGRADE**) plus:
   - rationale codes
   - policy version
   - correlation id
   - decision trace metadata (stable, non-sensitive)
5. Every request emits a structured audit event with correlation id, decision, rationale codes, policy version, and evaluation outcome.

### Optional “ML-adjacent” demo adapter (still MVP-compatible)
To demonstrate “gate in front of inference” without turning the product into an inference service:
- Provide `POST /infer` as a **demo adapter** that calls `POST /evaluate` internally first.
- If **ALLOW**, run a pinned simple model (e.g., sklearn artefact) and return prediction + decision metadata.
- If **BLOCK / REQUIRE_REVIEW / DEGRADE**, return a safe response (no inference) with decision metadata.

**PolicyGate’s identity remains `POST /evaluate`.** Inference is a demonstration adapter, not the core product.

## Must-have controls (governance + ops)

### Governance controls (MVP)
- **Policy-as-config (MVP):** versioned `policy.yaml`/`policy.json` with a strict schema; changes are diffable and reviewable.
- **Deterministic decisioning:** pure function behaviour; stable outputs for same inputs; no “LLM judgement,” no hidden heuristics.
- **Rationale codes:** every non-ALLOW outcome includes explicit reason codes (enumerated, not free-text).
- **Traceability:** logs link request → decision → policy version → (optional) model version.
- **Fail-closed stance:** if policy/config is invalid, missing, or unreadable, the system refuses to run (no silent defaults).
- **Decision explainability (bounded):** return a compact decision trace/metadata that is stable and safe to disclose.

### Governance controls (v2 / optional)
- **Policy-as-code plugin:** support an additional policy engine (e.g., OPA/Rego) behind the same `POST /evaluate` contract.
- **Policy engine pluggability:** config engine remains supported; OPA becomes an alternative engine selected by deployment configuration.

### Ops/MLOps controls (MVP)
- **Containerised runtime:** Docker build + run documented.
- **Health endpoint:** `/health` for readiness/liveness.
- **Structured logging:** JSON logs including correlation id and decision metadata.
- **AWS visibility:** logs visible in CloudWatch (log group and search patterns documented).
- **Minimal deployment path:** Terraform deploys to a single AWS target (ECS/Fargate + ALB).
- **CI quality gate (MVP):** On every PR, GitHub Actions runs pytest, ruff, mypy (or pyright), and docker build for the service. Dependencies are pinned so the image build is reproducible from a clean runner.

### Audit evidence (MVP)
- **Primary evidence source:** CloudWatch JSON logs (audit event per request).
- **Immutable event design:** audit record format is versioned and stable.

### Audit evidence (v2 / optional)
- **Append-only sink:** optional export to S3 (or DB) as an append-only audit trail.

## Tech boundaries (what we will/won’t use)

### Will use (MVP)
- Python, FastAPI, Pydantic
- Docker
- Terraform (minimal, single environment first; env separation can be documented)
- Cloud target: AWS-only (ECS/Fargate + ALB + CloudWatch). Azure is explicitly out of scope for now.
- Policy-as-config engine (schema-validated YAML/JSON)

### May add (v2)
- OPA/Rego policy engine plugin
- Optional S3 audit sink
- Optional JWT validation (if it materially improves the demo)

### Will not use (in this build)
- Kubernetes/EKS
- Airflow/Kedro
- MLflow (unless absolutely necessary; otherwise a pinned model artefact + version id is sufficient)
- Full SSO/OIDC integration (MVP uses “none” or simple API key)

## Definition of done
- Repo runs locally (and via Docker) with a one-command demo.
- End-to-end `POST /evaluate` shows: validation → decision → response.
- Audit event emitted for each request with: correlation id, decision, rationale codes, policy version, outcome.
- Terraform deploys to AWS and logs are visible in CloudWatch.
- README includes: architecture diagram, how to run, how to deploy, and what controls are demonstrated.
- (Optional demo) `POST /infer` demonstrates “gate in front of inference” while keeping `POST /evaluate` as the product core.
