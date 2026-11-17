import json
import zipfile

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
    sample_files = write_samples(tmp_path, [10, 2, 1], epochs=2)
    samples = list(Eval()._iter_samples_from_log_files(sample_files))
    expected = [(1, 1), (1, 2), (1, 10), (2, 1), (2, 2), (2, 10)]
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


def write_eval_log(path, samples, status=None):
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("_journal/start.json", json.dumps({"version": 2}))
        for sample in samples:
            archive.writestr(f"samples/{sample['id']}_epoch_{sample['epoch']}.json", json.dumps(sample))
        if status is not None:
            archive.writestr("header.json", json.dumps({"version": 2, "status": status}))


@pytest.mark.parametrize("streaming", [False, True])
def test_load_eval_logs_when_first_log_has_no_samples(tmp_path, streaming):
    # a run that is killed before writing any sample leaves a log with only _journal/start.json
    write_eval_log(tmp_path / "2026-01-01T00-00-00_task_killed.eval", [])
    samples = [{"id": sample_id, "epoch": 1, "input": f"question {sample_id}"} for sample_id in (1, 2)]
    write_eval_log(tmp_path / "2026-01-02T00-00-00_task_success.eval", samples, status="success")
    ds = load_dataset("eval", data_files=str(tmp_path / "*.eval"), split="train", streaming=streaming)
    assert list(ds) == samples
