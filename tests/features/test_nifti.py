## taken from: https://github.com/yarikoptic/nitest-balls1/blob/2cd07d86e2cc2d3c612d5d4d659daccd7a58f126/NIFTI/T1.nii.gz

from pathlib import Path

import pyarrow as pa
import pytest

from datasets import Dataset, Features, Nifti
from src.datasets.features.nifti import encode_nibabel_image

from ..utils import require_nibabel


@require_nibabel
@pytest.mark.parametrize("nifti_file", ["test_nifti.nii", "test_nifti.nii.gz"])
@pytest.mark.parametrize(
    "build_example",
    [
        lambda nifti_path: nifti_path,
        lambda nifti_path: Path(nifti_path),
        lambda nifti_path: open(nifti_path, "rb").read(),
        lambda nifti_path: {"path": nifti_path},
        lambda nifti_path: {"path": nifti_path, "bytes": None},
        lambda nifti_path: {"path": nifti_path, "bytes": open(nifti_path, "rb").read()},
        lambda nifti_path: {"path": None, "bytes": open(nifti_path, "rb").read()},
        lambda nifti_path: {"bytes": open(nifti_path, "rb").read()},
    ],
)
def test_nifti_feature_encode_example(shared_datadir, nifti_file, build_example):
    import nibabel

    nifti_path = str(shared_datadir / nifti_file)
    nifti = Nifti()
    encoded_example = nifti.encode_example(build_example(nifti_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = nifti.decode_example(encoded_example)
    assert isinstance(decoded_example, nibabel.nifti1.Nifti1Image)


@require_nibabel
@pytest.mark.parametrize("nifti_file", ["test_nifti.nii", "test_nifti.nii.gz"])
def test_dataset_with_nifti_feature(shared_datadir, nifti_file):
    import nibabel

    nifti_path = str(shared_datadir / nifti_file)
    data = {"nifti": [nifti_path]}
    features = Features({"nifti": Nifti()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"nifti"}
    assert isinstance(item["nifti"], nibabel.nifti1.Nifti1Image)
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"nifti"}
    assert isinstance(batch["nifti"], list) and all(
        isinstance(item, nibabel.nifti1.Nifti1Image) for item in batch["nifti"]
    )
    column = dset["nifti"]
    assert len(column) == 1
    assert all(isinstance(item, nibabel.nifti1.Nifti1Image) for item in column)

    # from bytes
    with open(nifti_path, "rb") as f:
        data = {"nifti": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"nifti"}
    assert isinstance(item["nifti"], nibabel.nifti1.Nifti1Image)


@require_nibabel
def test_encode_nibabel_image(shared_datadir):
    import nibabel

    nifti_path = str(shared_datadir / "test_nifti.nii")
    img = nibabel.load(nifti_path)
    encoded_example = encode_nibabel_image(img)
    nifti = Nifti()
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["path"] is not None and encoded_example["bytes"] is None
    decoded_example = nifti.decode_example(encoded_example)
    assert isinstance(decoded_example, nibabel.nifti1.Nifti1Image)

    # test bytes only
    img.file_map = None
    encoded_example_bytes = encode_nibabel_image(img)
    assert isinstance(encoded_example_bytes, dict)
    assert encoded_example_bytes["bytes"] is not None and encoded_example_bytes["path"] is None
    # this cannot be converted back from bytes (yet)


@require_nibabel
def test_embed_storage(shared_datadir):
    import nibabel

    nifti_path = str(shared_datadir / "test_nifti.nii")
    img = nibabel.load(nifti_path)
    nifti = Nifti()

    bytes_array = pa.array([None], type=pa.binary())
    path_array = pa.array([nifti_path], type=pa.string())
    storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"])

    embedded_storage = nifti.embed_storage(storage)

    embedded_bytes = embedded_storage[0]["bytes"].as_py()
    original_bytes = img.to_bytes()

    assert embedded_bytes is not None
    assert embedded_bytes == original_bytes
