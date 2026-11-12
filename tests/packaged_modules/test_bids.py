"""Tests for the packaged BIDS dataset builder."""

import json
import shutil
from fnmatch import fnmatch
from types import SimpleNamespace

import numpy as np
import pytest

import datasets
from datasets import Biosignal, Value, load_dataset
from datasets.data_files import get_data_patterns
from datasets.load import infer_module_for_data_files_list
from datasets.packaged_modules.bids import bids


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
    (tmp_path / "bids_like" / "dataset_description.json").write_text('{"Name": "Example", "BIDSVersion": "1.9.0"}')
    assert get_data_patterns(str(tmp_path / "bids_like")) == {"train": ["sub-*/**/sub-*"]}
    assert infer_module_for_data_files_list([str(sub_dir / "sub-01_task-rest_eeg.edf")]) == ("bids", {})
    if datasets.config.MNE_BIDS_AVAILABLE:
        from mne_bids.config import ALLOWED_DATATYPE_EXTENSIONS, EPHY_ALLOWED_DATATYPES

        file_extensions = {ext for dt in EPHY_ALLOWED_DATATYPES for ext in ALLOWED_DATATYPE_EXTENSIONS[dt]}
        assert file_extensions - {".ds", ".mefd"} <= set(bids.EXTENSIONS)  # directories are found through their files

    split_dirs = tmp_path / "split_dirs"
    for d in ("sub-01", "train", "test"):
        (split_dirs / d).mkdir(parents=True)
        (split_dirs / d / "x.csv").write_text("a\n1\n", encoding="utf-8")
    assert set(get_data_patterns(str(split_dirs))) == {"train", "test"}

    non_bids = tmp_path / "non_bids"
    non_bids.mkdir()
    (non_bids / "a.jsonl").write_text('{"x": 1}\n', encoding="utf-8")
    (non_bids / "b.jsonl").write_text('{"x": 2}\n', encoding="utf-8")
    (non_bids / "params.set").write_text("unused", encoding="utf-8")
    assert load_dataset(str(non_bids), split="train")["x"] == [1, 2]

    monkeypatch.setattr(datasets.config, "MNE_BIDS_AVAILABLE", False)
    with pytest.raises(ImportError, match="install 'mne-bids'"):
        load_dataset("bids", data_dir=str(tmp_path / "bids_like"), split="train")


@pytest.mark.parametrize("has_description", [False, True])
def test_bids_pdf_disambiguation(tmp_path, has_description):
    if has_description:
        (tmp_path / "dataset_description.json").write_text('{"Name": "Example", "BIDSVersion": "1.9.0"}')
    recording = tmp_path / "sub-01" / "meg" / "sub-01_task-rest_meg.pdf"
    recording.parent.mkdir(parents=True)
    recording.write_bytes(b"biosignal")
    document = tmp_path / "sub-01" / "documents" / "sub-01_report.pdf"
    document.parent.mkdir()
    document.write_bytes(b"%PDF-1.7")
    assert infer_module_for_data_files_list([str(recording)]) == ("bids" if has_description else "pdffolder", {})
    assert infer_module_for_data_files_list([str(document)]) == ("pdffolder", {})
    misplaced = tmp_path / "prefixsub-01" / "meg" / recording.name
    (tmp_path / "prefix").mkdir()
    (tmp_path / "prefix" / "dataset_description.json").write_text("{}")
    assert infer_module_for_data_files_list([str(misplaced)]) == ("pdffolder", {})
    if not has_description:
        assert get_data_patterns(str(tmp_path)) == {"train": ["**"]}


@require_mne_bids
def test_bids_sidecar_specificity(tmp_path):
    (tmp_path / "dataset_description.json").write_text('{"Name": "Example", "BIDSVersion": "1.9.0"}')
    directory = tmp_path / "sub-01" / "eeg"
    directory.mkdir(parents=True)
    (directory / "sub-01_task-rest_acq-high_eeg.edf").write_bytes(b"recording")
    (tmp_path / "task-rest_eeg.json").write_text('{"PowerLineFrequency": 50}')
    (tmp_path / "acq-high_task-rest_eeg.json").write_text('{"PowerLineFrequency": 60}')
    row = load_dataset(str(tmp_path), decode=False, split="train")[0]
    assert row["metadata"] == {"PowerLineFrequency": 60}
    (directory / "task-rest_eeg.json").write_text('{"EEGReference": "Cz"}')
    row = load_dataset(
        "bids", data_files=[str(directory / "sub-01_task-rest_acq-high_eeg.edf")], decode=False, split="train"
    )[0]
    assert row["metadata"] == {"PowerLineFrequency": 60, "EEGReference": "Cz"}


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
@pytest.mark.parametrize("missing_first", [False, True])
def test_bids_participant_types_across_roots(bids_root, tmp_path, missing_first):
    directory = tmp_path / "second" / "sub-02" / "eeg"
    directory.mkdir(parents=True)
    (tmp_path / "second" / "participants.tsv").write_text("participant_id\tage\nsub-02\tn/a\n")
    missing_age = directory / "sub-02_task-rest_eeg.edf"
    missing_age.write_bytes(b"recording")
    known_age = bids_root / "sub-01/ses-01/eeg/sub-01_ses-01_task-rest_run-01_eeg.vhdr"
    files = [str(missing_age), str(known_age)] if missing_first else [str(known_age), str(missing_age)]
    result = load_dataset("bids", data_files={"train": files[:1], "test": files[1:]}, decode=False)
    assert result["train"].features["age"] == result["test"].features["age"] == Value("int64")
    assert [result[split][0]["age"] for split in ("train", "test")] == ([None, 24] if missing_first else [24, None])


@require_mne_bids
def test_load_bids_streaming_splits_and_parquet(bids_root, tmp_path):
    import mne

    streamed = list(load_dataset(str(bids_root), split="train", streaming=True))
    assert [r["subject"] for r in streamed] == ["01", "01", "02"]
    assert [r["mmse"] for r in streamed] == [29, 29, None]
    assert isinstance(streamed[0]["biosignal"], mne.io.BaseRaw)
    assert list(load_dataset(str(bids_root), subjects="99", split="train", streaming=True)) == []

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
@pytest.mark.parametrize(
    "url", ["hf://datasets/test/bids@revision/", "https://huggingface.co/datasets/test/bids/resolve/revision/"]
)
def test_biosignal_hub_companions_and_sidecars(bids_root, tmp_path, monkeypatch, url):
    import huggingface_hub

    recording = "sub-01/ses-01/eeg/sub-01_ses-01_task-rest_run-01_eeg.vhdr"
    cached = tmp_path / "snapshot"
    requested = []

    def snapshot_download(repo_id, *, repo_type, revision, allow_patterns, token):
        assert (repo_id, repo_type, revision, token) == ("test/bids", "dataset", "revision", "private-token")
        for source in bids_root.rglob("*"):
            if source.is_file() and any(fnmatch(source.relative_to(bids_root).as_posix(), p) for p in allow_patterns):
                relative = source.relative_to(bids_root)
                target = cached / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                requested.append(relative.as_posix())
        return str(cached)

    monkeypatch.setattr(huggingface_hub, "snapshot_download", snapshot_download)
    monkeypatch.setattr(
        huggingface_hub.HfFileSystem,
        "resolve_path",
        lambda self, path: SimpleNamespace(
            repo_id="test/bids", repo_type="dataset", revision="revision", path_in_repo=recording
        ),
    )
    prefix = "datasets/test/bids@revision/"
    monkeypatch.setattr(
        huggingface_hub.HfFileSystem,
        "glob",
        lambda self, pattern: [
            prefix + p.relative_to(bids_root).as_posix() for p in bids_root.glob(pattern[len(prefix) :])
        ],
    )
    monkeypatch.setattr(
        huggingface_hub.HfFileSystem,
        "ls",
        lambda self, directory, detail: [
            prefix + p.relative_to(bids_root).as_posix() for p in (bids_root / directory[len(prefix) :]).iterdir()
        ],
    )

    def single_file_read(*args, **kwargs):
        raise AssertionError("A remote BrainVision recording needs its companion files and BIDS sidecars")

    monkeypatch.setattr("datasets.features.biosignal.xopen", single_file_read)
    raw = Biosignal().decode_example(url + recording, token_per_repo_id={"test/bids": "private-token"})
    assert raw.info["line_freq"] == 50.0 and list(raw.annotations.description) == ["ev_rest"]
    np.testing.assert_allclose(raw.get_data(), 1e-5)
    assert recording.replace(".vhdr", ".eeg") in requested
    assert not any("task-motor" in path and path.endswith(".eeg") for path in requested)
    monkeypatch.setattr(
        huggingface_hub.HfFileSystem,
        "resolve_path",
        lambda self, path: SimpleNamespace(path_in_repo="../../private_raw.fif"),
    )
    with pytest.raises(ValueError, match="must stay inside"):
        Biosignal().decode_example(url + "../../private_raw.fif")


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
    raw.save(str(meg_root / "sub-01" / "meg" / "sub-01_task-rest_proc-sss_meg.fif"), verbose="ERROR")

    meg_rows = {r["processing"]: r for r in load_dataset(str(meg_root), split="train", streaming=True)}
    assert set(meg_rows) == {None, "sss"} and meg_rows[None]["biosignal"].n_times == 20_000
    assert load_dataset(str(meg_root), split="train")[0]["biosignal"].n_times == 20_000

    # Directory-based CTF .ds container discovered via its single .res4 header
    ds_dir = tmp_path / "ctf_bids" / "sub-01" / "meg" / "sub-01_task-rest_meg.ds"
    ds_dir.mkdir(parents=True)
    (tmp_path / "ctf_bids" / "dataset_description.json").write_text('{"Name": "Example", "BIDSVersion": "1.9.0"}')
    (ds_dir / "sub-01_task-rest_meg.res4").write_bytes(b"hdr")
    (ds_dir / "sub-01_task-rest_meg.meg4").write_bytes(b"dat")
    ds_ctf = load_dataset(str(tmp_path / "ctf_bids"), decode=False, split="train", num_proc=2)
    assert len(ds_ctf) == 1 and ds_ctf[0]["extension"] == ".ds"
    assert ds_ctf[0]["biosignal"]["path"].endswith("sub-01_task-rest_meg.ds")
    ds_ctf_pkg = load_dataset("bids", data_dir=str(tmp_path / "ctf_bids"), decode=False, split="train", num_proc=2)
    assert len(ds_ctf_pkg) == 1 and ds_ctf_pkg[0]["extension"] == ".ds"


@require_mne_bids
@pytest.mark.skipif(not datasets.config.NIBABEL_AVAILABLE, reason="nibabel is not installed")
def test_bids_mri_with_eeg_and_sidecar_inheritance(bids_root, tmp_path):
    import mne
    import nibabel as nib

    root = tmp_path / "eeg_fmri"
    shutil.copytree(bids_root, root)
    image = nib.Nifti1Image(np.zeros((2, 2, 2, 3), dtype=np.int16), np.eye(4))
    for rel in [
        "sub-01/ses-01/anat/sub-01_ses-01_T1w.nii.gz",
        "sub-01/ses-01/func/sub-01_ses-01_task-rest_echo-1_bold.nii.gz",
        "derivatives/prep/sub-01/ses-01/func/sub-01_ses-01_task-rest_desc-clean_bold.nii.gz",
    ]:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        image.to_filename(str(root / rel))
    (root / "sub-01/ses-01/eye_tracker").mkdir()  # not a BIDS datatype: skipped
    (root / "sub-01/ses-01/eye_tracker/sub-01_ses-01_task-rest_et.edf").write_bytes(b"x")
    # inheritance: the root sidecar applies to every rest bold run, the run sidecar overrides it
    (root / "task-rest_bold.json").write_text(json.dumps({"RepetitionTime": 2.0, "TaskName": "rest"}))
    (root / "sub-01/ses-01/func/sub-01_ses-01_task-rest_echo-1_bold.json").write_text(
        json.dumps({"RepetitionTime": 1.5, "EchoTime": 0.03})
    )
    (root / "sub-01/ses-01/func/sub-01_ses-01_bold.json").write_text('["n/a"]')  # invalid sidecar: ignored

    ds = load_dataset(str(root), split="train")
    assert {"biosignal", "nifti", "echo", "metadata", "age"} <= set(ds.column_names)
    rows = {(r["subject"], r["suffix"], r["task"]): r for r in ds}
    assert len(rows) == 5 and ("01", "bold", "rest") in rows  # 3 EEG + T1w + bold; derivatives are not raw
    bold = rows["01", "bold", "rest"]
    assert bold["nifti"].shape == (2, 2, 2, 3) and bold["biosignal"] is None
    assert bold["echo"] == "1" and bold["datatype"] == "func" and bold["age"] == 24
    assert bold["metadata"] == {"RepetitionTime": 1.5, "TaskName": "rest", "EchoTime": 0.03}
    assert rows["01", "T1w", None]["metadata"] == {}
    eeg = rows["01", "eeg", "rest"]
    assert isinstance(eeg["biosignal"], mne.io.BaseRaw) and eeg["nifti"] is None
    assert eeg["metadata"]["PowerLineFrequency"] == 50.0
    assert load_dataset("bids", data_dir=str(root), datatypes="func", split="train")["suffix"] == ["bold"]
