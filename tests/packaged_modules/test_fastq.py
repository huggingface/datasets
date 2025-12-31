"""Tests for FASTQ file loader."""

import gzip
import textwrap

import pyarrow as pa
import pytest

from datasets import Features, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.fastq.fastq import Fastq, FastqConfig


@pytest.fixture
def fastq_file(tmp_path):
    """Create a simple FASTQ file with multiple records."""
    filename = tmp_path / "reads.fq"
    data = textwrap.dedent(
        """\
        @SEQ_ID_1 description 1
        GATCGATCGATCGATC
        +
        IIIIIIIIIIIIIIII
        @SEQ_ID_2 description 2
        ATCGATCGATCGATCG
        +
        HHHHHHHHHHHHHHHH
        @SEQ_ID_3
        TCGATCGATCGATCGA
        +
        GGGGGGGGGGGGGGGG
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def fastq_file_multiline(tmp_path):
    """Create a FASTQ file with multi-line sequences and quality scores."""
    filename = tmp_path / "reads_multiline.fastq"
    data = textwrap.dedent(
        """\
        @SEQ_ID_1 multi-line sequence
        GATCGATCGATCGATC
        ATCGATCGATCGATCG
        +
        IIIIIIIIIIIIIIII
        HHHHHHHHHHHHHHHH
        @SEQ_ID_2
        AAAA
        TTTT
        GGGG
        CCCC
        +
        !!!!
        ####
        $$$$
        %%%%
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def fastq_file_gzipped(tmp_path):
    """Create a gzipped FASTQ file."""
    filename = tmp_path / "reads.fq.gz"
    data = textwrap.dedent(
        """\
        @SEQ_ID_1 gzipped read
        GATCGATCGATCGATC
        +
        IIIIIIIIIIIIIIII
        @SEQ_ID_2
        ATCGATCGATCGATCG
        +
        HHHHHHHHHHHHHHHH
        """
    )
    with gzip.open(filename, "wt", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def fastq_file_large_sequences(tmp_path):
    """Create a FASTQ file with large sequences to test batching."""
    filename = tmp_path / "large_reads.fq"
    # Create sequences of varying sizes
    sequences = []
    for i in range(5):
        seq_len = 1000 * (i + 1)  # 1K, 2K, 3K, 4K, 5K bases
        seq = "ACGT" * (seq_len // 4)
        qual = "I" * seq_len
        sequences.append(f"@SEQ_{i} large sequence {i}\n{seq}\n+\n{qual}\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("".join(sequences))
    return str(filename)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = FastqConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = FastqConfig(name="name", data_files=data_files)


def test_fastq_basic_loading(fastq_file):
    """Test basic FASTQ file loading."""
    fastq = Fastq()
    generator = fastq._generate_tables([[fastq_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 3
    assert result["id"] == ["SEQ_ID_1", "SEQ_ID_2", "SEQ_ID_3"]
    assert result["description"] == ["description 1", "description 2", ""]
    assert result["sequence"] == ["GATCGATCGATCGATC", "ATCGATCGATCGATCG", "TCGATCGATCGATCGA"]
    assert result["quality"] == ["IIIIIIIIIIIIIIII", "HHHHHHHHHHHHHHHH", "GGGGGGGGGGGGGGGG"]


def test_fastq_multiline_sequences(fastq_file_multiline):
    """Test FASTQ with multi-line sequences and quality scores."""
    fastq = Fastq()
    generator = fastq._generate_tables([[fastq_file_multiline]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 2
    assert result["id"] == ["SEQ_ID_1", "SEQ_ID_2"]
    # Multi-line sequences should be concatenated
    assert result["sequence"][0] == "GATCGATCGATCGATCATCGATCGATCGATCG"
    assert result["quality"][0] == "IIIIIIIIIIIIIIIIHHHHHHHHHHHHHHHH"
    assert result["sequence"][1] == "AAAATTTTGGGGCCCC"
    assert result["quality"][1] == "!!!!####$$$$%%%%"


def test_fastq_gzipped(fastq_file_gzipped):
    """Test loading gzipped FASTQ files."""
    fastq = Fastq()
    generator = fastq._generate_tables([[fastq_file_gzipped]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 2
    assert result["id"] == ["SEQ_ID_1", "SEQ_ID_2"]
    assert result["description"][0] == "gzipped read"


def test_fastq_column_filtering(fastq_file):
    """Test loading with column subset."""
    fastq = Fastq(columns=["sequence", "quality"])
    generator = fastq._generate_tables([[fastq_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    # Should only have sequence and quality columns
    assert list(result.keys()) == ["sequence", "quality"]
    assert len(result["sequence"]) == 3
    assert len(result["quality"]) == 3


def test_fastq_column_filtering_single(fastq_file):
    """Test loading with single column."""
    fastq = Fastq(columns=["sequence"])
    generator = fastq._generate_tables([[fastq_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert list(result.keys()) == ["sequence"]
    assert len(result["sequence"]) == 3


def test_fastq_invalid_column():
    """Test that invalid column names raise an error."""
    fastq = Fastq(columns=["sequence", "invalid_column"])
    with pytest.raises(ValueError, match="Invalid column 'invalid_column'"):
        list(fastq._generate_tables([[]]))


def test_fastq_batch_size(fastq_file):
    """Test batch size configuration."""
    # Use batch_size=1 to create multiple batches
    fastq = Fastq(batch_size=1)
    generator = fastq._generate_tables([[fastq_file]])
    tables = [table for _, table in generator]

    # Should have 3 batches (one per record)
    assert len(tables) == 3

    # Each batch should have 1 record
    for table in tables:
        assert table.num_rows == 1


def test_fastq_batch_size_multiple(fastq_file):
    """Test batch size with multiple records per batch."""
    fastq = Fastq(batch_size=2)
    generator = fastq._generate_tables([[fastq_file]])
    tables = [table for _, table in generator]

    # Should have 2 batches (2 records, then 1 record)
    assert len(tables) == 2
    assert tables[0].num_rows == 2
    assert tables[1].num_rows == 1


def test_fastq_max_batch_bytes(fastq_file_large_sequences):
    """Test byte-based batching with max_batch_bytes."""
    # Set a small byte limit to force multiple batches
    fastq = Fastq(batch_size=1000, max_batch_bytes=5000)
    generator = fastq._generate_tables([[fastq_file_large_sequences]])
    tables = [table for _, table in generator]

    # Should create multiple batches due to byte limit
    assert len(tables) > 1


def test_fastq_no_byte_limit(fastq_file_large_sequences):
    """Test disabling byte-based batching."""
    fastq = Fastq(batch_size=1000, max_batch_bytes=None)
    generator = fastq._generate_tables([[fastq_file_large_sequences]])
    tables = [table for _, table in generator]

    # Should create single batch since batch_size is high
    assert len(tables) == 1
    assert tables[0].num_rows == 5


def test_fastq_schema_types(fastq_file):
    """Test that schema uses correct Arrow types."""
    fastq = Fastq()
    generator = fastq._generate_tables([[fastq_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    schema = pa_table.schema

    # id and description should be string
    assert schema.field("id").type == pa.string()
    assert schema.field("description").type == pa.string()
    # sequence and quality should be large_string for long reads
    assert schema.field("sequence").type == pa.large_string()
    assert schema.field("quality").type == pa.large_string()


def test_fastq_feature_casting(fastq_file):
    """Test feature casting to custom schema."""
    features = Features({
        "id": Value("string"),
        "description": Value("string"),
        "sequence": Value("large_string"),
        "quality": Value("large_string"),
    })
    fastq = Fastq(features=features)
    generator = fastq._generate_tables([[fastq_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    assert pa_table.schema.field("id").type == pa.string()
    assert pa_table.schema.field("sequence").type == pa.large_string()


def test_fastq_empty_file(tmp_path):
    """Test handling of empty FASTQ file."""
    filename = tmp_path / "empty.fq"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")

    fastq = Fastq()
    generator = fastq._generate_tables([[str(filename)]])
    tables = list(generator)

    # Empty file should produce no tables
    assert len(tables) == 0


def test_fastq_empty_lines(tmp_path):
    """Test FASTQ file with empty lines between records."""
    filename = tmp_path / "empty_lines.fq"
    data = textwrap.dedent(
        """\

        @SEQ_ID_1
        GATCGATC
        +

        IIIIIIII

        @SEQ_ID_2
        ATCGATCG
        +
        HHHHHHHH

        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    fastq = Fastq()
    generator = fastq._generate_tables([[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    # Parser should handle empty lines gracefully
    assert len(result["id"]) == 2


def test_fastq_special_characters_in_header(tmp_path):
    """Test FASTQ with special characters in header."""
    filename = tmp_path / "special.fq"
    data = textwrap.dedent(
        """\
        @SEQ:ID:1:2:3 length=16 organism="E. coli"
        GATCGATCGATCGATC
        +
        IIIIIIIIIIIIIIII
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    fastq = Fastq()
    generator = fastq._generate_tables([[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert result["id"][0] == "SEQ:ID:1:2:3"
    assert result["description"][0] == 'length=16 organism="E. coli"'


def test_fastq_quality_length_matches_sequence(fastq_file):
    """Test that quality scores match sequence length."""
    fastq = Fastq()
    generator = fastq._generate_tables([[fastq_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    for seq, qual in zip(result["sequence"], result["quality"]):
        assert len(seq) == len(qual), f"Sequence length {len(seq)} != quality length {len(qual)}"


def test_fastq_multiple_files(tmp_path):
    """Test loading multiple FASTQ files."""
    # Create two files
    file1 = tmp_path / "reads1.fq"
    file2 = tmp_path / "reads2.fq"

    with open(file1, "w", encoding="utf-8") as f:
        f.write("@SEQ1\nACGT\n+\nIIII\n")

    with open(file2, "w", encoding="utf-8") as f:
        f.write("@SEQ2\nTGCA\n+\nHHHH\n")

    fastq = Fastq()
    generator = fastq._generate_tables([[str(file1)], [str(file2)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 2
    assert "SEQ1" in result["id"]
    assert "SEQ2" in result["id"]


def test_fastq_extensions():
    """Test that correct extensions are defined."""
    assert ".fq" in Fastq.EXTENSIONS
    assert ".fastq" in Fastq.EXTENSIONS
