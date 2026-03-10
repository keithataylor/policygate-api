# tools/generate_policy_schema_md.py
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

SCHEMA_PATH = Path("contracts/policy.schema.json")
OUT_PATH = Path("policy/SCHEMA.md")


def md_table(rows: List[Tuple[str, str]]) -> str:
    out = ["| Field | Details |", "|---|---|"]
    for field, details in rows:
        out.append(f"| `{field}` | {details} |")
    return "\n".join(out)


def fmt_range(prop: Dict[str, Any]) -> str:
    parts = []
    if "type" in prop:
        parts.append(f"type: `{prop['type']}`")
    if "enum" in prop:
        parts.append("enum: " + ", ".join(f"`{x}`" for x in prop["enum"]))
    if "pattern" in prop:
        parts.append(f"pattern: `{prop['pattern']}`")
    if "minimum" in prop:
        parts.append(f"min: `{prop['minimum']}`")
    if "maximum" in prop:
        parts.append(f"max: `{prop['maximum']}`")
    if "minLength" in prop:
        parts.append(f"minLen: `{prop['minLength']}`")
    if "maxLength" in prop:
        parts.append(f"maxLen: `{prop['maxLength']}`")
    if "minItems" in prop:
        parts.append(f"minItems: `{prop['minItems']}`")
    if "maxProperties" in prop:
        parts.append(f"maxProps: `{prop['maxProperties']}`")
    desc = prop.get("description")
    if desc:
        parts.append(desc)
    return " • ".join(parts) if parts else ""


def get_in(d: Dict[str, Any], path: List[str]) -> Dict[str, Any]:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict):
            return {}
        cur = cur.get(p, {})
    return cur if isinstance(cur, dict) else {}


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    props = schema.get("properties", {})

    lines: List[str] = []
    lines.append("# Policy Schema Reference (auto-generated)\n")
    lines.append(f"Source: `{SCHEMA_PATH.as_posix()}`\n")

    # Top-level
    lines.append("## Top-level required fields\n")
    required = schema.get("required", [])
    lines.append(", ".join(f"`{r}`" for r in required) + "\n")

    rows = []
    for k, v in props.items():
        rows.append((k, fmt_range(v)))
    lines.append("## Top-level fields\n")
    lines.append(md_table(rows) + "\n")

    # Default object details
    default_obj = props.get("default", {})
    default_props = default_obj.get("properties", {})
    lines.append("## `default` object\n")
    default_rows = []
    for k, v in default_props.items():
        default_rows.append((f"default.{k}", fmt_range(v)))
    if default_rows:
        lines.append(md_table(default_rows) + "\n")
    else:
        lines.append("_No default object details found in schema._\n")

    # Rules overview
    rule_item = get_in(props, ["rules", "items"])
    rule_props = rule_item.get("properties", {})
    lines.append("## `rules[]` object\n")
    rule_rows = []
    for k, v in rule_props.items():
        rule_rows.append((f"rules[].{k}", fmt_range(v)))
    lines.append(md_table(rule_rows) + "\n")

    # When fields
    when_props = get_in(rule_props, ["when", "properties"])
    lines.append("## `rules[].when` fields\n")
    when_rows = []
    for k, v in when_props.items():
        when_rows.append((f"when.{k}", fmt_range(v)))
    lines.append(md_table(when_rows) + "\n")

    # Then fields
    then_props = get_in(rule_props, ["then", "properties"])
    lines.append("## `rules[].then` fields\n")
    then_rows = []
    for k, v in then_props.items():
        then_rows.append((f"then.{k}", fmt_range(v)))
    lines.append(md_table(then_rows) + "\n")

    # Actions enum (explicit list)
    when_action = get_in(rule_props, ["when", "properties", "action"])
    if "enum" in when_action:
        lines.append("## Actions\n")
        lines.append("Allowed values:\n")
        lines.append("\n".join(f"- `{x}`" for x in when_action["enum"]) + "\n")

    # Decisions enum (from default.decision if present, else then.decision)
    default_decision = get_in(props, ["default", "properties", "decision"])
    then_decision = get_in(rule_props, ["then", "properties", "decision"])
    decisions_enum = default_decision.get("enum") or then_decision.get("enum")
    if decisions_enum:
        lines.append("## Decisions\n")
        lines.append("Allowed values:\n")
        lines.append("\n".join(f"- `{x}`" for x in decisions_enum) + "\n")

    # Obligation types enum
    obligation_type = get_in(rule_props, ["then", "properties", "obligations", "items", "properties", "type"])
    if "enum" in obligation_type:
        lines.append("## Obligation types\n")
        lines.append("Allowed values:\n")
        lines.append("\n".join(f"- `{x}`" for x in obligation_type["enum"]) + "\n")

    # OUTPUT_CAP params (deep detail)
    params_schema = get_in(
        rule_props,
        ["then", "properties", "obligations", "items", "properties", "params"],
    )
    params_props = params_schema.get("properties", {})
    min_props = params_schema.get("minProperties")

    lines.append("## OUTPUT_CAP parameters\n")
    if min_props is not None:
        lines.append(f"**Constraint:** `params` must set at least `{min_props}` field(s).\n")
    if not params_props:
        lines.append("_No OUTPUT_CAP params found in schema._\n")
    else:
        cap_rows = []
        for k, v in params_props.items():
            cap_rows.append((f"OUTPUT_CAP.params.{k}", fmt_range(v)))
        lines.append(md_table(cap_rows) + "\n")

    OUT_PATH.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()