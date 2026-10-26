import bz2
import gzip
import io
import textwrap
import warnings
from pathlib import Path

import numpy as np
import pyarrow as pa
import pytest

from datasets import AtomicStructure, Dataset, Features, load_from_disk
from datasets.features.atomic_structure import get_atomic_structure_decoder, register_atomic_structure_decoder
from datasets.features.features import generate_from_dict

from ..utils import require_biotite, require_zstandard


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

# Acetic acid: a double bond and a single bond to oxygen.
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


def _features(**kwargs):
    return Features({"s": AtomicStructure(**kwargs)})


def test_storage_type():
    feature = AtomicStructure()
    annotations = feature.pa_type.field("annotations").type
    assert [f.name for f in annotations] == [
        "chain_id",
        "res_id",
        "ins_code",
        "res_name",
        "hetero",
        "atom_name",
        "element",
        "b_factor",
        "occupancy",
        "charge",
    ]
    assert feature.pa_type.field("coord").type == pa.list_(pa.list_(pa.list_(pa.float32(), 3)))
    assert feature.pa_type.get_field_index("global_annotations") < 0

    custom = AtomicStructure(
        annotations={"atom_id": "int64"},
        global_annotations={"resolution": "float32"},
        pair_annotations={"contact": "bool"},
    )
    assert [f.name for f in custom.pa_type.field("annotations").type][-1] == "atom_id"
    assert custom.pa_type.field("global_annotations").type == pa.struct([("resolution", pa.float32())])
    assert custom.pa_type.field("pair_annotations").type.field("contact").type.field("value").type == pa.list_(
        pa.bool_()
    )

    with pytest.raises(ValueError, match="core annotation"):
        AtomicStructure(annotations={"res_name": "string"})


@pytest.mark.parametrize(
    "feature",
    [
        AtomicStructure(),
        AtomicStructure(annotations={}, decoder="numpy"),
        AtomicStructure(
            annotations={"atom_id": "int64"}, global_annotations={"r": "float32"}, pair_annotations={"d": "float32"}
        ),
    ],
)
def test_serialization(feature):
    features = Features({"s": feature})
    assert generate_from_dict(features.to_dict()["s"]) == feature
    assert Features.from_arrow_schema(features.arrow_schema) == features
    assert Features._from_yaml_list(features._to_yaml_list()) == features


@require_biotite
@pytest.mark.parametrize(
    "source", ["path_pdb", "path_cif", "pathlib", "bytes_pdb", "bytes_cif", "dict_bytes", "dict_path"]
)
def test_encode_files(source):
    value = {
        "path_pdb": str(PDB_FILE),
        "path_cif": str(CIF_FILE),
        "pathlib": PDB_FILE,
        "bytes_pdb": PDB_FILE.read_bytes(),
        "bytes_cif": CIF_FILE.read_bytes(),
        "dict_bytes": {"bytes": CIF_FILE.read_bytes(), "path": "renamed.cif"},
        "dict_path": {"bytes": None, "path": str(PDB_FILE)},
    }[source]
    atoms = Dataset.from_dict({"s": [value]}, features=_features())[0]["s"]
    assert atoms.atom_name.tolist() == ATOM_NAMES
    assert atoms.res_id.tolist() == [1] * 5 + [2] * 4
    assert atoms.b_factor.tolist() == [20.0] * 9
    assert atoms.bonds.get_bond_count() == 8  # from the CCD, including the peptide bond
    np.testing.assert_allclose(atoms.coord[1], [1.458, 0.0, 0.0])


@require_biotite
@pytest.mark.parametrize("compress", [gzip.compress, bz2.compress, pytest.param("zstd", marks=require_zstandard)])
def test_encode_compressed(compress):
    if compress == "zstd":
        import zstandard

        compress = zstandard.ZstdCompressor().compress
    for data in (CIF_FILE.read_bytes(), PDB_FILE.read_bytes()):
        atoms = Dataset.from_dict({"s": [compress(data)]}, features=_features())[0]["s"]
        assert atoms.atom_name.tolist() == ATOM_NAMES


@require_biotite
def test_encode_bcif_with_atom_site_annotation():
    import biotite.structure.io.pdbx as pdbx

    atoms = pdbx.get_structure(pdbx.CIFFile.read(str(CIF_FILE)), model=1)
    bcif_file = pdbx.BinaryCIFFile()
    pdbx.set_structure(bcif_file, atoms)
    bcif = io.BytesIO()
    bcif_file.write(bcif)
    features = _features(annotations={"label_asym_id": "string", "b_factor": "float32"})
    atoms = Dataset.from_dict({"s": [bcif.getvalue()]}, features=features)[0]["s"]
    assert atoms.atom_name.tolist() == ATOM_NAMES
    assert atoms.label_asym_id.tolist() == ["A"] * 9
    assert "occupancy" not in atoms.get_annotation_categories()


@require_biotite
def test_encode_sdf_keeps_bond_orders():
    atoms = Dataset.from_dict({"s": [{"bytes": ACETIC_ACID_SDF.encode(), "path": "acid.sdf"}]}, features=_features())[
        0
    ]["s"]
    assert atoms.element.tolist() == ["C", "C", "O", "O"]
    assert sorted(atoms.bonds.as_array().tolist()) == [[0, 1, 1], [1, 2, 2], [1, 3, 1]]


@require_biotite
def test_multiple_models():
    import biotite.structure as struc

    dataset = Dataset.from_dict({"s": [MULTI_MODEL_PDB.encode()]}, features=_features())
    stack = dataset[0]["s"]
    assert isinstance(stack, struc.AtomArrayStack)
    assert stack.coord.shape == (2, 2, 3)
    assert stack.coord[1, :, 0].tolist() == [0.5, 1.5]
    raw = dataset.cast_column("s", AtomicStructure(decoder="numpy"))[0]["s"]
    assert raw["coord"].shape == (2, 2, 3)


@require_biotite
def test_encode_ase_periodic_structure():
    ase_build = pytest.importorskip("ase.build")

    crystal = ase_build.bulk("Cu", "fcc", a=3.6, cubic=True)
    atoms = Dataset.from_dict({"s": [crystal]}, features=_features())[0]["s"]
    assert atoms.element.tolist() == ["CU"] * 4
    np.testing.assert_allclose(atoms.coord, crystal.get_positions(), atol=1e-5)
    np.testing.assert_allclose(atoms.box, np.diag([3.6, 3.6, 3.6]), atol=1e-5)

    molecule = ase_build.molecule("H2O")
    atoms = Dataset.from_dict({"s": [molecule]}, features=_features())[0]["s"]
    assert atoms.box is None


@require_biotite
def test_encode_rdkit_molecule():
    Chem = pytest.importorskip("rdkit.Chem")
    AllChem = pytest.importorskip("rdkit.Chem.AllChem")

    mol = Chem.AddHs(Chem.MolFromSmiles("CCO"))
    AllChem.EmbedMolecule(mol, randomSeed=0)
    atoms = Dataset.from_dict({"s": [mol]}, features=_features())[0]["s"]
    assert atoms.array_length() == 9
    assert sorted(set(atoms.element.tolist())) == ["C", "H", "O"]
    assert atoms.bonds.get_bond_count() == 8


@require_biotite
def test_encode_atom_array_and_annotations():
    import biotite.structure as struc

    atoms = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=_features())[0]["s"]
    atoms.set_annotation("confidence", np.linspace(0, 1, 9))
    atoms.box = np.eye(3) * 50
    with pytest.warns(UserWarning, match="confidence"):
        again = Dataset.from_dict({"s": [atoms]}, features=_features())[0]["s"]
    assert "confidence" not in again.get_annotation_categories()

    features = _features(annotations={"confidence": "float32"})
    again = Dataset.from_dict({"s": [atoms]}, features=features)[0]["s"]
    np.testing.assert_allclose(again.confidence, np.linspace(0, 1, 9), atol=1e-6)
    np.testing.assert_allclose(again.box, np.eye(3) * 50)
    assert again.bonds == atoms.bonds
    assert isinstance(again, struc.AtomArray)


class _AtomArrayWithBodies:
    """Minimal stand-in for an AtomArray subclass with system-wide (n_body=0) and pairwise (n_body=2) annotations."""

    def __init__(self, atoms, global_annotations, pair_annotations):
        self._atoms, self._global, self._pairs = atoms, global_annotations, pair_annotations
        self.coord, self.bonds, self.box = atoms.coord, atoms.bonds, atoms.box

    def get_annotation_categories(self, n_body=1):
        return {0: list(self._global), 1: self._atoms.get_annotation_categories(), 2: list(self._pairs)}[n_body]

    def get_annotation(self, name, n_body=1):
        return {0: self._global, 2: self._pairs}[n_body][name] if n_body != 1 else self._atoms.get_annotation(name)


@require_biotite
def test_global_and_pair_annotations():
    from types import SimpleNamespace

    atoms = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=_features())[0]["s"]
    contacts = SimpleNamespace(pairs=np.array([[0, 5], [1, 6]]), values=np.array([3.5, 4.0]))
    value = _AtomArrayWithBodies(atoms, {"resolution": np.float64(1.8)}, {"distance": contacts})
    features = _features(
        global_annotations={"resolution": "float32"}, pair_annotations={"distance": "float32"}, decoder="numpy"
    )
    structure = Dataset.from_dict({"s": [value]}, features=features)[0]["s"]
    assert structure["global_annotations"] == {"resolution": pytest.approx(1.8)}
    assert structure["pair_annotations"]["distance"]["atom1"].tolist() == [0, 1]
    assert structure["pair_annotations"]["distance"]["atom2"].tolist() == [5, 6]
    assert structure["pair_annotations"]["distance"]["value"].tolist() == [3.5, 4.0]

    dataset = Dataset.from_dict({"s": [value]}, features=_features(global_annotations={"resolution": "float32"}))
    with pytest.warns(UserWarning, match="global or pair annotations"):
        dataset[0]["s"]


def test_numpy_decoder_needs_no_dependency(monkeypatch):
    monkeypatch.setattr("datasets.config.BIOTITE_AVAILABLE", False)
    value = {"coord": [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]], "annotations": {"atom_name": ["N", "CA"]}}
    structure = Dataset.from_dict({"s": [value]}, features=_features(decoder="numpy"))[0]["s"]
    assert structure["coord"].shape == (1, 2, 3)
    assert structure["annotations"]["atom_name"].tolist() == ["N", "CA"]
    assert structure["annotations"]["res_name"].tolist() == ["", ""]
    assert structure["annotations"]["res_id"].tolist() == [0, 0]
    assert np.isnan(structure["annotations"]["b_factor"]).all()
    assert structure["bonds"]["atom1"].tolist() == []
    assert structure["box"] is None

    with pytest.raises(ImportError, match="biotite"):
        Dataset.from_dict({"s": [value]}, features=_features())[0]["s"]
    with pytest.raises(ImportError, match="biotite"):
        AtomicStructure().encode_example(str(PDB_FILE))


@require_biotite
def test_decoded_numpy_structure_roundtrips():
    features = _features(decoder="numpy")
    structure = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=features)[0]["s"]
    again = Dataset.from_dict({"s": [structure]}, features=features)[0]["s"]
    np.testing.assert_array_equal(again["coord"], structure["coord"])
    for name, values in structure["annotations"].items():
        np.testing.assert_array_equal(again["annotations"][name], values)
    for name, values in structure["bonds"].items():
        np.testing.assert_array_equal(again["bonds"][name], values)


@require_biotite
def test_cast_column_from_paths_bytes_and_file_references():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE), str(CIF_FILE)]}).cast_column("s", AtomicStructure())
    assert [atoms.atom_name.tolist() for atoms in dataset["s"]] == [ATOM_NAMES, ATOM_NAMES]

    dataset = Dataset.from_dict({"s": [PDB_FILE.read_bytes()]}).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 9

    # file references as stored by other file-based features
    references = pa.array([{"bytes": CIF_FILE.read_bytes(), "path": "test_protein.cif"}])
    dataset = Dataset(pa.table({"s": references})).cast_column("s", AtomicStructure())
    assert len(dataset[0]["s"]) == 9


def test_encode_rejects_unknown_input():
    with pytest.raises(ValueError, match="An atomic structure should be"):
        AtomicStructure().encode_example(42)


@require_biotite
def test_decode_false_and_flatten():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE)]}, features=_features(decode=False))
    raw = dataset[0]["s"]
    assert raw["annotations"]["atom_name"] == ATOM_NAMES
    assert raw["coord"][0][1] == pytest.approx([1.458, 0.0, 0.0])
    flat = dataset.flatten()
    assert "s.annotations.atom_name" in flat.column_names
    assert "s.coord" in flat.column_names
    with pytest.raises(RuntimeError, match="Decoding is disabled"):
        AtomicStructure(decode=False).decode_example(raw)


@require_biotite
@pytest.mark.parametrize("format_type", [None, "numpy", "arrow"])
def test_formats(format_type):
    dataset = Dataset.from_dict({"s": [str(PDB_FILE), MULTI_MODEL_PDB.encode()]}, features=_features(decoder="numpy"))
    structure = dataset.with_format(format_type)[0]["s"]
    if format_type == "arrow":
        coord = structure.combine_chunks().field("coord").flatten().flatten().flatten().to_numpy()
        assert coord.reshape(-1, 3).shape == (9, 3)
    else:
        assert structure["coord"].shape == (1, 9, 3)
        assert structure["annotations"]["atom_name"].tolist() == ATOM_NAMES
        assert structure["annotations"]["charge"].tolist() == [0] * 9


@require_biotite
def test_save_and_load_from_disk(tmp_path):
    features = _features(annotations={"atom_id": "int32"}, global_annotations={"resolution": "float32"})
    dataset = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=features)
    dataset.save_to_disk(tmp_path / "saved")
    reloaded = load_from_disk(tmp_path / "saved")
    assert reloaded.features == dataset.features
    np.testing.assert_array_equal(reloaded[0]["s"].coord, dataset[0]["s"].coord)
    assert reloaded[0]["s"].atom_id.tolist() == list(range(1, 10))


@require_biotite
def test_register_decoder():
    register_atomic_structure_decoder("n_atoms", lambda structure: structure["coord"].shape[1])
    dataset = Dataset.from_dict({"s": [str(PDB_FILE)]}, features=_features(decoder="n_atoms"))
    assert dataset[0]["s"] == 9
    with pytest.raises(ValueError, match="Unknown atomic structure decoder 'missing'"):
        get_atomic_structure_decoder("missing")


@require_biotite
def test_no_warning_for_declared_annotations():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        Dataset.from_dict({"s": [str(PDB_FILE)]}, features=_features())[0]["s"]
    assert not [w for w in caught if "not declared" in str(w.message)]
