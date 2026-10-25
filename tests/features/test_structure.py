import bz2
import gzip
import textwrap
from pathlib import Path

import numpy as np
import pyarrow as pa
import pytest

from datasets import Dataset, Features, Structure, Value, load_from_disk
from datasets.features._structure_io import read_structure
from datasets.features.features import generate_from_dict
from datasets.features.structure import get_structure_decoder, register_structure_decoder

from ..utils import require_biotite, require_msgpack, require_zstandard


DATA_DIR = Path(__file__).parent / "data"
PDB_FILE = DATA_DIR / "test_protein.pdb"
CIF_FILE = DATA_DIR / "test_protein.cif"
ATOM_NAMES = ["N", "CA", "C", "O", "CB", "N", "CA", "C", "O"]

# Nucleotide and ligand with quoted atom names, a multi-line text field, missing values, a single-row
# category and struct_conn bonds (one to a symmetry mate, which is not stored).
CIF_WITH_BONDS = textwrap.dedent(
    """\
    data_1ABC
    _struct.title
    ;A multi-line title
    with 'quotes' and _underscores
    ;
    loop_
    _atom_site.group_PDB
    _atom_site.type_symbol
    _atom_site.label_atom_id
    _atom_site.label_alt_id
    _atom_site.label_comp_id
    _atom_site.label_asym_id
    _atom_site.label_entity_id
    _atom_site.label_seq_id
    _atom_site.pdbx_PDB_ins_code
    _atom_site.Cartn_x
    _atom_site.Cartn_y
    _atom_site.Cartn_z
    _atom_site.occupancy
    _atom_site.B_iso_or_equiv
    _atom_site.pdbx_formal_charge
    _atom_site.auth_seq_id
    _atom_site.auth_asym_id
    _atom_site.pdbx_PDB_model_num
    ATOM   O "O5'" . DA  A 1 1 ? 1.000  2.000  3.000  1.00 10.00 ? 1  B 1
    ATOM   C "C5'" . DA  A 1 1 ? 2.000  2.000  3.000  1.00 11.00 ? 1  B 1
    HETATM ZN ZN   . ZN  B 2 . ? 9.000  9.000  9.000  0.50 30.00 2 101 B 1
    HETATM O  O    . HOH C 3 . ? 5.000  5.000  5.000  1.00 40.00 ? 201 B 1
    #
    loop_
    _struct_conn.id
    _struct_conn.conn_type_id
    _struct_conn.ptnr1_auth_asym_id
    _struct_conn.ptnr1_auth_seq_id
    _struct_conn.ptnr1_label_comp_id
    _struct_conn.ptnr1_label_atom_id
    _struct_conn.ptnr1_symmetry
    _struct_conn.ptnr2_auth_asym_id
    _struct_conn.ptnr2_auth_seq_id
    _struct_conn.ptnr2_label_comp_id
    _struct_conn.ptnr2_label_atom_id
    _struct_conn.ptnr2_symmetry
    _struct_conn.pdbx_value_order
    metalc1 metalc B 1   DA  "O5'" 1_555 B 101 ZN ZN 1_555 ?
    metalc2 metalc B 201 HOH O     1_555 B 101 ZN ZN 2_655 ?
    #
    """
)

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
    HETATM    3 FE   HEM A 100      10.000  10.000  10.000  1.00  5.00          FE2+
    CONECT    1    2
    CONECT    2    1
    END
    """
)


def _bcif(columns: dict, header: str = "TEST") -> bytes:
    """Encode an `atom_site` category as BinaryCIF, exercising the encodings readers must undo."""
    import msgpack

    def byte_array(values, type_code, dtype):
        return np.asarray(values, dtype=dtype).tobytes(), [{"kind": "ByteArray", "type": type_code}]

    def encode(values):
        values = list(values)
        missing = np.array([v is None for v in values])
        mask = None
        if missing.any():
            data, encoding = byte_array(missing.astype(np.uint8), 4, "<u1")
            mask = {"data": data, "encoding": encoding}
        if all(isinstance(v, float) or v is None for v in values) and any(isinstance(v, float) for v in values):
            # FixedPoint -> Delta -> IntegerPacking (int8, with continuation) -> ByteArray
            fixed = np.round(np.array([0.0 if v is None else v for v in values]) * 1000).astype(np.int64)
            deltas = np.diff(fixed, prepend=fixed[0])
            packed = []
            for d in deltas.tolist():
                while d >= 127:
                    packed.append(127)
                    d -= 127
                while d <= -128:
                    packed.append(-128)
                    d += 128
                packed.append(d)
            data, tail = byte_array(packed, 1, "<i1")
            encoding = [
                {"kind": "FixedPoint", "factor": 1000, "srcType": 33},
                {"kind": "Delta", "origin": int(fixed[0]), "srcType": 3},
                {"kind": "IntegerPacking", "byteCount": 1, "isUnsigned": False, "srcSize": len(values)},
            ] + tail
        elif all(isinstance(v, int) or v is None for v in values):
            # RunLength -> ByteArray(int32)
            ints = [0 if v is None else v for v in values]
            runs = []
            for v in ints:
                if runs and runs[-2] == v:
                    runs[-1] += 1
                else:
                    runs += [v, 1]
            data, tail = byte_array(runs, 3, "<i4")
            encoding = [{"kind": "RunLength", "srcType": 3, "srcSize": len(values)}] + tail
        else:
            strings = sorted({v for v in values if v is not None})
            offsets = np.cumsum([0] + [len(s) for s in strings])
            indices = [-1 if v is None else strings.index(v) for v in values]
            data, _ = byte_array(indices, 3, "<i4")
            offset_data, offset_encoding = byte_array(offsets, 3, "<i4")
            encoding = [
                {
                    "kind": "StringArray",
                    "dataEncoding": [{"kind": "ByteArray", "type": 3}],
                    "stringData": "".join(strings),
                    "offsetEncoding": offset_encoding,
                    "offsets": offset_data,
                }
            ]
        return {"data": data, "encoding": encoding}, mask

    encoded_columns = []
    for name, values in columns.items():
        data, mask = encode(values)
        encoded_columns.append({"name": name, "data": data, "mask": mask})
    category = {"name": "_atom_site", "rowCount": len(next(iter(columns.values()))), "columns": encoded_columns}
    return msgpack.packb({"version": "0.3.0", "dataBlocks": [{"header": header, "categories": [category]}]})


def _fixture_as_bcif() -> bytes:
    pdb = read_structure(PDB_FILE.read_bytes())["atoms"]
    return _bcif(
        {
            "group_PDB": pdb["group_PDB"].tolist(),
            "type_symbol": pdb["type_symbol"].tolist(),
            "label_atom_id": pdb["label_atom_id"].tolist(),
            "label_comp_id": pdb["label_comp_id"].tolist(),
            "label_asym_id": pdb["label_asym_id"].tolist(),
            "label_seq_id": pdb["auth_seq_id"].tolist(),
            # values far apart so packed deltas need continuation bytes
            "Cartn_x": [float(x) * 100 for x in pdb["Cartn_xyz"][:, 0]],
            "Cartn_y": pdb["Cartn_xyz"][:, 1].astype(float).tolist(),
            "Cartn_z": pdb["Cartn_xyz"][:, 2].astype(float).tolist(),
            "B_iso_or_equiv": [20.0] * 8 + [None],
            "auth_seq_id": pdb["auth_seq_id"].tolist(),
            "auth_asym_id": pdb["auth_asym_id"].tolist(),
            "pdbx_PDB_model_num": [1] * 9,
        }
    )


def test_read_pdb():
    structure = read_structure(PDB_FILE.read_bytes(), str(PDB_FILE))
    atoms = structure["atoms"]
    assert structure["id"] == "TEST"
    assert atoms["Cartn_xyz"].shape == (9, 3)
    assert atoms["Cartn_xyz"].dtype == np.float32
    assert atoms["label_atom_id"].tolist() == ATOM_NAMES
    assert atoms["auth_seq_id"].tolist() == [1] * 5 + [2] * 4
    assert atoms["type_symbol"].tolist() == ["N", "C", "C", "O", "C", "N", "C", "C", "O"]
    assert atoms["label_seq_id"].tolist() == [None] * 9  # PDB files have no label numbering
    assert atoms["B_iso_or_equiv"].tolist() == [20.0] * 9


def test_read_mmcif_matches_pdb():
    from_cif = read_structure(CIF_FILE.read_bytes(), str(CIF_FILE))["atoms"]
    from_pdb = read_structure(PDB_FILE.read_bytes(), str(PDB_FILE))["atoms"]
    np.testing.assert_allclose(from_cif["Cartn_xyz"], from_pdb["Cartn_xyz"])
    for name in ["label_atom_id", "label_comp_id", "auth_asym_id", "auth_seq_id", "type_symbol", "group_PDB"]:
        assert from_cif[name].tolist() == from_pdb[name].tolist(), name
    assert from_cif["label_seq_id"].tolist() == [1] * 5 + [2] * 4


def test_read_mmcif_quoting_missing_values_and_bonds():
    structure = read_structure(CIF_WITH_BONDS.encode())
    atoms, bonds = structure["atoms"], structure["bonds"]
    assert structure["id"] == "1ABC"
    assert atoms["label_atom_id"].tolist() == ["O5'", "C5'", "ZN", "O"]
    assert atoms["label_alt_id"].tolist() == ["", "", "", ""]
    assert atoms["label_seq_id"].tolist() == [1, 1, None, None]
    assert atoms["pdbx_formal_charge"].tolist() == [None, None, 2, None]
    assert atoms["occupancy"].tolist() == [1.0, 1.0, 0.5, 1.0]
    # the bond to a symmetry mate (2_655) is dropped; the other one is kept
    assert bonds["atom_index_1"].tolist() == [0]
    assert bonds["atom_index_2"].tolist() == [2]
    assert bonds["conn_type_id"].tolist() == ["metalc"]
    assert bonds["pdbx_value_order"].tolist() == [""]


def test_read_mmcif_single_row_struct_conn():
    single_row = CIF_WITH_BONDS.split("loop_\n_struct_conn.id")[0] + textwrap.dedent(
        """\
        _struct_conn.id                 covale1
        _struct_conn.conn_type_id       covale
        _struct_conn.ptnr1_auth_asym_id B
        _struct_conn.ptnr1_auth_seq_id  1
        _struct_conn.ptnr1_label_comp_id DA
        _struct_conn.ptnr1_label_atom_id "C5'"
        _struct_conn.ptnr2_auth_asym_id B
        _struct_conn.ptnr2_auth_seq_id  201
        _struct_conn.ptnr2_label_comp_id HOH
        _struct_conn.ptnr2_label_atom_id O
        _struct_conn.pdbx_value_order   sing
        #
        """
    )
    bonds = read_structure(single_row.encode())["bonds"]
    assert bonds["atom_index_1"].tolist() == [1]
    assert bonds["atom_index_2"].tolist() == [3]
    assert bonds["pdbx_value_order"].tolist() == ["sing"]


def test_read_pdb_models_and_conect():
    structure = read_structure(MULTI_MODEL_PDB.encode())
    atoms, bonds = structure["atoms"], structure["bonds"]
    assert atoms["pdbx_PDB_model_num"].tolist() == [1, 1, 2, 2, 2]
    assert atoms["Cartn_xyz"][:, 0].tolist() == [0.0, 1.0, 0.5, 1.5, 10.0]
    assert atoms["type_symbol"].tolist() == ["N", "C", "N", "C", "Fe"]
    assert atoms["pdbx_formal_charge"].tolist() == [0, 0, 0, 0, 2]
    assert bonds["atom_index_1"].tolist() == [0]
    assert bonds["atom_index_2"].tolist() == [1]


@require_msgpack
def test_read_bcif_matches_pdb():
    structure = read_structure(_fixture_as_bcif())
    from_pdb = read_structure(PDB_FILE.read_bytes())["atoms"]
    atoms = structure["atoms"]
    assert structure["id"] == "TEST"
    np.testing.assert_allclose(atoms["Cartn_xyz"][:, 0], from_pdb["Cartn_xyz"][:, 0] * 100, atol=1e-3)
    np.testing.assert_allclose(atoms["Cartn_xyz"][:, 1:], from_pdb["Cartn_xyz"][:, 1:], atol=1e-3)
    for name in ["label_atom_id", "label_comp_id", "auth_asym_id", "auth_seq_id", "type_symbol"]:
        assert atoms[name].tolist() == from_pdb[name].tolist(), name
    assert atoms["label_seq_id"].tolist() == [1] * 5 + [2] * 4
    assert atoms["B_iso_or_equiv"][:8].tolist() == [20.0] * 8
    assert np.isnan(atoms["B_iso_or_equiv"][8])


@pytest.mark.parametrize(
    "compress",
    [gzip.compress, bz2.compress, pytest.param("zstd", marks=require_zstandard)],
)
@pytest.mark.parametrize("path", [None, "file.cif.compressed"])
def test_read_compressed(compress, path):
    if compress == "zstd":
        import zstandard

        compress = zstandard.ZstdCompressor().compress
    structure = read_structure(compress(CIF_FILE.read_bytes()), path)
    assert structure["atoms"]["label_atom_id"].tolist() == ATOM_NAMES


@pytest.mark.parametrize("file", [PDB_FILE, CIF_FILE])
def test_format_detected_from_content(file):
    assert read_structure(file.read_bytes())["atoms"]["label_atom_id"].tolist() == ATOM_NAMES


def test_read_errors():
    with pytest.raises(ValueError, match="no ATOM or HETATM"):
        read_structure(b"HEADER    EMPTY\nEND\n")
    with pytest.raises(ValueError, match="atom_site"):
        read_structure(b"data_EMPTY\n_entry.id EMPTY\n")
    with pytest.raises(ValueError, match="Malformed"):
        read_structure(b"data_X\nloop_\n_atom_site.Cartn_x\n_atom_site.Cartn_y\n1.0 2.0 3.0\n")


def test_feature_type_and_serialization():
    feature = Structure(decoder="biotite")
    assert feature() == Structure.pa_type
    assert generate_from_dict(Features({"s": feature}).to_dict()["s"]) == feature
    assert Features.from_arrow_schema(Features({"s": feature}).arrow_schema) == Features({"s": feature})


@pytest.mark.parametrize("source", ["path", "pathlib", "bytes", "dict_bytes", "dict_path"])
def test_encode_inputs(source):
    value = {
        "path": str(PDB_FILE),
        "pathlib": PDB_FILE,
        "bytes": PDB_FILE.read_bytes(),
        "dict_bytes": {"bytes": PDB_FILE.read_bytes(), "path": "renamed.pdb"},
        "dict_path": {"bytes": None, "path": str(PDB_FILE)},
    }[source]
    dataset = Dataset.from_dict({"structure": [value]}, features=Features({"structure": Structure()}))
    structure = dataset[0]["structure"]
    assert set(structure) == {"id", "atoms", "bonds"}
    assert structure["atoms"]["label_atom_id"].tolist() == ATOM_NAMES
    assert structure["atoms"]["Cartn_xyz"].shape == (9, 3)


def test_encode_rejects_unknown_input():
    with pytest.raises(ValueError, match="A structure should be"):
        Structure().encode_example(42)


def test_cast_column_from_paths_bytes_and_file_references():
    dataset = Dataset.from_dict({"path": [str(PDB_FILE), str(CIF_FILE)]})
    from_paths = dataset.cast_column("path", Structure())
    assert [row["path"]["atoms"]["label_atom_id"].tolist() for row in from_paths] == [ATOM_NAMES, ATOM_NAMES]

    dataset = Dataset.from_dict({"structure": [PDB_FILE.read_bytes()]})
    assert dataset.cast_column("structure", Structure())[0]["structure"]["id"] == "TEST"

    # e.g. a column stored as {"bytes", "path"} file references, as other file-based features do
    references = pa.array([{"bytes": CIF_FILE.read_bytes(), "path": "test_protein.cif"}])
    dataset = Dataset(pa.table({"structure": references}))
    assert dataset.cast_column("structure", Structure())[0]["structure"]["atoms"]["Cartn_xyz"].shape == (9, 3)


def test_decoded_structure_roundtrips():
    features = Features({"structure": Structure()})
    decoded = Dataset.from_dict({"structure": [str(CIF_FILE)]}, features=features)[0]["structure"]
    again = Dataset.from_dict({"structure": [decoded]}, features=features)[0]["structure"]
    for name, values in decoded["atoms"].items():
        np.testing.assert_array_equal(values, again["atoms"][name])


def test_missing_atom_items_are_filled():
    value = {"atoms": {"Cartn_xyz": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], "label_atom_id": ["N", "CA"]}}
    structure = Dataset.from_dict({"s": [value]}, features=Features({"s": Structure()}))[0]["s"]
    atoms = structure["atoms"]
    assert atoms["label_atom_id"].tolist() == ["N", "CA"]
    assert atoms["label_comp_id"].tolist() == ["", ""]
    assert atoms["label_seq_id"].tolist() == [-1, -1]
    assert atoms["pdbx_formal_charge"].tolist() == [0, 0]
    assert np.isnan(atoms["occupancy"]).all()
    assert structure["id"] == ""
    assert structure["bonds"]["atom_index_1"].tolist() == []


def test_decode_false_and_flatten():
    dataset = Dataset.from_dict({"s": [str(PDB_FILE)]}, features=Features({"s": Structure(decode=False)}))
    raw = dataset[0]["s"]
    assert raw["atoms"]["label_atom_id"] == ATOM_NAMES
    assert raw["atoms"]["Cartn_xyz"][1] == pytest.approx([1.458, 0.0, 0.0])
    flat = dataset.flatten()
    assert "s.atoms.Cartn_xyz" in flat.column_names
    assert flat.features["s.id"] == Value("string")
    with pytest.raises(RuntimeError, match="Decoding is disabled"):
        Structure(decode=False).decode_example(raw)


@pytest.mark.parametrize("format_type", [None, "numpy", "arrow"])
def test_formats(format_type):
    dataset = Dataset.from_dict({"s": [str(PDB_FILE), str(CIF_FILE)]}, features=Features({"s": Structure()}))
    row = dataset.with_format(format_type)[1]["s"]
    if format_type == "arrow":
        coords = row.combine_chunks().field("atoms").field("Cartn_xyz").flatten().flatten().to_numpy()
        assert coords.reshape(-1, 3).shape == (9, 3)
    else:
        assert row["atoms"]["Cartn_xyz"].shape == (9, 3)
        assert row["atoms"]["label_atom_id"].tolist() == ATOM_NAMES


def test_save_and_load_from_disk(tmp_path):
    dataset = Dataset.from_dict({"s": [str(CIF_FILE)]}, features=Features({"s": Structure(decoder="numpy")}))
    dataset.save_to_disk(tmp_path / "saved")
    reloaded = load_from_disk(tmp_path / "saved")
    assert reloaded.features == dataset.features
    np.testing.assert_array_equal(reloaded[0]["s"]["atoms"]["Cartn_xyz"], dataset[0]["s"]["atoms"]["Cartn_xyz"])


def test_register_decoder():
    register_structure_decoder("n_atoms", lambda structure: len(structure["atoms"]["Cartn_xyz"]))
    dataset = Dataset.from_dict({"s": [str(PDB_FILE)]}, features=Features({"s": Structure(decoder="n_atoms")}))
    assert dataset[0]["s"] == 9
    with pytest.raises(ValueError, match="Unknown structure decoder 'missing'"):
        get_structure_decoder("missing")


@require_biotite
def test_biotite_decoder_and_encoder():
    import biotite.structure as struc

    dataset = Dataset.from_dict(
        {"s": [CIF_WITH_BONDS.encode()]}, features=Features({"s": Structure(decoder="biotite")})
    )
    atom_array = dataset[0]["s"]
    assert isinstance(atom_array, struc.AtomArray)
    assert atom_array.atom_name.tolist() == ["O5'", "C5'", "ZN", "O"]
    assert atom_array.chain_id.tolist() == ["B"] * 4
    assert atom_array.hetero.tolist() == [False, False, True, True]
    assert atom_array.bonds.as_array()[:, :2].tolist() == [[0, 2]]

    encoded = Dataset.from_dict({"s": [atom_array]}, features=Features({"s": Structure()}))[0]["s"]
    np.testing.assert_allclose(encoded["atoms"]["Cartn_xyz"], atom_array.coord)
    assert encoded["atoms"]["label_atom_id"].tolist() == ["O5'", "C5'", "ZN", "O"]
    assert encoded["atoms"]["group_PDB"].tolist() == ["ATOM", "ATOM", "HETATM", "HETATM"]
    assert encoded["bonds"]["atom_index_2"].tolist() == [2]


@require_biotite
def test_biotite_decoder_multiple_models():
    import biotite.structure as struc

    two_models = MULTI_MODEL_PDB.replace(
        "HETATM    3 FE   HEM A 100      10.000  10.000  10.000  1.00  5.00          FE2+\n", ""
    )
    dataset = Dataset.from_dict({"s": [two_models.encode()]}, features=Features({"s": Structure(decoder="biotite")}))
    stack = dataset[0]["s"]
    assert isinstance(stack, struc.AtomArrayStack)
    assert stack.coord.shape == (2, 2, 3)
    assert stack.coord[1, :, 0].tolist() == [0.5, 1.5]

    # models with different atoms can't form a stack
    dataset = Dataset.from_dict(
        {"s": [MULTI_MODEL_PDB.encode()]}, features=Features({"s": Structure(decoder="biotite")})
    )
    with pytest.raises(ValueError, match="different atoms"):
        dataset[0]["s"]
