import pytest
from datasets import load_dataset


def test_load_and_schema_local_dummy():
    dset = load_dataset(
        path="wikipedia_2023_redirects",
        name="default",
        split="train",
    )
    assert len(dset) == 1

    ex = dset[0]
    assert set(ex.keys()) == {
        "id",
        "title",
        "url",
        "text",
        "redirects",
        "pageviews_2023",
        "timestamp",
    }
    assert ex["title"] == "Python (programming language)"
    assert "Py" in ex["redirects"]
    assert ex["pageviews_2023"] == 42


def test_streaming_dummy():
    dset = load_dataset(
        path="wikipedia_2023_redirects",
        name="default",
        split="train",
        streaming=True,
    )
    it = iter(dset)
    ex = next(it)
    assert ex["title"] == "Python (programming language)"
    assert "Py" in ex["redirects"]
    assert ex["pageviews_2023"] == 42
