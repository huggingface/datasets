import pytest

def parse_dataset_identifier(identifier: str) -> tuple[str, str]:
    cleaned = identifier.strip()
    if "/" in cleaned:
        org, name = cleaned.split("/", 1)
        return org.strip(), name.strip()
    return "", cleaned

def test_parse_namespaced_dataset():
    assert parse_dataset_identifier("glue/sst2") == ("glue", "sst2")
    assert parse_dataset_identifier("  squad/v2  ") == ("squad", "v2")

def test_parse_flat_dataset():
    assert parse_dataset_identifier("imdb") == ("", "imdb")
