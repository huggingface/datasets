"""Tests for the BioSequence and BioStructure feature types."""

import pytest

from datasets import Dataset, Features
from datasets.features import BioSequence, BioStructure


FASTA_BYTES = b">seq1 first record\nACGTACGTAC\n>seq2 second record\nTTTTGGGGCC\n"

# Minimal well-formed PDB: two atoms of one residue in one chain.
PDB_BYTES = (
    b"ATOM      1  N   MET A   1      11.104  13.207  10.567  1.00 20.00           N\n"
    b"ATOM      2  CA  MET A   1      12.560  13.099  10.500  1.00 20.00           C\n"
    b"TER       3      MET A   1\n"
    b"END\n"
)


@pytest.fixture
def fasta_path(tmp_path):
    path = tmp_path / "seqs.fasta"
    path.write_bytes(FASTA_BYTES)
    return str(path)


@pytest.fixture
def pdb_path(tmp_path):
    path = tmp_path / "struct.pdb"
    path.write_bytes(PDB_BYTES)
    return str(path)


# --------------------------------------------------------------------------
# Storage and encoding. These hold whether or not biopython is installed,
# because they never decode.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_storage_type_is_bytes_path_struct(feature_cls):
    """Both features store the same struct<bytes, path> as Audio, Image and Pdf do."""
    import pyarrow as pa

    assert feature_cls().pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert feature_cls()() == feature_cls().pa_type


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_encode_example_from_path(feature_cls, tmp_path):
    path = str(tmp_path / "x.dat")
    assert feature_cls().encode_example(path) == {"path": path, "bytes": None}


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_encode_example_from_bytes(feature_cls):
    assert feature_cls().encode_example(b"raw") == {"path": None, "bytes": b"raw"}


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_encode_example_rejects_empty_dict(feature_cls):
    with pytest.raises(ValueError, match="should have one of 'path' or 'bytes'"):
        feature_cls().encode_example({"path": None, "bytes": None})


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_decode_false_returns_raw_and_never_decodes(feature_cls, tmp_path):
    """With decode=False the user gets bytes back and biopython is never needed."""
    path = str(tmp_path / "x.dat")
    (tmp_path / "x.dat").write_bytes(b"payload")
    feature = feature_cls(decode=False)
    ds = Dataset.from_dict({"col": [path]}, features=Features({"col": feature}))
    assert ds[0]["col"] == {"bytes": None, "path": path}


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_decode_example_raises_when_decode_disabled(feature_cls):
    with pytest.raises(RuntimeError, match="Decoding is disabled"):
        feature_cls(decode=False).decode_example({"path": "x", "bytes": b"y"})


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_flatten_when_not_decoding(feature_cls):
    from datasets.features import Value

    assert feature_cls(decode=False).flatten() == {
        "bytes": Value("binary"),
        "path": Value("string"),
    }
    assert feature_cls(decode=True).flatten() == feature_cls(decode=True)


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_feature_roundtrips_through_dict(feature_cls):
    """A feature must survive Features.to_dict/from_dict, which is how it lands in dataset_info.json."""
    features = Features({"col": feature_cls()})
    assert Features.from_dict(features.to_dict()) == features


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_cast_storage_from_string_and_binary(feature_cls):
    import pyarrow as pa

    feature = feature_cls()
    from_str = feature.cast_storage(pa.array(["a.fa", "b.fa"], type=pa.string()))
    assert from_str.type == feature.pa_type
    assert from_str.to_pylist() == [{"bytes": None, "path": "a.fa"}, {"bytes": None, "path": "b.fa"}]

    from_bin = feature.cast_storage(pa.array([b"x"], type=pa.binary()))
    assert from_bin.to_pylist() == [{"bytes": b"x", "path": None}]


# --------------------------------------------------------------------------
# Decoding. Requires biopython.
# --------------------------------------------------------------------------

require_biopython = pytest.mark.skipif(
    not __import__("datasets").config.BIOPYTHON_AVAILABLE, reason="biopython is not installed"
)


@require_biopython
def test_bio_sequence_decodes_to_seqrecord(fasta_path):
    from Bio.SeqRecord import SeqRecord

    ds = Dataset.from_dict({"seq": [fasta_path]}, features=Features({"seq": BioSequence()}))
    record = ds[0]["seq"]
    assert isinstance(record, SeqRecord)
    assert record.id == "seq1"
    assert str(record.seq) == "ACGTACGTAC"


@require_biopython
def test_bio_sequence_decodes_from_bytes(fasta_path):
    ds = Dataset.from_dict(
        {"seq": [{"bytes": FASTA_BYTES, "path": "seqs.fasta"}]},
        features=Features({"seq": BioSequence()}),
    )
    assert str(ds[0]["seq"].seq) == "ACGTACGTAC"


@require_biopython
def test_bio_structure_decodes_to_structure(pdb_path):
    from Bio.PDB.Structure import Structure

    ds = Dataset.from_dict({"st": [pdb_path]}, features=Features({"st": BioStructure()}))
    structure = ds[0]["st"]
    assert isinstance(structure, Structure)
    assert [chain.id for chain in structure.get_chains()] == ["A"]
    assert len(list(structure.get_atoms())) == 2


@require_biopython
def test_bio_sequence_format_is_configurable(tmp_path):
    """The sequence format is a field, so FASTQ and GenBank reuse the same feature."""
    path = tmp_path / "r.fastq"
    path.write_bytes(b"@r1\nACGT\n+\nIIII\n")
    ds = Dataset.from_dict({"seq": [str(path)]}, features=Features({"seq": BioSequence(format="fastq")}))
    record = ds[0]["seq"]
    assert record.id == "r1"
    assert record.letter_annotations["phred_quality"] == [40, 40, 40, 40]


@pytest.mark.parametrize("bad_format", ["PDB", "cif", "mmCIF", "xyz"])
def test_bio_structure_rejects_unknown_format_at_construction(bad_format):
    """A format outside the supported table must fail before any bytes are written.

    Regression: encode_bio_structure() used to write mmCIF for every non-"pdb" value
    while decode_example() rejected the same value, so a mis-cased format stored bytes
    that could never be read back.
    """
    with pytest.raises(ValueError, match="Unsupported structure format"):
        BioStructure(format=bad_format)


@require_biopython
def test_bio_structure_encodes_structure_in_declared_format(pdb_path):
    """The bytes written for a Structure follow the feature's format, for both formats."""
    from Bio.PDB import PDBParser

    structure = PDBParser(QUIET=True).get_structure("x", str(pdb_path))
    pdb_bytes = BioStructure(format="pdb").encode_example(structure)["bytes"]
    cif_bytes = BioStructure(format="mmcif").encode_example(structure)["bytes"]
    assert pdb_bytes.startswith(b"ATOM")
    assert cif_bytes.startswith(b"data_")
    assert BioStructure(format="mmcif").decode_example({"path": None, "bytes": cif_bytes}).id == "structure"


def test_resolve_token_returns_none_for_non_hub_url():
    """string_to_dict() returns None for a URL that is not a Hub dataset URL; that must
    not surface as a TypeError when the remote path is plain https or s3."""
    from datasets.features.bio_sequence import _resolve_token

    tokens = {"user/repo": "hf_secret"}
    assert _resolve_token("https://example.com/data/seqs.fasta", tokens) is None
    assert _resolve_token("s3://bucket/seqs.fasta", tokens) is None
    assert _resolve_token("hf://datasets/user/repo@main/seqs.fasta", tokens) == "hf_secret"


@pytest.mark.parametrize("feature_cls", [BioSequence, BioStructure])
def test_embed_storage_keeps_path_only_rows_when_embedding_is_off(feature_cls):
    """With local_files=False a local path-only row is left as is, not nulled (as Image does)."""
    import pyarrow as pa

    feature = feature_cls()
    storage = pa.array([{"bytes": None, "path": "/data/seqs.fasta"}, None], type=feature.pa_type)
    embedded = feature.embed_storage(storage, local_files=False, remote_files=False)
    assert embedded.to_pylist() == [{"bytes": None, "path": "seqs.fasta"}, None]
