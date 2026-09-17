from pathlib import Path

import pyarrow as pa
import pytest

from datasets import Column, Dataset, Features, Mesh, Sequence, concatenate_datasets
from datasets.features.features import require_decoding

from ..utils import require_trimesh


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
def test_mesh_feature_encode_example(shared_datadir, build_example):
    mesh_path = str(shared_datadir / "test_mesh_glb.glb")
    mesh = Mesh()
    encoded_example = mesh.encode_example(build_example(mesh_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None


@require_trimesh
def test_mesh_decode_example(shared_datadir):
    import trimesh

    mesh_path = str(shared_datadir / "test_mesh_glb.glb")
    mesh = Mesh()
    with open(mesh_path, "rb") as f:
        mesh_bytes = f.read()

    decoded_example = mesh.decode_example({"path": mesh_path, "bytes": None})
    assert isinstance(decoded_example, (trimesh.Trimesh, trimesh.Scene))

    decoded_example = mesh.decode_example({"path": mesh_path, "bytes": mesh_bytes})
    assert isinstance(decoded_example, (trimesh.Trimesh, trimesh.Scene))

    with pytest.raises(ValueError, match="requires a 'path' value"):
        mesh.decode_example({"path": None, "bytes": mesh_bytes})

    with pytest.raises(RuntimeError):
        Mesh(decode=False).decode_example({"path": mesh_path, "bytes": None})


@require_trimesh
def test_dataset_with_mesh_feature(shared_datadir):
    import trimesh

    mesh_path = str(shared_datadir / "test_mesh_glb.glb")
    data = {"mesh": [mesh_path]}
    features = Features({"mesh": Mesh()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"mesh"}
    assert isinstance(item["mesh"], (trimesh.Trimesh, trimesh.Scene))

    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"mesh"}
    assert isinstance(batch["mesh"], list)
    assert isinstance(batch["mesh"][0], (trimesh.Trimesh, trimesh.Scene))

    column = dset["mesh"]
    assert len(column) == 1
    assert isinstance(column, Column)
    assert isinstance(column[0], (trimesh.Trimesh, trimesh.Scene))


def test_dataset_with_mesh_feature_decode_false(shared_datadir):
    mesh_path = str(shared_datadir / "test_mesh_glb.glb")
    data = {"mesh": [mesh_path]}
    features = Features({"mesh": Mesh(decode=False)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"mesh"}
    assert isinstance(item["mesh"], dict)
    assert item["mesh"]["path"] == mesh_path


@require_trimesh
def test_dataset_cast_to_mesh_features(shared_datadir):
    import trimesh

    mesh_path = str(shared_datadir / "test_mesh_glb.glb")
    data = {"mesh": [mesh_path]}
    dset = Dataset.from_dict(data)
    dset = dset.cast(Features({"mesh": Mesh()}))
    item = dset[0]
    assert isinstance(item["mesh"], (trimesh.Trimesh, trimesh.Scene))


def test_dataset_concatenate_mesh_features(shared_datadir):
    mesh_path = str(shared_datadir / "test_mesh_glb.glb")
    data1 = {"mesh": [mesh_path]}
    dset1 = Dataset.from_dict(data1, features=Features({"mesh": Mesh(decode=False)}))
    with open(mesh_path, "rb") as f:
        data2 = {"mesh": [{"bytes": f.read()}]}
    dset2 = Dataset.from_dict(data2, features=Features({"mesh": Mesh(decode=False)}))
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == 2
    assert concatenated_dataset[0]["mesh"]["path"] == dset1[0]["mesh"]["path"]
    assert concatenated_dataset[1]["mesh"]["bytes"] == dset2[0]["mesh"]["bytes"]


@require_trimesh
def test_mesh_feature_encode_trimesh_object():
    import trimesh

    mesh = trimesh.creation.box()
    encoded_example = Mesh().encode_example(mesh)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["path"] == "mesh.glb"
    assert encoded_example["bytes"] is not None
    decoded_example = Mesh().decode_example(encoded_example)
    assert isinstance(decoded_example, trimesh.Scene)


def test_require_decoding():
    assert require_decoding(Mesh())


def test_mesh_embed_storage(shared_datadir):
    mesh_path = str(shared_datadir / "test_mesh_glb.glb")
    example = {"bytes": None, "path": mesh_path}
    storage = pa.array([example], type=pa.struct({"bytes": pa.binary(), "path": pa.string()}))
    embedded_storage = Mesh().embed_storage(storage)
    embedded_example = embedded_storage.to_pylist()[0]
    assert embedded_example == {"bytes": open(mesh_path, "rb").read(), "path": "test_mesh_glb.glb"}

    non_embedded_storage = Mesh().embed_storage(storage, local_files=False)
    non_embedded_example = non_embedded_storage.to_pylist()[0]
    assert non_embedded_example == {"bytes": None, "path": mesh_path}
