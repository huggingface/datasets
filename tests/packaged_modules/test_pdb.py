"""Tests for PDB file loader."""

import gzip
import textwrap

import pyarrow as pa
import pytest

from datasets import Features, Value
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.pdb.pdb import (
    DEFAULT_PDB_COLUMNS,
    PDB_COLUMN_TYPES,
    Pdb,
    PdbConfig,
)


# Sample PDB content for testing
SAMPLE_PDB_CONTENT = textwrap.dedent("""\
ATOM      1  N   ALA A   1       1.000   2.000   3.000  1.00 10.00           N
ATOM      2  CA  ALA A   1       4.000   5.000   6.000  1.00 11.00           C
ATOM      3  C   ALA A   1       7.000   8.000   9.000  1.00 12.00           C
HETATM    4  O   HOH A 100      10.000  11.000  12.000  1.00 20.00           O
END
""")


@pytest.fixture
def pdb_file(tmp_path):
    """Create a sample PDB file."""
    filename = tmp_path / "test.pdb"
    filename.write_text(SAMPLE_PDB_CONTENT)
    return str(filename)


@pytest.fixture
def pdb_file_gzipped(tmp_path):
    """Create a gzipped PDB file."""
    filename = tmp_path / "test.pdb.gz"
    with gzip.open(filename, "wt", encoding="utf-8") as f:
        f.write(SAMPLE_PDB_CONTENT)
    return str(filename)


class TestPdbConfig:
    """Test PdbConfig validation."""

    def test_config_raises_when_invalid_name(self) -> None:
        with pytest.raises(InvalidConfigName, match="Bad characters"):
            _ = PdbConfig(name="name-with-*-invalid-character")

    @pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
    def test_config_raises_when_invalid_data_files(self, data_files) -> None:
        with pytest.raises(ValueError, match="Expected a DataFilesDict"):
            _ = PdbConfig(name="name", data_files=data_files)


class TestPdbLoader:
    """Test PDB file loading functionality."""

    def test_pdb_basic_loading(self, pdb_file):
        """Test basic PDB file loading."""
        pdb = Pdb()
        generator = pdb._generate_tables([[pdb_file]])
        pa_table = pa.concat_tables([table for _, table in generator])

        # Should have 4 records (3 ATOM + 1 HETATM)
        assert pa_table.num_rows == 4
        # Should have default columns
        assert set(pa_table.column_names) == set(DEFAULT_PDB_COLUMNS)

    def test_pdb_column_filtering(self, pdb_file):
        """Test selecting specific columns."""
        columns = ["atom_name", "x", "y", "z"]
        pdb = Pdb(columns=columns)
        generator = pdb._generate_tables([[pdb_file]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert set(pa_table.column_names) == set(columns)
        assert pa_table.num_rows == 4

    def test_pdb_atom_only(self, pdb_file):
        """Test loading only ATOM records."""
        pdb = Pdb(record_types=["ATOM"])
        generator = pdb._generate_tables([[pdb_file]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 3
        record_types = pa_table["record_type"].to_pylist()
        assert all(rt == "ATOM" for rt in record_types)

    def test_pdb_hetatm_only(self, pdb_file):
        """Test loading only HETATM records."""
        pdb = Pdb(record_types=["HETATM"])
        generator = pdb._generate_tables([[pdb_file]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 1
        record_types = pa_table["record_type"].to_pylist()
        assert all(rt == "HETATM" for rt in record_types)

    def test_pdb_gzipped(self, pdb_file_gzipped):
        """Test loading gzipped PDB files."""
        pdb = Pdb()
        generator = pdb._generate_tables([[pdb_file_gzipped]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 4

    def test_pdb_multichain(self, tmp_path):
        """Test loading PDB with multiple chains."""
        pdb_content = textwrap.dedent("""\
ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00 10.00           C
ATOM      2  CA  ALA B   1       4.000   5.000   6.000  1.00 11.00           C
ATOM      3  CA  ALA C   1       7.000   8.000   9.000  1.00 12.00           C
END
""")
        file_path = tmp_path / "multichain.pdb"
        file_path.write_text(pdb_content)

        pdb = Pdb()
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 3
        chain_ids = pa_table["chain_id"].to_pylist()
        assert chain_ids == ["A", "B", "C"]

    def test_pdb_alternate_locations(self, tmp_path):
        """Test parsing alternate location indicators."""
        pdb_content = textwrap.dedent("""\
ATOM      1  CA AALA A   1       1.000   2.000   3.000  0.50 10.00           C
ATOM      2  CA BALA A   1       1.100   2.100   3.100  0.50 10.00           C
END
""")
        file_path = tmp_path / "altloc.pdb"
        file_path.write_text(pdb_content)

        pdb = Pdb(columns=["atom_name", "alt_loc", "occupancy"])
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 2
        alt_locs = pa_table["alt_loc"].to_pylist()
        assert alt_locs == ["A", "B"]
        occupancies = pa_table["occupancy"].to_pylist()
        assert all(occ == 0.5 for occ in occupancies)

    def test_pdb_charged_atoms(self, tmp_path):
        """Test parsing atoms with charges."""
        pdb_content = textwrap.dedent("""\
ATOM      1  N   LYS A   1       1.000   2.000   3.000  1.00 10.00           N1+
ATOM      2  OE1 GLU A   2       4.000   5.000   6.000  1.00 11.00           O1-
END
""")
        file_path = tmp_path / "charged.pdb"
        file_path.write_text(pdb_content)

        pdb = Pdb(columns=["atom_name", "element", "charge"])
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 2
        charges = pa_table["charge"].to_pylist()
        assert charges == ["1+", "1-"]

    def test_pdb_batch_size(self, tmp_path):
        """Test batch size configuration."""
        # Create PDB with more records than batch size
        lines = []
        for i in range(10):
            lines.append(
                f"ATOM  {i+1:5d}  CA  ALA A{i+1:4d}       1.000   2.000   3.000  1.00 10.00           C"
            )
        lines.append("END")
        pdb_content = "\n".join(lines) + "\n"

        file_path = tmp_path / "large.pdb"
        file_path.write_text(pdb_content)

        # Use batch_size=3 to force multiple batches
        pdb = Pdb(batch_size=3)
        batches = list(pdb._generate_tables([[str(file_path)]]))

        # Should have 4 batches: 3+3+3+1
        assert len(batches) == 4
        total_rows = sum(table.num_rows for _, table in batches)
        assert total_rows == 10

    def test_pdb_schema_types(self, pdb_file):
        """Test that schema types are correct."""
        pdb = Pdb()
        generator = pdb._generate_tables([[pdb_file]])
        pa_table = pa.concat_tables([table for _, table in generator])

        # Check numeric columns
        assert pa.types.is_float32(pa_table.schema.field("x").type)
        assert pa.types.is_float32(pa_table.schema.field("y").type)
        assert pa.types.is_float32(pa_table.schema.field("z").type)
        assert pa.types.is_float32(pa_table.schema.field("occupancy").type)
        assert pa.types.is_float32(pa_table.schema.field("temp_factor").type)
        assert pa.types.is_int32(pa_table.schema.field("atom_serial").type)
        assert pa.types.is_int32(pa_table.schema.field("residue_seq").type)

        # Check string columns
        assert pa.types.is_string(pa_table.schema.field("atom_name").type)
        assert pa.types.is_string(pa_table.schema.field("residue_name").type)
        assert pa.types.is_string(pa_table.schema.field("chain_id").type)

    def test_pdb_feature_casting(self, pdb_file):
        """Test feature casting to specified types."""
        features = Features({
            "atom_name": Value("string"),
            "x": Value("float64"),
            "y": Value("float64"),
            "z": Value("float64"),
        })
        pdb = Pdb(columns=["atom_name", "x", "y", "z"], features=features)
        generator = pdb._generate_tables([[pdb_file]])
        pa_table = pa.concat_tables([table for _, table in generator])

        # Cast to features
        pa_table = pdb._cast_table(pa_table)

        assert pa.types.is_float64(pa_table.schema.field("x").type)
        assert pa.types.is_float64(pa_table.schema.field("y").type)
        assert pa.types.is_float64(pa_table.schema.field("z").type)

    def test_pdb_empty_file(self, tmp_path):
        """Test handling empty PDB file."""
        file_path = tmp_path / "empty.pdb"
        file_path.write_text("END\n")

        pdb = Pdb()
        batches = list(pdb._generate_tables([[str(file_path)]]))

        # No records should be yielded
        assert len(batches) == 0

    def test_pdb_multiple_files(self, tmp_path):
        """Test loading multiple PDB files."""
        pdb_content1 = textwrap.dedent("""\
ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00 10.00           C
END
""")
        pdb_content2 = textwrap.dedent("""\
ATOM      1  CA  GLY B   1       4.000   5.000   6.000  1.00 11.00           C
END
""")
        file1 = tmp_path / "file1.pdb"
        file2 = tmp_path / "file2.pdb"
        file1.write_text(pdb_content1)
        file2.write_text(pdb_content2)

        pdb = Pdb()
        generator = pdb._generate_tables([[str(file1), str(file2)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 2
        residue_names = pa_table["residue_name"].to_pylist()
        assert set(residue_names) == {"ALA", "GLY"}

    def test_pdb_extensions(self):
        """Test that correct extensions are registered."""
        assert ".pdb" in Pdb.EXTENSIONS
        assert ".ent" in Pdb.EXTENSIONS

    def test_pdb_default_columns(self):
        """Test default columns are defined correctly."""
        assert "atom_serial" in DEFAULT_PDB_COLUMNS
        assert "atom_name" in DEFAULT_PDB_COLUMNS
        assert "residue_name" in DEFAULT_PDB_COLUMNS
        assert "chain_id" in DEFAULT_PDB_COLUMNS
        assert "x" in DEFAULT_PDB_COLUMNS
        assert "y" in DEFAULT_PDB_COLUMNS
        assert "z" in DEFAULT_PDB_COLUMNS
        # Optional columns should not be in default
        assert "charge" not in DEFAULT_PDB_COLUMNS
        assert "insertion_code" not in DEFAULT_PDB_COLUMNS

    def test_pdb_insertion_codes(self, tmp_path):
        """Test parsing insertion codes."""
        pdb_content = textwrap.dedent("""\
ATOM      1  CA  ALA A  27       1.000   2.000   3.000  1.00 10.00           C
ATOM      2  CA  ALA A  27A      4.000   5.000   6.000  1.00 11.00           C
ATOM      3  CA  ALA A  27B      7.000   8.000   9.000  1.00 12.00           C
END
""")
        file_path = tmp_path / "insertion.pdb"
        file_path.write_text(pdb_content)

        pdb = Pdb(columns=["residue_seq", "insertion_code", "x"])
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 3
        insertion_codes = pa_table["insertion_code"].to_pylist()
        # First one has no insertion code, others have A and B
        assert insertion_codes[0] in ["", None]
        assert insertion_codes[1] == "A"
        assert insertion_codes[2] == "B"

    def test_pdb_short_lines(self, tmp_path):
        """Test handling lines shorter than 80 characters."""
        # Some PDB files have lines shorter than spec (missing element/charge)
        pdb_content = textwrap.dedent("""\
ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00 10.00
ATOM      2  CA  GLY A   2       4.000   5.000   6.000  1.00 11.00
END
""")
        file_path = tmp_path / "short.pdb"
        file_path.write_text(pdb_content)

        pdb = Pdb()
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 2
        # Element should be empty or None for short lines
        elements = pa_table["element"].to_pylist()
        assert all(e in ["", None] for e in elements)

    def test_pdb_ent_extension(self, tmp_path):
        """Test loading .ent files (PDB entry format)."""
        pdb_content = textwrap.dedent("""\
ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00 10.00           C
END
""")
        file_path = tmp_path / "structure.ent"
        file_path.write_text(pdb_content)

        pdb = Pdb()
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 1

    def test_pdb_negative_coordinates(self, tmp_path):
        """Test parsing negative coordinates."""
        pdb_content = textwrap.dedent("""\
ATOM      1  N   ALA A   1     -10.123 -20.456 -30.789  1.00 10.00           N
ATOM      2  CA  ALA A   1     -40.111  50.222 -60.333  1.00 11.00           C
END
""")
        file_path = tmp_path / "negative.pdb"
        file_path.write_text(pdb_content)

        pdb = Pdb(columns=["x", "y", "z"])
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 2
        x_vals = pa_table["x"].to_pylist()
        y_vals = pa_table["y"].to_pylist()
        z_vals = pa_table["z"].to_pylist()

        assert abs(x_vals[0] - (-10.123)) < 0.001
        assert abs(y_vals[0] - (-20.456)) < 0.001
        assert abs(z_vals[0] - (-30.789)) < 0.001
        assert abs(x_vals[1] - (-40.111)) < 0.001
        assert abs(y_vals[1] - 50.222) < 0.001
        assert abs(z_vals[1] - (-60.333)) < 0.001

    def test_pdb_all_columns(self, tmp_path):
        """Test loading all available columns."""
        pdb_content = textwrap.dedent("""\
ATOM      1  N  AALA A   1A      1.000   2.000   3.000  0.50 10.00           N1+
END
""")
        file_path = tmp_path / "allcols.pdb"
        file_path.write_text(pdb_content)

        all_columns = list(PDB_COLUMN_TYPES.keys())
        pdb = Pdb(columns=all_columns)
        generator = pdb._generate_tables([[str(file_path)]])
        pa_table = pa.concat_tables([table for _, table in generator])

        assert pa_table.num_rows == 1
        assert set(pa_table.column_names) == set(all_columns)

        # Verify specific values
        row = {col: pa_table[col][0].as_py() for col in all_columns}
        assert row["record_type"] == "ATOM"
        assert row["atom_serial"] == 1
        assert row["atom_name"] == "N"
        assert row["alt_loc"] == "A"
        assert row["residue_name"] == "ALA"
        assert row["chain_id"] == "A"
        assert row["residue_seq"] == 1
        assert row["insertion_code"] == "A"
        assert abs(row["x"] - 1.0) < 0.001
        assert abs(row["y"] - 2.0) < 0.001
        assert abs(row["z"] - 3.0) < 0.001
        assert abs(row["occupancy"] - 0.5) < 0.001
        assert abs(row["temp_factor"] - 10.0) < 0.001
        assert row["element"] == "N"
        assert row["charge"] == "1+"
