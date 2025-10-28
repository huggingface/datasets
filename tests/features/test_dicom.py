from pathlib import Path

import pytest

from datasets import Dataset, Dicom, Features
from src.datasets.features.dicom import encode_pydicom_dataset

from ..utils import require_pydicom


@require_pydicom
@pytest.mark.parametrize(
    "build_example",
    [
        lambda dicom_path: dicom_path,
        lambda dicom_path: Path(dicom_path),
        lambda dicom_path: open(dicom_path, "rb").read(),
        lambda dicom_path: {"path": dicom_path},
        lambda dicom_path: {"path": dicom_path, "bytes": None},
        lambda dicom_path: {"path": dicom_path, "bytes": open(dicom_path, "rb").read()},
        lambda dicom_path: {"path": None, "bytes": open(dicom_path, "rb").read()},
        lambda dicom_path: {"bytes": open(dicom_path, "rb").read()},
    ],
)
def test_dicom_feature_encode_example(tmp_path, build_example):
    import pydicom
    from pydicom import examples

    dicom_path = str(tmp_path / "test_example_dicom.dcm")
    ds = examples.ct
    ds.save_as(dicom_path, write_like_original=False)

    dicom = Dicom()
    encoded_example = dicom.encode_example(build_example(dicom_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = dicom.decode_example(encoded_example)
    assert isinstance(decoded_example, pydicom.dataset.FileDataset)


@require_pydicom
def test_dataset_with_dicom_feature(tmp_path):
    import pydicom
    from pydicom import examples

    dicom_path = str(tmp_path / "test_example_dicom.dcm")
    ds = examples.mr
    ds.save_as(dicom_path, write_like_original=False)

    data = {"dicom": [dicom_path]}
    features = Features({"dicom": Dicom()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"dicom"}
    assert isinstance(item["dicom"], pydicom.dataset.FileDataset)
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"dicom"}
    assert isinstance(batch["dicom"], list) and all(
        isinstance(item, pydicom.dataset.FileDataset) for item in batch["dicom"]
    )
    column = dset["dicom"]
    assert len(column) == 1
    assert all(isinstance(item, pydicom.dataset.FileDataset) for item in column)

    # from bytes
    with open(dicom_path, "rb") as f:
        data = {"dicom": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"dicom"}
    assert isinstance(item["dicom"], pydicom.dataset.FileDataset)


@require_pydicom
def test_dataset_cast_dicom_column(shared_datadir):
    """Test the example from the Dicom docstring using shared_datadir"""
    import pydicom

    # File take from: https://github.com/robyoung/dicom-test-files/blob/master/data/pydicom/693_J2KI.dcm
    dicom_path = str(shared_datadir / "test_dicom_693_J2KI.dcm")

    # decode=True (default)
    ds = Dataset.from_dict({"dicom": [dicom_path]}).cast_column("dicom", Dicom())
    assert ds.features["dicom"] == Dicom(decode=True, id=None)
    assert isinstance(ds[0]["dicom"], pydicom.dataset.FileDataset)

    # decode=False
    ds = ds.cast_column("dicom", Dicom(decode=False))
    assert ds.features["dicom"] == Dicom(decode=False, id=None)
    decoded_item = ds[0]["dicom"]
    assert isinstance(decoded_item, dict)
    assert decoded_item.keys() == {"bytes", "path"}
    assert decoded_item["path"] == dicom_path
    assert decoded_item["bytes"] is None


@require_pydicom
def test_dicom_force_parameter(shared_datadir):
    """Test loading DICOM file that requires force=True"""
    import pydicom

    # File from: https://github.com/pydicom/pydicom/blob/main/src/pydicom/data/test_files/no_meta.dcm
    # This file is missing DICOM File Meta Information header but can be read using force=True
    dicom_path = str(shared_datadir / "test_dicom_no_meta.dcm")

    ds_no_force = Dataset.from_dict({"dicom": [dicom_path]}).cast_column("dicom", Dicom(force=False))
    with pytest.raises(pydicom.errors.InvalidDicomError):
        item = ds_no_force[0]

    ds_with_force = Dataset.from_dict({"dicom": [dicom_path]}).cast_column("dicom", Dicom(force=True))
    item = ds_with_force[0]
    assert isinstance(item["dicom"], pydicom.dataset.FileDataset)


@require_pydicom
def test_encode_pydicom_dataset(tmp_path):
    import pydicom
    from pydicom import examples

    dicom_path = str(tmp_path / "test_example_dicom.dcm")
    ds = examples.rt_ss
    ds.save_as(dicom_path, write_like_original=False)

    img = pydicom.dcmread(dicom_path)
    encoded_example = encode_pydicom_dataset(img)
    dicom = Dicom()
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["path"] is not None and encoded_example["bytes"] is None
    decoded_example = dicom.decode_example(encoded_example)
    assert isinstance(decoded_example, pydicom.dataset.FileDataset)

    # test bytes only
    img.filename = None
    encoded_example_bytes = encode_pydicom_dataset(img)
    assert encoded_example_bytes["bytes"] is not None
    assert encoded_example_bytes["path"] is None
    decoded_example_bytes = dicom.decode_example(encoded_example_bytes)
    assert isinstance(decoded_example_bytes, pydicom.dataset.FileDataset)
