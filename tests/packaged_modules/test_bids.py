"""Tests for the packaged BIDS dataset builder."""

import numpy as np
import pytest

import datasets
from datasets import Biosignal, Value, load_dataset


require_mne_bids = pytest.mark.skipif(
    not (datasets.config.MNE_AVAILABLE and datasets.config.MNE_BIDS_AVAILABLE),
    reason="mne and mne_bids are not installed",
)


@pytest.fixture
def bids_root(tmp_path):
    import mne
    import mne_bids

    root = tmp_path / "bids_dataset"
    info = mne.create_info(["Fp1", "Fp2"], sfreq=100.0, ch_types="eeg")
    data = np.ones((2, 100), dtype=np.float64) * 1e-5

    recordings = [
        ("01", "01", "rest", "01", 50.0),
        ("01", "01", "motor", "01", 50.0),
        ("02", "01", "rest", "01", 60.0),
    ]
    for sub, ses, task, run, line_freq in recordings:
        raw = mne.io.RawArray(data.copy(), info.copy(), verbose="ERROR")
        raw.info["line_freq"] = line_freq
        raw.set_annotations(mne.Annotations(onset=[0.1], duration=[0.2], description=[f"ev_{task}"]))
        bp = mne_bids.BIDSPath(
            subject=sub,
            session=ses,
            task=task,
            run=run,
            datatype="eeg",
            suffix="eeg",
            extension=".vhdr",
            root=root,
        )
        mne_bids.write_raw_bids(raw, bp, allow_preload=True, format="BrainVision", overwrite=True, verbose="ERROR")

    (root / "participants.tsv").write_text(
        "participant_id\tage\tsex\nsub-01\t24\tF\nsub-02\t31\tM\n",
        encoding="utf-8",
    )
    return root


@require_mne_bids
def test_load_bids_dataset_from_data_dir_and_auto_infer(bids_root):
    import mne

    ds = load_dataset("bids", data_dir=str(bids_root), split="train")
    assert len(ds) == 3
    assert isinstance(ds.features["biosignal"], Biosignal)
    assert ds.features["subject"] == Value("string")
    assert ds.features["age"] == Value("int64")
    assert ds.features["sex"] == Value("string")

    assert ds["subject"] == ["01", "01", "02"]
    assert ds["task"] == ["motor", "rest", "rest"]
    assert ds["datatype"] == ["eeg", "eeg", "eeg"]
    assert ds["age"] == [24, 24, 31]
    assert ds["sex"] == ["F", "F", "M"]

    raw0 = ds[0]["biosignal"]
    assert isinstance(raw0, mne.io.BaseRaw)
    assert raw0.ch_names == ["Fp1", "Fp2"]
    assert raw0.info["line_freq"] == 50.0
    assert list(raw0.annotations.description) == ["ev_motor"]

    # Also test automatic builder inference from a BIDS folder path (via dataset_description.json)
    ds_auto = load_dataset(str(bids_root), split="train")
    assert len(ds_auto) == 3
    assert ds_auto["subject"] == ["01", "01", "02"]


@require_mne_bids
def test_load_bids_with_entity_filters(bids_root):
    ds_sub01_rest = load_dataset(
        "bids",
        data_dir=str(bids_root),
        subjects="01",
        tasks="rest",
        datatypes="eeg",
        split="train",
    )
    assert len(ds_sub01_rest) == 1
    assert ds_sub01_rest[0]["subject"] == "01"
    assert ds_sub01_rest[0]["task"] == "rest"
    assert ds_sub01_rest[0]["age"] == 24


@require_mne_bids
def test_load_bids_decode_false(bids_root):
    ds = load_dataset("bids", data_dir=str(bids_root), decode=False, split="train")
    assert len(ds) == 3
    item = ds[0]["biosignal"]
    assert isinstance(item, dict)
    assert item["bytes"] is None
    assert item["path"].endswith(".vhdr")


@require_mne_bids
def test_load_bids_explicit_splits_and_parquet_export(bids_root, tmp_path):
    import mne

    sub01_vhdr = str(bids_root / "sub-01" / "ses-01" / "eeg" / "sub-01_ses-01_task-rest_run-01_eeg.vhdr")
    sub02_vhdr = str(bids_root / "sub-02" / "ses-01" / "eeg" / "sub-02_ses-01_task-rest_run-01_eeg.vhdr")

    ds_dict = load_dataset("bids", data_files={"train": [sub01_vhdr], "test": [sub02_vhdr]})
    assert list(ds_dict.keys()) == ["train", "test"]
    assert ds_dict["train"][0]["subject"] == "01"
    assert ds_dict["train"][0]["age"] == 24
    assert ds_dict["test"][0]["subject"] == "02"
    assert ds_dict["test"][0]["age"] == 31

    # Verify Parquet export (used by push_to_hub for NEMAR / eegdash datasets)
    parquet_file = tmp_path / "train.parquet"
    ds_dict["train"].to_parquet(str(parquet_file))
    reloaded = load_dataset("parquet", data_files=str(parquet_file), split="train")
    assert reloaded[0]["subject"] == "01"
    assert reloaded[0]["task"] == "rest"
    raw = reloaded[0]["biosignal"]
    assert isinstance(raw, mne.io.BaseRaw)
    assert list(raw.annotations.description) == ["ev_rest"]


@require_mne_bids
def test_load_bids_without_dataset_description_and_ignores_sourcedata(bids_root, tmp_path):
    import shutil

    partial_root = tmp_path / "partial_bids"
    shutil.copytree(bids_root, partial_root)
    (partial_root / "dataset_description.json").unlink()

    # Add a nested sourcedata directory with its own dataset_description.json to bids_root
    sourcedata_dir = bids_root / "sourcedata" / "sub-99" / "eeg"
    sourcedata_dir.mkdir(parents=True)
    (bids_root / "sourcedata" / "dataset_description.json").write_text('{"Name": "raw source"}', encoding="utf-8")
    for f in (bids_root / "sub-01" / "ses-01" / "eeg").iterdir():
        shutil.copy(f, sourcedata_dir / f.name.replace("sub-01", "sub-99"))

    ds_with_sourcedata = load_dataset(str(bids_root), split="train")
    assert len(ds_with_sourcedata) == 3
    assert "99" not in ds_with_sourcedata["subject"]

    # Partial BIDS download without dataset_description.json still auto-infers "bids" and attaches sidecars
    ds_partial = load_dataset(str(partial_root), split="train")
    assert len(ds_partial) == 3
    assert list(ds_partial[0]["biosignal"].annotations.description) == ["ev_motor"]
