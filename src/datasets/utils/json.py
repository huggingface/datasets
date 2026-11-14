from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

import pandas as pd


if TYPE_CHECKING:
    from ..features.features import FeatureType


def ujson_dumps(*args, **kwargs):
    try:
        return pd.io.json.ujson_dumps(*args, **kwargs)
    except AttributeError:
        # Before pandas-2.2.0, ujson_dumps was renamed to dumps: import ujson_dumps as dumps
        return pd.io.json.dumps(*args, **kwargs)


def ujson_loads(*args, **kwargs):
    try:
        return pd.io.json.ujson_loads(*args, **kwargs)
    except AttributeError:
        # Before pandas-2.2.0, ujson_loads was renamed to loads: import ujson_loads as loads
        return pd.io.json.loads(*args, **kwargs)


def json_encode_field(example: Any, json_field_path: list[str], as_string: bool = False) -> Any:
    if json_field_path:
        field, *json_field_path = json_field_path
        if example is None:
            return None
        elif field == 0:
            return [json_encode_field(x, json_field_path, as_string=as_string) for x in example]
        else:
            return {**example, field: json_encode_field(example.get(field), json_field_path, as_string=as_string)}
    elif example is None:
        # keep missing values as real nulls instead of the JSON string "null"
        return None
    elif as_string and isinstance(example, str):
        # declared as a string field: keep the string as it is (don't double-encode it)
        return example
    elif as_string:
        # cast to string like Arrow would when casting to Value("string")
        if isinstance(example, bool):
            return "true" if example else "false"
        return str(example)
    else:
        try:
            ujson_loads(example)
        except Exception:
            return ujson_dumps(example)
        else:
            return example


def json_decode_field(example: Any, json_field_path: str) -> Any:
    if json_field_path:
        field, *json_field_path = json_field_path
        if example is None:
            return None
        elif field == 0:
            return [json_decode_field(x, json_field_path) for x in example]
        else:
            return {**example, field: json_decode_field(example.get(field), json_field_path)}
    elif example is None:
        return None
    else:
        try:
            return ujson_loads(example)
        except Exception:
            return example


def find_mixed_struct_types_field_paths(examples: list, allow_root=False) -> list[list[str]]:
    mixed_struct_types_field_paths = []
    examples = [example for example in examples if example is not None]
    if not examples:
        return []
    paths_and_content_to_check = [([], examples)]
    while paths_and_content_to_check:
        path, content = paths_and_content_to_check.pop(0)
        if all(isinstance(x, dict) for x in content):
            if (allow_root or path) and (any(set(x) != set(content[0]) for x in content) or not content[0]):
                mixed_struct_types_field_paths.append(path)
            else:
                for subfield in {field for x in content for field in x}:
                    examples = [x[subfield] for x in content if subfield in x and x[subfield] is not None]
                    if not examples:
                        continue
                    paths_and_content_to_check.append((path + [subfield], examples))
        elif all(isinstance(x, list) for x in content):
            examples = [x for sublist in content for x in sublist if x is not None]
            if not examples:
                continue
            paths_and_content_to_check.append((path + [0], examples))
        elif any(isinstance(x, (dict, list)) for x in content):
            mixed_struct_types_field_paths.append(path)
    return mixed_struct_types_field_paths


def get_json_field_path_from_pyarrow_json_error(
    err_str: str, *, examples: Iterable[Any] | None = None
) -> list[str | int]:
    column = err_str.split("Column(", 1)[1].rsplit(") changed from", 1)[0]
    if examples is None:
        return [0 if seg == "[]" else seg for seg in column.strip("/").split("/")]
    if not column:
        return []  # The error is at the root, not at a field.
    if "/" not in column[1:] and column != "/[]":
        return [column[1:]]

    # Arrow does not escape slashes in keys or distinguish a literal "[]" key from a list step.
    match = None
    for example in examples:
        pending = [(example, column, [])]
        while pending:
            value, remaining, path = pending.pop()
            if not remaining:
                if match is not None and path != match:
                    raise ValueError(f"Cannot resolve mixed-type JSON field {column!r}: ambiguous field path")
                match = path
            elif isinstance(value, dict):
                for key, child in value.items():
                    prefix = f"/{key}"
                    if remaining == prefix or remaining.startswith(prefix + "/"):
                        pending.append((child, remaining[len(prefix) :], path + [key]))
            elif isinstance(value, list) and (remaining == "/[]" or remaining.startswith("/[]/")):
                pending.extend((child, remaining[3:], path + [0]) for child in value)
    if match is None:
        raise ValueError(f"Cannot resolve mixed-type JSON field {column!r}: field path not found")
    return match


def insert_json_field_path(json_field_paths: list[list[str]], json_field_path: list[str]) -> None:
    # Add to list of json_field_paths and check if other share a common path
    for i in range(len(json_field_paths)):
        if json_field_paths[i][: len(json_field_path)] == json_field_path:
            json_field_paths[i] = json_field_path
            break
    else:
        json_field_paths.append(json_field_path)


def json_encode_fields_in_json_lines(
    original_batch: bytes, json_field_paths: list[list[str]], string_field_paths: list[list[str]] = ()
) -> bytes:
    examples = [ujson_loads(line) for line in original_batch.splitlines()]
    string_field_paths = {tuple(path) for path in string_field_paths}
    for json_field_path in json_field_paths:
        as_string = tuple(json_field_path) in string_field_paths
        examples = [json_encode_field(example, json_field_path, as_string=as_string) for example in examples]
    return "\n".join(ujson_dumps(example) for example in examples).encode()


def get_json_field_paths_from_feature(feature: "FeatureType") -> list[list[str]]:
    from datasets.features.features import Json, _visit_with_path

    json_field_paths = []

    def get_json_type_path(_feature, feature_path):
        if isinstance(_feature, Json):
            json_field_paths.append(feature_path)
        return _feature

    _visit_with_path(feature, get_json_type_path)
    return json_field_paths


def get_string_field_paths_from_feature(feature: "FeatureType") -> list[list[str]]:
    from datasets.features.features import Json, Value, _visit_with_path

    string_field_paths = []

    def get_string_type_path(_feature, feature_path):
        if isinstance(_feature, Value) and _feature.dtype == "string" and not isinstance(_feature, Json):
            string_field_paths.append(feature_path)
        return _feature

    _visit_with_path(feature, get_string_type_path)
    return string_field_paths


def set_json_types_in_feature(feature: "FeatureType", json_field_paths: list[list[str]]) -> None:
    from datasets.features.features import Json, _visit_with_path

    def set_json_type(feature, feature_path):
        return Json() if feature_path in json_field_paths else feature

    feature = _visit_with_path(feature, set_json_type)
    return feature
