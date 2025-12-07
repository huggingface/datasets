import gzip
from textwrap import dedent

import pytest

from datasets import Features, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesDict, DataFilesList
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.fasta.fasta import FASTA, FASTAConfig


# ┌─────────────────────────┐
# │ Fixtures: FASTA files   │
# └─────────────────────────┘


@pytest.fixture
def fasta_basic(tmp_path):
    p = tmp_path / "basic.fasta"
    # Put the header on the same line as '>'
    p.write_text(">seq1 description here\nATGCATGC\nATGC\n>seq2 another desc\nGGGTTT\n>seq3\nAAAA\nTTTT\nCCCC\nGGGG\n")
    return str(p)


@pytest.fixture
def fasta_with_whitespace(tmp_path):
    p = tmp_path / "whitespace.fasta"
    # Headers on the same line; sequences contain spaces/blank lines intentionally
    p.write_text(">id1 some desc\nATG C A T   GC\n\n>id2   desc with   spaces\nG G G T T T \n>id3\nA T G C\n")
    return str(p)


@pytest.fixture
def fasta_empty(tmp_path):
    p = tmp_path / "empty.fasta"
    p.write_text("")  # no records
    return str(p)


@pytest.fixture
def fasta_multi(tmp_path):
    p1 = tmp_path / "file1.fasta"
    p2 = tmp_path / "file2.fasta"
    p1.write_text(">a\nAAA\n>b\nBBBB\n")
    p2.write_text(">c\nC\n>d desc\nDDD\n")
    return str(p1), str(p2)


@pytest.fixture
def fasta_gz(tmp_path):
    p = tmp_path / "gz.fasta.gz"
    content = ">gz1 first\nATATAT\n>gz2\nGCGC\n"
    with gzip.open(p, "wb") as f:
        f.write(content.encode("utf-8"))
    return str(p)


# ┌─────────────────────────┐
# │ Fixtures: FASTQ files   │
# └─────────────────────────┘


@pytest.fixture
def fastq_basic(tmp_path):
    p = tmp_path / "basic.fastq"
    content = dedent("""\
        @SRR001666.1 071112_SLXA-EAS1_s_7:5:1:817:345 length=36
        GGGTGATGGCCGCTGCCGATGGCGTCAAATCCCACC
        +SRR001666.1 071112_SLXA-EAS1_s_7:5:1:817:345 length=36
        IIIIIIIIIIIIIIIIIIIIIIIIIIIIII9IG9IC
        @SRR001666.2 071112_SLXA-EAS1_s_7:5:1:801:338 length=36
        GTTCAGGGATACGACGTTTGTATTTTAAGAATCTGA
        +SRR001666.2 071112_SLXA-EAS1_s_7:5:1:801:338 length=36
        IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII6IBI
    """)
    p.write_text(content)
    return str(p)


@pytest.fixture
def fastq_multiline(tmp_path):
    p = tmp_path / "multiline.fastq"
    # FASTQ with multi-line sequences and quality scores
    content = dedent("""\
        @read1
        GATTTGGGGTTCAAAGCAGTATCGATCAAATAGT
        AAATCCATTTGTTCAACTCACAGTTT
        +
        !''*((((***+))%%%++)(%%%%).1***-+*'
        '))**55CCF>>>>>>CCCCCCC65
        @read2
        ACGT
        ACGT
        +
        IIII
        IIII
    """)
    p.write_text(content)
    return str(p)


@pytest.fixture
def fastq_empty(tmp_path):
    p = tmp_path / "empty.fastq"
    p.write_text("")
    return str(p)


@pytest.fixture
def fastq_multi(tmp_path):
    p1 = tmp_path / "file1.fastq"
    p2 = tmp_path / "file2.fastq"
    p1.write_text("@read1\nATGC\n+\nIIII\n@read2\nGGGG\n+\n!!!!\n")
    p2.write_text("@read3\nAAAA\n+\nHHHH\n@read4\nTTTT\n+\n####\n")
    return str(p1), str(p2)


@pytest.fixture
def fastq_gz(tmp_path):
    p = tmp_path / "compressed.fastq.gz"
    content = "@gz_read1\nATGCATGC\n+\nIIIIIIII\n@gz_read2\nGGGGTTTT\n+\nHHHHHHHH\n"
    with gzip.open(p, "wb") as f:
        f.write(content.encode("utf-8"))
    return str(p)


# ┌──────────────────────┐
# │ Config validation    │
# └──────────────────────┘


def test_config_raises_when_invalid_name():
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = FASTAConfig(name="bad*name")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files):
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = FASTAConfig(name="ok", data_files=data_files)


# ┌──────────────────────────────┐
# │ Basic functionality & schema │
# └──────────────────────────────┘


def test_fasta_basic_functionality(fasta_basic):
    fasta = FASTA()
    generator = fasta._generate_examples([[fasta_basic]])
    examples = list(generator)
    assert len(examples) >= 1

    # Collect all rows
    all_rows = [example for _, example in examples]

    # Check columns
    assert {"id", "description", "sequence"} <= set(all_rows[0].keys())

    # Order should match stream order: seq1, seq2, seq3
    assert all_rows[0]["id"] == "seq1"
    assert all_rows[0]["description"] == "seq1 description here"
    assert all_rows[0]["sequence"] == "ATGCATGCATGC"  # concatenated

    assert all_rows[1]["id"] == "seq2"
    assert all_rows[1]["description"] == "seq2 another desc"
    assert all_rows[1]["sequence"] == "GGGTTT"

    assert all_rows[2]["id"] == "seq3"
    assert all_rows[2]["description"] == "seq3"
    assert all_rows[2]["sequence"].lower() == "aaaattttccccgggg"


def test_fasta_whitespace_and_multiline(fasta_with_whitespace):
    fasta = FASTA()
    generator = fasta._generate_examples([[fasta_with_whitespace]])
    examples = list(generator)

    # Collect all rows
    rows = [example for _, example in examples]

    assert rows[0]["id"] == "id1"
    assert rows[0]["sequence"] == "ATGCATGC"  # spaces & blank lines stripped

    assert rows[1]["id"] == "id2"
    assert rows[1]["description"].startswith("id2")
    assert rows[1]["sequence"] == "GGGTTT"

    assert rows[2]["id"] == "id3"
    assert rows[2]["sequence"] == "ATGC"


# ┌───────────────┐
# │ Batching      │
# └───────────────┘


def test_fasta_batch_processing(fasta_basic):
    config = FASTAConfig(batch_size=2)
    fasta = FASTA()
    fasta.config = config

    generator = fasta._generate_examples([[fasta_basic]])
    examples = list(generator)

    # 3 records in the file (batch_size doesn't affect _generate_examples)
    assert len(examples) == 3


# ┌───────────────────┐
# │ Column filtering  │
# └───────────────────┘


def test_fasta_column_filtering(fasta_basic):
    config = FASTAConfig(columns=["id", "sequence"])
    
    fasta = FASTA()
    fasta.config = config
    # Call _info to initialize features (they're already set correctly in config)
    info = fasta._info()
    fasta.info.features = Features({col: feat for col, feat in info.features.items() if col in config.columns})

    generator = fasta._generate_examples([[fasta_basic]])
    examples = list(generator)

    # Ensure only selected columns appear
    for _, example in examples:
        assert set(example.keys()) == {"id", "sequence"}
        assert isinstance(example["id"], str)
        assert isinstance(example["sequence"], str)


def test_fasta_columns_features_mismatch():
    features = Features({"id": Value("string"), "sequence": Value("string")})
    config = FASTAConfig(
        name="t",
        columns=["id", "description"],  # mismatch vs features
        features=features,
    )
    fasta = FASTA()
    fasta.config = config
    with pytest.raises(ValueError, match="must contain the same columns"):
        fasta._info()


# ┌───────────────────────┐
# │ Features & casting    │
# └───────────────────────┘


def test_fasta_default_features(fasta_basic):
    fasta = FASTA()
    info = fasta._info()
    assert set(info.features.keys()) == {"id", "description", "sequence"}


def test_fasta_feature_specification_casting(fasta_basic):
    features = Features({"id": Value("string"), "description": Value("string"), "sequence": Value("string")})
    config = FASTAConfig(features=features)
    fasta = FASTA()
    fasta.config = config

    examples = list(fasta._generate_examples([[fasta_basic]]))
    # Check that examples have the correct columns
    _, example = examples[0]
    for col in features:
        assert col in example
        assert isinstance(example[col], str)


# ┌───────────────────────────────┐
# │ Empty files & warnings        │
# └───────────────────────────────┘


def test_fasta_empty_file_warning(fasta_empty, caplog):
    fasta = FASTA()
    examples = list(fasta._generate_examples([[fasta_empty]]))
    assert len(examples) == 0
    # A warning may be logged by your builder; this just asserts "no examples" behavior.


# ┌───────────────────────────────┐
# │ Multiple files & splits       │
# └───────────────────────────────┘


def test_fasta_multiple_files(fasta_multi):
    f1, f2 = fasta_multi
    fasta = FASTA()
    examples = list(fasta._generate_examples([[f1, f2]]))
    # Expect records from both files in order
    ids = [example["id"] for _, example in examples]
    assert len(examples) == 4
    assert ids == ["a", "b", "c", "d"]


def test_fasta_gz_via_dl_manager(fasta_gz, tmp_path):
    # Test that gzipped FASTA files can be read via StreamingDownloadManager.
    # This validates that the FASTA implementation properly handles compressed files
    data_files = DataFilesDict({"train": [fasta_gz]})
    config = FASTAConfig(data_files=data_files)
    fasta = FASTA()
    fasta.config = config

    dlm = StreamingDownloadManager()
    splits = fasta._split_generators(dlm)
    assert len(splits) == 1
    # Generate examples using files from dl_manager (ensures .gz is extracted on the fly)
    examples = list(fasta._generate_examples(splits[0].gen_kwargs["files"]))
    assert len(examples) >= 1

    # Collect all examples
    rows = [example for _, example in examples]

    assert len(rows) == 2
    assert rows[0]["id"] == "gz1"
    assert rows[0]["sequence"] == "ATATAT"
    assert rows[1]["id"] == "gz2"
    assert rows[1]["sequence"] == "GCGC"


# ┌───────────────────────────────┐
# │ Integration: load_dataset     │
# └───────────────────────────────┘


def test_fasta_load_dataset_like_usage(fasta_basic, tmp_path, monkeypatch):
    # This test demonstrates that the packaged module can be consumed as a HF dataset script.
    # If your builder is shipped as a packaged module, adjust `path` accordingly or skip this.
    # Here we call the builder directly to avoid I/O complexity.
    config = FASTAConfig()
    fasta = FASTA()
    fasta.config = config
    examples = list(fasta._generate_examples([[fasta_basic]]))
    assert len(examples) >= 1

    # Verify that examples have the expected structure
    _, example = examples[0]
    assert "id" in example
    assert "description" in example
    assert "sequence" in example


# ┌───────────────────────────────┐
# │ Edge cases                    │
# └───────────────────────────────┘


def test_fasta_handles_no_trailing_newline(tmp_path):
    p = tmp_path / "no_newline.fasta"
    p.write_text(">x\nATGC")  # no trailing newline
    fasta = FASTA()
    examples = list(fasta._generate_examples([[str(p)]]))
    rows = [example for _, example in examples]
    assert rows == [{"id": "x", "description": "x", "sequence": "ATGC"}]


def test_fasta_single_record(tmp_path):
    p = tmp_path / "single.fasta"
    p.write_text(
        dedent(""">
        only
        A
    """)
        .strip()
        .replace("\n        ", "\n")
    )
    fasta = FASTA()
    examples = list(fasta._generate_examples([[str(p)]]))
    assert len(examples) == 1


# ┌───────────────────────────────────┐
# │ FASTQ: Basic functionality        │
# └───────────────────────────────────┘


def test_fastq_basic_functionality(fastq_basic):
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()
    generator = fasta._generate_examples([[fastq_basic]])
    examples = list(generator)
    assert len(examples) >= 1

    # Collect all rows
    all_rows = [example for _, example in examples]

    assert set(all_rows[0].keys()) == {"id", "description", "sequence", "quality"}

    # Verify first record
    assert all_rows[0]["id"] == "SRR001666.1"
    assert all_rows[0]["description"] == "SRR001666.1 071112_SLXA-EAS1_s_7:5:1:817:345 length=36"
    assert all_rows[0]["sequence"] == "GGGTGATGGCCGCTGCCGATGGCGTCAAATCCCACC"
    assert all_rows[0]["quality"] == "IIIIIIIIIIIIIIIIIIIIIIIIIIIIII9IG9IC"

    # Verify second record
    assert all_rows[1]["id"] == "SRR001666.2"
    assert all_rows[1]["description"] == "SRR001666.2 071112_SLXA-EAS1_s_7:5:1:801:338 length=36"
    assert all_rows[1]["sequence"] == "GTTCAGGGATACGACGTTTGTATTTTAAGAATCTGA"
    assert all_rows[1]["quality"] == "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII6IBI"


def test_fastq_multiline_sequences(fastq_multiline):
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()
    generator = fasta._generate_examples([[fastq_multiline]])
    examples = list(generator)

    # Collect all rows
    rows = [example for _, example in examples]

    # First record - multi-line sequence and quality should be concatenated
    assert rows[0]["id"] == "read1"
    assert rows[0]["sequence"] == "GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT"
    assert rows[0]["quality"] == "!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65"

    # Second record
    assert rows[1]["id"] == "read2"
    assert rows[1]["sequence"] == "ACGTACGT"
    assert rows[1]["quality"] == "IIIIIIII"


def test_fastq_default_features(fastq_basic):
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()
    # FASTQ should have id, description, sequence, and quality
    assert set(fasta.info.features.keys()) == {"id", "description", "sequence", "quality"}


def test_fastq_column_filtering(fastq_basic):
    config = FASTAConfig(
        file_type="fastq",
        columns=["id", "sequence", "quality"]
        )
    fasta = FASTA()
    fasta.config = config
    # Call _info to initialize features (they're already set correctly in config)
    info = fasta._info()
    fasta.info.features = Features({col: feat for col, feat in info.features.items() if col in config.columns})

    generator = fasta._generate_examples([[fastq_basic]])
    examples = list(generator)

    # Ensure only selected columns appear
    for _, example in examples:
        assert set(example.keys()) == {"id", "sequence", "quality"}
        assert isinstance(example["id"], str)
        assert isinstance(example["sequence"], str)
        assert isinstance(example["quality"], str)


def test_fastq_batch_processing(fastq_basic):
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()

    generator = fasta._generate_examples([[fastq_basic]])
    examples = list(generator)

    # 2 records in the file
    assert len(examples) == 2


def test_fastq_empty_file(fastq_empty):
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()
    examples = list(fasta._generate_examples([[fastq_empty]]))
    assert len(examples) == 0


def test_fastq_multiple_files(fastq_multi):
    f1, f2 = fastq_multi
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()
    examples = list(fasta._generate_examples([[f1, f2]]))

    ids = [example["id"] for _, example in examples]

    assert len(examples) == 4
    assert ids == ["read1", "read2", "read3", "read4"]


def test_fastq_gz_via_dl_manager(fastq_gz, tmp_path):
    # Test that gzipped FASTQ files can be read via StreamingDownloadManager
    data_files = DataFilesDict({"train": [fastq_gz]})
    config = FASTAConfig(data_files=data_files, file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()

    dlm = StreamingDownloadManager()
    splits = fasta._split_generators(dlm)
    assert len(splits) == 1

    examples = list(fasta._generate_examples(splits[0].gen_kwargs["files"]))
    assert len(examples) >= 1

    # Collect all examples
    rows = [example for _, example in examples]

    assert len(rows) == 2
    assert rows[0]["id"] == "gz_read1"
    assert rows[0]["sequence"] == "ATGCATGC"
    assert rows[0]["quality"] == "IIIIIIII"
    assert rows[1]["id"] == "gz_read2"
    assert rows[1]["sequence"] == "GGGGTTTT"
    assert rows[1]["quality"] == "HHHHHHHH"


def test_fastq_quality_scores_preserved(fastq_basic):
    # Verify that quality scores with special characters are preserved correctly
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()
    generator = fasta._generate_examples([[fastq_basic]])
    examples = list(generator)

    rows = [example for _, example in examples]

    # Check that quality characters are preserved (high quality 'I' and moderate quality digits)
    assert "I" in rows[0]["quality"]
    assert "9" in rows[0]["quality"]
    assert "G" in rows[0]["quality"]
    assert "C" in rows[0]["quality"]
    assert "6" in rows[1]["quality"]
    assert "B" in rows[1]["quality"]


def test_fastq_handles_no_trailing_newline(tmp_path):
    p = tmp_path / "no_newline.fastq"
    p.write_text("@read1\nATGC\n+\nIIII")  # no trailing newline
    config = FASTAConfig(file_type="fastq")
    fasta = FASTA()
    fasta.config = config
    fasta.info = fasta._info()
    examples = list(fasta._generate_examples([[str(p)]]))
    rows = [example for _, example in examples]
    assert len(rows) == 1
    assert rows[0]["id"] == "read1"
    assert rows[0]["sequence"] == "ATGC"
    assert rows[0]["quality"] == "IIII"