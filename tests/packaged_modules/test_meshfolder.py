import shutil
import textwrap

import pytest

from datasets import ClassLabel, Features, Mesh
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesDict, get_data_patterns
from datasets.packaged_modules.meshfolder.meshfolder import MeshFolder, MeshFolderConfig


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "meshfolder_cache_dir")


@pytest.fixture
def data_files_with_labels_no_metadata(tmp_path, mesh_file):
    data_dir = tmp_path / "data_files_with_labels_no_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "chair"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "table"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    mesh_filename = subdir_class_0 / "mesh_chair.glb"
    shutil.copyfile(mesh_file, mesh_filename)
    mesh_filename2 = subdir_class_1 / "mesh_table.glb"
    shutil.copyfile(mesh_file, mesh_filename2)

    data_files_with_labels_no_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )

    return data_files_with_labels_no_metadata


@pytest.fixture
def mesh_file_with_metadata(tmp_path, mesh_file):
    mesh_filename = tmp_path / "mesh_file.glb"
    shutil.copyfile(mesh_file, mesh_filename)
    mesh_metadata_filename = tmp_path / "metadata.jsonl"
    mesh_metadata = textwrap.dedent(
        """\
        {"file_name": "mesh_file.glb", "text": "Mesh description"}
        """
    )
    with open(mesh_metadata_filename, "w", encoding="utf-8") as f:
        f.write(mesh_metadata)
    return str(mesh_filename), str(mesh_metadata_filename)


def test_meshfolder_config_and_extensions():
    # Verify extensions
    assert MeshFolder.EXTENSIONS == [".glb", ".ply", ".stl"]
    assert MeshFolder.BASE_FEATURE == Mesh
    assert MeshFolder.BASE_COLUMN_NAME == "mesh"


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = MeshFolderConfig(name="name-with-*-invalid-character")


def test_generate_examples_with_labels(data_files_with_labels_no_metadata, cache_dir):
    # there are no metadata.jsonl files in this test case
    meshfolder = MeshFolder(data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False)
    meshfolder.download_and_prepare()
    assert meshfolder.info.features == Features({"mesh": Mesh(), "label": ClassLabel(names=["chair", "table"])})
    dataset = list(meshfolder.as_dataset()["train"])
    label_feature = meshfolder.info.features["label"]

    assert dataset[0]["label"] == label_feature._str2int["chair"]
    assert dataset[1]["label"] == label_feature._str2int["table"]


@pytest.mark.parametrize("streaming", [False, True])
def test_data_files_with_metadata_and_single_split(streaming, cache_dir, mesh_file_with_metadata):
    mesh_file, mesh_metadata_file = mesh_file_with_metadata
    meshfolder = MeshFolder(data_files={"train": [mesh_file, mesh_metadata_file]}, cache_dir=cache_dir)
    meshfolder.download_and_prepare()
    dataset = meshfolder.as_streaming_dataset()["train"] if streaming else meshfolder.as_dataset()["train"]

    item = next(iter(dataset)) if streaming else dataset[0]
    assert "mesh" in item
    assert item["text"] == "Mesh description"
