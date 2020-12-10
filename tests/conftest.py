import json
import lzma

import pytest


FILE_CONTENT = """\
    Text data.
    Second line of data."""


@pytest.fixture(scope="session")
def text_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.txt"
    data = FILE_CONTENT
    with open(filename, "w") as f:
        f.write(data)
    return filename


@pytest.fixture(scope="session")
def xz_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.xz"
    data = bytes(FILE_CONTENT, "utf-8")
    with lzma.open(filename, "wb") as f:
        f.write(data)
    return filename


@pytest.fixture(scope="session")
def json_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.json"
    data = {
        "data-1": [
            {"title": "title-1", "text": "text-1"},
            {"title": "title-2", "text": "text-2"},
            {"title": "title-3", "text": "text-3"},
        ],
        "data-2": {
            "lemmas": ["lemma-1", "lemma-2", "lemma-3"],
            "tokens": ["token-1", "token-2", "token-3"],
        },
        "data-3": {
            "terms": {
                "lemmas": ["lemma-1", "lemma-2", "lemma-3"],
                "tokens": ["token-1", "token-2", "token-3"],
            },
            "opinions": {
                "polarities": ["polarity-1", "polarity-2", "polarity-3"],
                "intensities": ["intensity-1", "intensity-2", "intensity-3"],
            },
        },
    }
    with open(filename, "w") as f:
        json.dump(data, f)
    return filename
