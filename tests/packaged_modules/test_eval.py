import json
import zipfile
from pathlib import Path

import pytest

from datasets import load_dataset
from datasets.packaged_modules.eval.eval import Eval


def write_samples(tmp_path, sample_ids, epochs=1):
    samples_dir = tmp_path / "samples"
    samples_dir.mkdir()
    sample_files = []
    for epoch in range(1, epochs + 1):
        for sample_id in sample_ids:
            sample_file = samples_dir / f"{sample_id}_epoch_{epoch}.json"
            sample_file.write_text(json.dumps({"id": sample_id, "epoch": epoch}))
            sample_files.append(str(sample_file))
    return sample_files


def test_iter_samples_sorted_by_epoch_then_int_id(tmp_path):
    sample_files = write_samples(tmp_path, [10, -1, 2, -10, 0, -2, 1], epochs=2)
    samples = list(Eval()._iter_samples_from_log_files(sample_files))
    expected = [(epoch, sample_id) for epoch in (1, 2) for sample_id in (-10, -2, -1, 0, 1, 2, 10)]
    assert [(sample["epoch"], sample["id"]) for sample in samples] == expected


def test_iter_samples_with_str_ids(tmp_path):
    sample_files = write_samples(tmp_path, ["django__django-11099", "astropy__astropy-12907", "a_epoch_b"])
    samples = list(Eval()._iter_samples_from_log_files(sample_files))
    assert [sample["id"] for sample in samples] == ["a_epoch_b", "astropy__astropy-12907", "django__django-11099"]


def test_iter_samples_with_digit_ids_int_rejects(tmp_path):
    # "12³".isdigit() is True but int("12³") raises, so it sorts as a string id
    sample_files = write_samples(tmp_path, ["12³", "10", "2"])
    samples = list(Eval()._iter_samples_from_log_files(sample_files))
    assert [sample["id"] for sample in samples] == ["2", "10", "12³"]


def test_iter_samples_with_numeric_and_other_string_ids(tmp_path):
    sample_ids = ["10", "02", "2", "-2", "-10", "--2", "-", "+2", " 2", "1_0", "a_epoch_b", "12³"]
    sample_files = write_samples(tmp_path, sample_ids)
    samples = list(Eval()._iter_samples_from_log_files(sample_files))
    assert [sample["id"] for sample in samples] == [
        "-10",
        "-2",
        "02",
        "2",
        "10",
        " 2",
        "+2",
        "-",
        "--2",
        "12³",
        "1_0",
        "a_epoch_b",
    ]


@pytest.mark.parametrize("streaming", [False, True])
def test_load_eval_with_negative_int_ids(tmp_path, streaming):
    sample_files = write_samples(tmp_path, [10, -1, 2, -10, 0, -2, 1], epochs=2)
    log_file = tmp_path / "signed.eval"
    with zipfile.ZipFile(log_file, "w") as archive:
        for sample_file in reversed(sample_files):
            archive.write(sample_file, arcname=f"samples/{Path(sample_file).name}")
    ds = load_dataset("eval", data_files=str(log_file), split="train", streaming=streaming)
    expected = [(epoch, sample_id) for epoch in (1, 2) for sample_id in (-10, -2, -1, 0, 1, 2, 10)]
    assert [(sample["epoch"], sample["id"]) for sample in ds] == expected
