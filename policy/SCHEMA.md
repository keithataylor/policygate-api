# Policy Schema Reference (auto-generated)

Source: `contracts/policy.schema.json`

## Top-level required fields

`policy_id`, `policy_version`, `default`, `rules`

## Top-level fields

| Field | Details |
|---|---|
| `policy_id` | type: `string` • minLen: `1` • maxLen: `128` |
| `policy_version` | type: `string` • minLen: `1` • maxLen: `128` |
| `default` | type: `object` |
| `rules` | type: `array` • minItems: `1` |

## `default` object

| Field | Details |
|---|---|
| `default.decision` | type: `string` • enum: `ALLOW`, `BLOCK`, `REQUIRE_REVIEW`, `DEGRADE` |
| `default.rationale_codes` | type: `array` • minItems: `1` |

## `rules[]` object

| Field | Details |
|---|---|
| `rules[].rule_id` | type: `string` • minLen: `1` • maxLen: `128` |
| `rules[].priority` | type: `integer` • min: `0` • max: `1000000` |
| `rules[].when` | type: `object` |
| `rules[].then` | type: `object` |

## `rules[].when` fields

| Field | Details |
|---|---|
| `when.action` | type: `string` • enum: `infer:run`, `data:read`, `data:write`, `tool:invoke`, `policy:admin` |
| `when.env` | type: `object` |
| `when.resource` | type: `object` |
| `when.subject` | type: `object` |
| `when.signals` | type: `object` • maxProps: `50` • Rule match on signals uses exact key/value equality. |

## `rules[].then` fields

| Field | Details |
|---|---|
| `then.decision` | type: `string` • enum: `ALLOW`, `BLOCK`, `REQUIRE_REVIEW`, `DEGRADE` |
| `then.rationale_codes` | type: `array` • minItems: `1` |
| `then.obligations` | type: `array` |

## Actions

Allowed values:

- `infer:run`
- `data:read`
- `data:write`
- `tool:invoke`
- `policy:admin`

## Decisions

Allowed values:

- `ALLOW`
- `BLOCK`
- `REQUIRE_REVIEW`
- `DEGRADE`

## Obligation types

Allowed values:

- `OUTPUT_CAP`

## OUTPUT_CAP parameters

**Constraint:** `params` must set at least `1` field(s).

| Field | Details |
|---|---|
| `OUTPUT_CAP.params.max_tokens` | type: `integer` • min: `1` • max: `100000` |
| `OUTPUT_CAP.params.max_items` | type: `integer` • min: `1` • max: `1000000` |
| `OUTPUT_CAP.params.max_bytes` | type: `integer` • min: `1` • max: `100000000` |
