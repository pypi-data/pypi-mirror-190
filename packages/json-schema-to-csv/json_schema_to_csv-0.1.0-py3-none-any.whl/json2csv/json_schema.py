import json

from jsonschema.exceptions import SchemaError
from jsonschema.validators import Draft7Validator


def read_json_schema(json_schema_file: str) -> dict:

    with open(json_schema_file) as f:
        json_schema = json.load(f)
        Draft7Validator.check_schema(json_schema)
        return json_schema
