import shutil
import textwrap
from pathlib import Path

import pytest

from datasets import ClassLabel, DownloadManager, Features, Video
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesDict, DataFilesList, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.videofolder.videofolder import VideoFolder, VideoFolderConfig


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "videofolder_cache_dir")


@pytest.fixture
def video_file_path():
    return Path(__file__).resolve().parents[1] / "features" / "data" / "test_video_66x50.mov"


@pytest.fixture
def data_files_with_labels_no_metadata(tmp_path, video_file_path):
    data_dir = tmp_path / "data_files_with_labels_no_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "cat"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "dog"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    video_filename = subdir_class_0 / "video_cat.mov"
    shutil.copyfile(video_file_path, video_filename)
    video_filename2 = subdir_class_1 / "video_dog.mov"
    shutil.copyfile(video_file_path, video_filename2)

    data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    return data_files


@pytest.fixture
def video_file_with_metadata(tmp_path, video_file_path):
    video_filename = tmp_path / "video.mov"
    shutil.copyfile(video_file_path, video_filename)
    metadata_filename = tmp_path / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "video.mov", "caption": "A short video"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)
    return str(video_filename), str(metadata_filename)


@pytest.fixture
def data_files_with_zip_archives(tmp_path, video_file_path):
    data_dir = tmp_path / "videofolder_data_dir_with_zip_archives"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = data_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    subdir = archive_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    video_filename = archive_dir / "video.mov"
    shutil.copyfile(video_file_path, video_filename)
    video_filename2 = subdir / "video2.mov"
    shutil.copyfile(video_file_path, video_filename2)

    metadata_filename = archive_dir / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "video.mov", "caption": "First video"}
        {"file_name": "subdir/video2.mov", "caption": "Second video"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    shutil.make_archive(archive_dir, "zip", archive_dir)
    shutil.rmtree(str(archive_dir))

    data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    assert len(data_files) == 1
    assert len(data_files["train"]) == 1
    return data_files


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = VideoFolderConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = VideoFolderConfig(name="name", data_files=data_files)


def test_generate_examples_with_labels(data_files_with_labels_no_metadata, cache_dir):
    videofolder = VideoFolder(data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False)
    gen_kwargs = videofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    assert videofolder.info.features == Features({"video": Video(), "label": ClassLabel(names=["cat", "dog"])})
    generator = videofolder._generate_examples(**gen_kwargs)
    assert all(example["label"] in {"cat", "dog"} for _, example in generator)


def test_generate_examples_with_metadata(video_file_with_metadata, cache_dir):
    video_file, metadata_file = video_file_with_metadata
    videofolder = VideoFolder(data_files=[video_file, metadata_file], cache_dir=cache_dir)
    gen_kwargs = videofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generated_examples = [example for _, example in videofolder._generate_examples(**gen_kwargs)]
    assert len(generated_examples) == 1
    assert generated_examples[0].keys() == {"video", "caption"}
    assert generated_examples[0]["video"].endswith("video.mov")
    assert generated_examples[0]["caption"] == "A short video"


@pytest.mark.parametrize("streaming", [False, True])
def test_data_files_with_metadata_and_archives(streaming, cache_dir, data_files_with_zip_archives):
    videofolder = VideoFolder(data_files=data_files_with_zip_archives, cache_dir=cache_dir)
    download_manager = StreamingDownloadManager() if streaming else DownloadManager()
    generated_splits = videofolder._split_generators(download_manager)
    for (split, files), generated_split in zip(data_files_with_zip_archives.items(), generated_splits):
        assert split == generated_split.name
        num_of_archives = len(files)
        expected_num_of_examples = 2 * num_of_archives
        generated_examples = list(videofolder._generate_examples(**generated_split.gen_kwargs))
        assert len(generated_examples) == expected_num_of_examples
        assert len({example["video"] for _, example in generated_examples}) == expected_num_of_examples
        assert len({example["caption"] for _, example in generated_examples}) == expected_num_of_examples
