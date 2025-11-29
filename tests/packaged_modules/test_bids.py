import json

import numpy as np
import pytest

import datasets.config


@pytest.fixture
def minimal_bids_dataset(tmp_path):
    """Minimal valid BIDS dataset with one subject, one T1w scan."""
    # dataset_description.json (required)
    (tmp_path / "dataset_description.json").write_text(
        json.dumps({"Name": "Test BIDS Dataset", "BIDSVersion": "1.10.1"})
    )

    # Create subject/anat folder
    anat_dir = tmp_path / "sub-01" / "anat"
    anat_dir.mkdir(parents=True)

    # Create dummy NIfTI
    if datasets.config.NIBABEL_AVAILABLE:
        import nibabel as nib

        data = np.zeros((4, 4, 4), dtype=np.float32)
        img = nib.Nifti1Image(data, np.eye(4))
        nib.save(img, str(anat_dir / "sub-01_T1w.nii.gz"))
    else:
        # Fallback if nibabel not available (shouldn't happen in test env ideally)
        (anat_dir / "sub-01_T1w.nii.gz").write_bytes(b"DUMMY NIFTI CONTENT")

    # JSON sidecar
    (anat_dir / "sub-01_T1w.json").write_text(json.dumps({"RepetitionTime": 2.0}))

    return str(tmp_path)


@pytest.fixture
def multi_subject_bids(tmp_path):
    """BIDS dataset with multiple subjects and sessions."""
    (tmp_path / "dataset_description.json").write_text(
        json.dumps({"Name": "Multi-Subject Test", "BIDSVersion": "1.10.1"})
    )

    data = np.zeros((4, 4, 4), dtype=np.float32)

    if datasets.config.NIBABEL_AVAILABLE:
        import nibabel as nib
    else:
        nib = None

    for sub in ["01", "02"]:
        for ses in ["baseline", "followup"]:
            anat_dir = tmp_path / f"sub-{sub}" / f"ses-{ses}" / "anat"
            anat_dir.mkdir(parents=True)

            file_path = anat_dir / f"sub-{sub}_ses-{ses}_T1w.nii.gz"
            if nib:
                img = nib.Nifti1Image(data, np.eye(4))
                nib.save(img, str(file_path))
            else:
                file_path.write_bytes(b"DUMMY NIFTI CONTENT")

            (anat_dir / f"sub-{sub}_ses-{ses}_T1w.json").write_text(json.dumps({"RepetitionTime": 2.0}))

    return str(tmp_path)


def test_bids_module_imports():
    from datasets.packaged_modules.bids import Bids, BidsConfig

    assert Bids is not None
    assert BidsConfig is not None


def test_bids_requires_pybids(monkeypatch):
    """Test helpful error when pybids not installed."""
    import datasets.config
    from datasets.packaged_modules.bids.bids import Bids

    monkeypatch.setattr(datasets.config, "PYBIDS_AVAILABLE", False)

    with pytest.raises(ImportError, match="pybids"):
        Bids()


@pytest.mark.skipif(not datasets.config.PYBIDS_AVAILABLE, reason="pybids not installed")
def test_bids_loads_single_subject(minimal_bids_dataset):
    from datasets import load_dataset

    ds = load_dataset("bids", data_dir=minimal_bids_dataset)

    assert "train" in ds
    assert len(ds["train"]) == 1

    sample = ds["train"][0]
    assert sample["subject"] == "01"
    assert sample["suffix"] == "T1w"
    assert sample["datatype"] == "anat"
    assert sample["session"] is None


@pytest.mark.skipif(not datasets.config.PYBIDS_AVAILABLE, reason="pybids not installed")
def test_bids_multi_subject(multi_subject_bids):
    from datasets import load_dataset

    ds = load_dataset("bids", data_dir=multi_subject_bids)

    assert len(ds["train"]) == 4  # 2 subjects × 2 sessions

    subjects = {sample["subject"] for sample in ds["train"]}
    assert subjects == {"01", "02"}

    sessions = {sample["session"] for sample in ds["train"]}
    assert sessions == {"baseline", "followup"}
