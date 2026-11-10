import bz2
import gzip
import io
from pathlib import Path

import numpy as np
import pyarrow as pa
import pytest

from datasets import AtomicStructure, Dataset, Features, Value, load_from_disk
from datasets.features.features import generate_from_dict

from ..utils import require_atomworks, require_zstandard


DATA_DIR = Path(__file__).parent / "data"
PDB_FILE = DATA_DIR / "test_protein.pdb"
CIF_FILE = DATA_DIR / "test_protein.cif"

MULTI_MODEL_PDB = (DATA_DIR / "test_models.pdb").read_text()

# Acetic acid: a double bond and a single bond to oxygen. The atoms have no names and no residue.
ACETIC_ACID_SDF = (DATA_DIR / "test_acetic_acid.sdf").read_text()

ETHANOL_MOL2 = (DATA_DIR / "test_ethanol.mol2").read_text()


def _features(**kwargs):
    return Features({"s": AtomicStructure(**kwargs)})


def _parse_with_atomworks(path):
    from atomworks.io import atom_array_from_file

    return atom_array_from_file(str(path))


def _assert_same_atoms(actual, expected):
    """Compare decoded atoms against the public AtomWorks reader."""
    assert actual.array_length() == expected.array_length()
    np.testing.assert_array_equal(actual.coord, expected.coord)
    assert set(actual.get_annotation_categories()) == set(expected.get_annotation_categories())
    for name in expected.get_annotation_categories():
        want, got = expected.get_annotation(name), actual.get_annotation(name)
        assert got.dtype == want.dtype, name
        np.testing.assert_array_equal(got, want, err_msg=name)
    assert actual.bonds == expected.bonds


def _roundtrip(value, **kwargs):
    return Dataset.from_dict({"s": [value]}, features=_features(**kwargs))[0]["s"]


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


@require_atomworks
@pytest.mark.parametrize("filename", ["test_protein.pdb", "test_protein.cif"])
@pytest.mark.parametrize(
    "build_example",
    [str, lambda p: p, lambda p: p.read_bytes(), lambda p: {"path": str(p)}, lambda p: {"bytes": p.read_bytes()}],
)
def test_encode_file_inputs(shared_datadir, filename, build_example):
    path = shared_datadir / filename
    _assert_same_atoms(_roundtrip(build_example(path)), _parse_with_atomworks(path))


@require_atomworks
@pytest.mark.parametrize("compress", [gzip.compress, bz2.compress, pytest.param("zstd", marks=require_zstandard)])
def test_encode_compressed(compress):
    if compress == "zstd":
        import zstandard

        compress = zstandard.ZstdCompressor().compress
    for path in (CIF_FILE, PDB_FILE):
        _assert_same_atoms(_roundtrip(compress(path.read_bytes())), _parse_with_atomworks(path))


@require_atomworks
def test_materialized_binarycif_opens_with_biotite():
    import biotite.structure.io.pdbx as pdbx

    row = AtomicStructure().encode_example(_parse_with_atomworks(CIF_FILE))
    assert row["path"] is None
    file = pdbx.BinaryCIFFile.read(io.BytesIO(row["bytes"]))
    assert not any(name.startswith("hf_atomic_structure") for name in file.block)
    assert "chem_comp_bond" in file.block
    plain = pdbx.get_structure(file, model=1, include_bonds=True)
    expected = _parse_with_atomworks(CIF_FILE)
    assert plain.atom_name.tolist() == expected.atom_name.tolist()
    np.testing.assert_allclose(plain.coord, expected.coord, atol=1e-3)


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
    row = AtomicStructure().encode_example(buffer.getvalue())
    assert row["bytes"] == buffer.getvalue()
    assert AtomicStructure().decode_example(row).atom_name.tolist() == atoms.atom_name.tolist()


@require_atomworks
def test_decode_rejects_missing_path_and_bytes():
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
    assert stack.coord[1, :2, 0].tolist() == [0.5, 1.5]


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
    restored = _roundtrip(AtomicStructure().materialize(atoms))
    np.testing.assert_array_equal(restored.coord, atoms.coord)
    assert restored.bonds == atoms.bonds


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
def test_encode_ase_structure():
    ase_build = pytest.importorskip("ase.build")

    crystal = ase_build.bulk("Cu", "fcc", a=3.6, cubic=True)
    atoms = _roundtrip(crystal)
    np.testing.assert_allclose(atoms.coord, crystal.get_positions(), atol=1e-3)


@require_atomworks
@pytest.mark.parametrize("missing", [False, True])
def test_materialize_preserves_coordinate_precision(missing):
    atoms = _roundtrip(str(CIF_FILE))
    atoms.coord += np.random.default_rng(1).random(atoms.coord.shape).astype(np.float32) * 1e-4
    if missing:
        atoms.coord[2] = np.nan
    np.testing.assert_array_equal(_roundtrip(AtomicStructure().materialize(atoms)).coord, atoms.coord)


@require_atomworks
def test_biotite_array_roundtrips():
    import biotite.structure.io.pdbx as pdbx

    atoms = pdbx.get_structure(pdbx.CIFFile.read(str(CIF_FILE)), model=1, include_bonds=True)
    again = _roundtrip(atoms)
    assert again.atom_name.tolist() == atoms.atom_name.tolist()
    assert again.bonds == atoms.bonds


@require_atomworks
def test_cast_column_from_paths_bytes_and_file_references():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE), str(CIF_FILE)]}).cast_column("s", AtomicStructure())
    assert [len(atoms) for atoms in dataset["s"]] == [9, 9]

    dataset = Dataset.from_dict({"s": [PDB_FILE.read_bytes()]}).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 9

    # file references as stored by other file-based features, e.g. the existing `BioStructure` feature
    references = pa.array([{"bytes": CIF_FILE.read_bytes(), "path": "test_protein.cif"}])
    dataset = Dataset(pa.table({"s": references})).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 9
    # casting a column that is already stored keeps the bytes
    again = dataset.cast_column("s", AtomicStructure(parse_config={"preset": "rcsb"}))
    assert again.data.column("s").to_pylist() == dataset.data.column("s").to_pylist()


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
def test_save_and_load_from_disk(tmp_path):
    dataset = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=_features())
    dataset.save_to_disk(tmp_path / "saved")
    reloaded = load_from_disk(tmp_path / "saved")
    assert reloaded.features == dataset.features
    _assert_same_atoms(reloaded[0]["s"], dataset[0]["s"])


def test_missing_atomworks_raises(monkeypatch):
    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", False)
    assert AtomicStructure().encode_example(str(CIF_FILE)) == {"path": str(CIF_FILE), "bytes": None}
    with pytest.raises(ImportError, match="please install 'atomworks>=3.1.0'"):
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
def test_default_minimal_parse_preserves_source_conformers_and_hydrogens():
    payload = (DATA_DIR / "test_altloc.cif").read_bytes()
    result = _roundtrip(payload)
    assert result.atom_name.tolist() == ["CA", "H"]
    _assert_same_atoms(result, _parse_with_atomworks(DATA_DIR / "test_altloc.cif"))
    assert AtomicStructure().encode_example(result)["bytes"] == payload


@require_atomworks
@pytest.mark.parametrize("selection", [slice(None, 2), slice(3, 7)])
def test_slicing_decoded_array_does_not_reencode_original(selection):
    atoms = _roundtrip(str(PDB_FILE))
    sliced = atoms[selection]
    encoded = AtomicStructure().encode_example(sliced)
    assert encoded["bytes"] != PDB_FILE.read_bytes()
    restored = AtomicStructure().decode_example(encoded)
    np.testing.assert_array_equal(restored.coord, sliced.coord)
    assert restored.bonds == sliced.bonds


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
    atoms.del_annotation("_hf_encoded", n_body=0)
    targets = np.arange(len(atoms)) % 2 == 0
    S_ATM.set_annotation(atoms, targets)
    restored = _roundtrip(atoms)
    np.testing.assert_array_equal(S_ATM.annotation(restored), targets)


@require_atomworks
def test_assembly_is_decode_only():
    payload = (DATA_DIR / "test_assembly.cif").read_bytes()
    feature = AtomicStructure(assembly="1")
    encoded = feature.encode_example(payload)
    assembled = feature.decode_example(encoded)
    original = _roundtrip(payload)
    assert assembled.array_length() == 2 * original.array_length()
    np.testing.assert_allclose(assembled.coord[: len(original)], original.coord)
    np.testing.assert_allclose(assembled.coord[len(original) :], original.coord + [10, 0, 0])
    assert feature.encode_example(assembled)["bytes"] == payload
    dataset = Dataset.from_dict(
        {"s": [payload], "label": ["example"]}, features=Features({"s": AtomicStructure(), "label": Value("string")})
    )
    stored = dataset.cast_column("s", feature).map(
        lambda row: {"s": AtomicStructure().materialize(row["s"])}, features=dataset.features
    )
    assert stored[0]["label"] == "example"
    assert stored.features["s"] == AtomicStructure()
    np.testing.assert_allclose(stored[0]["s"].coord, assembled.coord)
    np.testing.assert_array_equal(stored[0]["s"].chain_id, assembled.chain_id)
    assert stored[0]["s"].bonds == assembled.bonds


def test_old_atomworks_api_has_actionable_import_error(monkeypatch):
    import sys
    from types import ModuleType

    monkeypatch.setattr("datasets.config.ATOMWORKS_AVAILABLE", True)
    monkeypatch.setitem(sys.modules, "atomworks.io", ModuleType("atomworks.io"))
    with pytest.raises(ImportError, match="AtomWorks >=3.1.0"):
        AtomicStructure().decode_example({"bytes": b"unused", "path": None})


@require_atomworks
def test_materialize_saves_edits_without_mutating_source():
    atoms = _roundtrip(str(CIF_FILE))
    original = atoms.get_annotation("_hf_encoded", n_body=0).item().copy()
    atoms.coord += 3
    encoded = AtomicStructure().materialize(atoms)
    np.testing.assert_array_equal(_roundtrip(encoded).coord, atoms.coord)
    assert atoms.get_annotation("_hf_encoded", n_body=0).item() == original
    assert AtomicStructure().encode_example(atoms)["bytes"] == CIF_FILE.read_bytes()
    dataset = Dataset.from_dict({"s": [CIF_FILE.read_bytes()]}, features=_features())

    def edit(row):
        row["s"].coord += 3
        return {"s": AtomicStructure().materialize(row["s"])}

    np.testing.assert_array_equal(dataset.map(edit)[0]["s"].coord, atoms.coord)


@require_atomworks
@pytest.mark.parametrize("heterogeneous", [False, True])
def test_materialize_models_keeps_coordinates(heterogeneous):
    from biotite.structure import stack

    first = _roundtrip(str(CIF_FILE))
    second = first[:3] if heterogeneous else first.copy()
    second.coord = second.coord + 5
    source = [first, second] if heterogeneous else stack([first, second])
    result = _roundtrip(AtomicStructure().materialize(source))
    assert len(result) == 2
    for got, want in zip(result, [first, second]):
        np.testing.assert_array_equal(got.coord, want.coord)


@require_atomworks
@pytest.mark.parametrize("dtype", [np.int8, np.int32, np.int64, np.float32, np.float64, np.bool_, "U8"])
def test_materialize_scalar_annotation_values(dtype):
    atoms = _roundtrip(str(CIF_FILE))
    values = np.arange(len(atoms)).astype(dtype)
    if np.dtype(dtype).kind == "f":
        values = values / 3
        values[2] = np.nan
    atoms.set_annotation("custom_value", values)
    result = _roundtrip(AtomicStructure().materialize(atoms))
    # The upstream reader infers extra-field dtypes; the contract here is value preservation.
    got = result.get_annotation("custom_value").astype(dtype)
    if np.dtype(dtype).kind == "f":
        np.testing.assert_allclose(got, values, rtol=1e-6, equal_nan=True)
    else:
        np.testing.assert_array_equal(got, values)


@require_atomworks
def test_materialize_rejects_integer_overflow():
    atoms = _roundtrip(str(CIF_FILE))
    atoms.set_annotation("large_id", np.full(len(atoms), 2**40, dtype=np.int64))
    with pytest.raises(ValueError, match="signed 32-bit"):
        AtomicStructure().materialize(atoms)


@require_atomworks
@pytest.mark.parametrize("kind", ["multidimensional", "system", "pairwise"])
def test_materialize_rejects_each_unsupported_annotation_kind(kind):
    from atomworks.io.utils.atom_array_plus import AnnotationList2D

    atoms = _roundtrip(str(CIF_FILE))
    if kind == "multidimensional":
        atoms.set_annotation("custom", np.zeros((len(atoms), 3)))
    elif kind == "system":
        atoms.set_annotation("custom", np.array(1.0), n_body=0)
    else:
        atoms.set_annotation("custom", AnnotationList2D(len(atoms), np.array([[0, 1]]), np.array([1.0])), n_body=2)
    with pytest.raises(ValueError, match="custom annotations losslessly"):
        AtomicStructure().materialize(atoms)


@require_atomworks
@pytest.mark.parametrize("preset", ["minimal", "default", "rcsb"])
@pytest.mark.parametrize("file_type", ["cif", "bcif"])
def test_parse_presets_match_atomworks(preset, file_type):
    from atomworks.io import atom_array_to_file, parse
    from atomworks.io.config import ParseConfig

    payload = (
        CIF_FILE.read_bytes()
        if file_type == "cif"
        else atom_array_to_file(_parse_with_atomworks(CIF_FILE), file_type="bcif")
    )
    source = io.StringIO(payload.decode()) if file_type == "cif" else io.BytesIO(payload)
    expected = parse(
        source,
        config=ParseConfig.from_preset(preset, file_type=file_type, build_assembly=None, return_atom_array_plus=True),
    )["asym_unit"][0]
    actual = _roundtrip(payload, parse_config={"preset": preset})
    np.testing.assert_array_equal(actual.coord, expected.coord)
    np.testing.assert_array_equal(actual.atom_name, expected.atom_name)
    assert actual.bonds == expected.bonds
    assert AtomicStructure().encode_example(actual)["bytes"] == payload


@require_atomworks
@pytest.mark.parametrize("model", [1, 2, -1])
def test_select_model_from_materialized_stack(model):
    from biotite.structure import stack

    first = _roundtrip(str(CIF_FILE))
    second = first.copy()
    second.coord += 5
    payload = AtomicStructure().materialize(stack([first, second]))
    result = _roundtrip(payload, parse_config={"model": model})
    expected = first if model == 1 else second
    np.testing.assert_array_equal(result.coord, expected.coord)
    assert result.bonds == expected.bonds


@require_atomworks
@pytest.mark.parametrize("num_proc", [None, 2])
def test_preprocessing_with_map(tmp_path, num_proc):
    policy = AtomicStructure(parse_config={"remove_waters": True})
    dataset = Dataset.from_dict({"s": [CIF_FILE.read_bytes(), None]}, features=_features())

    def prepare(example):
        atoms = example["s"]
        return {"s": None if atoms is None else AtomicStructure().materialize(atoms)}

    prepared = dataset.cast_column("s", policy).map(
        prepare, features=dataset.features, load_from_cache_file=False, num_proc=num_proc
    )
    prepared.save_to_disk(tmp_path / "prepared")
    restored = load_from_disk(tmp_path / "prepared")
    assert restored.features["s"] == AtomicStructure()
    assert restored[1]["s"] is None
    np.testing.assert_array_equal(restored[0]["s"].coord, dataset.cast_column("s", policy)[0]["s"].coord)
    assert dataset.data.column("s")[0].as_py()["bytes"] == CIF_FILE.read_bytes()


@require_atomworks
@pytest.mark.parametrize("altloc", ["first", "B"])
def test_select_alternate_conformer_without_changing_storage(altloc):
    payload = (DATA_DIR / "test_altloc.cif").read_bytes()
    result = _roundtrip(payload, parse_config={"altloc": altloc})
    assert result.label_alt_id.tolist() == ["A" if altloc == "first" else "B", "."]
    assert AtomicStructure().encode_example(result)["bytes"] == payload


@require_atomworks
@pytest.mark.parametrize(
    "path,token",
    [
        ("https://example.com/structure.cif", None),
        ("https://huggingface.co/datasets/user/structures/resolve/main/structure.cif", "test-token"),
        ("hf://datasets/user/structures@main/structure.cif", "test-token"),
    ],
)
def test_decode_remote_file(monkeypatch, path, token):
    def open_remote(url, mode, download_config):
        assert url == path
        assert mode == "rb"
        assert download_config.token == token
        return io.BytesIO(CIF_FILE.read_bytes())

    monkeypatch.setattr("datasets.features.atomic_structure.xopen", open_remote)
    atoms = AtomicStructure().decode_example(
        {"path": path, "bytes": None}, token_per_repo_id={"user/structures": "test-token"}
    )
    _assert_same_atoms(atoms, _parse_with_atomworks(CIF_FILE))
