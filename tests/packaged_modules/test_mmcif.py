"""Tests for mmCIF file loader."""

import gzip
import textwrap

import pyarrow as pa
import pytest

from datasets import Features, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.mmcif.mmcif import Mmcif, MmcifConfig


@pytest.fixture
def mmcif_file(tmp_path):
    """Create a simple mmCIF file with atom_site data."""
    filename = tmp_path / "structure.cif"
    data = textwrap.dedent(
        """\
        data_test
        #
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        _atom_site.group_PDB
        1  N  N   ALA A 1  10.000 20.000 30.000 1.00 15.00 ATOM
        2  C  CA  ALA A 1  11.000 21.000 31.000 1.00 14.00 ATOM
        3  C  C   ALA A 1  12.000 22.000 32.000 1.00 13.00 ATOM
        4  O  O   ALA A 1  13.000 23.000 33.000 1.00 12.00 ATOM
        5  C  CB  ALA A 1  14.000 24.000 34.000 1.00 16.00 ATOM
        #
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def mmcif_file_with_hetatm(tmp_path):
    """Create mmCIF file with ATOM and HETATM records."""
    filename = tmp_path / "structure_hetatm.cif"
    data = textwrap.dedent(
        """\
        data_test
        #
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        _atom_site.group_PDB
        1  N  N   ALA A 1  10.000 20.000 30.000 1.00 15.00 ATOM
        2  C  CA  ALA A 1  11.000 21.000 31.000 1.00 14.00 ATOM
        3  O  O   HOH B 1   5.000 10.000 15.000 1.00 20.00 HETATM
        4  O  O   HOH B 2   6.000 11.000 16.000 1.00 21.00 HETATM
        #
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def mmcif_file_gzipped(tmp_path):
    """Create a gzipped mmCIF file."""
    filename = tmp_path / "structure.cif.gz"
    data = textwrap.dedent(
        """\
        data_test
        #
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        _atom_site.group_PDB
        1  N  N   GLY A 1  10.000 20.000 30.000 1.00 15.00 ATOM
        2  C  CA  GLY A 1  11.000 21.000 31.000 1.00 14.00 ATOM
        #
        """
    )
    with gzip.open(filename, "wt", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def mmcif_file_quoted_values(tmp_path):
    """Create mmCIF file with quoted values."""
    filename = tmp_path / "structure_quoted.cif"
    data = textwrap.dedent(
        """\
        data_test
        #
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        _atom_site.group_PDB
        1  N  "N"   'ALA' A 1  10.000 20.000 30.000 1.00 15.00 ATOM
        2  C  "CA"  'ALA' A 1  11.000 21.000 31.000 1.00 14.00 ATOM
        #
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def mmcif_file_missing_values(tmp_path):
    """Create mmCIF file with missing values (. and ?)."""
    filename = tmp_path / "structure_missing.cif"
    data = textwrap.dedent(
        """\
        data_test
        #
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        _atom_site.group_PDB
        1  N  N   ALA A .  10.000 20.000 30.000 1.00 ?     ATOM
        2  C  CA  ALA A ?  11.000 21.000 31.000 .    15.00 ATOM
        #
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def mmcif_file_large(tmp_path):
    """Create a larger mmCIF file for batch testing."""
    filename = tmp_path / "structure_large.cif"

    # Build header
    lines = [
        "data_test",
        "#",
        "loop_",
        "_atom_site.id",
        "_atom_site.type_symbol",
        "_atom_site.label_atom_id",
        "_atom_site.label_comp_id",
        "_atom_site.label_asym_id",
        "_atom_site.label_seq_id",
        "_atom_site.Cartn_x",
        "_atom_site.Cartn_y",
        "_atom_site.Cartn_z",
        "_atom_site.occupancy",
        "_atom_site.B_iso_or_equiv",
        "_atom_site.group_PDB",
    ]

    # Add 500 atoms
    for i in range(500):
        atom_name = ["N", "CA", "C", "O", "CB"][i % 5]
        element = "N" if atom_name == "N" else ("O" if atom_name == "O" else "C")
        residue = i // 5 + 1
        lines.append(
            f"{i+1}  {element}  {atom_name}  ALA A {residue}  "
            f"{10.0 + i * 0.1:.3f} {20.0 + i * 0.1:.3f} {30.0 + i * 0.1:.3f} "
            f"1.00 15.00 ATOM"
        )

    lines.append("#")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return str(filename)


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = MmcifConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = MmcifConfig(name="name", data_files=data_files)


def test_mmcif_basic_loading(mmcif_file):
    """Test basic mmCIF file loading."""
    mmcif = Mmcif()
    generator = mmcif._generate_tables([[mmcif_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 5
    assert result["id"] == [1, 2, 3, 4, 5]
    assert result["type_symbol"] == ["N", "C", "C", "O", "C"]
    assert result["label_atom_id"] == ["N", "CA", "C", "O", "CB"]
    assert result["label_comp_id"] == ["ALA", "ALA", "ALA", "ALA", "ALA"]
    assert result["Cartn_x"][0] == pytest.approx(10.0)
    assert result["Cartn_y"][0] == pytest.approx(20.0)
    assert result["Cartn_z"][0] == pytest.approx(30.0)


def test_mmcif_column_filtering(mmcif_file):
    """Test loading with column subset."""
    mmcif = Mmcif(columns=["label_atom_id", "Cartn_x", "Cartn_y", "Cartn_z"])
    generator = mmcif._generate_tables([[mmcif_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    # Should only have specified columns
    assert set(result.keys()) == {"label_atom_id", "Cartn_x", "Cartn_y", "Cartn_z"}
    assert len(result["label_atom_id"]) == 5


def test_mmcif_hetatm_filtering(mmcif_file_with_hetatm):
    """Test excluding HETATM records."""
    # Include HETATM (default)
    mmcif_with = Mmcif(include_hetatm=True, columns=["id", "group_PDB"])
    generator = mmcif_with._generate_tables([[mmcif_file_with_hetatm]])
    pa_table = pa.concat_tables([table for _, table in generator])
    result_with = pa_table.to_pydict()

    assert len(result_with["id"]) == 4
    assert "HETATM" in result_with["group_PDB"]

    # Exclude HETATM
    mmcif_without = Mmcif(include_hetatm=False, columns=["id", "group_PDB"])
    generator = mmcif_without._generate_tables([[mmcif_file_with_hetatm]])
    pa_table = pa.concat_tables([table for _, table in generator])
    result_without = pa_table.to_pydict()

    assert len(result_without["id"]) == 2
    assert "HETATM" not in result_without["group_PDB"]


def test_mmcif_gzipped(mmcif_file_gzipped):
    """Test loading gzipped mmCIF files."""
    mmcif = Mmcif()
    generator = mmcif._generate_tables([[mmcif_file_gzipped]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 2
    assert result["label_comp_id"] == ["GLY", "GLY"]


def test_mmcif_quoted_values(mmcif_file_quoted_values):
    """Test parsing quoted values."""
    mmcif = Mmcif()
    generator = mmcif._generate_tables([[mmcif_file_quoted_values]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert result["label_atom_id"] == ["N", "CA"]
    assert result["label_comp_id"] == ["ALA", "ALA"]


def test_mmcif_missing_values(mmcif_file_missing_values):
    """Test handling of missing values (. and ?)."""
    mmcif = Mmcif()
    generator = mmcif._generate_tables([[mmcif_file_missing_values]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 2
    # Missing values should be None
    assert result["label_seq_id"][0] is None
    assert result["label_seq_id"][1] is None
    assert result["B_iso_or_equiv"][0] is None
    assert result["occupancy"][1] is None


def test_mmcif_batch_size(mmcif_file_large):
    """Test batch size configuration."""
    # Use batch_size=100 to create multiple batches
    mmcif = Mmcif(batch_size=100)
    generator = mmcif._generate_tables([[mmcif_file_large]])
    tables = [table for _, table in generator]

    # Should have 5 batches (500 atoms / 100)
    assert len(tables) == 5

    # Each batch should have 100 records
    for table in tables:
        assert table.num_rows == 100


def test_mmcif_schema_types(mmcif_file):
    """Test that schema uses correct Arrow types."""
    mmcif = Mmcif()
    generator = mmcif._generate_tables([[mmcif_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    schema = pa_table.schema

    # Check numeric types
    assert schema.field("id").type == pa.int32()
    assert schema.field("label_seq_id").type == pa.int32()
    assert schema.field("Cartn_x").type == pa.float32()
    assert schema.field("Cartn_y").type == pa.float32()
    assert schema.field("Cartn_z").type == pa.float32()
    assert schema.field("occupancy").type == pa.float32()
    assert schema.field("B_iso_or_equiv").type == pa.float32()

    # Check string types
    assert schema.field("type_symbol").type == pa.string()
    assert schema.field("label_atom_id").type == pa.string()
    assert schema.field("label_comp_id").type == pa.string()


def test_mmcif_feature_casting(mmcif_file):
    """Test feature casting to custom schema."""
    features = Features({
        "id": Value("int32"),
        "type_symbol": Value("string"),
        "Cartn_x": Value("float32"),
        "Cartn_y": Value("float32"),
        "Cartn_z": Value("float32"),
    })
    mmcif = Mmcif(features=features, columns=["id", "type_symbol", "Cartn_x", "Cartn_y", "Cartn_z"])
    generator = mmcif._generate_tables([[mmcif_file]])
    pa_table = pa.concat_tables([table for _, table in generator])

    assert pa_table.schema.field("id").type == pa.int32()
    assert pa_table.schema.field("Cartn_x").type == pa.float32()


def test_mmcif_empty_file(tmp_path):
    """Test handling of empty mmCIF file."""
    filename = tmp_path / "empty.cif"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")

    mmcif = Mmcif()
    generator = mmcif._generate_tables([[str(filename)]])
    tables = list(generator)

    # Empty file should produce no tables
    assert len(tables) == 0


def test_mmcif_no_atom_site(tmp_path):
    """Test mmCIF file without atom_site category."""
    filename = tmp_path / "no_atoms.cif"
    data = textwrap.dedent(
        """\
        data_test
        #
        _entry.id test
        _struct.title "Test structure"
        #
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    mmcif = Mmcif()
    generator = mmcif._generate_tables([[str(filename)]])
    tables = list(generator)

    # No atom_site should produce no tables
    assert len(tables) == 0


def test_mmcif_multiple_files(tmp_path):
    """Test loading multiple mmCIF files."""
    # Create two files
    file1 = tmp_path / "structure1.cif"
    file2 = tmp_path / "structure2.cif"

    data1 = textwrap.dedent(
        """\
        data_test1
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        1  N  N  ALA A 1  10.0 20.0 30.0 1.0 15.0
        """
    )

    data2 = textwrap.dedent(
        """\
        data_test2
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        1  C  CA  GLY B 1  11.0 21.0 31.0 1.0 14.0
        """
    )

    with open(file1, "w", encoding="utf-8") as f:
        f.write(data1)
    with open(file2, "w", encoding="utf-8") as f:
        f.write(data2)

    mmcif = Mmcif()
    generator = mmcif._generate_tables([[str(file1)], [str(file2)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()

    assert len(result["id"]) == 2
    assert result["label_comp_id"] == ["ALA", "GLY"]


def test_mmcif_extensions():
    """Test that correct extensions are defined."""
    assert ".cif" in Mmcif.EXTENSIONS
    assert ".mmcif" in Mmcif.EXTENSIONS


def test_mmcif_comments_handling(tmp_path):
    """Test that comments are properly skipped."""
    filename = tmp_path / "comments.cif"
    data = textwrap.dedent(
        """\
        data_test
        # This is a comment
        #
        loop_
        _atom_site.id
        _atom_site.type_symbol
        _atom_site.label_atom_id
        _atom_site.label_comp_id
        _atom_site.label_asym_id
        _atom_site.label_seq_id
        _atom_site.Cartn_x
        _atom_site.Cartn_y
        _atom_site.Cartn_z
        _atom_site.occupancy
        _atom_site.B_iso_or_equiv
        # Another comment
        1  N  N  ALA A 1  10.0 20.0 30.0 1.0 15.0
        # Comment between data
        2  C  CA  ALA A 1  11.0 21.0 31.0 1.0 14.0
        #
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    mmcif = Mmcif()
    generator = mmcif._generate_tables([[str(filename)]])
    pa_table = pa.concat_tables([table for _, table in generator])

    result = pa_table.to_pydict()
    assert len(result["id"]) == 2


def test_mmcif_default_columns():
    """Test that default columns are sensible."""
    from datasets.packaged_modules.mmcif.mmcif import DEFAULT_ATOM_SITE_COLUMNS

    # Essential columns should be in defaults
    assert "id" in DEFAULT_ATOM_SITE_COLUMNS
    assert "type_symbol" in DEFAULT_ATOM_SITE_COLUMNS
    assert "label_atom_id" in DEFAULT_ATOM_SITE_COLUMNS
    assert "label_comp_id" in DEFAULT_ATOM_SITE_COLUMNS
    assert "Cartn_x" in DEFAULT_ATOM_SITE_COLUMNS
    assert "Cartn_y" in DEFAULT_ATOM_SITE_COLUMNS
    assert "Cartn_z" in DEFAULT_ATOM_SITE_COLUMNS
