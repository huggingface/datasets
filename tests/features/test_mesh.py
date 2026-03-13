import os
from pathlib import Path

import pyarrow as pa
import pytest

from datasets import Column, Dataset, Features, Mesh, Sequence, Value, concatenate_datasets
from datasets.features.features import require_decoding


def test_mesh_instantiation():
    mesh = Mesh()
    assert mesh.id is None
    assert mesh.pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert mesh._type == "Mesh"


def test_mesh_feature_type_to_arrow():
    features = Features({"mesh": Mesh()})
    assert features.arrow_schema == pa.schema({"mesh": Mesh().pa_type})
    features = Features({"struct_containing_a_mesh": {"mesh": Mesh()}})
    assert features.arrow_schema == pa.schema({"struct_containing_a_mesh": pa.struct({"mesh": Mesh().pa_type})})
    features = Features({"sequence_of_meshes": Sequence(Mesh())})
    assert features.arrow_schema == pa.schema({"sequence_of_meshes": pa.list_(Mesh().pa_type)})


@pytest.mark.parametrize(
    "build_example",
    [
        lambda mesh_path: mesh_path,
        lambda mesh_path: Path(mesh_path),
        lambda mesh_path: open(mesh_path, "rb").read(),
        lambda mesh_path: {"path": mesh_path},
        lambda mesh_path: {"path": mesh_path, "bytes": None},
        lambda mesh_path: {"path": mesh_path, "bytes": open(mesh_path, "rb").read()},
        lambda mesh_path: {"path": None, "bytes": open(mesh_path, "rb").read()},
        lambda mesh_path: {"bytes": open(mesh_path, "rb").read()},
    ],
)
def test_mesh_feature_encode_example(mesh_file, build_example):
    mesh = Mesh()
    encoded_example = mesh.encode_example(build_example(mesh_file))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None


def test_mesh_decode_example(mesh_file):
    mesh = Mesh()
    with open(mesh_file, "rb") as f:
        mesh_bytes = f.read()

    # Decoding should just return the raw dict
    decoded_example = mesh.decode_example({"path": mesh_file, "bytes": None})
    assert isinstance(decoded_example, dict)
    assert decoded_example["path"] == mesh_file
    assert decoded_example["bytes"] == mesh_bytes

    with pytest.raises(RuntimeError):
        Mesh(decode=False).decode_example({"path": mesh_file, "bytes": None})


def test_dataset_with_mesh_feature(mesh_file):
    data = {"mesh": [mesh_file]}
    features = Features({"mesh": Mesh()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"mesh"}
    assert isinstance(item["mesh"], dict)
    assert item["mesh"]["path"] == mesh_file
    with open(mesh_file, "rb") as f:
        assert item["mesh"]["bytes"] == f.read()

    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"mesh"}
    assert isinstance(batch["mesh"], list)
    assert batch["mesh"][0]["path"] == mesh_file

    column = dset["mesh"]
    assert len(column) == 1
    assert isinstance(column, Column)
    assert column[0]["path"] == mesh_file


def test_dataset_cast_to_mesh_features(mesh_file):
    data = {"mesh": [mesh_file]}
    dset = Dataset.from_dict(data)
    dset = dset.cast(Features({"mesh": Mesh()}))
    item = dset[0]
    assert isinstance(item["mesh"], dict)
    assert item["mesh"]["path"] == mesh_file


def test_dataset_concatenate_mesh_features(mesh_file):
    data1 = {"mesh": [mesh_file]}
    dset1 = Dataset.from_dict(data1, features=Features({"mesh": Mesh()}))
    with open(mesh_file, "rb") as f:
        data2 = {"mesh": [{"bytes": f.read()}]}
    dset2 = Dataset.from_dict(data2, features=Features({"mesh": Mesh()}))
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == 2
    assert concatenated_dataset[0]["mesh"]["path"] == dset1[0]["mesh"]["path"]
    assert concatenated_dataset[1]["mesh"]["bytes"] == dset2[0]["mesh"]["bytes"]


def test_require_decoding():
    assert require_decoding(Mesh())


def test_mesh_embed_storage(mesh_file):
    features = Features({"mesh": Mesh()})

    with open(mesh_file, "rb") as f:
        content = f.read()

    # Test bytes are embedded
    storage = features["mesh"].embed_storage(pa.array([{"path": mesh_file, "bytes": None}]))
    assert storage.to_pylist() == [{"path": os.path.basename(mesh_file), "bytes": content}]
