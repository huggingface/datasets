"""Tests for GenBank file loader."""

import bz2
import gzip
import json
import lzma
import textwrap

import pyarrow as pa
import pytest

from datasets import Features, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.genbank.genbank import GenBank, GenBankConfig


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
    return str(filename)


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
    return str(filename)


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
    return str(filename)


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
    genbank = GenBank(parse_features=True)
    generator = genbank._generate_tables([[genbank_file_complex_features]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()
    features = json.loads(result["features"][0])

    assert len(features) >= 3

    # Find the complement feature
    rev_gene = next((f for f in features if f.get("qualifiers", {}).get("gene") == "revGene"), None)
    assert rev_gene is not None
    assert rev_gene["location"]["strand"] == -1

    # Find the join feature
    split_gene = next((f for f in features if f.get("qualifiers", {}).get("gene") == "splitGene"), None)
    assert split_gene is not None
    assert "parts" in split_gene["location"]
    assert len(split_gene["location"]["parts"]) == 3


def test_genbank_feature_parsing_disabled(genbank_file):
    """Test that feature parsing can be disabled."""
    genbank = GenBank(parse_features=False)
    generator = genbank._generate_tables([[genbank_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    # Features should be empty string when parsing is disabled
    assert result["features"][0] == ""


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
    """Test that invalid column names raise an error."""
    genbank = GenBank(columns=["sequence", "invalid_column"])
    with pytest.raises(ValueError, match="Invalid column 'invalid_column'"):
        list(genbank._generate_tables([[]]))


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

    # Large string for sequence and features
    assert schema.field("sequence").type == pa.large_string()
    assert schema.field("features").type == pa.large_string()

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

    genbank = GenBank(parse_features=True)
    generator = genbank._generate_tables([[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()
    features = json.loads(result["features"][0])

    gene_feature = next((f for f in features if f["type"] == "gene"), None)
    assert gene_feature is not None
    assert gene_feature["qualifiers"].get("pseudo") == "true"
