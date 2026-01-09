"""Tests for PdbFolder - folder-based PDB structure loader."""

import shutil
import textwrap

import pytest

from datasets import ClassLabel, DownloadManager, ProteinStructure
from datasets.data_files import DataFilesDict, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.pdb.pdb import PdbFolder, PdbFolderConfig


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "pdb_cache_dir")


@pytest.fixture
def data_files_with_labels_no_metadata(tmp_path, pdb_file):
    data_dir = tmp_path / "pdb_data_dir_with_labels"
    data_dir.mkdir(parents=True, exist_ok=True)

    subdir_class_0 = data_dir / "enzyme"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "receptor"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    shutil.copy(pdb_file, subdir_class_0 / "structure1.pdb")
    shutil.copy(pdb_file, subdir_class_1 / "structure2.pdb")

    data_files_with_labels_no_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )

    return data_files_with_labels_no_metadata


@pytest.fixture
def file_with_metadata(tmp_path, pdb_file):
    filename = tmp_path / "structure.pdb"
    shutil.copy(pdb_file, filename)
    metadata_filename = tmp_path / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "structure.pdb", "resolution": 2.5, "method": "X-ray"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)
    return str(filename), str(metadata_filename)


@pytest.fixture
def data_files_with_one_split_and_metadata(tmp_path, pdb_file):
    data_dir = tmp_path / "pdb_data_dir_with_metadata_one_split"
    data_dir.mkdir(parents=True, exist_ok=True)

    filename = data_dir / "structure1.pdb"
    shutil.copy(pdb_file, filename)
    filename2 = data_dir / "structure2.ent"
    shutil.copy(pdb_file, filename2)

    metadata_filename = data_dir / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "structure1.pdb", "resolution": 2.5}
        {"file_name": "structure2.ent", "resolution": 1.8}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)
    data_files_with_one_split_and_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )
    assert len(data_files_with_one_split_and_metadata) == 1
    assert len(data_files_with_one_split_and_metadata["train"]) == 3
    return data_files_with_one_split_and_metadata


@pytest.fixture
def data_files_with_two_splits_and_metadata(tmp_path, pdb_file):
    data_dir = tmp_path / "pdb_data_dir_with_metadata_two_splits"
    data_dir.mkdir(parents=True, exist_ok=True)
    train_dir = data_dir / "train"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir = data_dir / "test"
    test_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy(pdb_file, train_dir / "train_structure1.pdb")
    shutil.copy(pdb_file, train_dir / "train_structure2.ent")
    shutil.copy(pdb_file, test_dir / "test_structure1.pdb")

    train_metadata_filename = train_dir / "metadata.jsonl"
    train_metadata = textwrap.dedent(
        """\
        {"file_name": "train_structure1.pdb", "resolution": 2.5}
        {"file_name": "train_structure2.ent", "resolution": 1.8}
        """
    )
    with open(train_metadata_filename, "w", encoding="utf-8") as f:
        f.write(train_metadata)
    test_metadata_filename = test_dir / "metadata.jsonl"
    test_metadata = textwrap.dedent(
        """\
        {"file_name": "test_structure1.pdb", "resolution": 3.0}
        """
    )
    with open(test_metadata_filename, "w", encoding="utf-8") as f:
        f.write(test_metadata)
    data_files_with_two_splits_and_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )
    assert len(data_files_with_two_splits_and_metadata) == 2
    assert len(data_files_with_two_splits_and_metadata["train"]) == 3
    assert len(data_files_with_two_splits_and_metadata["test"]) == 2
    return data_files_with_two_splits_and_metadata


def test_config_valid_name():
    config = PdbFolderConfig(name="valid_name")
    assert config.name == "valid_name"


def test_inferring_labels_from_data_dirs(data_files_with_labels_no_metadata, cache_dir):
    pdbfolder = PdbFolder(data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False)
    gen_kwargs = pdbfolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    assert pdbfolder.info.features["label"] == ClassLabel(names=["enzyme", "receptor"])
    generator = pdbfolder._generate_examples(**gen_kwargs)
    assert all(example["label"] in {"enzyme", "receptor"} for _, example in generator)


@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_labels(data_files_with_labels_no_metadata, drop_metadata, drop_labels, cache_dir):
    pdbfolder = PdbFolder(
        data_files=data_files_with_labels_no_metadata,
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        cache_dir=cache_dir,
    )
    gen_kwargs = pdbfolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # removing labels explicitly requires drop_labels=True
    assert gen_kwargs["add_labels"] is not bool(drop_labels)
    assert gen_kwargs["add_metadata"] is False
    generator = pdbfolder._generate_examples(**gen_kwargs)
    if not drop_labels:
        assert all(
            example.keys() == {"structure", "label"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"structure"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_metadata(file_with_metadata, drop_metadata, drop_labels, cache_dir):
    file, metadata_file = file_with_metadata
    pdbfolder = PdbFolder(
        data_files=[file, metadata_file],
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        cache_dir=cache_dir,
    )
    gen_kwargs = pdbfolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # since the dataset has metadata, removing the metadata explicitly requires drop_metadata=True
    assert gen_kwargs["add_metadata"] is not bool(drop_metadata)
    # since the dataset has metadata, adding the labels explicitly requires drop_labels=False
    assert gen_kwargs["add_labels"] is False
    generator = pdbfolder._generate_examples(**gen_kwargs)
    expected_columns = {"structure"}
    if gen_kwargs["add_metadata"]:
        expected_columns.update({"resolution", "method"})
    if gen_kwargs["add_labels"]:
        expected_columns.add("label")
    result = [example for _, example in generator]
    assert len(result) == 1
    example = result[0]
    assert example.keys() == expected_columns
    for column in expected_columns:
        assert example[column] is not None


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("n_splits", [1, 2])
def test_data_files_with_metadata_and_splits(
    streaming, cache_dir, n_splits, data_files_with_one_split_and_metadata, data_files_with_two_splits_and_metadata
):
    data_files = data_files_with_one_split_and_metadata if n_splits == 1 else data_files_with_two_splits_and_metadata
    pdbfolder = PdbFolder(
        data_files=data_files,
        cache_dir=cache_dir,
    )
    download_manager = StreamingDownloadManager() if streaming else DownloadManager()
    generated_splits = pdbfolder._split_generators(download_manager)
    for (split, files), generated_split in zip(data_files.items(), generated_splits):
        assert split == generated_split.name
        expected_num_of_examples = len(files) - 1
        generated_examples = list(pdbfolder._generate_examples(**generated_split.gen_kwargs))
        assert len(generated_examples) == expected_num_of_examples
        assert len({example["structure"] for _, example in generated_examples}) == expected_num_of_examples
        assert len({example["resolution"] for _, example in generated_examples}) == expected_num_of_examples
        assert all(example["resolution"] is not None for _, example in generated_examples)


def test_structure_content_decoded(data_files_with_labels_no_metadata, cache_dir):
    pdbfolder = PdbFolder(
        data_files=data_files_with_labels_no_metadata,
        cache_dir=cache_dir,
        drop_labels=True,
    )
    pdbfolder.download_and_prepare()
    dataset = list(pdbfolder.as_dataset()["train"])

    for example in dataset:
        content = example["structure"]
        assert isinstance(content, str)
        # PDB files should contain standard PDB format markers
        assert "HEADER" in content or "ATOM" in content


def test_extensions_supported():
    expected_extensions = [".pdb", ".ent"]
    assert all(ext in PdbFolder.EXTENSIONS for ext in expected_extensions)
    # Should NOT contain mmCIF extensions
    assert ".cif" not in PdbFolder.EXTENSIONS
    assert ".mmcif" not in PdbFolder.EXTENSIONS


def test_base_feature_is_protein_structure():
    assert PdbFolder.BASE_FEATURE == ProteinStructure


def test_base_column_name():
    assert PdbFolder.BASE_COLUMN_NAME == "structure"
