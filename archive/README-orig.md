# PolicyGate

PolicyGate is a deployable **inference policy gate** for internal AI services and gateways.

It is delivered primarily as an **implementation-first package**: deployed into the customer environment and integrated into the customer’s own service boundary. PolicyGate makes deterministic policy decisions; the customer’s service or gateway enforces them.

## Positioning

PolicyGate is designed for organisations that need a **runtime decision point** in front of internal AI or inference workflows, where requests may need to be:

- allowed
- blocked
- degraded
- sent for review

with explicit rationale codes and auditable decision records.

This fits environments where AI use must be controlled consistently rather than left to ad hoc checks inside individual services.

## What PolicyGate is

PolicyGate is a deployable **Policy Decision Point (PDP)** service.

A trusted service calls `POST /evaluate` with policy-relevant facts. PolicyGate returns a deterministic decision such as:

- `ALLOW`
- `BLOCK`
- `REQUIRE_REVIEW`
- `DEGRADE`

along with rationale codes and any applicable obligations.

PolicyGate is intended to sit behind a customer-owned service or gateway, not to be called directly by end users or LLMs.

## What PolicyGate is not

PolicyGate is not:

- a full MLOps platform
- a compliance certification product
- a policy authoring UI
- a model hosting platform
- a general workflow orchestration system

It is a narrow runtime control component.

## How it fits into real systems

PolicyGate follows a **PDP / PEP** pattern:

- **PolicyGate (PDP)** decides
- **Your service or gateway (PEP)** enforces

Typical flow:

1. A customer-owned business endpoint receives a request
2. That service derives the policy-relevant facts for the request
3. It calls `POST /evaluate` on PolicyGate
4. PolicyGate returns a decision
5. The customer service enforces the result and returns the business response

This separation keeps business payloads business-shaped while keeping policy decisioning generic and deterministic.

## Why this design

PolicyGate separates:

- **fact collection and mapping**  
  customer-specific logic in the calling service

from

- **policy decisioning**  
  generic, validated rules evaluated by PolicyGate

Customers adapt behaviour by changing:

- policy rules
- mapped facts / signals sent to PolicyGate

not by changing PolicyGate engine code.

## API

Core endpoints:

- `POST /evaluate`
- `GET /health`

Optional demo/reference endpoints may exist in the reference PEP/service layer to show how PolicyGate can sit in front of an inference-style workflow.

## Policy configuration

Policy is stored as rules, for example:

- `policy/policy.yaml`

Supporting guidance lives in:

- `policy/README.md`

PolicyGate validates policy structure and policy semantics separately, so invalid or ambiguous policies can be rejected at load time rather than producing unclear runtime behaviour.

## Deterministic decisioning

PolicyGate is intentionally narrow and explicit.

Design principles include:

- fixed evaluation route: `POST /evaluate`
- deterministic decision output
- explicit rule priorities
- semantic validation of invalid policy conditions
- customer-controlled mapping of policy-relevant facts
- no hidden LLM behaviour inside policy evaluation

The aim is predictable enforcement, not flexible natural-language reasoning.

## Auditability and evidence

PolicyGate is intended to produce structured, auditable decision records.

A completed decision can be tied to:

- request correlation ID
- decision
- matched rule ID
- rationale codes
- policy identity / version / fingerprint
- minimal decision-relevant context

This supports runtime evidence and investigation without turning PolicyGate into a general logging platform.

## Deployment model

PolicyGate is designed to be deployed into the customer environment.

Initial deployment shape:

- Dockerised service
- AWS-oriented deployment path
- suitable for ECS / Fargate / IAM / ALB based environments

Likely deployment patterns over time:

- central PDP service
- service-adjacent deployment for lower latency
- later Kubernetes-aligned deployment patterns where needed

PolicyGate is not positioned as a general public SaaS endpoint.

## Reference integration code

The repository includes reference customer-side integration code outside the PDP core.

This code demonstrates the intended pattern:

- `reference_service.py`  
  a reference customer/business service acting as the enforcement boundary

- `reference_client.py`  
  a simple caller/test harness for the reference service

These files are examples of how a customer service can:

- derive policy-relevant facts
- call PolicyGate
- enforce returned decisions
- keep business endpoints business-shaped

They are not part of the core PDP engine.

## Frozen contracts

Contract files may include artifacts such as:

- `contracts/decision_contract.*`
- `contracts/evaluate_request.schema.json`
- `contracts/evaluate_response.schema.json`
- `contracts/audit_event.schema.json`

These help keep the decision interface stable and explicit.

## Run locally

_Exact commands to be added._

## Run with Docker

_Exact commands to be added._

## Deploy to AWS with Terraform

_Exact commands to be added._

## Repository layout

_Concise tree to be added._

## Implementation-first delivery

PolicyGate is intended to be sold and delivered primarily as an implementation package, for example:

- deploy PolicyGate into the customer environment
- integrate it with a customer-owned service or gateway
- provide an initial policy baseline
- test the decision path end-to-end
- hand over deployment and policy guidance
- provide limited post-delivery support

## Current product boundary

PolicyGate’s value is in providing:

- a deployable runtime policy decision point
- deterministic allow/block/review/degrade decisions
- explainable rationale codes
- auditable decision output
- clean integration into customer-owned AI service boundaries

That narrow boundary is deliberate.