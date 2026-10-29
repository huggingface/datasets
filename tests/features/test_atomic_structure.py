import bz2
import gzip
import io
import textwrap
from pathlib import Path

import numpy as np
import pyarrow as pa
import pytest

from datasets import AtomicStructure, Dataset, Features, load_from_disk
from datasets.features.atomic_structure import _is_bcif, _is_stored
from datasets.features.features import generate_from_dict

from ..utils import require_atomworks, require_zstandard


DATA_DIR = Path(__file__).parent / "data"
PDB_FILE = DATA_DIR / "test_protein.pdb"
CIF_FILE = DATA_DIR / "test_protein.cif"
ATOM_NAMES = ["N", "CA", "C", "O", "CB", "N", "CA", "C", "O"]

MULTI_MODEL_PDB = textwrap.dedent(
    """\
    MODEL        1
    ATOM      1  N   GLY A   1       0.000   0.000   0.000  1.00  0.00           N
    ATOM      2  CA  GLY A   1       1.000   0.000   0.000  1.00  0.00           C
    ENDMDL
    MODEL        2
    ATOM      1  N   GLY A   1       0.500   0.000   0.000  1.00  0.00           N
    ATOM      2  CA  GLY A   1       1.500   0.000   0.000  1.00  0.00           C
    ENDMDL
    END
    """
)

# Acetic acid: a double bond and a single bond to oxygen. The atoms have no names and no residue.
ACETIC_ACID_SDF = textwrap.dedent(
    """\
    acetic acid
      test

      4  3  0  0  0  0  0  0  0  0999 V2000
        0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
        1.5000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
        2.1000    1.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
        2.1000   -1.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
      1  2  1  0
      2  3  2  0
      2  4  1  0
    M  END
    $$$$
    """
)

ETHANOL_MOL2 = textwrap.dedent(
    """\
    @<TRIPOS>MOLECULE
    ethanol
     3 2 0 0 0
    SMALL
    GASTEIGER

    @<TRIPOS>ATOM
          1 C1          0.0000    0.0000    0.0000 C.3     1  LIG1        0.0000
          2 C2          1.5200    0.0000    0.0000 C.3     1  LIG1        0.0000
          3 O1          2.0000    1.3000    0.0000 O.3     1  LIG1        0.0000
    @<TRIPOS>BOND
         1     1     2    1
         2     2     3    1
    """
)


def _features(**kwargs):
    return Features({"s": AtomicStructure(**kwargs)})


def _parse_with_atomworks(path):
    from atomworks.io import parse

    atoms = parse(str(path), config="default")["asym_unit"]
    return atoms[0] if hasattr(atoms, "stack_depth") and atoms.stack_depth() == 1 else atoms


def _assert_same_atoms(actual, expected):
    """Same atoms: exact coordinates, every annotation with its dtype, bonds and box."""
    assert actual.array_length() == expected.array_length()
    np.testing.assert_array_equal(actual.coord, expected.coord)
    assert set(actual.get_annotation_categories()) == set(expected.get_annotation_categories())
    for name in expected.get_annotation_categories():
        want, got = expected.get_annotation(name), actual.get_annotation(name)
        assert got.dtype == want.dtype, name
        np.testing.assert_array_equal(got, want, err_msg=name)
    assert actual.bonds == expected.bonds
    assert (actual.box is None) == (expected.box is None)


def _roundtrip(value, **kwargs):
    return Dataset.from_dict({"s": [value]}, features=_features(**kwargs))[0]["s"]


def test_storage_type():
    assert AtomicStructure().pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert AtomicStructure().flatten() is not None


@pytest.mark.parametrize(
    "feature", [AtomicStructure(), AtomicStructure(parse_config={"preset": "rcsb"}, assembly="1")]
)
def test_serialization(feature):
    features = Features({"s": feature})
    assert generate_from_dict(features.to_dict()["s"]) == feature
    assert Features.from_arrow_schema(features.arrow_schema) == features
    assert Features._from_yaml_list(features._to_yaml_list()) == features


def test_encode_rejects_unknown_input():
    with pytest.raises(ValueError, match="An atomic structure should be"):
        AtomicStructure().encode_example(42)


def test_empty_and_missing_values():
    assert len(Dataset.from_dict({"s": []}, features=_features())) == 0
    assert Dataset.from_dict({"s": [None, None]}, features=_features())["s"] == [None, None]


# ----------------------------------------------------------------------------------------------- files


@require_atomworks
@pytest.mark.parametrize("path", [CIF_FILE, PDB_FILE])
def test_decoding_gives_what_atomworks_parses(path):
    atoms = _roundtrip(str(path))
    assert type(atoms).__name__ == "AtomArrayPlus"
    # the atomworks annotations (entities, molecules, chain types, ...) are stored, not just the biotite ones
    assert {"molecule_id", "chain_type", "is_polymer", "pn_unit_id"} <= set(atoms.get_annotation_categories())
    _assert_same_atoms(atoms, _parse_with_atomworks(path))


@require_atomworks
@pytest.mark.parametrize("source", ["pathlib", "bytes_pdb", "bytes_cif", "dict_bytes", "dict_path"])
def test_encode_file_inputs(source):
    value = {
        "pathlib": PDB_FILE,
        "bytes_pdb": PDB_FILE.read_bytes(),
        "bytes_cif": CIF_FILE.read_bytes(),
        "dict_bytes": {"bytes": CIF_FILE.read_bytes(), "path": "renamed.cif"},
        "dict_path": {"bytes": None, "path": str(PDB_FILE)},
    }[source]
    expected = _parse_with_atomworks(CIF_FILE if source in ("bytes_cif", "dict_bytes") else PDB_FILE)
    _assert_same_atoms(_roundtrip(value), expected)


@require_atomworks
@pytest.mark.parametrize("compress", [gzip.compress, bz2.compress, pytest.param("zstd", marks=require_zstandard)])
def test_encode_compressed(compress):
    if compress == "zstd":
        import zstandard

        compress = zstandard.ZstdCompressor().compress
    for path in (CIF_FILE, PDB_FILE):
        _assert_same_atoms(_roundtrip(compress(path.read_bytes())), _parse_with_atomworks(path))


@require_atomworks
def test_stored_bytes_are_a_bcif_file_any_reader_opens():
    import biotite.structure.io.pdbx as pdbx

    row = AtomicStructure().encode_example(str(CIF_FILE))
    assert row["path"] == "test_protein.cif"
    assert _is_stored(row["bytes"])
    plain = pdbx.get_structure(pdbx.BinaryCIFFile.read(io.BytesIO(row["bytes"])), model=1, include_bonds=True)
    expected = _parse_with_atomworks(CIF_FILE)
    assert plain.atom_name.tolist() == expected.atom_name.tolist()
    np.testing.assert_allclose(plain.coord, expected.coord, atol=1e-3)


@require_atomworks
def test_encoding_a_stored_structure_keeps_it():
    row = AtomicStructure().encode_example(str(PDB_FILE))
    assert AtomicStructure().encode_example(row)["bytes"] == row["bytes"]
    assert AtomicStructure().encode_example(gzip.compress(row["bytes"]))["bytes"] == row["bytes"]


@require_atomworks
def test_encode_bcif_written_by_another_tool():
    import biotite.structure.io.pdbx as pdbx

    atoms = pdbx.get_structure(pdbx.CIFFile.read(str(CIF_FILE)), model=1)
    file = pdbx.BinaryCIFFile()
    pdbx.set_structure(file, atoms)
    buffer = io.BytesIO()
    file.write(buffer)
    assert _is_bcif(buffer.getvalue()) and not _is_stored(buffer.getvalue())
    row = AtomicStructure().encode_example(buffer.getvalue())
    assert _is_stored(row["bytes"])
    assert "molecule_id" in AtomicStructure().decode_example(row).get_annotation_categories()


@require_atomworks
def test_decode_a_row_without_bytes():
    _assert_same_atoms(
        AtomicStructure().decode_example({"bytes": None, "path": str(CIF_FILE)}), _parse_with_atomworks(CIF_FILE)
    )
    with pytest.raises(ValueError, match="both are None"):
        AtomicStructure().decode_example({"bytes": None, "path": None})


@require_atomworks
def test_parse_config_and_assembly():
    atoms = _roundtrip(str(CIF_FILE), parse_config={"preset": "lightweight"})
    assert atoms.array_length() == 9  # the lightweight preset adds no atoms
    with pytest.raises(ValueError, match="Invalid assembly ID"):
        AtomicStructure(assembly="99").encode_example(str(CIF_FILE))


@require_atomworks
def test_multiple_models():
    stack = _roundtrip(MULTI_MODEL_PDB.encode())
    assert type(stack).__name__ == "AtomArrayPlusStack"
    assert stack.coord.shape[0] == 2
    assert stack.coord[1, :2, 0].tolist() == [0.5, 1.5]  # atomworks adds the missing atoms of the residue


# ---------------------------------------------------------------------------------------- other inputs


@require_atomworks
def test_encode_sdf_keeps_bond_orders():
    atoms = _roundtrip({"bytes": ACETIC_ACID_SDF.encode(), "path": "acid.sdf"})
    assert atoms.element.tolist() == ["C", "C", "O", "O"]
    assert atoms.chain_id.tolist() == ["A"] * 4
    assert atoms.hetero.all()
    assert sorted(atoms.bonds.as_array().tolist()) == [[0, 1, 1], [1, 2, 2], [1, 3, 1]]


@require_atomworks
def test_encode_mol2():
    atoms = _roundtrip({"bytes": ETHANOL_MOL2.encode(), "path": "ethanol.mol2"})
    assert atoms.element.tolist() == ["C", "C", "O"]
    assert atoms.bonds.get_bond_count() == 2


@require_atomworks
def test_encode_rdkit_molecule():
    Chem = pytest.importorskip("rdkit.Chem")
    AllChem = pytest.importorskip("rdkit.Chem.AllChem")

    mol = Chem.AddHs(Chem.MolFromSmiles("CCO"))
    AllChem.EmbedMolecule(mol, randomSeed=0)
    atoms = _roundtrip(mol)
    assert atoms.element.tolist() == ["C", "C", "O"]  # atomworks removes hydrogens
    assert atoms.bonds.get_bond_count() == 2


@require_atomworks
def test_encode_ase_periodic_structure():
    ase_build = pytest.importorskip("ase.build")

    crystal = ase_build.bulk("Cu", "fcc", a=3.6, cubic=True)
    atoms = _roundtrip(crystal)
    np.testing.assert_allclose(atoms.coord, crystal.get_positions(), atol=1e-3)
    np.testing.assert_allclose(atoms.box, np.diag([3.6, 3.6, 3.6]), atol=1e-5)
    assert _roundtrip(ase_build.molecule("H2O")).box is None


# ------------------------------------------------------------------------------------- exact round trips


@require_atomworks
def test_array_with_all_annotation_kinds_roundtrips_exactly():
    """Every annotation comes back with its values and dtype, which mmCIF itself does not carry."""
    from atomworks.io.utils.atom_array_plus import AnnotationList2D

    atoms = _roundtrip(str(CIF_FILE))
    n = atoms.array_length()
    rng = np.random.default_rng(0)
    atoms.set_annotation("small_int", np.arange(n, dtype=np.int8))
    atoms.set_annotation("wide_int", np.arange(n, dtype=np.int64) * 1000)
    atoms.set_annotation("flag", np.arange(n) % 2 == 0)
    atoms.set_annotation("score32", rng.random(n).astype(np.float32))
    atoms.set_annotation("score64", np.where(np.arange(n) == 3, np.nan, rng.random(n)))
    atoms.set_annotation("label", np.array(["", "a", "bb", "ccc"] * (n // 4) + [""] * (n % 4)))
    atoms.set_annotation("embedding", rng.random((n, 4)).astype(np.float32))
    atoms.set_annotation("resolution", np.array(2.5, dtype=np.float32), n_body=0)
    pairs = np.array([[0, 5], [3, 8]])
    atoms.set_annotation("contact", AnnotationList2D(n, pairs, np.array([1.5, 2.5])), n_body=2)
    atoms.box = np.diag([50.0, 51.0, 52.0]).astype(np.float32)
    again = _roundtrip(atoms)
    _assert_same_atoms(again, atoms)
    np.testing.assert_array_equal(again.score64, atoms.score64)  # NaN included
    np.testing.assert_allclose(again.box, atoms.box)
    assert float(again.get_annotation("resolution", n_body=0)) == 2.5
    contact = again.get_annotation("contact", n_body=2)
    np.testing.assert_array_equal(contact.pairs, pairs)
    np.testing.assert_array_equal(contact.values, [1.5, 2.5])


@require_atomworks
def test_coordinates_are_exact_even_beyond_fixed_point_precision():
    """Coordinates that BinaryCIF's 0.001 A fixed point can't hold (e.g. atoms placed by a parser) are kept exactly."""
    atoms = _roundtrip(str(CIF_FILE))
    rng = np.random.default_rng(1)
    atoms.coord = (atoms.coord + rng.random(atoms.coord.shape) * 1e-4).astype(np.float32)
    np.testing.assert_array_equal(_roundtrip(atoms).coord, atoms.coord)
    row = AtomicStructure().encode_example(_roundtrip(str(CIF_FILE)))
    assert b"atomworks_coord" not in row["bytes"]  # not needed when atom_site is exact


@require_atomworks
def test_biotite_array_roundtrips():
    import biotite.structure.io.pdbx as pdbx

    atoms = pdbx.get_structure(pdbx.CIFFile.read(str(CIF_FILE)), model=1, include_bonds=True)
    again = _roundtrip(atoms)
    assert again.atom_name.tolist() == atoms.atom_name.tolist()
    assert again.bonds == atoms.bonds


# ---------------------------------------------------------------------------------- dataset plumbing


@require_atomworks
def test_cast_column_from_paths_bytes_and_file_references():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE), str(CIF_FILE)]}).cast_column("s", AtomicStructure())
    assert [len(atoms) for atoms in dataset["s"]] == [20, 20]

    dataset = Dataset.from_dict({"s": [PDB_FILE.read_bytes()]}).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 20

    # file references as stored by other file-based features, e.g. the `BioStructure` feature this replaces
    references = pa.array([{"bytes": CIF_FILE.read_bytes(), "path": "test_protein.cif"}])
    dataset = Dataset(pa.table({"s": references})).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 20
    # casting a column that is already stored keeps the bytes
    again = dataset.cast_column("s", AtomicStructure(parse_config={"preset": "rcsb"}))
    assert again.data.column("s").to_pylist() == dataset.data.column("s").to_pylist()


@require_atomworks
def test_decode_false_and_flatten():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE)]}, features=_features(decode=False))
    raw = dataset[0]["s"]
    assert set(raw) == {"bytes", "path"} and raw["path"] == "test_protein.pdb"
    assert _is_stored(raw["bytes"])
    assert set(dataset.flatten().column_names) == {"s.bytes", "s.path"}
    with pytest.raises(RuntimeError, match="Decoding is disabled"):
        AtomicStructure(decode=False).decode_example(raw)


def test_embed_storage_keeps_bytes_and_reads_missing_ones():
    """A row that holds its bytes is not read from its path again, which may not exist any more."""
    kept = {"bytes": b"embedded", "path": "gone/1abc.cif"}
    missing = {"bytes": None, "path": str(CIF_FILE)}
    storage = pa.array([kept, missing, None], type=AtomicStructure.pa_type)
    embedded = AtomicStructure().embed_storage(storage).to_pylist()
    assert embedded[0] == {"bytes": b"embedded", "path": "1abc.cif"}
    assert embedded[1] == {"bytes": CIF_FILE.read_bytes(), "path": "test_protein.cif"}
    assert embedded[2] is None
    skipped = AtomicStructure().embed_storage(storage, local_files=False).to_pylist()
    assert skipped[1]["bytes"] is None


@require_atomworks
def test_arrow_format():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE)]}, features=_features())
    structure = dataset.with_format("arrow")[0]["s"]
    assert _is_stored(structure.combine_chunks().field("bytes")[0].as_py())


@require_atomworks
def test_save_and_load_from_disk(tmp_path):
    dataset = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=_features())
    dataset.save_to_disk(tmp_path / "saved")
    reloaded = load_from_disk(tmp_path / "saved")
    assert reloaded.features == dataset.features
    _assert_same_atoms(reloaded[0]["s"], dataset[0]["s"])


def test_missing_atomworks_raises(monkeypatch):
    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", False)
    with pytest.raises(ImportError, match="please install 'atomworks'"):
        AtomicStructure().encode_example(str(CIF_FILE))
    with pytest.raises(ImportError, match="please install 'atomworks'"):
        AtomicStructure().decode_example({"bytes": b"", "path": None})


@require_atomworks
def test_from_dict_with_array_objects():
    """A live biotite array passed to `Dataset.from_dict` is encoded, as `PIL` images are."""
    atoms = _roundtrip(str(CIF_FILE))
    dataset = Dataset.from_dict({"s": [atoms]})
    assert set(dataset.features["s"]) == {"bytes", "path"}
    assert _is_stored(dataset[0]["s"]["bytes"])
    _assert_same_atoms(AtomicStructure().decode_example(dataset[0]["s"]), atoms)
