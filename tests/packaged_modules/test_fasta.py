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
    generator = fasta._generate_tables([[fasta_basic]])
    tables = list(generator)
    # Expect a single batch with all rows by default (_writer_batch_size may change this in HF CI;
    # still, we only assert data correctness)
    assert len(tables) >= 1

    # Merge batches virtually by reading first batch for sanity
    _, first_table = tables[0]
    cols = set(first_table.column_names)
    assert {"id", "description", "sequence"} <= cols

    # Collect all rows across batches
    all_rows = []
    for _, tbl in tables:
        for i in range(len(tbl)):
            all_rows.append({c: tbl[c][i].as_py() for c in tbl.column_names})

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
    generator = fasta._generate_tables([[fasta_with_whitespace]])
    tables = list(generator)

    # Flatten rows
    rows = []
    for _, tbl in tables:
        for i in range(len(tbl)):
            rows.append({c: tbl[c][i].as_py() for c in tbl.column_names})

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

    generator = fasta._generate_tables([[fasta_basic]])
    tables = list(generator)

    # 3 records; batch_size=2 -> 2 batches
    assert len(tables) == 2

    # First batch has 2 rows, final has 1
    assert len(tables[0][1]) == 2
    assert len(tables[1][1]) == 1


# ┌───────────────────┐
# │ Column filtering  │
# └───────────────────┘


def test_fasta_column_filtering(fasta_basic):
    config = FASTAConfig(columns=["id", "sequence"])
    fasta = FASTA()
    fasta.config = config
    # Call _info to initialize default features, then manually filter to match columns
    info = fasta._info()
    # Manually apply column filtering since we're not going through _split_generators
    fasta.info.features = Features({col: feat for col, feat in info.features.items() if col in config.columns})
    generator = fasta._generate_tables([[fasta_basic]])
    tables = list(generator)

    # Ensure only selected columns appear
    for _, tbl in tables:
        assert set(tbl.column_names) == {"id", "sequence"}
        # basic sanity on values
        assert isinstance(tbl["id"][0].as_py(), str)
        assert isinstance(tbl["sequence"][0].as_py(), str)


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

    tables = list(fasta._generate_tables([[fasta_basic]]))
    # Check schema cast
    _, tbl = tables[0]
    for col in features:
        assert tbl.schema.field(col).type == features[col].pa_type


# ┌───────────────────────────────┐
# │ Empty files & warnings        │
# └───────────────────────────────┘


def test_fasta_empty_file_warning(fasta_empty, caplog):
    fasta = FASTA()
    tables = list(fasta._generate_tables([[fasta_empty]]))
    assert len(tables) == 0
    # A warning may be logged by your builder; this just asserts "no tables" behavior.


# ┌───────────────────────────────┐
# │ Multiple files & splits       │
# └───────────────────────────────┘


def test_fasta_multiple_files(fasta_multi):
    f1, f2 = fasta_multi
    fasta = FASTA()
    tables = list(fasta._generate_tables([[f1, f2]]))
    # Expect records from both files in order (builder yields per file batches)
    total_rows = 0
    ids = []
    for _, tbl in tables:
        total_rows += len(tbl)
        ids += [tbl["id"][i].as_py() for i in range(len(tbl))]
    assert total_rows == 4
    assert ids == ["a", "b", "c", "d"]


def test_fasta_gz_via_dl_manager(fasta_gz, tmp_path):
    # Test that gzipped FASTA files can be read via StreamingDownloadManager.
    # This validates that the FASTA implementation properly uses xopen() to handle
    # fsspec paths like "gzip://file.fasta::path/to/file.gz"
    data_files = DataFilesDict({"train": [fasta_gz]})
    config = FASTAConfig(data_files=data_files)
    fasta = FASTA()
    fasta.config = config

    dlm = StreamingDownloadManager()
    splits = fasta._split_generators(dlm)
    assert len(splits) == 1
    # Generate tables using files from dl_manager (ensures .gz is extracted on the fly)
    tables = list(fasta._generate_tables(splits[0].gen_kwargs["files"]))
    assert len(tables) >= 1

    # Flatten and check content
    rows = []
    for _, tbl in tables:
        for i in range(len(tbl)):
            rows.append({c: tbl[c][i].as_py() for c in tbl.column_names})

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
    tables = list(fasta._generate_tables([[fasta_basic]]))
    assert len(tables) >= 1

    # Optionally, verify that features match expected when building a Dataset
    # (constructing a Dataset from pyarrow tables directly is possible, but out of scope here).


# ┌───────────────────────────────┐
# │ Edge cases                    │
# └───────────────────────────────┘


def test_fasta_handles_no_trailing_newline(tmp_path):
    p = tmp_path / "no_newline.fasta"
    p.write_text(">x\nATGC")  # no trailing newline
    fasta = FASTA()
    tables = list(fasta._generate_tables([[str(p)]]))
    rows = []
    for _, tbl in tables:
        for i in range(len(tbl)):
            rows.append({c: tbl[c][i].as_py() for c in tbl.column_names})
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
    tables = list(fasta._generate_tables([[str(p)]]))
    total = sum(len(tbl) for _, tbl in tables)
    assert total == 1
