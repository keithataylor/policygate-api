# PolicyGate Policy Guide (policy.yaml)

This folder contains the **user-editable policy configuration** for PolicyGate.

PolicyGate evaluates requests against `policy.yaml` and returns a deterministic decision:

- **ALLOW** – proceed normally
- **BLOCK** – do not proceed
- **REQUIRE_REVIEW** – do not proceed automatically; route for approval
- **DEGRADE** – proceed only under explicit restrictions (e.g. output caps)

PolicyGate also emits an **audit event** for every evaluation (correlation id, policy version, decision, rationale codes).

---

## Who edits policy?

Typically **engineers** (platform/security/ML platform) edit `policy.yaml`, because it changes runtime behaviour. Non-engineers can propose changes, but they should go through review.

---

## Safe workflow (recommended)

1. Edit `policy.yaml` in a Git branch.
2. Open a Pull Request.
3. CI validates the policy against the PolicyGate policy schema.
4. Merge only if validation/tests pass.
5. Deploy PolicyGate with the updated policy.

**Fail-closed:** if the policy is missing or invalid, PolicyGate refuses to run or returns a fail-closed error (no silent unsafe defaults).

---

## What you typically change in policy.yaml

- `policy_version` (bump it for every change)
- rule conditions in `when` (e.g. prod vs dev, restricted vs public)
- rule outcomes in `then` (decision, rationale codes)
- obligation parameters (e.g. `OUTPUT_CAP.max_tokens`)

You do **not** change:
- decision meanings
- API request/response shapes
- supported obligation types or their parameter formats

Those are fixed by PolicyGate contracts and validated by schema.

---

## OUTPUT CAP

PEP enforces OUTPUT_CAP at generation-time if possible; if not possible, it fails closed (BLOCK)

---

## Minimal example

```yaml
policy_id: "policygate-mvp"
policy_version: "2026-03-02.1"

default:
  decision: "BLOCK"
  rationale_codes:
    - "POLICY_DEFAULT_DENY"

rules:
  - rule_id: "allow_infer_public"
    priority: 100
    when:
      action: "infer:run"
      resource:
        sensitivity: "public"
    then:
      decision: "ALLOW"
      rationale_codes:
        - "ALLOW_PUBLIC_INFER"

  - rule_id: "degrade_infer_restricted_cap_output"
    priority: 90
    when:
      action: "infer:run"
      resource:
        sensitivity: "restricted"
    then:
      decision: "DEGRADE"
      rationale_codes:
        - "SENSITIVE_OUTPUT_LIMIT"
      obligations:
        - type: "OUTPUT_CAP"
          params:
            max_tokens: 200
```

---

## Troubleshooting

If PolicyGate fails to start or returns a fail-closed error, check logs for a schema validation error in `policy.yaml` (typos, unknown fields, invalid values).
