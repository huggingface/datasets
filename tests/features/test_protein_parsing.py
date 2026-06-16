"""Tests for the dependency-free protein structure parsers (PDB + mmCIF).

These cover the shared, format-agnostic parsing layer that turns raw PDB/mmCIF
text into a struct-of-arrays keyed by mmCIF/PDBx-dictionary column names. The
parsing layer is reused by the ProteinStructure feature for both formats so that
PDB- and mmCIF-derived datasets expose the same column vocabulary.
"""

import pyarrow as pa
import pytest

from datasets.features.protein_parsing import (
    DEFAULT_ATOM_COLUMNS,
    PROTEIN_ATOM_TYPES,
    parse_mmcif_atoms,
    parse_pdb_atoms,
)


@pytest.fixture
def pdb_text(shared_datadir):
    return (shared_datadir / "test_protein.pdb").read_text()


@pytest.fixture
def cif_text(shared_datadir):
    return (shared_datadir / "test_protein.cif").read_text()


def test_default_columns_are_a_subset_of_known_schema():
    # No hard-coded duplication: defaults must be drawn from the canonical type table.
    assert set(DEFAULT_ATOM_COLUMNS).issubset(set(PROTEIN_ATOM_TYPES))
    # The canonical coordinate + identity columns are present.
    for required in ("label_atom_id", "type_symbol", "label_comp_id", "Cartn_x", "Cartn_y", "Cartn_z"):
        assert required in DEFAULT_ATOM_COLUMNS


def test_parse_pdb_atoms_returns_struct_of_arrays(pdb_text):
    atoms = parse_pdb_atoms(pdb_text)
    # All default columns present, each a list of equal length (one entry per atom).
    assert set(DEFAULT_ATOM_COLUMNS).issubset(set(atoms))
    lengths = {len(atoms[col]) for col in DEFAULT_ATOM_COLUMNS}
    assert lengths == {9}  # sample has 9 ATOM records (ALA x5, GLY x4)


def test_parse_pdb_atoms_values_match_sample(pdb_text):
    atoms = parse_pdb_atoms(pdb_text)
    # First atom: ATOM 1  N  ALA A 1  0.000 0.000 0.000  1.00 20.00  N
    assert atoms["label_atom_id"][0] == "N"
    assert atoms["type_symbol"][0] == "N"
    assert atoms["label_comp_id"][0] == "ALA"
    assert atoms["label_asym_id"][0] == "A"
    assert atoms["label_seq_id"][0] == 1
    assert atoms["Cartn_x"][0] == pytest.approx(0.0)
    # Fifth atom CB has the only negative coords: 1.986 -0.760 -1.217
    assert atoms["Cartn_y"][4] == pytest.approx(-0.760)
    assert atoms["Cartn_z"][4] == pytest.approx(-1.217)
    # Residue transition ALA(1) -> GLY(2) at index 5.
    assert atoms["label_comp_id"][5] == "GLY"
    assert atoms["label_seq_id"][5] == 2
    # Occupancy / B-factor uniform in the sample.
    assert all(v == pytest.approx(1.0) for v in atoms["occupancy"])
    assert all(v == pytest.approx(20.0) for v in atoms["B_iso_or_equiv"])


def test_parse_mmcif_atoms_values_match_sample(cif_text):
    atoms = parse_mmcif_atoms(cif_text)
    assert len(atoms["label_atom_id"]) == 9
    assert atoms["label_atom_id"][0] == "N"
    assert atoms["type_symbol"][0] == "N"
    assert atoms["label_comp_id"][0] == "ALA"
    assert atoms["label_asym_id"][0] == "A"
    assert atoms["label_seq_id"][0] == 1
    assert atoms["Cartn_z"][4] == pytest.approx(-1.217)
    assert atoms["label_comp_id"][5] == "GLY"


def test_pdb_and_mmcif_yield_same_schema(pdb_text, cif_text):
    # The whole point of mmCIF-native naming: both formats expose identical columns.
    pdb_atoms = parse_pdb_atoms(pdb_text)
    cif_atoms = parse_mmcif_atoms(cif_text)
    assert set(DEFAULT_ATOM_COLUMNS).issubset(set(pdb_atoms))
    assert set(DEFAULT_ATOM_COLUMNS).issubset(set(cif_atoms))
    for col in DEFAULT_ATOM_COLUMNS:
        assert pdb_atoms[col] == cif_atoms[col], f"column {col} differs between PDB and mmCIF"


def test_include_hetatm_filter_drops_hetatm():
    # Generalizable filter: a HETATM line must be excluded when include_hetatm=False.
    text = (
        "ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00 20.00           N\n"
        "HETATM    2  O   HOH A   2       1.000   1.000   1.000  1.00 20.00           O\n"
        "END\n"
    )
    kept = parse_pdb_atoms(text, include_hetatm=False)
    dropped = parse_pdb_atoms(text, include_hetatm=True)
    assert len(kept["label_atom_id"]) == 1
    assert kept["label_comp_id"][0] == "ALA"
    assert len(dropped["label_atom_id"]) == 2


def test_columns_subset_selection(pdb_text):
    # Requesting a subset returns exactly those columns (validated against schema).
    atoms = parse_pdb_atoms(pdb_text, columns=["label_atom_id", "Cartn_x"])
    assert set(atoms) == {"label_atom_id", "Cartn_x"}


def test_unknown_column_raises(pdb_text):
    # No silent drop of an unknown column name.
    with pytest.raises(ValueError):
        parse_pdb_atoms(pdb_text, columns=["not_a_real_column"])


def test_protein_atom_types_dtypes_are_arrow_types():
    # The canonical type table maps every column to a pyarrow DataType (no stringly-typed dtypes).
    for col, dtype in PROTEIN_ATOM_TYPES.items():
        assert isinstance(dtype, pa.DataType), f"{col} dtype is not a pa.DataType"
