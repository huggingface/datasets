from pathlib import Path

import pyarrow as pa
import pytest

from datasets import Dataset, Features, ProteinStructure


@pytest.mark.parametrize(
    "build_example",
    [
        lambda structure_path: structure_path,
        lambda structure_path: Path(structure_path),
        lambda structure_path: open(structure_path, "rb").read(),
        lambda structure_path: {"path": structure_path},
        lambda structure_path: {"path": structure_path, "bytes": None},
        lambda structure_path: {"path": structure_path, "bytes": open(structure_path, "rb").read()},
        lambda structure_path: {"path": None, "bytes": open(structure_path, "rb").read()},
        lambda structure_path: {"bytes": open(structure_path, "rb").read()},
    ],
)
def test_protein_structure_feature_encode_example(shared_datadir, build_example):
    structure_path = str(shared_datadir / "test_protein.pdb")
    protein_structure = ProteinStructure()
    encoded_example = protein_structure.encode_example(build_example(structure_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = protein_structure.decode_example(encoded_example)
    assert isinstance(decoded_example, str)


def test_protein_structure_decode_example_pdb(shared_datadir):
    structure_path = str(shared_datadir / "test_protein.pdb")
    protein_structure = ProteinStructure()
    decoded_example = protein_structure.decode_example({"path": structure_path, "bytes": None})

    assert isinstance(decoded_example, str)
    assert "ATOM" in decoded_example
    assert "HEADER" in decoded_example

    with pytest.raises(RuntimeError):
        ProteinStructure(decode=False).decode_example({"path": structure_path, "bytes": None})


def test_protein_structure_decode_example_cif(shared_datadir):
    structure_path = str(shared_datadir / "test_protein.cif")
    protein_structure = ProteinStructure()
    decoded_example = protein_structure.decode_example({"path": structure_path, "bytes": None})

    assert isinstance(decoded_example, str)
    assert "data_" in decoded_example
    assert "_atom_site" in decoded_example


def test_dataset_with_protein_structure_feature(shared_datadir):
    structure_path = str(shared_datadir / "test_protein.pdb")
    data = {"structure": [structure_path]}
    features = Features({"structure": ProteinStructure()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"structure"}
    assert isinstance(item["structure"], str)
    assert "ATOM" in item["structure"]
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"structure"}
    assert isinstance(batch["structure"], list) and all(isinstance(item, str) for item in batch["structure"])
    column = dset["structure"]
    assert len(column) == 1
    assert all(isinstance(item, str) for item in column)

    # from bytes
    with open(structure_path, "rb") as f:
        data = {"structure": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"structure"}
    assert isinstance(item["structure"], str)


def test_protein_structure_pa_type():
    protein_structure = ProteinStructure()
    pa_type = protein_structure.pa_type

    assert pa.types.is_struct(pa_type)
    assert pa_type.get_field_index("bytes") >= 0
    assert pa_type.get_field_index("path") >= 0
    assert pa.types.is_binary(pa_type.field("bytes").type)
    assert pa.types.is_string(pa_type.field("path").type)


def test_protein_structure_cast_storage(shared_datadir):
    structure_path = str(shared_datadir / "test_protein.pdb")
    protein_structure = ProteinStructure()

    # From string array (path)
    string_array = pa.array([structure_path], type=pa.string())
    casted = protein_structure.cast_storage(string_array)
    assert pa.types.is_struct(casted.type)
    assert casted.type.get_field_index("bytes") >= 0
    assert casted.type.get_field_index("path") >= 0

    # From binary array (bytes)
    with open(structure_path, "rb") as f:
        content = f.read()
    binary_array = pa.array([content], type=pa.binary())
    casted = protein_structure.cast_storage(binary_array)
    assert pa.types.is_struct(casted.type)

    # From struct array
    bytes_array = pa.array([content], type=pa.binary())
    path_array = pa.array([structure_path], type=pa.string())
    struct_array = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"])
    casted = protein_structure.cast_storage(struct_array)
    assert pa.types.is_struct(casted.type)


def test_protein_structure_embed_storage(shared_datadir):
    structure_path = str(shared_datadir / "test_protein.pdb")
    protein_structure = ProteinStructure()

    bytes_array = pa.array([None], type=pa.binary())
    path_array = pa.array([structure_path], type=pa.string())
    storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"])

    embedded_storage = protein_structure.embed_storage(storage)

    embedded_bytes = embedded_storage[0]["bytes"].as_py()
    assert embedded_bytes is not None
    assert len(embedded_bytes) > 0

    content = embedded_bytes.decode("utf-8")
    assert "ATOM" in content


def test_protein_structure_flatten():
    # With decode=True
    protein_structure = ProteinStructure(decode=True)
    flattened = protein_structure.flatten()
    assert flattened is protein_structure  # Returns self when decode=True

    # With decode=False
    protein_structure_no_decode = ProteinStructure(decode=False)
    flattened = protein_structure_no_decode.flatten()
    assert isinstance(flattened, dict)
    assert "bytes" in flattened
    assert "path" in flattened
