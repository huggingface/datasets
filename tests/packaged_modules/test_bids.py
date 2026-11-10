"""Tests for the packaged BIDS dataset builder."""

import shutil

import numpy as np
import pytest

import datasets
from datasets import Biosignal, Value, load_dataset
from datasets.data_files import get_data_patterns


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
        "participant_id\tage\tsex\tmmse\nsub-01\t24\tF\t29\nsub-02\t31\tM\tn/a\n", encoding="utf-8"
    )
    return root


def test_bids_patterns_and_module_inference(tmp_path, monkeypatch):
    sub_dir = tmp_path / "bids_like" / "sub-01" / "eeg"
    sub_dir.mkdir(parents=True)
    (sub_dir / "sub-01_task-rest_eeg.edf").write_bytes(b"x")
    assert get_data_patterns(str(tmp_path / "bids_like")) == {"train": ["sub-*/**"]}

    non_bids = tmp_path / "non_bids"
    non_bids.mkdir()
    (non_bids / "a.jsonl").write_text('{"x": 1}\n', encoding="utf-8")
    (non_bids / "b.jsonl").write_text('{"x": 2}\n', encoding="utf-8")
    (non_bids / "params.set").write_text("unused", encoding="utf-8")
    assert load_dataset(str(non_bids), split="train")["x"] == [1, 2]

    monkeypatch.setattr(datasets.config, "MNE_BIDS_AVAILABLE", False)
    with pytest.raises(ImportError, match="install 'mne-bids'"):
        load_dataset("bids", data_dir=str(tmp_path / "bids_like"), split="train")


@require_mne_bids
@pytest.mark.parametrize(
    "use_auto_path,kwargs,expected_subjects,expected_tasks",
    [
        (False, {}, ["01", "01", "02"], ["motor", "rest", "rest"]),
        (True, {}, ["01", "01", "02"], ["motor", "rest", "rest"]),
        (False, {"subjects": "01", "tasks": "rest", "datatypes": "eeg"}, ["01"], ["rest"]),
        (False, {"subjects": "02", "num_proc": 2}, ["02"], ["rest"]),
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
    assert ds.features["age"] == Value("int64") and ds.features["mmse"] == Value("int64")

    first = ds[0]["biosignal"]
    if kwargs.get("decode", True):
        assert isinstance(first, mne.io.BaseRaw)
        assert first.info["line_freq"] == (60.0 if expected_subjects[0] == "02" else 50.0)
        assert list(first.annotations.description) == [f"ev_{expected_tasks[0]}"]
    else:
        assert isinstance(first, dict) and first["bytes"] is None and first["path"].endswith(".vhdr")


@require_mne_bids
def test_load_bids_streaming_archive_splits_and_parquet(bids_root, tmp_path):
    import mne

    streamed = list(load_dataset(str(bids_root), split="train", streaming=True))
    assert [r["subject"] for r in streamed] == ["01", "01", "02"]
    assert [r["mmse"] for r in streamed] == [29, 29, None]
    assert isinstance(streamed[0]["biosignal"], mne.io.BaseRaw)
    assert list(load_dataset(str(bids_root), subjects="99", split="train", streaming=True)) == []

    zip_file = shutil.make_archive(str(tmp_path / "bids_archive"), "zip", root_dir=bids_root)
    ds_zip = load_dataset("bids", data_files=zip_file, split="train")
    assert ds_zip["subject"] == ["01", "01", "02"] and ds_zip["mmse"] == [29, 29, None]
    zip_stream = list(load_dataset("bids", data_files=zip_file, decode=False, split="train", streaming=True))
    assert [r["mmse"] for r in zip_stream] == [29, 29, None]

    sub01 = str(bids_root / "sub-01" / "ses-01" / "eeg" / "sub-01_ses-01_task-rest_run-01_eeg.vhdr")
    sub02 = str(bids_root / "sub-02" / "ses-01" / "eeg" / "sub-02_ses-01_task-rest_run-01_eeg.vhdr")
    ds_dict = load_dataset("bids", data_files={"train": [sub01], "test": [sub02]})
    assert ds_dict["train"][0]["mmse"] == 29 and ds_dict["test"][0]["mmse"] is None
    assert ds_dict["train"].features == ds_dict["test"].features

    parquet_file = tmp_path / "train.parquet"
    ds_dict["train"].to_parquet(str(parquet_file))
    raw = load_dataset("parquet", data_files=str(parquet_file), split="train")[0]["biosignal"]
    assert isinstance(raw, mne.io.BaseRaw) and list(raw.annotations.description) == ["ev_rest"]

    work_root = tmp_path / "bids_copy"
    shutil.copytree(bids_root, work_root)
    sourcedata_dir = work_root / "sourcedata" / "sub-99" / "eeg"
    sourcedata_dir.mkdir(parents=True)
    (work_root / "sourcedata" / "dataset_description.json").write_text('{"Name": "raw"}', encoding="utf-8")
    for f in (work_root / "sub-01" / "ses-01" / "eeg").iterdir():
        shutil.copy(f, sourcedata_dir / f.name.replace("sub-01", "sub-99"))
    assert "99" not in load_dataset(str(work_root), split="train", num_proc=2)["subject"]

    shutil.rmtree(work_root / "sourcedata")
    (work_root / "dataset_description.json").unlink()
    ds_partial = load_dataset(str(work_root), split="train")
    assert len(ds_partial) == 3 and list(ds_partial[0]["biosignal"].annotations.description) == ["ev_motor"]


@require_mne_bids
def test_bids_meg_splits_crosstalk_and_containers(tmp_path):
    import mne
    import mne_bids

    meg_root = tmp_path / "meg_bids"
    info = mne.create_info([f"MEG{i:04d}" for i in range(20)], sfreq=1000.0, ch_types="mag")
    raw = mne.io.RawArray(np.ones((20, 20_000), dtype=np.float64) * 1e-12, info, verbose="ERROR")
    bp = mne_bids.BIDSPath(subject="01", task="rest", datatype="meg", suffix="meg", extension=".fif", root=meg_root)
    mne_bids.write_raw_bids(raw, bp, allow_preload=True, format="FIF", overwrite=True, verbose="ERROR")
    # Re-save as split FIF chunks (split-01 + split-02) plus an acq-crosstalk calibration file
    unsplit_fpath = meg_root / "sub-01" / "meg" / "sub-01_task-rest_meg.fif"
    unsplit_fpath.unlink()
    raw.save(str(unsplit_fpath), split_size=1_200_000, split_naming="bids", overwrite=True, verbose="ERROR")
    assert (meg_root / "sub-01" / "meg" / "sub-01_task-rest_split-01_meg.fif").exists()
    assert (meg_root / "sub-01" / "meg" / "sub-01_task-rest_split-02_meg.fif").exists()
    (meg_root / "sub-01" / "meg" / "sub-01_acq-crosstalk_meg.fif").write_bytes(b"crosstalk")

    ds_meg = load_dataset(str(meg_root), split="train")
    assert len(ds_meg) == 1 and ds_meg[0]["biosignal"].n_times == 20_000

    # Directory-based CTF .ds container discovered via its single .res4 header
    ds_dir = tmp_path / "ctf_bids" / "sub-01" / "meg" / "sub-01_task-rest_meg.ds"
    ds_dir.mkdir(parents=True)
    (ds_dir / "sub-01_task-rest_meg.res4").write_bytes(b"hdr")
    (ds_dir / "sub-01_task-rest_meg.meg4").write_bytes(b"dat")
    ds_ctf = load_dataset(str(tmp_path / "ctf_bids"), decode=False, split="train", num_proc=2)
    assert len(ds_ctf) == 1 and ds_ctf[0]["extension"] == ".ds"
    assert ds_ctf[0]["biosignal"]["path"].endswith("sub-01_task-rest_meg.ds")
