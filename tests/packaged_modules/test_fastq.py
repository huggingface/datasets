"""Tests for FASTQ file loader."""

import gzip
import os
import textwrap

import pyarrow as pa
import pytest

from datasets import BioSequence, DatasetInfo, Features, Value, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.download.streaming_download_manager import _get_extraction_protocol
from datasets.packaged_modules.fastq.fastq import Fastq, FastqConfig


require_biopython = pytest.mark.skipif(
    not __import__("datasets").config.BIOPYTHON_AVAILABLE, reason="biopython is not installed"
)


def _compression_uri(path):
    """Build the chained fsspec URI datasets uses to read a single compressed file.

    The builder opens files with the streaming-patched ``open()`` (``xopen``), which
    handles compression via ``<protocol>://<inner>::<outer>`` URIs rather than by
    sniffing magic bytes. The protocol is derived from datasets' own extraction logic
    so the test tracks the loader's real behavior. ``inner`` is the decompressed name.
    """
    path = str(path)
    protocol = _get_extraction_protocol(path)
    inner = os.path.basename(path).rsplit(".", 1)[0]
    return f"{protocol}://{inner}::{path}"


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
    with open(filename, "w", encoding="utf-8", newline="") as f:
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
    with open(filename, "w", encoding="utf-8", newline="") as f:
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
    with gzip.open(filename, "wt", encoding="utf-8", newline="") as f:
        f.write(data)
    return _compression_uri(filename)


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

    with open(filename, "w", encoding="utf-8", newline="") as f:
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
    with pytest.raises(ValueError, match="Invalid column 'invalid_column'"):
        Fastq(columns=["sequence", "invalid_column"])


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
    features = Features(
        {
            "id": Value("string"),
            "description": Value("string"),
            "sequence": Value("large_string"),
            "quality": Value("large_string"),
        }
    )
    fastq = Fastq(features=features)
    generator = fastq._generate_tables([[fastq_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    assert pa_table.schema.field("id").type == pa.string()
    assert pa_table.schema.field("sequence").type == pa.large_string()


def test_fastq_empty_file(tmp_path):
    """Test handling of empty FASTQ file."""
    filename = tmp_path / "empty.fq"
    with open(filename, "w", encoding="utf-8", newline="") as f:
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
    with open(filename, "w", encoding="utf-8", newline="") as f:
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
    with open(filename, "w", encoding="utf-8", newline="") as f:
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

    with open(file1, "w", encoding="utf-8", newline="") as f:
        f.write("@SEQ1\nACGT\n+\nIIII\n")

    with open(file2, "w", encoding="utf-8", newline="") as f:
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


@pytest.mark.parametrize(
    "text, reason",
    [
        ("@r1\nACGT\n+\n!!\n", "quality shorter than sequence"),
        ("@r1\nACGT\n+\n!!!!!!\n@r2\nA\n+\n!\n", "quality longer than sequence"),
        ("@r1\nACGT\nACGT\n", "no '+' separator before end of file"),
    ],
)
def test_fastq_parser_rejects_corrupt_record(text, reason):
    """A FASTQ record whose quality length differs from its sequence length is corrupt
    (typically a truncated download). It must raise rather than be yielded with
    mismatched columns."""
    import io

    with pytest.raises(ValueError, match="r1"):
        list(Fastq()._parse_fastq(io.StringIO(text)))


def test_fastq_parser_rejects_mismatched_separator_id():
    """When the '+' line repeats an identifier it must match the header's identifier."""
    import io

    with pytest.raises(ValueError, match="r2"):
        list(Fastq()._parse_fastq(io.StringIO("@r1\nAC\n+r2\n!!\n")))
    assert list(Fastq()._parse_fastq(io.StringIO("@r1 d\nAC\n+r1 d\n!!\n"))) == [("r1", "d", "AC", "!!")]


def test_fastq_empty_columns_is_rejected():
    with pytest.raises(ValueError, match="at least one column"):
        Fastq(columns=[])._get_columns()


@pytest.mark.parametrize("features", [None, Features({"id": Value("string")})])
def test_fastq_duplicate_columns_is_rejected(features):
    with pytest.raises(ValueError, match="Duplicate column 'id'"):
        Fastq(columns=["id", "id"], features=features)


def test_fastq_columns_project_custom_features(tmp_path):
    """columns= applies to a user-supplied features schema too."""
    filename = tmp_path / "proj.fq"
    filename.write_bytes(b"@r\nAC\n+\n!!\n")
    features = Features({col: Value("string") for col in ["id", "description", "sequence", "quality"]})
    fastq = Fastq(columns=["sequence"], features=features)
    assert fastq.info.features == Features({"sequence": Value("string")})
    table = next(iter(fastq._generate_tables([[str(filename)]])))[1]
    assert table.column_names == ["sequence"]
    assert Features.from_arrow_schema(table.schema) == fastq.info.features
    with pytest.raises(ValueError, match="not in features"):
        Fastq(columns=["sequence"], features=Features({"id": Value("string")}))._info()


@pytest.mark.parametrize("columns", [None, ["record"]])
def test_fastq_preserves_supplied_info_features(fastq_file, columns):
    features = Features(
        {
            "id": Value("string"),
            "description": Value("string"),
            "sequence": Value("large_string"),
            "quality": Value("large_string"),
            "record": BioSequence(format="fastq", decode=False),
        }
    )
    fastq = Fastq(info=DatasetInfo(features=features, description="custom info"), columns=columns)
    expected = features if columns is None else Features({"record": features["record"]})
    assert fastq.info.features == expected
    assert fastq.info.description == "custom info"
    _, table = next(fastq._generate_tables([[fastq_file]]))
    assert Features.from_arrow_schema(table.schema) == expected


def test_fastq_record_features(fastq_file):
    fastq = Fastq()
    expected = Features(
        {
            "id": Value("string"),
            "description": Value("string"),
            "sequence": Value("large_string"),
            "quality": Value("large_string"),
            "record": BioSequence(format="fastq"),
        }
    )
    assert fastq.info.features == expected
    _, table = next(fastq._generate_tables([[fastq_file]]))
    assert table.schema.field("record").type == BioSequence().pa_type
    assert Features.from_arrow_schema(table.schema) == expected


@require_biopython
@pytest.mark.parametrize("streaming", [False, True])
def test_fastq_record_decoding(fastq_file, streaming):
    from Bio.SeqRecord import SeqRecord

    dataset = load_dataset("fastq", data_files=fastq_file, split="train", streaming=streaming)
    assert dataset.features["record"] == BioSequence(format="fastq")
    rows = list(dataset)
    assert len(rows) == 3
    for row in rows:
        assert isinstance(row["record"], SeqRecord)
        assert row["record"].id == row["id"]
        assert str(row["record"].seq) == row["sequence"]
        assert row["record"].letter_annotations["phred_quality"] == [ord(char) - 33 for char in row["quality"]]


@pytest.mark.parametrize("fixture_name", ["fastq_file", "fastq_file_multiline", "fastq_file_gzipped"])
def test_fastq_record_bytes(fixture_name, request):
    filename = request.getfixturevalue(fixture_name)
    tables = list(Fastq(batch_size=1)._generate_tables([[filename]]))
    records = [table.to_pydict()["record"][0] for _, table in tables]
    opener = gzip.open if "::" in filename else open
    with opener(filename.split("::")[-1], "rb") as f:
        expected = [b"@" + record for record in f.read().split(b"@")[1:]]
    assert records == [{"bytes": record, "path": None} for record in expected]


@pytest.mark.parametrize("newline", [b"\n", b"\r\n", b"\r"])
@pytest.mark.parametrize("compressed", [False, True])
def test_fastq_record_preserves_raw_lines(tmp_path, newline, compressed):
    # Preserve header whitespace, UTF-8, blank lines, wrapping and the '+' line.
    first = b"@a caf\xc3\xa9 \t\nAC\n\nGT  \n+a caf\xc3\xa9 \t\nII\n\n@@\n".replace(b"\n", newline)
    second = b"@b\nTT\nAA\n+\n++\nII".replace(b"\n", newline)
    content = newline + first + newline + second
    filename = tmp_path / ("raw.fq.gz" if compressed else "raw.fq")
    filename.write_bytes(gzip.compress(content) if compressed else content)
    path = _compression_uri(filename) if compressed else str(filename)
    _, table = next(Fastq(columns=["record"])._generate_tables([[path]]))
    assert table.to_pydict() == {"record": [{"bytes": first, "path": None}, {"bytes": second, "path": None}]}


def test_fastq_record_cast_decode_false(fastq_file, monkeypatch):
    monkeypatch.setattr("datasets.config.BIOPYTHON_AVAILABLE", False)
    dataset = load_dataset("fastq", data_files=fastq_file, split="train")
    dataset = dataset.cast_column("record", BioSequence(decode=False))
    with open(fastq_file, "rb") as f:
        expected = [b"@" + record for record in f.read().split(b"@")[1:]]
    assert dataset["record"] == [{"bytes": record, "path": None} for record in expected]


def test_fastq_record_preserves_empty_quality_line(tmp_path):
    first = b"@empty\n\n+\n\n"
    second = b"@next\nA\n+\nI\n"
    filename = tmp_path / "empty_read.fq"
    filename.write_bytes(first + second)
    _, table = next(Fastq()._generate_tables([[str(filename)]]))
    expected = [b"@" + record for record in filename.read_bytes().split(b"@")[1:]]
    assert table.to_pydict()["record"] == [{"bytes": record, "path": None} for record in expected]


def test_fastq_columns_drop_record_without_biopython(fastq_file, monkeypatch):
    monkeypatch.setattr("datasets.config.BIOPYTHON_AVAILABLE", False)
    dataset = load_dataset("fastq", data_files=fastq_file, split="train", columns=["id", "sequence"])
    assert dataset.features == Features({"id": Value("string"), "sequence": Value("large_string")})
    assert len(list(dataset)) == 3
    assert dataset.column_names == ["id", "sequence"]


def test_fastq_record_column_validation():
    with pytest.raises(ValueError, match="Invalid column.*Valid columns are:.*record"):
        Fastq(columns=["invalid_column"])._get_columns()
    with pytest.raises(ValueError, match="columns.*record.*not in features"):
        Fastq(columns=["record"], features=Features({"id": Value("string")}))


def test_fastq_record_bytes_count_toward_batch_limit(tmp_path):
    filename = tmp_path / "batch.fq"
    # Parsed fields fit in one batch; their raw records push the total over the limit.
    filename.write_bytes(b"@a\nACGT\n+\nIIII\n@b\nTGCA\n+\nHHHH\n")
    tables = list(Fastq(max_batch_bytes=30)._generate_tables([[str(filename)]]))
    assert [table.num_rows for _, table in tables] == [1, 1]
    tables = list(Fastq(columns=["id", "sequence"], max_batch_bytes=30)._generate_tables([[str(filename)]]))
    assert [table.num_rows for _, table in tables] == [2]


def test_fastq_explicit_features_without_record(fastq_file):
    """A user-supplied schema selects its own columns, so pinning the four parsed columns still works."""
    features = Features(
        {
            "id": Value("string"),
            "description": Value("string"),
            "sequence": Value("large_string"),
            "quality": Value("large_string"),
        }
    )
    fastq = Fastq(features=features)
    assert fastq._get_columns() == ["id", "description", "sequence", "quality"]
    assert fastq.info.features == features
    generator = fastq._generate_tables([[fastq_file]])
    table = pa.concat_tables([table for _, table in generator])
    assert table.column_names == ["id", "description", "sequence", "quality"]
    with pytest.raises(ValueError, match="Invalid feature column"):
        Fastq(features=Features({"id": Value("string"), "invalid_column": Value("string")}))
