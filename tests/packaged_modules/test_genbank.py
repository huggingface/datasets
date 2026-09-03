"""Tests for GenBank file loader."""

import bz2
import gzip
import json
import lzma
import os
import textwrap

import pyarrow as pa
import pytest

from datasets import Features, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.download.streaming_download_manager import _get_extraction_protocol
from datasets.packaged_modules.genbank.genbank import GenBank, GenBankConfig


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
def genbank_file(tmp_path):
    """Create a simple GenBank file with a single record."""
    filename = tmp_path / "sequence.gb"
    data = textwrap.dedent(
        """\
        LOCUS       SCU49845     5028 bp    DNA             PLN       21-JUN-1999
        DEFINITION  Saccharomyces cerevisiae TCP1-beta gene, partial cds.
        ACCESSION   U49845
        VERSION     U49845.1
        KEYWORDS    .
        SOURCE      Saccharomyces cerevisiae (baker's yeast)
          ORGANISM  Saccharomyces cerevisiae
                    Eukaryota; Fungi; Dikarya; Ascomycota; Saccharomycotina;
                    Saccharomycetes.
        FEATURES             Location/Qualifiers
             source          1..5028
                             /organism="Saccharomyces cerevisiae"
                             /mol_type="genomic DNA"
             CDS             687..3158
                             /gene="TCP1-beta"
                             /product="TCP1-beta"
                             /protein_id="AAA98665.1"
        ORIGIN
                1 gatcgatcga tcgatcgatc gatcgatcga tcgatcgatc gatcgatcga tcgatcgatc
               61 gatcgatcga tcgatcgatc
        //
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def genbank_file_multi_record(tmp_path):
    """Create a GenBank file with multiple records."""
    filename = tmp_path / "multi_sequence.gb"
    data = textwrap.dedent(
        """\
        LOCUS       SEQ001       100 bp    DNA             BCT       01-JAN-2024
        DEFINITION  Test sequence 1.
        ACCESSION   SEQ001
        VERSION     SEQ001.1
        KEYWORDS    test.
        SOURCE      Escherichia coli
          ORGANISM  Escherichia coli
                    Bacteria; Proteobacteria; Gammaproteobacteria.
        FEATURES             Location/Qualifiers
             source          1..100
                             /organism="Escherichia coli"
             gene            10..90
                             /gene="testA"
        ORIGIN
                1 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
               61 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
        //
        LOCUS       SEQ002       50 bp    RNA             VRL       01-JAN-2024
        DEFINITION  Test sequence 2.
        ACCESSION   SEQ002
        VERSION     SEQ002.1
        KEYWORDS    .
        SOURCE      Test virus
          ORGANISM  Test virus
                    Viruses; RNA viruses.
        FEATURES             Location/Qualifiers
             source          1..50
                             /organism="Test virus"
        ORIGIN
                1 augcaugcau gcaugcaugc augcaugcau gcaugcaugc augcaugcau
        //
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def genbank_file_gzipped(tmp_path):
    """Create a gzipped GenBank file."""
    filename = tmp_path / "sequence.gb.gz"
    data = textwrap.dedent(
        """\
        LOCUS       GZSEQ        80 bp    DNA             PLN       01-JAN-2024
        DEFINITION  Gzipped test sequence.
        ACCESSION   GZSEQ
        VERSION     GZSEQ.1
        KEYWORDS    gzip; test.
        SOURCE      Test organism
          ORGANISM  Test organism
                    Eukaryota; Testaceae.
        FEATURES             Location/Qualifiers
             source          1..80
                             /organism="Test organism"
        ORIGIN
                1 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
               61 atcgatcgat cgatcgatcg
        //
        """
    )
    with gzip.open(filename, "wt", encoding="utf-8") as f:
        f.write(data)
    return _compression_uri(filename)


@pytest.fixture
def genbank_file_bz2(tmp_path):
    """Create a bzip2 compressed GenBank file."""
    filename = tmp_path / "sequence.gb.bz2"
    data = textwrap.dedent(
        """\
        LOCUS       BZ2SEQ       60 bp    DNA             PLN       01-JAN-2024
        DEFINITION  Bzip2 test sequence.
        ACCESSION   BZ2SEQ
        VERSION     BZ2SEQ.1
        KEYWORDS    bzip2.
        SOURCE      Test organism
          ORGANISM  Test organism
                    Eukaryota; Testaceae.
        FEATURES             Location/Qualifiers
             source          1..60
                             /organism="Test organism"
        ORIGIN
                1 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
        //
        """
    )
    with bz2.open(filename, "wt", encoding="utf-8") as f:
        f.write(data)
    return _compression_uri(filename)


@pytest.fixture
def genbank_file_xz(tmp_path):
    """Create an xz/lzma compressed GenBank file."""
    filename = tmp_path / "sequence.gb.xz"
    data = textwrap.dedent(
        """\
        LOCUS       XZSEQ        40 bp    DNA             PLN       01-JAN-2024
        DEFINITION  XZ test sequence.
        ACCESSION   XZSEQ
        VERSION     XZSEQ.1
        KEYWORDS    .
        SOURCE      Test organism
          ORGANISM  Test organism
                    Eukaryota; Testaceae.
        FEATURES             Location/Qualifiers
             source          1..40
                             /organism="Test organism"
        ORIGIN
                1 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
        //
        """
    )
    with lzma.open(filename, "wt", encoding="utf-8") as f:
        f.write(data)
    return _compression_uri(filename)


@pytest.fixture
def genbank_file_complex_features(tmp_path):
    """Create a GenBank file with complex feature locations."""
    filename = tmp_path / "complex_features.gb"
    data = textwrap.dedent(
        """\
        LOCUS       COMPLEX      300 bp    DNA             PLN       01-JAN-2024
        DEFINITION  Sequence with complex feature locations.
        ACCESSION   COMPLEX
        VERSION     COMPLEX.1
        KEYWORDS    complex; features.
        SOURCE      Test organism
          ORGANISM  Test organism
                    Eukaryota; Testaceae.
        FEATURES             Location/Qualifiers
             source          1..300
                             /organism="Test organism"
             gene            complement(10..100)
                             /gene="revGene"
             CDS             join(1..50,100..150,200..250)
                             /gene="splitGene"
                             /product="split protein"
             misc_feature    <1..>300
                             /note="partial feature"
        ORIGIN
                1 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
               61 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
              121 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
              181 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
              241 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
        //
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def genbank_file_large_sequences(tmp_path):
    """Create a GenBank file with large sequences to test batching."""
    filename = tmp_path / "large_sequences.gb"
    records = []
    for i in range(5):
        seq_len = 1000 * (i + 1)  # 1K, 2K, 3K, 4K, 5K bases
        seq = "ACGT" * (seq_len // 4)
        # Format sequence with GenBank-style line breaks
        formatted_seq = ""
        for j in range(0, len(seq), 60):
            line_num = j + 1
            line_seq = seq[j : j + 60]
            # Add spaces every 10 bases
            spaced = " ".join(line_seq[k : k + 10] for k in range(0, len(line_seq), 10))
            formatted_seq += f"{line_num:>9} {spaced}\n"

        record = f"""LOCUS       LARGE{i:03d}    {seq_len} bp    DNA             PLN       01-JAN-2024
DEFINITION  Large sequence {i}.
ACCESSION   LARGE{i:03d}
VERSION     LARGE{i:03d}.1
KEYWORDS    large.
SOURCE      Test organism
  ORGANISM  Test organism
            Eukaryota; Testaceae.
FEATURES             Location/Qualifiers
     source          1..{seq_len}
                     /organism="Test organism"
ORIGIN
{formatted_seq}//
"""
        records.append(record)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(records))
    return str(filename)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = GenBankConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = GenBankConfig(name="name", data_files=data_files)


def test_genbank_basic_loading(genbank_file):
    """Test basic GenBank file loading."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["locus_name"]) == 1
    assert result["locus_name"][0] == "SCU49845"
    assert result["accession"][0] == "U49845"
    assert result["version"][0] == "U49845.1"
    assert "Saccharomyces cerevisiae TCP1-beta gene" in result["definition"][0]
    assert result["organism"][0] == "Saccharomyces cerevisiae"
    assert "Eukaryota" in result["taxonomy"][0]
    assert result["length"][0] == 5028
    assert result["molecule_type"][0] == "DNA"


def test_genbank_multi_record(genbank_file_multi_record):
    """Test loading GenBank file with multiple records."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file_multi_record]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["locus_name"]) == 2
    assert result["locus_name"] == ["SEQ001", "SEQ002"]
    assert result["accession"] == ["SEQ001", "SEQ002"]
    assert result["molecule_type"] == ["DNA", "RNA"]
    assert result["organism"] == ["Escherichia coli", "Test virus"]


def test_genbank_gzipped(genbank_file_gzipped):
    """Test loading gzipped GenBank files."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file_gzipped]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["locus_name"]) == 1
    assert result["locus_name"][0] == "GZSEQ"
    assert result["keywords"][0] == "gzip; test."


def test_genbank_bz2(genbank_file_bz2):
    """Test loading bzip2 compressed GenBank files."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file_bz2]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["locus_name"]) == 1
    assert result["locus_name"][0] == "BZ2SEQ"
    assert result["keywords"][0] == "bzip2."


def test_genbank_xz(genbank_file_xz):
    """Test loading xz/lzma compressed GenBank files."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file_xz]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["locus_name"]) == 1
    assert result["locus_name"][0] == "XZSEQ"


def test_genbank_feature_parsing(genbank_file_complex_features):
    """Test parsing of complex feature locations."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file_complex_features]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()
    features = json.loads(result["features"][0])

    assert len(features) >= 3

    # Find the complement feature
    rev_gene = next((f for f in features if f.get("qualifiers", {}).get("gene") == ["revGene"]), None)
    assert rev_gene is not None
    assert rev_gene["location"]["strand"] == -1

    # Find the join feature
    split_gene = next((f for f in features if f.get("qualifiers", {}).get("gene") == ["splitGene"]), None)
    assert split_gene is not None
    assert "parts" in split_gene["location"]
    assert len(split_gene["location"]["parts"]) == 3


def test_genbank_column_filtering(genbank_file):
    """Test loading with column subset."""
    genbank = GenBank(columns=["locus_name", "sequence", "length"])
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert list(result.keys()) == ["locus_name", "sequence", "length"]
    assert len(result["locus_name"]) == 1


def test_genbank_column_filtering_single(genbank_file):
    """Test loading with single column."""
    genbank = GenBank(columns=["sequence"])
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert list(result.keys()) == ["sequence"]


def test_genbank_invalid_column():
    """Test that invalid column names raise an error.

    Validation happens at builder construction time (via _info -> _get_columns),
    so the error surfaces as soon as the invalid columns are configured.
    """
    with pytest.raises(ValueError, match="Invalid column 'invalid_column'"):
        GenBank(columns=["sequence", "invalid_column"])


def test_genbank_batch_size(genbank_file_multi_record):
    """Test batch size configuration."""
    genbank = GenBank(batch_size=1)
    generator = genbank._generate_tables([[genbank_file_multi_record]])
    tables = [table for _, table in generator]

    # Should have 2 batches (one per record)
    assert len(tables) == 2

    for table in tables:
        assert table.num_rows == 1


def test_genbank_max_batch_bytes(genbank_file_large_sequences):
    """Test byte-based batching with max_batch_bytes."""
    genbank = GenBank(batch_size=1000, max_batch_bytes=5000)
    generator = genbank._generate_tables([[genbank_file_large_sequences]])
    tables = [table for _, table in generator]

    # Should create multiple batches due to byte limit
    assert len(tables) > 1


def test_genbank_no_byte_limit(genbank_file_large_sequences):
    """Test disabling byte-based batching."""
    genbank = GenBank(batch_size=1000, max_batch_bytes=None)
    generator = genbank._generate_tables([[genbank_file_large_sequences]])
    tables = [table for _, table in generator]

    # Should create single batch since batch_size is high
    assert len(tables) == 1
    assert tables[0].num_rows == 5


def test_genbank_schema_types(genbank_file):
    """Test that schema uses correct Arrow types."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    schema = pa_table.schema

    # Regular string columns
    assert schema.field("locus_name").type == pa.string()
    assert schema.field("accession").type == pa.string()
    assert schema.field("version").type == pa.string()
    assert schema.field("definition").type == pa.string()
    assert schema.field("organism").type == pa.string()
    assert schema.field("taxonomy").type == pa.string()
    assert schema.field("keywords").type == pa.string()
    assert schema.field("molecule_type").type == pa.string()

    # Large string for sequence
    assert schema.field("sequence").type == pa.large_string()

    # JSON extension type for features (parsed into objects on read)
    assert schema.field("features").type == pa.json_()

    # Integer for length
    assert schema.field("length").type == pa.int64()


def test_genbank_feature_casting(genbank_file):
    """Test feature casting to custom schema."""
    features = Features(
        {
            "locus_name": Value("string"),
            "accession": Value("string"),
            "version": Value("string"),
            "definition": Value("string"),
            "organism": Value("string"),
            "taxonomy": Value("string"),
            "keywords": Value("string"),
            "sequence": Value("large_string"),
            "features": Value("large_string"),
            "length": Value("int64"),
            "molecule_type": Value("string"),
        }
    )
    genbank = GenBank(features=features)
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    assert pa_table.schema.field("locus_name").type == pa.string()
    assert pa_table.schema.field("sequence").type == pa.large_string()
    assert pa_table.schema.field("length").type == pa.int64()


def test_genbank_empty_file(tmp_path):
    """Test handling of empty GenBank file."""
    filename = tmp_path / "empty.gb"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")

    genbank = GenBank()
    generator = genbank._generate_tables([[str(filename)]])
    tables = list(generator)

    # Empty file should produce no tables
    assert len(tables) == 0


def test_genbank_sequence_parsing(genbank_file):
    """Test that sequence is parsed correctly."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    # Sequence should be uppercase with no whitespace or numbers
    sequence = result["sequence"][0]
    assert sequence.isupper()
    assert " " not in sequence
    assert all(c in "ACGT" for c in sequence)


def test_genbank_multiple_files(tmp_path):
    """Test loading multiple GenBank files."""
    file1 = tmp_path / "seq1.gb"
    file2 = tmp_path / "seq2.gb"

    data1 = textwrap.dedent(
        """\
        LOCUS       FILE1SEQ     20 bp    DNA             PLN       01-JAN-2024
        DEFINITION  File 1 sequence.
        ACCESSION   FILE1
        VERSION     FILE1.1
        KEYWORDS    .
        SOURCE      Test organism
          ORGANISM  Test organism
                    Eukaryota.
        FEATURES             Location/Qualifiers
             source          1..20
                             /organism="Test organism"
        ORIGIN
                1 atcgatcgat cgatcgatcg
        //
        """
    )

    data2 = textwrap.dedent(
        """\
        LOCUS       FILE2SEQ     20 bp    DNA             PLN       01-JAN-2024
        DEFINITION  File 2 sequence.
        ACCESSION   FILE2
        VERSION     FILE2.1
        KEYWORDS    .
        SOURCE      Test organism
          ORGANISM  Test organism
                    Eukaryota.
        FEATURES             Location/Qualifiers
             source          1..20
                             /organism="Test organism"
        ORIGIN
                1 gctagctagc tagctagcta
        //
        """
    )

    with open(file1, "w", encoding="utf-8") as f:
        f.write(data1)
    with open(file2, "w", encoding="utf-8") as f:
        f.write(data2)

    genbank = GenBank()
    generator = genbank._generate_tables([[str(file1)], [str(file2)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["accession"]) == 2
    assert "FILE1" in result["accession"]
    assert "FILE2" in result["accession"]


def test_genbank_extensions():
    """Test that correct extensions are defined."""
    assert ".gb" in GenBank.EXTENSIONS
    assert ".gbk" in GenBank.EXTENSIONS
    assert ".genbank" in GenBank.EXTENSIONS


def test_genbank_all_columns():
    """Test that all expected columns are defined."""
    expected_columns = [
        "locus_name",
        "accession",
        "version",
        "definition",
        "organism",
        "taxonomy",
        "keywords",
        "sequence",
        "features",
        "length",
        "molecule_type",
        "secondary_accessions",
        "contig",
    ]
    assert GenBank.ALL_COLUMNS == expected_columns


def test_genbank_locus_parsing_variations(tmp_path):
    """Test parsing different LOCUS line formats."""
    filename = tmp_path / "locus_variations.gb"
    # Minimal LOCUS line
    data = textwrap.dedent(
        """\
        LOCUS       MINSEQ          100 bp    mRNA            01-JAN-2024
        DEFINITION  Minimal sequence.
        ACCESSION   MINSEQ
        VERSION     MINSEQ.1
        KEYWORDS    .
        SOURCE      Test
          ORGANISM  Test
                    Test.
        FEATURES             Location/Qualifiers
             source          1..100
        ORIGIN
                1 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
               61 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg
        //
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    genbank = GenBank()
    generator = genbank._generate_tables([[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert result["locus_name"][0] == "MINSEQ"
    assert result["length"][0] == 100
    assert result["molecule_type"][0] == "mRNA"


def test_genbank_keywords_empty(genbank_file):
    """Test that '.' keywords are handled correctly."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    # The fixture has KEYWORDS    . which should result in empty keywords
    assert result["keywords"][0] == ""


def test_genbank_taxonomy_continuation(genbank_file):
    """Test multi-line taxonomy parsing."""
    genbank = GenBank()
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    # Taxonomy should include continuation lines
    taxonomy = result["taxonomy"][0]
    assert "Eukaryota" in taxonomy
    assert "Fungi" in taxonomy


def test_genbank_feature_boolean_qualifier(tmp_path):
    """Test parsing of boolean qualifiers like /pseudo."""
    filename = tmp_path / "boolean_qual.gb"
    data = textwrap.dedent(
        """\
        LOCUS       BOOLSEQ      50 bp    DNA             PLN       01-JAN-2024
        DEFINITION  Sequence with boolean qualifier.
        ACCESSION   BOOLSEQ
        VERSION     BOOLSEQ.1
        KEYWORDS    .
        SOURCE      Test
          ORGANISM  Test
                    Test.
        FEATURES             Location/Qualifiers
             gene            1..50
                             /gene="testGene"
                             /pseudo
        ORIGIN
                1 atcgatcgat cgatcgatcg atcgatcgat cgatcgatcg atcgatcgat
        //
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    genbank = GenBank()
    generator = genbank._generate_tables([[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()
    features = json.loads(result["features"][0])

    gene_feature = next((f for f in features if f["type"] == "gene"), None)
    assert gene_feature is not None
    assert gene_feature["qualifiers"].get("pseudo") == [""]  # valueless, as Biopython stores it


# ---------------------------------------------------------------------------
# Regression tests for parser defects found in review. Each one reproduces a
# case that valid GenBank files hit routinely: repeated qualifiers, locations
# and header fields wrapped across lines, and protein LOCUS records.
# ---------------------------------------------------------------------------

_LOCUS_DNA = "LOCUS       T           100 bp    DNA     linear   PLN 01-JAN-2024\n"
_ORIGIN = "ORIGIN\n        1 atcgatcgat\n//\n"


def _parse_one(tmp_path, text, name="reg.gb"):
    """Load a single inline GenBank record and return (record, decoded features)."""
    filename = tmp_path / name
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    tables = [table for _, table in GenBank()._generate_tables([[str(filename)]])]
    result = pa.concat_tables(tables).to_pydict()
    features = json.loads(result["features"][0]) if result["features"][0] else []
    return result, features


def test_genbank_repeated_qualifiers_are_all_kept(tmp_path):
    """A feature with two /db_xref entries must keep both, not just the last."""
    _, features = _parse_one(
        tmp_path,
        _LOCUS_DNA
        + "FEATURES             Location/Qualifiers\n"
        + "     gene            1..100\n"
        + '                     /gene="g1"\n'
        + '                     /db_xref="TAX:1"\n'
        + '                     /db_xref="TAX:2"\n'
        + _ORIGIN,
    )
    qualifiers = features[0]["qualifiers"]
    assert qualifiers["db_xref"] == ["TAX:1", "TAX:2"]
    assert qualifiers["gene"] == ["g1"]


def test_genbank_order_location_parses(tmp_path):
    """order(...) is a valid location operator and must not crash the loader."""
    _, features = _parse_one(
        tmp_path,
        _LOCUS_DNA
        + "FEATURES             Location/Qualifiers\n"
        + "     gene            order(1..5,8..10)\n"
        + _ORIGIN,
    )
    location = features[0]["location"]
    assert location["operator"] == "order"
    assert location["parts"] == [[1, 5], [8, 10]]
    assert (location["start"], location["end"]) == (1, 10)


def test_genbank_wrapped_join_location(tmp_path):
    """A join(...) location wrapped onto a second line must parse completely."""
    _, features = _parse_one(
        tmp_path,
        _LOCUS_DNA
        + "FEATURES             Location/Qualifiers\n"
        + "     CDS             join(1..10,20..30,\n"
        + "                     40..50)\n"
        + '                     /gene="split"\n'
        + _ORIGIN,
    )
    location = features[0]["location"]
    assert location["parts"] == [[1, 10], [20, 30], [40, 50]]
    assert location["start"] == 1
    assert location["end"] == 50


def test_genbank_wrapped_definition_is_complete(tmp_path):
    """A DEFINITION wrapped onto a second line must not be truncated."""
    result, _ = _parse_one(
        tmp_path,
        "LOCUS       T           100 bp    DNA     linear   PLN 01-JAN-2024\n"
        "DEFINITION  First line of a long definition that\n"
        "            continues on a second line.\n"
        "ACCESSION   T\n" + _ORIGIN,
    )
    assert result["definition"][0] == "First line of a long definition that continues on a second line."


def test_genbank_taxonomy_separators_and_no_reference_bleed(tmp_path):
    """Taxonomy keeps the file's own delimiters and ignores later header blocks."""
    result, _ = _parse_one(
        tmp_path,
        "LOCUS       T           100 bp    DNA     linear   PLN 01-JAN-2024\n"
        "SOURCE      Test organism\n"
        "  ORGANISM  Test organism\n"
        "            Eukaryota; Fungi;\n"
        "            Ascomycota.\n"
        "REFERENCE   1  (bases 1 to 100)\n"
        "  AUTHORS   Someone,A.\n"
        "            Wrapped author line here\n" + _ORIGIN,
    )
    taxonomy = result["taxonomy"][0]
    assert taxonomy == "Eukaryota; Fungi; Ascomycota."
    assert ";;" not in taxonomy
    assert "author" not in taxonomy.lower()


def test_genbank_protein_locus_lowercase_aa(tmp_path):
    """A protein LOCUS line using the lowercase `aa` unit is a protein record."""
    result, _ = _parse_one(
        tmp_path,
        "LOCUS       P            50 aa            linear   PLN 01-JAN-2024\nORIGIN\n        1 mkwvtfisll\n//\n",
    )
    assert result["length"][0] == 50
    assert result["molecule_type"][0] == "protein"


_HDR = _LOCUS_DNA + "FEATURES             Location/Qualifiers\n"


def test_genbank_join_of_complements_parses_recursively(tmp_path):
    """complement() may appear inside join()/order(); each part is parsed on its own."""
    _, features = _parse_one(
        tmp_path, _HDR + "     CDS             join(complement(6..10),complement(1..5))\n" + _ORIGIN
    )
    location = features[0]["location"]
    assert location["operator"] == "join"
    assert location["parts"] == [[6, 10], [1, 5]]
    assert location["strand"] == -1


def test_genbank_mixed_strand_join_has_no_single_strand(tmp_path):
    """A trans-spliced join mixes strands; Biopython reports strand None for that case."""
    _, features = _parse_one(tmp_path, _HDR + "     CDS             join(1..5,complement(8..10))\n" + _ORIGIN)
    assert features[0]["location"]["strand"] is None
    assert features[0]["location"]["parts"] == [[1, 5], [8, 10]]


def test_genbank_remote_reference_in_join(tmp_path):
    """A part may name another record (ACCESSION.VERSION:range); the range still parses."""
    _, features = _parse_one(tmp_path, _HDR + "     CDS             join(AB000001.1:1..10,20..30)\n" + _ORIGIN)
    assert features[0]["location"]["parts"] == [[1, 10], [20, 30]]


def test_genbank_wrapped_free_text_qualifier_keeps_word_boundary(tmp_path):
    """Wrapped free-text values join with a space (Biopython: q_value.replace("\\n", " "))."""
    text = (
        _HDR
        + '     gene            1..10\n                     /note="alpha beta\n                     gamma"\n'
        + _ORIGIN
    )
    _, features = _parse_one(tmp_path, text)
    assert features[0]["qualifiers"]["note"] == ["alpha beta gamma"]


def test_genbank_wrapped_translation_joins_without_space(tmp_path):
    """/translation is the one qualifier whose wrapped lines concatenate directly."""
    text = (
        _HDR
        + '     CDS             1..10\n                     /translation="MRLL\n                     ELKA"\n'
        + _ORIGIN
    )
    _, features = _parse_one(tmp_path, text)
    assert features[0]["qualifiers"]["translation"] == ["MRLLELKA"]


def test_genbank_slash_inside_open_quoted_value_is_not_a_new_qualifier(tmp_path):
    """A continuation line starting with '/' belongs to the still-open quoted value."""
    text = (
        _HDR + '     gene            1..10\n                     /note="see\n                     /docs"\n' + _ORIGIN
    )
    _, features = _parse_one(tmp_path, text)
    assert features[0]["qualifiers"] == {"note": ["see /docs"]}


def test_genbank_base_count_line_is_not_a_feature(tmp_path):
    """Legacy BASE COUNT sits between FEATURES and ORIGIN and is a keyword, not a feature."""
    text = _HDR + "     source          1..4\nBASE COUNT       1 a 1 c 1 g 1 t\n" + _ORIGIN
    _, features = _parse_one(tmp_path, text)
    assert [f["type"] for f in features] == ["source"]


def test_genbank_contig_line_is_not_sequence(tmp_path):
    """A CONTIG keyword line must not be folded into the sequence text."""
    result, _ = _parse_one(tmp_path, _LOCUS_DNA + "ORIGIN\nCONTIG      join(AB000001.1:1..10,AB000002.1:1..10)\n//\n")
    assert result["sequence"] == [""]


def test_genbank_locus_strandedness_prefixed_molecule_type(tmp_path):
    """LOCUS may carry ss-/ds-/ms- prefixed molecule types such as ds-DNA."""
    result, _ = _parse_one(tmp_path, "LOCUS       T             10 bp ds-DNA     linear   PLN 01-JAN-2024\n" + _ORIGIN)
    assert result["molecule_type"] == ["ds-DNA"]


def test_genbank_columns_project_custom_features(tmp_path):
    """columns= applies to a user-supplied features schema too."""
    filename = tmp_path / "proj.gb"
    filename.write_text(_LOCUS_DNA + _ORIGIN, encoding="utf-8")
    builder = GenBank(columns=["sequence"], features=GenBank.DEFAULT_FEATURES)
    table = next(iter(builder._generate_tables([[str(filename)]])))[1]
    assert table.column_names == ["sequence"]
    with pytest.raises(ValueError, match="not in features"):
        GenBank(columns=["sequence"], features=Features({"locus_name": Value("string")}))._info()


def test_genbank_partial_location_markers_are_kept(tmp_path):
    """'<' and '>' mark boundaries beyond the coordinate (Biopython Before/AfterPosition)."""
    _, features = _parse_one(
        tmp_path,
        _HDR
        + "     gene            <1..>10\n     CDS             3..8\n     mRNA            join(<1..5,8..>10)\n"
        + _ORIGIN,
    )
    fuzzy, exact, compound = (f["location"] for f in features)
    assert (fuzzy["start_partial"], fuzzy["end_partial"]) == (True, True)
    assert (exact["start_partial"], exact["end_partial"]) == (False, False)
    assert (compound["start_partial"], compound["end_partial"]) == (True, True)
    assert (fuzzy["start"], fuzzy["end"]) == (1, 10)


def test_genbank_secondary_accessions_including_continuation_lines(tmp_path):
    result, _ = _parse_one(tmp_path, _LOCUS_DNA + "ACCESSION   M55673 M25818\n            M27095\n" + _ORIGIN)
    assert result["accession"] == ["M55673"]
    assert result["secondary_accessions"] == [["M25818", "M27095"]]


def test_genbank_contig_expression_is_stored(tmp_path):
    """CONTIG follows the feature table and may wrap; it is kept whole and is not sequence."""
    text = _HDR + "     source          1..20\nCONTIG      join(AB000001.1:1..10,\n            AB000002.1:1..10)\n//\n"
    result, features = _parse_one(tmp_path, text)
    assert result["contig"] == ["join(AB000001.1:1..10,AB000002.1:1..10)"]
    assert result["sequence"] == [""]
    assert [f["type"] for f in features] == ["source"]
    result, _ = _parse_one(tmp_path, _LOCUS_DNA + "CONTIG      join(X.1:1..5)\n" + _ORIGIN)
    assert result["contig"] == ["join(X.1:1..5)"]


def test_genbank_features_subset_selects_columns(tmp_path):
    """A features schema naming a subset of columns yields exactly those columns."""
    filename = tmp_path / "sub.gb"
    filename.write_text(_LOCUS_DNA + _ORIGIN, encoding="utf-8")
    features = Features({"locus_name": Value("string"), "sequence": Value("large_string")})
    table = next(iter(GenBank(features=features)._generate_tables([[str(filename)]])))[1]
    assert table.column_names == ["locus_name", "sequence"]
