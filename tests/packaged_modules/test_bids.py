"""Tests for the packaged BIDS dataset builder."""

import shutil

import numpy as np
import pytest

import datasets
from datasets import Biosignal, Value, load_dataset


require_mne_bids = pytest.mark.skipif(
    not (datasets.config.MNE_AVAILABLE and datasets.config.MNE_BIDS_AVAILABLE),
    reason="mne and mne_bids are not installed",
)


@pytest.fixture(scope="module")
def bids_root(tmp_path_factory):
    import mne
    import mne_bids

    root = tmp_path_factory.mktemp("bids_dataset")
    info = mne.create_info(["Fp1", "Fp2"], sfreq=100.0, ch_types="eeg")
    data = np.ones((2, 100), dtype=np.float64) * 1e-5

    for sub, ses, task, run, line_freq in [
        ("01", "01", "rest", "01", 50.0),
        ("01", "01", "motor", "01", 50.0),
        ("02", "01", "rest", "01", 60.0),
    ]:
        raw = mne.io.RawArray(data.copy(), info.copy(), verbose="ERROR")
        raw.info["line_freq"] = line_freq
        raw.set_annotations(mne.Annotations(onset=[0.1], duration=[0.2], description=[f"ev_{task}"]))
        bp = mne_bids.BIDSPath(
            subject=sub, session=ses, task=task, run=run, datatype="eeg", suffix="eeg", extension=".vhdr", root=root
        )
        mne_bids.write_raw_bids(raw, bp, allow_preload=True, format="BrainVision", overwrite=True, verbose="ERROR")

    (root / "participants.tsv").write_text(
        "participant_id\tage\tsex\nsub-01\t24\tF\nsub-02\t31\tM\n", encoding="utf-8"
    )
    return root


@require_mne_bids
@pytest.mark.parametrize(
    "use_auto_path,kwargs,expected_subjects,expected_tasks",
    [
        (False, {}, ["01", "01", "02"], ["motor", "rest", "rest"]),
        (True, {}, ["01", "01", "02"], ["motor", "rest", "rest"]),
        (False, {"subjects": "01", "tasks": "rest", "datatypes": "eeg"}, ["01"], ["rest"]),
        (False, {"decode": False}, ["01", "01", "02"], ["motor", "rest", "rest"]),
    ],
)
def test_load_bids_parametrized(bids_root, use_auto_path, kwargs, expected_subjects, expected_tasks):
    import mne

    ds = (
        load_dataset(str(bids_root), split="train", **kwargs)
        if use_auto_path
        else load_dataset("bids", data_dir=str(bids_root), split="train", **kwargs)
    )
    assert ds["subject"] == expected_subjects and ds["task"] == expected_tasks
    assert isinstance(ds.features["biosignal"], Biosignal)
    assert ds.features["age"] == Value("int64") and ds.features["sex"] == Value("string")

    first = ds[0]["biosignal"]
    if kwargs.get("decode", True):
        assert isinstance(first, mne.io.BaseRaw)
        assert first.info["line_freq"] == 50.0 and list(first.annotations.description) == [f"ev_{expected_tasks[0]}"]
    else:
        assert isinstance(first, dict) and first["bytes"] is None and first["path"].endswith(".vhdr")


@require_mne_bids
def test_load_bids_splits_parquet_and_sourcedata(bids_root, tmp_path):
    import mne

    sub01 = str(bids_root / "sub-01" / "ses-01" / "eeg" / "sub-01_ses-01_task-rest_run-01_eeg.vhdr")
    sub02 = str(bids_root / "sub-02" / "ses-01" / "eeg" / "sub-02_ses-01_task-rest_run-01_eeg.vhdr")
    ds_dict = load_dataset("bids", data_files={"train": [sub01], "test": [sub02]})
    assert ds_dict["train"][0]["subject"] == "01" and ds_dict["test"][0]["age"] == 31

    parquet_file = tmp_path / "train.parquet"
    ds_dict["train"].to_parquet(str(parquet_file))
    reloaded = load_dataset("parquet", data_files=str(parquet_file), split="train")
    raw = reloaded[0]["biosignal"]
    assert isinstance(raw, mne.io.BaseRaw) and list(raw.annotations.description) == ["ev_rest"]

    work_root = tmp_path / "bids_copy"
    shutil.copytree(bids_root, work_root)
    sourcedata_dir = work_root / "sourcedata" / "sub-99" / "eeg"
    sourcedata_dir.mkdir(parents=True)
    (work_root / "sourcedata" / "dataset_description.json").write_text('{"Name": "raw"}', encoding="utf-8")
    for f in (work_root / "sub-01" / "ses-01" / "eeg").iterdir():
        shutil.copy(f, sourcedata_dir / f.name.replace("sub-01", "sub-99"))
    assert "99" not in load_dataset(str(work_root), split="train")["subject"]

    shutil.rmtree(work_root / "sourcedata")
    (work_root / "dataset_description.json").unlink()
    ds_partial = load_dataset(str(work_root), split="train")
    assert len(ds_partial) == 3 and list(ds_partial[0]["biosignal"].annotations.description) == ["ev_motor"]
