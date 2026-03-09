flowchart TD
  A[Client / Upstream System] --> PEP[PEP: Caller service / gateway<br/>(enforces decisions)]
  PEP -->|POST /evaluate| PDP[PolicyGate (PDP)<br/>FastAPI]
  PDP --> V[Input Validation<br/>Pydantic + JSON Schema]
  V --> PL[Policy Loader<br/>policy/policy.yaml + schema validation]
  PL --> DE[Decision Engine<br/>deterministic rules]
  DE --> AUD[Audit Event Writer<br/>structured JSON log]
  DE -->|Decision + obligations| PEP

  PEP -->|ALLOW| ACT[Perform action<br/>(e.g., inference/tool/data op)]
  PEP -->|DEGRADE| DEG[Perform restricted action<br/>(e.g., OUTPUT_CAP enforcement)]
  PEP -->|BLOCK| BLK[Deny]
  PEP -->|REQUIRE_REVIEW| REV[Route to review workflow]

  AUD --> CW[(CloudWatch Logs<br/>MVP evidence source)]