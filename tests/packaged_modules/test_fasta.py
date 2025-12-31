"""Tests for the FASTA file loader."""

import pyarrow as pa
import pytest

from datasets import Features, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.fasta.fasta import Fasta, FastaConfig


# Sample FASTA content for inline fixtures
FASTA_CONTENT = """\
>seq1 Example protein sequence
MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPF
EDHVKLVNEVTEFAKTCVADESHAGCEKSLHTLFGDELCKVASLRETYGDMADCCEKQEP
>seq2 Another sequence with multi-line
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH
GSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLL
SHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR
>seq3
ATGCATGCATGCATGCATGCATGCATGC
"""


@pytest.fixture
def fasta_file(tmp_path):
    filename = tmp_path / "sequences.fasta"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(FASTA_CONTENT)
    return str(filename)


@pytest.fixture
def fasta_file_fa(tmp_path):
    filename = tmp_path / "sequences.fa"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(FASTA_CONTENT)
    return str(filename)


@pytest.fixture
def fasta_gz_file(tmp_path):
    import gzip

    filename = tmp_path / "sequences.fasta.gz"
    with gzip.open(filename, "wt", encoding="utf-8") as f:
        f.write(FASTA_CONTENT)
    return str(filename)


@pytest.fixture
def fasta_bz2_file(tmp_path):
    import bz2

    filename = tmp_path / "sequences.fasta.bz2"
    with bz2.open(filename, "wt", encoding="utf-8") as f:
        f.write(FASTA_CONTENT)
    return str(filename)


@pytest.fixture
def fasta_xz_file(tmp_path):
    import lzma

    filename = tmp_path / "sequences.fasta.xz"
    with lzma.open(filename, "wt", encoding="utf-8") as f:
        f.write(FASTA_CONTENT)
    return str(filename)


@pytest.fixture
def fasta_long_sequence_file(tmp_path):
    """Create a file with a very long sequence to test large_string handling."""
    filename = tmp_path / "long_sequence.fasta"
    long_seq = "ATGCATGCATGCATGC" * 1000  # 16KB sequence
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f">long_seq Very long sequence\n{long_seq}\n")
    return str(filename)


@pytest.fixture
def fasta_empty_description_file(tmp_path):
    """Create a FASTA file with sequences that have no description."""
    filename = tmp_path / "no_description.fasta"
    content = """\
>seq1
ATGCATGC
>seq2
GCTAGCTA
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return str(filename)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = FastaConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = FastaConfig(name="name", data_files=data_files)


def test_fasta_basic_loading(fasta_file):
    """Test basic FASTA file loading."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_file]])
    tables = list(generator)

    assert len(tables) == 1
    key, pa_table = tables[0]

    # Check columns
    assert pa_table.column_names == ["id", "description", "sequence"]

    # Check data
    data = pa_table.to_pydict()
    assert data["id"] == ["seq1", "seq2", "seq3"]
    assert data["description"] == [
        "Example protein sequence",
        "Another sequence with multi-line",
        "",
    ]
    # Sequences should be concatenated (multi-line merged)
    assert data["sequence"][0] == (
        "MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPF"
        "EDHVKLVNEVTEFAKTCVADESHAGCEKSLHTLFGDELCKVASLRETYGDMADCCEKQEP"
    )
    assert data["sequence"][2] == "ATGCATGCATGCATGCATGCATGCATGC"


def test_fasta_fa_extension(fasta_file_fa):
    """Test loading with .fa extension."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_file_fa]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]
    assert pa_table.num_rows == 3


def test_fasta_gzip_compression(fasta_gz_file):
    """Test loading gzipped FASTA files."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_gz_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]
    data = pa_table.to_pydict()
    assert data["id"] == ["seq1", "seq2", "seq3"]


def test_fasta_bz2_compression(fasta_bz2_file):
    """Test loading bz2-compressed FASTA files."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_bz2_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]
    data = pa_table.to_pydict()
    assert data["id"] == ["seq1", "seq2", "seq3"]


def test_fasta_xz_compression(fasta_xz_file):
    """Test loading xz-compressed FASTA files."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_xz_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]
    data = pa_table.to_pydict()
    assert data["id"] == ["seq1", "seq2", "seq3"]


def test_fasta_long_sequence(fasta_long_sequence_file):
    """Test handling of very long sequences with large_string type."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_long_sequence_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]

    # Check that sequence column uses large_string type
    assert pa_table.schema.field("sequence").type == pa.large_string()

    data = pa_table.to_pydict()
    expected_length = len("ATGCATGCATGCATGC" * 1000)
    assert len(data["sequence"][0]) == expected_length


def test_fasta_column_filtering(fasta_file):
    """Test loading only specific columns."""
    fasta = Fasta(columns=["id", "sequence"])
    generator = fasta._generate_tables([[fasta_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]

    # Only selected columns should be present
    assert pa_table.column_names == ["id", "sequence"]
    data = pa_table.to_pydict()
    assert "description" not in data


def test_fasta_sequence_only(fasta_file):
    """Test loading only the sequence column."""
    fasta = Fasta(columns=["sequence"])
    generator = fasta._generate_tables([[fasta_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]
    assert pa_table.column_names == ["sequence"]


def test_fasta_invalid_column():
    """Test that invalid column names raise an error."""
    with pytest.raises(ValueError, match="Invalid column"):
        fasta = Fasta(columns=["invalid_column"])
        list(fasta._generate_tables([[]]))


def test_fasta_batch_size(fasta_file):
    """Test batch size configuration."""
    fasta = Fasta(batch_size=1)
    generator = fasta._generate_tables([[fasta_file]])
    tables = list(generator)

    # With batch_size=1, we should get 3 separate tables
    assert len(tables) == 3
    for _, pa_table in tables:
        assert pa_table.num_rows == 1


def test_fasta_empty_description(fasta_empty_description_file):
    """Test sequences with no description."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_empty_description_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]
    data = pa_table.to_pydict()
    assert data["description"] == ["", ""]


def test_fasta_schema_types(fasta_file):
    """Test that the Arrow schema has correct types."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_file]])
    tables = list(generator)

    _, pa_table = tables[0]
    schema = pa_table.schema

    # id and description should be string
    assert schema.field("id").type == pa.string()
    assert schema.field("description").type == pa.string()
    # sequence should be large_string to handle long sequences
    assert schema.field("sequence").type == pa.large_string()


def test_fasta_feature_casting(fasta_file):
    """Test custom feature casting."""
    features = Features({
        "id": Value("string"),
        "sequence": Value("large_string"),
    })
    fasta = Fasta(columns=["id", "sequence"], features=features)
    generator = fasta._generate_tables([[fasta_file]])
    tables = list(generator)

    assert len(tables) == 1
    _, pa_table = tables[0]
    assert pa_table.num_rows == 3


def test_fasta_multiple_files(fasta_file, fasta_file_fa):
    """Test loading multiple FASTA files."""
    fasta = Fasta()
    generator = fasta._generate_tables([[fasta_file], [fasta_file_fa]])
    tables = list(generator)

    # Should get one batch from each file
    assert len(tables) == 2

    total_rows = sum(pa_table.num_rows for _, pa_table in tables)
    assert total_rows == 6  # 3 sequences per file * 2 files


def test_fasta_max_batch_bytes(tmp_path):
    """Test byte-based batching for handling large sequences.

    This tests the adaptive batching that prevents Parquet page size errors
    when dealing with very large sequences (e.g., complete genomes).
    """
    # Create sequences of known sizes
    # Each sequence is ~100 bytes (id + description + sequence)
    filename = tmp_path / "batch_test.fasta"
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(5):
            seq = "A" * 80  # 80 byte sequence
            f.write(f">seq{i} description{i}\n{seq}\n")

    # With max_batch_bytes=200, we should get multiple batches
    # Each record is ~100 bytes, so ~2 records per batch
    fasta = Fasta(batch_size=10000, max_batch_bytes=200)
    generator = fasta._generate_tables([[str(filename)]])
    tables = list(generator)

    # Should have multiple batches due to byte limit
    assert len(tables) >= 2

    # Total rows should still be 5
    total_rows = sum(pa_table.num_rows for _, pa_table in tables)
    assert total_rows == 5


def test_fasta_max_batch_bytes_disabled(tmp_path):
    """Test that max_batch_bytes=None disables byte-based batching."""
    filename = tmp_path / "large_seqs.fasta"
    # Create 3 sequences with 1KB each
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(3):
            seq = "ATGC" * 256  # 1KB sequence
            f.write(f">seq{i}\n{seq}\n")

    # With max_batch_bytes=None, only batch_size matters
    fasta = Fasta(batch_size=10000, max_batch_bytes=None)
    generator = fasta._generate_tables([[str(filename)]])
    tables = list(generator)

    # Should be single batch since batch_size is large and byte limit is disabled
    assert len(tables) == 1
    _, pa_table = tables[0]
    assert pa_table.num_rows == 3


def test_fasta_large_genome_batching(tmp_path):
    """Test handling of genome-scale sequences that would exceed Parquet page limits.

    This simulates the scenario described in PR #7851 where very large sequences
    (e.g., viral genomes of 30KB+) could cause Parquet page size errors.
    """
    filename = tmp_path / "genome.fasta"
    # Create a "genome" of 50KB - this would cause issues without byte-based batching
    genome_seq = "ATGCGTACGT" * 5000  # 50KB sequence

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f">genome1 Large viral genome\n{genome_seq}\n")
        f.write(f">genome2 Another large genome\n{genome_seq}\n")

    # With small max_batch_bytes, each genome should be in its own batch
    fasta = Fasta(batch_size=10000, max_batch_bytes=60000)  # 60KB limit
    generator = fasta._generate_tables([[str(filename)]])
    tables = list(generator)

    # Each 50KB genome should be in separate batch
    assert len(tables) == 2

    for _, pa_table in tables:
        assert pa_table.num_rows == 1
        data = pa_table.to_pydict()
        assert len(data["sequence"][0]) == 50000


def test_fasta_default_max_batch_bytes():
    """Test that default max_batch_bytes is set correctly."""
    from datasets.packaged_modules.fasta.fasta import DEFAULT_MAX_BATCH_BYTES

    # Default should be 256MB
    assert DEFAULT_MAX_BATCH_BYTES == 256 * 1024 * 1024

    # Config should use this default
    config = FastaConfig(name="test")
    assert config.max_batch_bytes == DEFAULT_MAX_BATCH_BYTES
