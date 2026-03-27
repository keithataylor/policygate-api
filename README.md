# PolicyGate

PolicyGate is a deployable **inference policy gate** for internal AI services and gateways.

It is delivered primarily as an **implementation-first package**: deployed into the customer environment and integrated into the customer’s own service boundary. PolicyGate provides deterministic policy decisioning through its core PDP service and includes reference PEP scaffolding to help customers enforce those decisions correctly.

## Positioning

PolicyGate is designed for organisations that need a **runtime decision point** in front of internal AI or inference workflows, where requests may need to be:

- allowed
- blocked
- degraded
- sent for review

with explicit rationale codes and auditable decision records.

This fits environments where AI use must be controlled consistently rather than left to ad hoc checks inside individual services.

## What PolicyGate is

PolicyGate consists of:

- a core **Policy Decision Point (PDP)** service in `policygate/`
- reference **Policy Enforcement Point (PEP)** scaffolding in `policygate_pep/`

A trusted service calls `POST /evaluate` with policy-relevant facts. PolicyGate returns a deterministic decision such as:

- `ALLOW`
- `BLOCK`
- `REQUIRE_REVIEW`
- `DEGRADE`

along with rationale codes and any applicable obligations.

The reference PEP scaffolding shows how those returned decisions can be enforced consistently in a customer-owned service or gateway.

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
- **The PEP layer** enforces the returned result

This repository includes both:

- the core PDP
- a reference PEP pattern showing how enforcement can be wired correctly around the PDP response

Typical flow:

1. A customer-owned business endpoint receives a request
2. That service derives the policy-relevant facts for the request
3. It calls `POST /evaluate` on PolicyGate
4. PolicyGate returns a decision response, including decision, rationale codes, and any obligations
5. The customer-side enforcer interprets that response and dispatches to the appropriate decision handler
6. A structured audit event is emitted for the completed evaluation
7. The service returns the business response

This separation keeps business payloads business-shaped while keeping policy decisioning generic and deterministic.

## Why this design

PolicyGate separates:

- **fact collection and mapping**  
  customer-specific logic in the calling service

from

- **policy decisioning**  
  generic, validated rules evaluated by PolicyGate

from

- **business enforcement behaviour**  
  customer-specific handling of allow / block / degrade / review outcomes

Customers adapt behaviour by changing:

- policy rules
- mapped facts / signals sent to PolicyGate
- customer-side handler implementations

not by changing PolicyGate engine code.

## API

Core endpoints:

- `POST /evaluate`
- `GET /health`
- optional `GET /version`

Optional reference endpoints may exist in the reference PEP/service layer to show how PolicyGate can sit in front of an inference-style workflow.

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
- standalone PDP service deployable to ECS / Fargate with IAM and CloudWatch logging
- ALB-backed HTTP service shape for controlled internal or external caller access where required

Likely deployment patterns over time:

- central PDP service behind a customer-owned service or gateway
- service-adjacent deployment for lower latency where justified
- later Kubernetes-aligned deployment patterns where needed

PolicyGate is not positioned as a general public SaaS endpoint. The preferred proof shape is a standalone audited PDP service with customer-side mapping/enforcement and a clear caller flow through a customer-owned service boundary.

## Reference integration code

The repository includes customer-side reference integration code outside the PDP core.

This code is intended to show two things clearly:

- which PEP/scaffolding logic should remain stable so PDP decisions are enforced correctly
- which customer-side files are expected to be adapted for business-specific behaviour

The intended split is:

- stable PEP/enforcement scaffolding in `policygate_pep/core/`
- adaptable reference/customer-side code in `policygate_pep/reference/`

Reference code may include files such as:

- `reference_service.py`  
  a reference customer/business service acting as the enforcement boundary

- `enforcer.py`  
  stable decision-dispatch logic that routes returned decisions to supplied handler callbacks

- `reference_handlers.py`  
  reference customer-side handler stubs that can be copied, edited, or replaced

- `reference_client.py`  
  a simple caller/test harness for the reference service

The customer is not required to use fixed internal function names. The important contract is that the customer supplies handler callables compatible with the expected decision categories.

These files are not part of the core PDP engine.

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

PolicyGate is intended to be sold and delivered primarily as an implementation package.

Engagements may begin at different points depending on the customer need, for example:

- planning and design
- deployment into the customer environment
- integration with a customer-owned service or gateway
- initial policy baseline setup
- end-to-end decision-path testing
- handover and deployment/policy guidance
- limited post-delivery support

The primary deliverable is a defined working implementation using PolicyGate inside the customer environment, rather than a self-serve SaaS product.

## Current product boundary

PolicyGate’s value is in providing:

- a deployable runtime policy decision point
- deterministic allow/block/review/degrade decisions
- explainable rationale codes
- auditable decision output
- clean integration into customer-owned AI service boundaries
- reference PEP scaffolding that helps customers enforce PDP outcomes correctly
- a credible AWS deployment shape for a standalone PDP service

That narrow boundary is deliberate.
