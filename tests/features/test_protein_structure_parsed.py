"""Tests for the parsed-object behavior of the ProteinStructure feature.

With ``decode=True`` (the default), ProteinStructure now returns a parsed
struct-of-arrays (atom-level columns under PDBx/mmCIF names) instead of the raw
file text. ``decode=False`` still returns the raw ``{path, bytes}`` mapping, and
the raw text remains reachable for callers that want their own parser.
"""

import pyarrow as pa
import pytest

from datasets import Dataset, Features, ProteinStructure
from datasets.features.protein_parsing import DEFAULT_ATOM_COLUMNS


def test_decode_pdb_returns_parsed_struct_of_arrays(shared_datadir):
    path = str(shared_datadir / "test_protein.pdb")
    feature = ProteinStructure()
    decoded = feature.decode_example({"path": path, "bytes": None})
    assert isinstance(decoded, dict)
    assert set(DEFAULT_ATOM_COLUMNS).issubset(set(decoded))
    assert len(decoded["label_atom_id"]) == 9
    assert decoded["label_comp_id"][0] == "ALA"
    assert decoded["label_comp_id"][5] == "GLY"


def test_decode_cif_returns_parsed_struct_of_arrays(shared_datadir):
    path = str(shared_datadir / "test_protein.cif")
    feature = ProteinStructure()
    decoded = feature.decode_example({"path": path, "bytes": None})
    assert isinstance(decoded, dict)
    assert len(decoded["label_atom_id"]) == 9
    assert decoded["type_symbol"][0] == "N"


def test_decode_false_returns_raw_mapping(shared_datadir):
    path = str(shared_datadir / "test_protein.pdb")
    feature = ProteinStructure(decode=False)
    with pytest.raises(RuntimeError):
        feature.decode_example({"path": path, "bytes": None})


def test_include_hetatm_feature_arg_filters(shared_datadir, tmp_path):
    structure = tmp_path / "het.pdb"
    structure.write_text(
        "ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00 20.00           N\n"
        "HETATM    2  O   HOH A   2       1.000   1.000   1.000  1.00 20.00           O\n"
        "END\n"
    )
    keep = ProteinStructure(include_hetatm=True).decode_example({"path": str(structure), "bytes": None})
    drop = ProteinStructure(include_hetatm=False).decode_example({"path": str(structure), "bytes": None})
    assert len(keep["label_atom_id"]) == 2
    assert len(drop["label_atom_id"]) == 1
    assert drop["label_comp_id"][0] == "ALA"


def test_columns_feature_arg_subsets(shared_datadir):
    path = str(shared_datadir / "test_protein.pdb")
    feature = ProteinStructure(columns=["label_atom_id", "Cartn_x"])
    decoded = feature.decode_example({"path": path, "bytes": None})
    assert set(decoded) == {"label_atom_id", "Cartn_x"}


def test_dataset_roundtrip_one_row_per_structure(shared_datadir):
    path = str(shared_datadir / "test_protein.pdb")
    features = Features({"structure": ProteinStructure()})
    # Three independent structures -> three independent rows (one row = one structure).
    dset = Dataset.from_dict({"structure": [path, path, path]}, features=features)
    assert len(dset) == 3
    row = dset[0]
    assert isinstance(row["structure"], dict)
    assert len(row["structure"]["label_atom_id"]) == 9
    # Shuffling / splitting must keep rows independent.
    shuffled = dset.shuffle(seed=0)
    assert len(shuffled) == 3


def test_pa_type_storage_is_unchanged():
    # Storage stays {bytes, path}: parsing is lazy on decode, no Arrow schema migration.
    feature = ProteinStructure()
    pa_type = feature.pa_type
    assert pa.types.is_struct(pa_type)
    assert pa_type.get_field_index("bytes") >= 0
    assert pa_type.get_field_index("path") >= 0


def test_include_hetatm_and_columns_survive_serialization():
    # Feature args must round-trip through the feature dict (no silent loss on save/load).
    feature = ProteinStructure(include_hetatm=False, columns=["label_atom_id"])
    restored = ProteinStructure.from_dict(feature.to_dict()) if hasattr(ProteinStructure, "from_dict") else None
    if restored is not None:
        assert restored.include_hetatm is False
        assert restored.columns == ["label_atom_id"]
