import json
import os
import tempfile

from datasets import load_dataset


def _make_json_file():
    tmp_dir = tempfile.mkdtemp()
    path = os.path.join(tmp_dir, "data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            [
                {"question": "什么是RAG？", "answer": "检索增强生成"},
                {"question": "什么是LoRA？", "answer": "低秩适配"},
            ],
            f,
            ensure_ascii=False,
        )
    return path


def test_return_file_name_enabled():
    ds = load_dataset("json", data_files=_make_json_file(), return_file_name=True)
    assert "file_name" in ds["train"].column_names
    assert ds["train"][0]["file_name"].endswith("data.json")


def test_return_file_name_disabled_by_default():
    ds = load_dataset("json", data_files=_make_json_file())
    assert "file_name" not in ds["train"].column_names
