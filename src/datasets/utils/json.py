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


def json_encode_field(example: Any, json_field_path: str) -> Any:
    if json_field_path:
        field, *json_field_path = json_field_path
        if example is None:
            return None
        elif field == 0:
            return [json_encode_field(x, json_field_path) for x in example]
        else:
            return {**example, field: json_encode_field(example.get(field), json_field_path)}
        return example
    else:
        try:
            ujson_loads(example)
        except Exception:
            return ujson_dumps(example)
        else:
            return example


def find_mixed_struct_types_field_paths(examples: list, allow_root=False) -> list[str]:
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


def get_json_field_path_from_pyarrow_json_error(err_str: str) -> str:
    # e.g. json_field_path_str = "col/subfield_containing_a_list/[]/subsubfield_in_item_in_the_list"
    json_field_path_str = err_str.split("Column(", 1)[1].rsplit(") changed from", 1)[0].strip("/")
    # e.g. json_field_path = ["col", "subfield_containing_a_list", 0, "subsubfield_in_item_in_the_list"]
    json_field_path = [0 if seg == "[]" else seg for seg in json_field_path_str.split("/")]
    return json_field_path


def insert_json_field_path(json_field_paths: list[str], json_field_path: str) -> None:
    # Add to list of json_field_paths and check if other share a common path
    for i in range(len(json_field_paths)):
        if json_field_paths[i][: len(json_field_path)] == json_field_path:
            json_field_paths[i] = json_field_path
            break
    else:
        json_field_paths.append(json_field_path)


def json_encode_fields_in_json_lines(original_batch: bytes, json_field_paths: list[str]) -> bytes:
    examples = [ujson_loads(line) for line in original_batch.splitlines()]
    for json_field_path in json_field_paths:
        examples = [json_encode_field(example, json_field_path) for example in examples]
    batch = "\n".join([ujson_dumps(example) for example in examples]).encode()
    return batch


def get_json_field_paths_from_feature(feature: "FeatureType") -> list[str]:
    from datasets.features.features import Json, _visit_with_path

    json_field_paths = []

    def get_json_type_path(_feature, feature_path):
        if isinstance(_feature, Json):
            json_field_paths.append(feature_path)
        return _feature

    _visit_with_path(feature, get_json_type_path)
    return json_field_paths


def set_json_types_in_feature(feature: "FeatureType", json_field_paths: list[str]) -> None:
    from datasets.features.features import Json, _visit_with_path

    def set_json_type(feature, feature_path):
        return Json() if feature_path in json_field_paths else feature

    feature = _visit_with_path(feature, set_json_type)
    return feature
