import bz2
import gzip
import io
import textwrap
from pathlib import Path

import numpy as np
import pyarrow as pa
import pytest

from datasets import AtomicStructure, Dataset, Features, load_from_disk
from datasets.features.atomic_structure import _is_bcif
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
    from atomworks.io import atom_array_from_file

    return atom_array_from_file(str(path))


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
    # Minimal reading preserves the source without deriving chemical annotations.
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

    row = AtomicStructure().encode_example(_parse_with_atomworks(CIF_FILE))
    assert row["path"] is None
    assert _is_bcif(row["bytes"])
    plain = pdbx.get_structure(pdbx.BinaryCIFFile.read(io.BytesIO(row["bytes"])), model=1, include_bonds=True)
    expected = _parse_with_atomworks(CIF_FILE)
    assert plain.atom_name.tolist() == expected.atom_name.tolist()
    np.testing.assert_allclose(plain.coord, expected.coord, atol=1e-3)


@require_atomworks
def test_encoding_a_stored_structure_keeps_it():
    row = AtomicStructure().encode_example(PDB_FILE.read_bytes())
    assert AtomicStructure().encode_example(row) == row
    compressed = gzip.compress(row["bytes"])
    assert AtomicStructure().encode_example(compressed)["bytes"] == compressed


@require_atomworks
def test_encode_bcif_written_by_another_tool():
    import biotite.structure.io.pdbx as pdbx

    atoms = pdbx.get_structure(pdbx.CIFFile.read(str(CIF_FILE)), model=1)
    file = pdbx.BinaryCIFFile()
    pdbx.set_structure(file, atoms)
    buffer = io.BytesIO()
    file.write(buffer)
    assert _is_bcif(buffer.getvalue())
    row = AtomicStructure().encode_example(buffer.getvalue())
    assert row["bytes"] == buffer.getvalue()
    assert AtomicStructure().decode_example(row).atom_name.tolist() == atoms.atom_name.tolist()


@require_atomworks
def test_decode_a_row_without_bytes():
    _assert_same_atoms(
        AtomicStructure().decode_example({"bytes": None, "path": str(CIF_FILE)}), _parse_with_atomworks(CIF_FILE)
    )
    with pytest.raises(ValueError, match="both are None"):
        AtomicStructure().decode_example({"bytes": None, "path": None})


@require_atomworks
def test_parse_config_and_assembly():
    assert _roundtrip(str(CIF_FILE)).array_length() == 9  # as in the file: no atoms added or removed
    atoms = _roundtrip(str(CIF_FILE), parse_config={"preset": "lightweight"})
    assert atoms.array_length() == 9  # the lightweight preset adds no atoms
    with pytest.raises(ValueError, match="Invalid assembly ID"):
        AtomicStructure(assembly="99").decode_example({"path": str(CIF_FILE), "bytes": None})


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
    assert atoms.element.tolist() == [atom.GetSymbol() for atom in mol.GetAtoms()]
    assert atoms.bonds.get_bond_count() == mol.GetNumBonds()


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
def test_unsupported_custom_annotations_raise_instead_of_losing_data():
    """PR514 supports StandardAnnotations, not arbitrary multidimensional custom annotations."""
    from atomworks.io.utils.atom_array_plus import AnnotationList2D

    atoms = _roundtrip(str(CIF_FILE))
    atoms.source_info.pop("_hf_encoded", None)
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
    with pytest.raises(ValueError, match="cannot serialize.*custom annotations losslessly"):
        _roundtrip(atoms)


@require_atomworks
def test_coordinates_are_exact_even_beyond_fixed_point_precision():
    """Coordinates that BinaryCIF's 0.001 A fixed point can't hold (e.g. atoms placed by a parser) are kept exactly."""
    atoms = _roundtrip(str(CIF_FILE))
    atoms.source_info.pop("_hf_encoded", None)
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
    assert [len(atoms) for atoms in dataset["s"]] == [9, 9]

    dataset = Dataset.from_dict({"s": [PDB_FILE.read_bytes()]}).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 9

    # file references as stored by other file-based features, e.g. the `BioStructure` feature this replaces
    references = pa.array([{"bytes": CIF_FILE.read_bytes(), "path": "test_protein.cif"}])
    dataset = Dataset(pa.table({"s": references})).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 9
    # casting a column that is already stored keeps the bytes
    again = dataset.cast_column("s", AtomicStructure(parse_config={"preset": "rcsb"}))
    assert again.data.column("s").to_pylist() == dataset.data.column("s").to_pylist()


@require_atomworks
def test_decode_false_and_flatten():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE)]}, features=_features(decode=False))
    raw = dataset[0]["s"]
    assert raw == {"bytes": None, "path": str(PDB_FILE)}
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
    assert structure.combine_chunks().field("bytes")[0].as_py() is None
    assert structure.combine_chunks().field("path")[0].as_py() == str(PDB_FILE)


@require_atomworks
def test_save_and_load_from_disk(tmp_path):
    dataset = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=_features())
    dataset.save_to_disk(tmp_path / "saved")
    reloaded = load_from_disk(tmp_path / "saved")
    assert reloaded.features == dataset.features
    _assert_same_atoms(reloaded[0]["s"], dataset[0]["s"])


def test_missing_atomworks_raises(monkeypatch):
    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", False)
    assert AtomicStructure().encode_example(str(CIF_FILE)) == {"path": str(CIF_FILE), "bytes": None}
    with pytest.raises(ImportError, match="please install 'atomworks'"):
        AtomicStructure().decode_example({"bytes": b"", "path": None})


@require_atomworks
def test_from_dict_with_array_objects():
    """A live biotite array passed to `Dataset.from_dict` is encoded, as `PIL` images are."""
    atoms = _roundtrip(str(CIF_FILE))
    dataset = Dataset.from_dict({"s": [atoms]})
    assert set(dataset.features["s"]) == {"bytes", "path"}
    assert dataset[0]["s"]["bytes"] == CIF_FILE.read_bytes()
    _assert_same_atoms(AtomicStructure().decode_example(dataset[0]["s"]), atoms)


@pytest.mark.parametrize("arrow_type", [pa.string(), pa.large_string(), pa.binary(), pa.large_binary()])
def test_cast_does_not_read_or_require_atomworks(monkeypatch, arrow_type):
    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", False)
    value = "missing.cif" if pa.types.is_string(arrow_type) or pa.types.is_large_string(arrow_type) else b"original"
    storage = AtomicStructure().cast_storage(pa.array([value, None], type=arrow_type)).to_pylist()
    assert storage[0] == ({"path": value, "bytes": None} if isinstance(value, str) else {"path": None, "bytes": value})
    assert storage[1] is None


def test_bytes_take_precedence_over_existing_path(monkeypatch):
    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", False)
    original = {"bytes": gzip.compress(CIF_FILE.read_bytes()), "path": str(PDB_FILE)}
    dataset = Dataset.from_dict({"s": [original]}, features=_features(decode=False))
    assert dataset[0]["s"] == original
    assert (
        AtomicStructure().embed_storage(dataset.data.column("s").combine_chunks()).field("bytes")[0].as_py()
        == original["bytes"]
    )


@require_atomworks
def test_identity_map_preserves_compressed_source(tmp_path):
    payload = gzip.compress(CIF_FILE.read_bytes())
    dataset = Dataset.from_dict({"s": [{"bytes": payload, "path": "original.cif.gz"}]}, features=_features())
    mapped = dataset.map(lambda example: example)
    assert mapped.data.column("s").to_pylist() == dataset.data.column("s").to_pylist()
    mapped.save_to_disk(tmp_path / "saved")
    assert (
        load_from_disk(tmp_path / "saved").cast_column("s", AtomicStructure(decode=False))[0]["s"]["bytes"] == payload
    )


@require_atomworks
@pytest.mark.parametrize("file_type", ["cif", "bcif"])
def test_cleanup_is_decode_only_including_binarycif(file_type):
    import biotite.structure as struc
    from atomworks.io import CIFWriteConfig, atom_array_to_file

    atoms = struc.array(
        [
            struc.Atom(
                [0.0, 0.0, 0.0], chain_id="A", res_id=1, res_name="HOH", atom_name="O", element="O", hetero=True
            ),
            struc.Atom([1.0, 0.0, 0.0], chain_id="B", res_id=1, res_name="GLY", atom_name="CA", element="C"),
        ]
    )
    atoms.bonds = struc.BondList(2)
    payload = atom_array_to_file(atoms, file_type=file_type, config=CIFWriteConfig(chem_comp_source="array"))
    payload = payload.encode() if isinstance(payload, str) else payload
    dataset = Dataset.from_dict({"s": [{"bytes": payload, "path": "source." + file_type}]}, features=_features())
    assert dataset[0]["s"].res_name.tolist() == ["HOH", "GLY"]
    prepared = dataset.cast_column("s", AtomicStructure(parse_config={"remove_waters": True}))
    assert prepared[0]["s"].res_name.tolist() == ["GLY"]
    assert prepared.data.column("s").to_pylist() == dataset.data.column("s").to_pylist()
    assert prepared.map(lambda row: row).data.column("s").to_pylist() == dataset.data.column("s").to_pylist()


@require_atomworks
def test_default_keeps_alternate_conformers_hydrogens_and_insertion_codes():
    import biotite.structure as struc
    from atomworks.io import CIFWriteConfig, atom_array_to_file

    atoms = struc.array(
        [
            struc.Atom(
                [0.0, 0.0, 0.0], chain_id="A", res_id=1, ins_code="B", res_name="GLY", atom_name="CA", element="C"
            ),
            struc.Atom(
                [1.0, 0.0, 0.0], chain_id="A", res_id=1, ins_code="B", res_name="GLY", atom_name="H", element="H"
            ),
        ]
    )
    atoms.bonds = struc.BondList(2)
    # Introduce two conformers directly in the CIF; the live-array writer rejects ambiguous atom identities.
    from biotite.structure.io.pdbx import CIFFile

    file = CIFFile.read(
        io.StringIO(atom_array_to_file(atoms, file_type="cif", config=CIFWriteConfig(chem_comp_source="array")))
    )
    site = file.block["atom_site"]
    for name in list(site):
        values = site[name].as_array(str)
        site[name] = np.concatenate([values[:1], values])
    site["label_alt_id"] = ["A", "B", "."]
    site["id"] = [1, 2, 3]
    buffer = io.StringIO()
    file.write(buffer)
    payload = buffer.getvalue().encode()
    result = _roundtrip(payload)
    assert result.atom_name.tolist() == ["CA", "CA", "H"]
    assert result.ins_code.tolist() == ["B", "B", "B"]
    assert AtomicStructure().encode_example(result)["bytes"] == payload


@require_atomworks
def test_slicing_decoded_array_does_not_reencode_original():
    atoms = _roundtrip(str(PDB_FILE))
    sliced = atoms[:2]
    encoded = AtomicStructure().encode_example(sliced)
    assert encoded["bytes"] != PDB_FILE.read_bytes()
    assert len(AtomicStructure().decode_example(encoded)) == 2


@pytest.mark.parametrize("type_name,format", [("BioStructure", "pdb"), ("BioSequence", "fasta")])
def test_legacy_feature_metadata_loads_without_atomworks(tmp_path, monkeypatch, type_name, format):
    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", False)
    feature = generate_from_dict({"_type": type_name, "format": format, "decode": False})
    raw = PDB_FILE.read_bytes() if type_name == "BioStructure" else b">seq\nACGT\n"
    dataset = Dataset.from_dict({"s": [raw]}, features=Features({"s": feature}))
    dataset.save_to_disk(tmp_path / "legacy")
    restored = load_from_disk(tmp_path / "legacy")
    assert restored.features.to_dict()["s"]["_type"] == type_name
    assert restored[0]["s"]["bytes"] == raw


@require_atomworks
def test_different_atom_models_preserve_original_on_map():
    payload = MULTI_MODEL_PDB.replace(
        "ATOM      2  CA  GLY A   1       1.500   0.000   0.000  1.00  0.00           C\n", ""
    ).encode()
    dataset = Dataset.from_dict({"s": [payload]}, features=_features())
    assert [len(model) for model in dataset[0]["s"]] == [2, 1]
    assert dataset.map(lambda row: row).data.column("s")[0].as_py()["bytes"] == payload


@require_atomworks
def test_registered_standard_annotations_survive_live_array_encoding():
    from atomworks.io.utils.standard_annotations import S_ATM

    atoms = _roundtrip(str(CIF_FILE))
    atoms.source_info.pop("_hf_encoded")
    targets = np.arange(len(atoms)) % 2 == 0
    S_ATM.set_annotation(atoms, targets)
    restored = _roundtrip(atoms)
    np.testing.assert_array_equal(S_ATM.annotation(restored), targets)


@require_atomworks
def test_assembly_is_decode_only():
    from biotite.structure.io.pdbx import CIFCategory, CIFFile

    file = CIFFile.read(str(CIF_FILE))
    file.block["pdbx_struct_assembly_gen"] = CIFCategory(
        {"assembly_id": ["1"], "oper_expression": ["1,2"], "asym_id_list": ["A"]}
    )
    operators = {"id": ["1", "2"], "type": ["identity operation", "crystal symmetry operation"]}
    for i in range(1, 4):
        operators[f"vector[{i}]"] = [0.0, 10.0 if i == 1 else 0.0]
        for j in range(1, 4):
            operators[f"matrix[{i}][{j}]"] = [float(i == j)] * 2
    file.block["pdbx_struct_oper_list"] = CIFCategory(operators)
    buffer = io.StringIO()
    file.write(buffer)
    payload = buffer.getvalue().encode()
    feature = AtomicStructure(assembly="1")
    encoded = feature.encode_example(payload)
    assembled = feature.decode_example(encoded)
    original = _roundtrip(payload)
    assert assembled.array_length() == 2 * original.array_length()
    np.testing.assert_allclose(assembled.coord[: len(original)], original.coord)
    np.testing.assert_allclose(assembled.coord[len(original) :], original.coord + [10, 0, 0])
    assert feature.encode_example(assembled)["bytes"] == payload


def test_old_atomworks_api_has_actionable_import_error(monkeypatch):
    import builtins

    original_import = builtins.__import__

    def legacy_import(name, *args, **kwargs):
        if name == "atomworks.io":
            raise ImportError("missing atom_array_from_file")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", True)
    monkeypatch.setattr(builtins, "__import__", legacy_import)
    with pytest.raises(ImportError, match="supported development version"):
        AtomicStructure().decode_example({"bytes": b"unused", "path": None})
