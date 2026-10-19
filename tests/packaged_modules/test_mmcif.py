"""Tests for MmcifFolder - folder-based mmCIF structure loader."""

import os
import shutil
import textwrap
from pathlib import Path

import pytest

from datasets import BioStructure, ClassLabel, DownloadManager, Value, config, load_from_disk
from datasets.data_files import DataFilesDict, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.mmcif.mmcif import MmcifFolder, MmcifFolderConfig


require_biopython = pytest.mark.skipif(
    not __import__("datasets").config.BIOPYTHON_AVAILABLE, reason="biopython is not installed"
)


def _normalize_path(path):
    # Compare local paths independently of platform-specific separators and case.
    return os.path.normcase(os.path.normpath(path))


def _metadata_string_feature(feature, metadata_file):
    # CSV string width depends on the pandas version used for inference.
    if Path(metadata_file).suffix == ".csv":
        assert feature in (Value("string"), Value("large_string"))
    else:
        assert feature == Value("string")
    return feature


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "mmcif_cache_dir")


@pytest.fixture
def data_files_with_labels_no_metadata(tmp_path, cif_file):
    data_dir = tmp_path / "mmcif_data_dir_with_labels"
    data_dir.mkdir(parents=True, exist_ok=True)

    subdir_class_0 = data_dir / "enzyme"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "receptor"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    shutil.copy(cif_file, subdir_class_0 / "structure1.cif")
    shutil.copy(cif_file, subdir_class_1 / "structure2.cif")

    data_files_with_labels_no_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )

    return data_files_with_labels_no_metadata


@pytest.fixture(params=["jsonl", "csv"])
def file_with_metadata(tmp_path, cif_file, request):
    filename = tmp_path / "structure.cif"
    shutil.copy(cif_file, filename)
    metadata_filename = tmp_path / f"metadata.{request.param}"
    metadata = (
        '{"file_name": "structure.cif", "resolution": 2.5, "method": "X-ray"}\n'
        if request.param == "jsonl"
        else "file_name,resolution,method\nstructure.cif,2.5,X-ray\n"
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)
    return str(filename), str(metadata_filename)


@pytest.fixture
def data_files_with_one_split_and_metadata(tmp_path, cif_file):
    data_dir = tmp_path / "mmcif_data_dir_with_metadata_one_split"
    data_dir.mkdir(parents=True, exist_ok=True)

    filename = data_dir / "structure1.cif"
    shutil.copy(cif_file, filename)
    filename2 = data_dir / "structure2.mmcif"
    shutil.copy(cif_file, filename2)

    metadata_filename = data_dir / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "structure1.cif", "resolution": 2.5}
        {"file_name": "structure2.mmcif", "resolution": 1.8}
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
def data_files_with_two_splits_and_metadata(tmp_path, cif_file):
    data_dir = tmp_path / "mmcif_data_dir_with_metadata_two_splits"
    data_dir.mkdir(parents=True, exist_ok=True)
    train_dir = data_dir / "train"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir = data_dir / "test"
    test_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy(cif_file, train_dir / "train_structure1.cif")
    shutil.copy(cif_file, train_dir / "train_structure2.mmcif")
    shutil.copy(cif_file, test_dir / "test_structure1.cif")

    train_metadata_filename = train_dir / "metadata.jsonl"
    train_metadata = textwrap.dedent(
        """\
        {"file_name": "train_structure1.cif", "resolution": 2.5}
        {"file_name": "train_structure2.mmcif", "resolution": 1.8}
        """
    )
    with open(train_metadata_filename, "w", encoding="utf-8") as f:
        f.write(train_metadata)
    test_metadata_filename = test_dir / "metadata.jsonl"
    test_metadata = textwrap.dedent(
        """\
        {"file_name": "test_structure1.cif", "resolution": 3.0}
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
    config = MmcifFolderConfig(name="valid_name")
    assert config.name == "valid_name"


def test_inferring_labels_from_data_dirs(data_files_with_labels_no_metadata, cache_dir):
    mmciffolder = MmcifFolder(data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False)
    gen_kwargs = mmciffolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    assert mmciffolder.info.features == {
        "structure": BioStructure(format="mmcif"),
        "label": ClassLabel(names=["enzyme", "receptor"]),
    }
    generator = mmciffolder._generate_examples(**gen_kwargs)
    assert all(example["label"] in {"enzyme", "receptor"} for _, example in generator)


@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_labels(data_files_with_labels_no_metadata, drop_metadata, drop_labels, cache_dir):
    mmciffolder = MmcifFolder(
        data_files=data_files_with_labels_no_metadata,
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        cache_dir=cache_dir,
    )
    gen_kwargs = mmciffolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # removing labels explicitly requires drop_labels=True
    assert gen_kwargs["add_labels"] is not bool(drop_labels)
    assert gen_kwargs["add_metadata"] is False
    expected_features = {"structure": BioStructure(format="mmcif")}
    if not drop_labels:
        expected_features["label"] = ClassLabel(names=["enzyme", "receptor"])
    assert mmciffolder.info.features == expected_features
    generator = mmciffolder._generate_examples(**gen_kwargs)
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
    mmciffolder = MmcifFolder(
        data_files=[file, metadata_file],
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        cache_dir=cache_dir,
    )
    gen_kwargs = mmciffolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # since the dataset has metadata, removing the metadata explicitly requires drop_metadata=True
    assert gen_kwargs["add_metadata"] is not bool(drop_metadata)
    # since the dataset has metadata, adding the labels explicitly requires drop_labels=False
    assert gen_kwargs["add_labels"] is False
    generator = mmciffolder._generate_examples(**gen_kwargs)
    expected_features = {"structure": BioStructure(format="mmcif")}
    if gen_kwargs["add_metadata"]:
        expected_features.update(
            {
                "resolution": Value("float64"),
                "method": _metadata_string_feature(mmciffolder.info.features["method"], metadata_file),
            }
        )
    assert mmciffolder.info.features == expected_features
    result = [example for _, example in generator]
    assert len(result) == 1
    example = result[0]
    example["structure"] = _normalize_path(example["structure"])
    expected_example = {"structure": _normalize_path(file)}
    if gen_kwargs["add_metadata"]:
        expected_example.update({"resolution": 2.5, "method": "X-ray"})
    assert example == expected_example


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("n_splits", [1, 2])
def test_data_files_with_metadata_and_splits(
    streaming, cache_dir, n_splits, data_files_with_one_split_and_metadata, data_files_with_two_splits_and_metadata
):
    data_files = data_files_with_one_split_and_metadata if n_splits == 1 else data_files_with_two_splits_and_metadata
    mmciffolder = MmcifFolder(
        data_files=data_files,
        cache_dir=cache_dir,
    )
    download_manager = StreamingDownloadManager() if streaming else DownloadManager()
    generated_splits = mmciffolder._split_generators(download_manager)
    expected_features = {"structure": BioStructure(format="mmcif"), "resolution": Value("float64")}
    assert mmciffolder.info.features == expected_features
    for (split, files), generated_split in zip(data_files.items(), generated_splits):
        assert split == generated_split.name
        expected_num_of_examples = len(files) - 1
        generated_examples = list(mmciffolder._generate_examples(**generated_split.gen_kwargs))
        assert len(generated_examples) == expected_num_of_examples
        assert (
            len({_normalize_path(example["structure"]) for _, example in generated_examples})
            == expected_num_of_examples
        )
        assert len({example["resolution"] for _, example in generated_examples}) == expected_num_of_examples
        assert all(example["resolution"] is not None for _, example in generated_examples)

    if streaming:
        dataset = mmciffolder.as_streaming_dataset()
    else:
        mmciffolder.download_and_prepare()
        dataset = mmciffolder.as_dataset()
    for split, files in data_files.items():
        assert dataset[split].features == expected_features
        rows = list(dataset[split].cast_column("structure", BioStructure(format="mmcif", decode=False)))
        assert len(rows) == len(files) - 1
        assert {_normalize_path(row["structure"]["path"]) for row in rows} == {
            _normalize_path(file) for file in files if Path(file).suffix in {".cif", ".mmcif"}
        }
        assert all(row["structure"]["bytes"] is None for row in rows)
        assert [row["resolution"] for row in rows] == ([3.0] if split == "test" else [2.5, 1.8])


@require_biopython
@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("drop_labels", [False, True])
def test_structure_content_decoded(data_files_with_labels_no_metadata, cache_dir, streaming, drop_labels, cif_file):
    from Bio.PDB.PDBExceptions import PDBConstructionException
    from Bio.PDB.Structure import Structure

    # Omitting the loader's format would select the PDB parser, which rejects this fixture.
    with pytest.raises(PDBConstructionException, match="Invalid or missing coordinate"):
        BioStructure(format="pdb").decode_example({"path": cif_file, "bytes": None})

    mmciffolder = MmcifFolder(
        data_files=data_files_with_labels_no_metadata,
        cache_dir=cache_dir,
        drop_labels=drop_labels,
    )
    if streaming:
        dataset = mmciffolder.as_streaming_dataset(split="train")
    else:
        mmciffolder.download_and_prepare()
        dataset = mmciffolder.as_dataset(split="train")
    expected_features = {"structure": BioStructure(format="mmcif")}
    if not drop_labels:
        expected_features["label"] = ClassLabel(names=["enzyme", "receptor"])
    assert dataset.features == expected_features

    structures = [example["structure"] for example in dataset]
    assert [structure.id for structure in structures] == ["structure1", "structure2"]
    for structure in structures:
        assert isinstance(structure, Structure)
        assert len(list(structure.get_atoms())) == 9


def test_structure_embedded_bytes_match_file(file_with_metadata, cache_dir, tmp_path):
    file, metadata_file = file_with_metadata
    mmciffolder = MmcifFolder(data_files=[file, metadata_file], cache_dir=cache_dir)
    mmciffolder.download_and_prepare()
    dataset = mmciffolder.as_dataset(split="train")
    saved_path = tmp_path / "embedded"
    dataset.save_to_disk(saved_path)
    dataset = load_from_disk(saved_path)
    assert dataset.features == {
        "structure": BioStructure(format="mmcif"),
        "resolution": Value("float64"),
        "method": _metadata_string_feature(dataset.features["method"], metadata_file),
    }
    dataset = dataset.cast_column("structure", BioStructure(format="mmcif", decode=False))
    [row] = list(dataset)
    assert row["structure"]["bytes"] == Path(file).read_bytes()
    assert row["structure"]["path"] == Path(file).name
    assert row["resolution"] == 2.5
    assert row["method"] == "X-ray"


@pytest.mark.parametrize("streaming", [False, True])
def test_structure_without_biopython(data_files_with_labels_no_metadata, cache_dir, monkeypatch, streaming):
    monkeypatch.setattr(config, "BIOPYTHON_AVAILABLE", False)
    mmciffolder = MmcifFolder(
        data_files=data_files_with_labels_no_metadata,
        cache_dir=cache_dir,
        drop_labels=True,
    )
    if streaming:
        dataset = mmciffolder.as_streaming_dataset(split="train")
    else:
        mmciffolder.download_and_prepare()
        dataset = mmciffolder.as_dataset(split="train")
    assert dataset.features == {"structure": BioStructure(format="mmcif")}
    with pytest.raises(ImportError, match="biopython"):
        next(iter(dataset))

    dataset = dataset.cast_column("structure", BioStructure(format="mmcif", decode=False))
    rows = list(dataset)
    for row in rows:
        row["structure"]["path"] = _normalize_path(row["structure"]["path"])
    assert rows == [
        {"structure": {"bytes": None, "path": _normalize_path(path)}}
        for path in data_files_with_labels_no_metadata["train"]
    ]


@pytest.fixture
def file_with_hetatm(tmp_path):
    data_dir = tmp_path / "mmcif_hetatm"
    data_dir.mkdir(parents=True, exist_ok=True)
    structure = data_dir / "structure.cif"
    structure.write_text(
        textwrap.dedent("""\
            data_TEST
            loop_
            _atom_site.group_PDB
            _atom_site.id
            _atom_site.type_symbol
            _atom_site.label_atom_id
            _atom_site.label_alt_id
            _atom_site.label_comp_id
            _atom_site.label_asym_id
            _atom_site.label_seq_id
            _atom_site.pdbx_PDB_ins_code
            _atom_site.Cartn_x
            _atom_site.Cartn_y
            _atom_site.Cartn_z
            _atom_site.occupancy
            _atom_site.B_iso_or_equiv
            _atom_site.auth_asym_id
            _atom_site.auth_seq_id
            _atom_site.pdbx_PDB_model_num
            ATOM   1 N N  . ALA A 1 ? 0.000 0.000 0.000 1.00 20.00 A 1 1
            ATOM   2 C CA . ALA A 1 ? 1.458 0.000 0.000 1.00 20.00 A 1 1
            HETATM 3 O O  . HOH A 2 ? 5.000 5.000 5.000 1.00 30.00 A 2 1
            #
            """)
    )
    return DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())


@require_biopython
def test_structure_keeps_hetatm(file_with_hetatm, cache_dir):
    builder = MmcifFolder(data_files=file_with_hetatm, cache_dir=cache_dir, drop_labels=True)
    builder.download_and_prepare()
    [row] = list(builder.as_dataset()["train"])
    structure = row["structure"]
    assert len(list(structure.get_atoms())) == 3
    assert [residue.resname for residue in structure.get_residues()] == ["ALA", "HOH"]


def test_extensions_supported():
    expected_extensions = [".cif", ".mmcif"]
    assert all(ext in MmcifFolder.EXTENSIONS for ext in expected_extensions)
    # Should NOT contain PDB extensions
    assert ".pdb" not in MmcifFolder.EXTENSIONS
    assert ".ent" not in MmcifFolder.EXTENSIONS


def test_base_feature_is_bio_structure():
    assert MmcifFolder.BASE_FEATURE == BioStructure


def test_base_column_name():
    assert MmcifFolder.BASE_COLUMN_NAME == "structure"
