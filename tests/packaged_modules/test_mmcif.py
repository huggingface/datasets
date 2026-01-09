"""Tests for MmcifFolder packaged module.

Tests the folder-based mmCIF loader that follows the one-row-per-structure pattern
(similar to ImageFolder pattern).
"""

import textwrap

import pyarrow as pa
import pytest

from datasets import ClassLabel, Dataset, DatasetDict, ProteinStructure, load_dataset
from datasets.packaged_modules.mmcif.mmcif import MmcifFolder


# Test data - minimal mmCIF format
MMCIF_CONTENT = """\
data_TEST
#
_entry.id   TEST
#
_cell.length_a           50.000
_cell.length_b           50.000
_cell.length_c           50.000
_cell.angle_alpha        90.00
_cell.angle_beta         90.00
_cell.angle_gamma        90.00
#
loop_
_atom_site.group_PDB
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
ATOM   1  N  N   ALA A 1  0.000   0.000   0.000  1.00 20.00
ATOM   2  C  CA  ALA A 1  1.458   0.000   0.000  1.00 20.00
#
"""


@pytest.fixture
def mmcif_file(tmp_path):
    """Create a single mmCIF test file."""
    path = tmp_path / "structure.cif"
    path.write_text(MMCIF_CONTENT)
    return str(path)


@pytest.fixture
def mmcif_file_mmcif_ext(tmp_path):
    """Create a single mmCIF test file with .mmcif extension."""
    path = tmp_path / "structure.mmcif"
    path.write_text(MMCIF_CONTENT)
    return str(path)


@pytest.fixture
def mmcif_data_dir(tmp_path):
    """Create a directory with mmCIF files."""
    data_dir = tmp_path / "mmcif_data"
    data_dir.mkdir()

    # Create several mmCIF files
    for i in range(3):
        (data_dir / f"structure_{i}.cif").write_text(MMCIF_CONTENT.replace("TEST", f"TEST_{i}"))

    return str(data_dir)


@pytest.fixture
def mmcif_data_dir_with_labels(tmp_path):
    """Create directories with label-based structure."""
    data_dir = tmp_path / "mmcif_labeled"

    # Create labeled directories (like ImageFolder pattern)
    for label in ["enzymes", "receptors"]:
        label_dir = data_dir / label
        label_dir.mkdir(parents=True)
        for i in range(2):
            content = MMCIF_CONTENT.replace("TEST", f"{label.upper()}_{i}")
            (label_dir / f"{label}_{i}.cif").write_text(content)

    return str(data_dir)


@pytest.fixture
def mmcif_data_dir_with_metadata(tmp_path):
    """Create directory with metadata.csv file."""
    data_dir = tmp_path / "mmcif_metadata"
    data_dir.mkdir()

    # Create mmCIF files
    for i in range(3):
        (data_dir / f"structure_{i}.cif").write_text(MMCIF_CONTENT.replace("TEST", f"META_{i}"))

    # Create metadata.csv
    metadata = textwrap.dedent("""\
        file_name,resolution,method
        structure_0.cif,2.5,X-RAY
        structure_1.cif,1.8,CRYO-EM
        structure_2.cif,3.0,NMR
    """)
    (data_dir / "metadata.csv").write_text(metadata)

    return str(data_dir)


class TestMmcifFolderConfig:
    """Tests for MmcifFolderConfig."""

    def test_config_defaults(self):
        """Test default config values."""
        builder = MmcifFolder(data_dir=".")
        assert builder.config.drop_labels is None
        assert builder.config.drop_metadata is None

    def test_config_custom_values(self):
        """Test custom config values."""
        builder = MmcifFolder(data_dir=".", drop_labels=True, drop_metadata=True)
        assert builder.config.drop_labels is True
        assert builder.config.drop_metadata is True


class TestMmcifFolderBuilder:
    """Tests for MmcifFolder builder properties."""

    def test_base_feature(self):
        """Test BASE_FEATURE is ProteinStructure."""
        assert MmcifFolder.BASE_FEATURE == ProteinStructure

    def test_base_column_name(self):
        """Test BASE_COLUMN_NAME is 'structure'."""
        assert MmcifFolder.BASE_COLUMN_NAME == "structure"

    def test_extensions(self):
        """Test supported extensions."""
        assert ".cif" in MmcifFolder.EXTENSIONS
        assert ".mmcif" in MmcifFolder.EXTENSIONS
        assert len(MmcifFolder.EXTENSIONS) == 2


class TestMmcifFolderLoading:
    """Tests for loading mmCIF datasets."""

    def test_load_single_file(self, mmcif_file):
        """Test loading a single mmCIF file."""
        dataset = load_dataset("mmcif", data_files=mmcif_file, split="train")
        assert len(dataset) == 1
        assert "structure" in dataset.column_names

    def test_load_mmcif_extension(self, mmcif_file_mmcif_ext):
        """Test loading .mmcif extension."""
        dataset = load_dataset("mmcif", data_files=mmcif_file_mmcif_ext, split="train")
        assert len(dataset) == 1
        assert "structure" in dataset.column_names

    def test_load_directory(self, mmcif_data_dir):
        """Test loading from directory."""
        dataset = load_dataset("mmcif", data_dir=mmcif_data_dir, split="train")
        assert len(dataset) == 3
        assert "structure" in dataset.column_names

    def test_load_with_labels(self, mmcif_data_dir_with_labels):
        """Test loading with folder-based labels."""
        dataset = load_dataset("mmcif", data_dir=mmcif_data_dir_with_labels, split="train")
        assert len(dataset) == 4
        assert "structure" in dataset.column_names
        assert "label" in dataset.column_names
        # Check labels are ClassLabel
        assert isinstance(dataset.features["label"], ClassLabel)

    def test_load_drop_labels(self, mmcif_data_dir_with_labels):
        """Test dropping labels."""
        dataset = load_dataset(
            "mmcif", data_dir=mmcif_data_dir_with_labels, split="train", drop_labels=True
        )
        assert len(dataset) == 4
        assert "structure" in dataset.column_names
        assert "label" not in dataset.column_names

    def test_load_with_metadata(self, mmcif_data_dir_with_metadata):
        """Test loading with metadata.csv."""
        dataset = load_dataset("mmcif", data_dir=mmcif_data_dir_with_metadata, split="train")
        assert len(dataset) == 3
        assert "structure" in dataset.column_names
        assert "resolution" in dataset.column_names
        assert "method" in dataset.column_names

    def test_load_drop_metadata(self, mmcif_data_dir_with_metadata):
        """Test dropping metadata."""
        dataset = load_dataset(
            "mmcif", data_dir=mmcif_data_dir_with_metadata, split="train", drop_metadata=True
        )
        assert len(dataset) == 3
        assert "structure" in dataset.column_names
        assert "resolution" not in dataset.column_names
        assert "method" not in dataset.column_names


class TestMmcifFolderFeatures:
    """Tests for ProteinStructure feature in mmCIF datasets."""

    def test_feature_type(self, mmcif_file):
        """Test feature type is ProteinStructure."""
        dataset = load_dataset("mmcif", data_files=mmcif_file, split="train")
        assert isinstance(dataset.features["structure"], ProteinStructure)

    def test_structure_content_decoded(self, mmcif_file):
        """Test structure content is accessible when decoded (default)."""
        dataset = load_dataset("mmcif", data_files=mmcif_file, split="train")
        sample = dataset[0]
        structure = sample["structure"]

        # With decode=True (default), structure is a string
        assert isinstance(structure, str)
        assert "data_TEST" in structure
        assert "_atom_site" in structure

    def test_structure_content_undecoded(self, mmcif_file):
        """Test structure content when decode=False."""
        dataset = load_dataset("mmcif", data_files=mmcif_file, split="train")
        # Cast to decode=False to get raw bytes/path dict
        dataset = dataset.cast_column("structure", ProteinStructure(decode=False))
        sample = dataset[0]
        structure = sample["structure"]

        # Should have bytes and path
        assert "bytes" in structure or "path" in structure
        # Path should end with .cif
        if structure["path"]:
            assert structure["path"].endswith(".cif")

    def test_arrow_type(self, mmcif_file):
        """Test underlying Arrow type."""
        dataset = load_dataset("mmcif", data_files=mmcif_file, split="train")
        feature = dataset.features["structure"]
        pa_type = feature.pa_type

        # Should be a struct with bytes and path
        assert pa.types.is_struct(pa_type)
        field_names = [f.name for f in pa_type]
        assert "bytes" in field_names
        assert "path" in field_names


class TestMmcifFolderIntegration:
    """Integration tests for MmcifFolder."""

    def test_dataset_operations(self, mmcif_data_dir):
        """Test common dataset operations."""
        dataset = load_dataset("mmcif", data_dir=mmcif_data_dir, split="train")

        # Test filter
        filtered = dataset.filter(lambda x: True)
        assert len(filtered) == len(dataset)

        # Test select
        selected = dataset.select([0, 1])
        assert len(selected) == 2

        # Test shuffle
        shuffled = dataset.shuffle(seed=42)
        assert len(shuffled) == len(dataset)

    def test_train_test_split(self, mmcif_data_dir):
        """Test train/test split."""
        dataset = load_dataset("mmcif", data_dir=mmcif_data_dir, split="train")
        splits = dataset.train_test_split(test_size=0.3)

        assert isinstance(splits, DatasetDict)
        assert "train" in splits
        assert "test" in splits
        assert len(splits["train"]) + len(splits["test"]) == len(dataset)

    def test_map_function(self, mmcif_data_dir):
        """Test map function on dataset."""
        dataset = load_dataset("mmcif", data_dir=mmcif_data_dir, split="train")

        def extract_entry_id(example):
            # structure is decoded as a string by default
            content = example["structure"]
            # Extract entry ID from mmCIF content
            for line in content.split("\n"):
                if line.startswith("data_"):
                    return {"entry_id": line.replace("data_", "")}
            return {"entry_id": "unknown"}

        mapped = dataset.map(extract_entry_id)
        assert "entry_id" in mapped.column_names

    def test_save_and_load(self, mmcif_data_dir, tmp_path):
        """Test save and reload dataset."""
        dataset = load_dataset("mmcif", data_dir=mmcif_data_dir, split="train")

        # Save to disk
        save_path = tmp_path / "saved_mmcif"
        dataset.save_to_disk(str(save_path))

        # Reload
        reloaded = Dataset.load_from_disk(str(save_path))
        assert len(reloaded) == len(dataset)
        assert reloaded.features["structure"] == dataset.features["structure"]


class TestMmcifFolderEdgeCases:
    """Edge case tests for MmcifFolder."""

    def test_empty_directory(self, tmp_path):
        """Test loading from empty directory raises error."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        with pytest.raises(Exception):  # FileNotFoundError or similar
            load_dataset("mmcif", data_dir=str(empty_dir), split="train")

    def test_mixed_extensions(self, tmp_path):
        """Test directory with both .cif and .mmcif files."""
        data_dir = tmp_path / "mixed"
        data_dir.mkdir()

        (data_dir / "structure1.cif").write_text(MMCIF_CONTENT.replace("TEST", "CIF1"))
        (data_dir / "structure2.mmcif").write_text(MMCIF_CONTENT.replace("TEST", "MMCIF2"))

        dataset = load_dataset("mmcif", data_dir=str(data_dir), split="train")
        assert len(dataset) == 2

    def test_nested_directories(self, tmp_path):
        """Test nested directory structure."""
        data_dir = tmp_path / "nested"
        sub_dir = data_dir / "sub1" / "sub2"
        sub_dir.mkdir(parents=True)

        (data_dir / "root.cif").write_text(MMCIF_CONTENT.replace("TEST", "ROOT"))
        (sub_dir / "nested.cif").write_text(MMCIF_CONTENT.replace("TEST", "NESTED"))

        dataset = load_dataset("mmcif", data_dir=str(data_dir), split="train")
        # Should find files in nested directories
        assert len(dataset) >= 1

    def test_large_mmcif_content(self, tmp_path):
        """Test with larger mmCIF file."""
        data_dir = tmp_path / "large"
        data_dir.mkdir()

        # Create mmCIF with many atoms
        atoms = []
        for i in range(100):
            atoms.append(f"ATOM   {i+1}  N  N   ALA A {i+1}  {i}.000   0.000   0.000  1.00 20.00")

        large_content = MMCIF_CONTENT.replace(
            "ATOM   1  N  N   ALA A 1  0.000   0.000   0.000  1.00 20.00\n"
            "ATOM   2  C  CA  ALA A 1  1.458   0.000   0.000  1.00 20.00",
            "\n".join(atoms)
        )

        (data_dir / "large.cif").write_text(large_content)

        dataset = load_dataset("mmcif", data_dir=str(data_dir), split="train")
        assert len(dataset) == 1

        # Verify content is complete (decoded as string by default)
        content = dataset[0]["structure"]
        assert isinstance(content, str)
        assert "ALA A 100" in content
