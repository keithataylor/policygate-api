import json
from jsonschema import validate, ValidationError
import yaml


def load_and_validate_policy(policy_path: str, schema_path: str) -> dict:
    """
    Load a YAML policy file and validate it against a JSON Schema.

    Returns:
        dict: Parsed policy document (validated).
    Raises:
        FileNotFoundError: if policy or schema file is missing.
        ValueError: if policy fails schema validation.
    """
    with open(policy_path, "r", encoding="utf-8") as f:
        policy = yaml.safe_load(f)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    try:
        validate(instance=policy, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Policy validation failed for '{policy_path}': {e.message}") from e

    return policy