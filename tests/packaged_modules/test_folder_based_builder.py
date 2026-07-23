import importlib
import json
import os
import shutil
import textwrap

import pytest

from datasets import ClassLabel, DownloadManager
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesDict, DataFilesList, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.folder_based_builder.folder_based_builder import (
    FolderBasedBuilder,
    FolderBasedBuilderConfig,
    _metadata_reference_is_contained,
)


remote_files = [
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/hallo.txt",
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/hello.txt",
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/class1/bonjour.txt",
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/class1/bonjour2.txt",
]


class DummyFeature:
    pass


class DummyFolderBasedBuilder(FolderBasedBuilder):
    BASE_FEATURE = DummyFeature
    BASE_COLUMN_NAME = "base"
    BUILDER_CONFIG_CLASS = FolderBasedBuilderConfig
    EXTENSIONS = [".txt"]


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "autofolder_cache_dir")


@pytest.fixture
def auto_text_file(text_file):
    return str(text_file)


@pytest.fixture
def data_files_with_labels_no_metadata(tmp_path, auto_text_file):
    data_dir = tmp_path / "data_files_with_labels_no_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "class0"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "class1"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    filename = subdir_class_0 / "file0.txt"
    shutil.copyfile(auto_text_file, filename)
    filename2 = subdir_class_1 / "file1.txt"
    shutil.copyfile(auto_text_file, filename2)

    data_files_with_labels_no_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )

    return data_files_with_labels_no_metadata


@pytest.fixture
def data_files_with_different_levels_no_metadata(tmp_path, auto_text_file):
    data_dir = tmp_path / "data_files_with_different_levels"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "class0"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "subdir" / "class1"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    filename = subdir_class_0 / "file0.txt"
    shutil.copyfile(auto_text_file, filename)
    filename2 = subdir_class_1 / "file1.txt"
    shutil.copyfile(auto_text_file, filename2)

    data_files_with_different_levels = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )

    return data_files_with_different_levels


@pytest.fixture
def data_files_with_one_label_no_metadata(tmp_path, auto_text_file):
    # only one label found = all files in a single dir/in a root dir
    data_dir = tmp_path / "data_files_with_one_label"
    data_dir.mkdir(parents=True, exist_ok=True)

    filename = data_dir / "file0.txt"
    shutil.copyfile(auto_text_file, filename)
    filename2 = data_dir / "file1.txt"
    shutil.copyfile(auto_text_file, filename2)

    data_files_with_one_label = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())

    return data_files_with_one_label


@pytest.fixture
def files_with_labels_and_duplicated_label_key_in_metadata(tmp_path, auto_text_file):
    data_dir = tmp_path / "files_with_labels_and_label_key_in_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "class0"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "class1"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    filename = subdir_class_0 / "file_class0.txt"
    shutil.copyfile(auto_text_file, filename)
    filename2 = subdir_class_1 / "file_class1.txt"
    shutil.copyfile(auto_text_file, filename2)

    metadata_filename = tmp_path / data_dir / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "class0/file_class0.txt", "additional_feature": "First dummy file", "label": "CLASS_0"}
        {"file_name": "class1/file_class1.txt", "additional_feature": "Second dummy file", "label": "CLASS_1"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    return str(filename), str(filename2), str(metadata_filename)


@pytest.fixture
def file_with_metadata(tmp_path, text_file):
    filename = tmp_path / "file.txt"
    shutil.copyfile(text_file, filename)
    metadata_filename = tmp_path / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Dummy file"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)
    return str(filename), str(metadata_filename)


@pytest.fixture
def data_files_with_one_split_and_metadata(tmp_path, auto_text_file):
    data_dir = tmp_path / "autofolder_data_dir_with_metadata_one_split"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir = data_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    filename = data_dir / "file.txt"
    shutil.copyfile(auto_text_file, filename)
    filename2 = data_dir / "file2.txt"
    shutil.copyfile(auto_text_file, filename2)
    filename3 = subdir / "file3.txt"  # in subdir
    shutil.copyfile(auto_text_file, filename3)

    metadata_filename = data_dir / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Dummy file"}
        {"file_name": "file2.txt", "additional_feature": "Second dummy file"}
        {"file_name": "./subdir/file3.txt", "additional_feature": "Third dummy file"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)
    data_files_with_one_split_and_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )
    assert len(data_files_with_one_split_and_metadata) == 1
    assert len(data_files_with_one_split_and_metadata["train"]) == 4
    return data_files_with_one_split_and_metadata


@pytest.fixture
def data_files_with_two_splits_and_metadata(tmp_path, auto_text_file):
    data_dir = tmp_path / "autofolder_data_dir_with_metadata_two_splits"
    data_dir.mkdir(parents=True, exist_ok=True)
    train_dir = data_dir / "train"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir = data_dir / "test"
    test_dir.mkdir(parents=True, exist_ok=True)

    filename = train_dir / "file.txt"  # train
    shutil.copyfile(auto_text_file, filename)
    filename2 = train_dir / "file2.txt"  # train
    shutil.copyfile(auto_text_file, filename2)
    filename3 = test_dir / "file3.txt"  # test
    shutil.copyfile(auto_text_file, filename3)

    train_metadata_filename = train_dir / "metadata.jsonl"
    train_metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Train dummy file"}
        {"file_name": "file2.txt", "additional_feature": "Second train dummy file"}
        """
    )
    with open(train_metadata_filename, "w", encoding="utf-8") as f:
        f.write(train_metadata)
    test_metadata_filename = test_dir / "metadata.jsonl"
    test_metadata = textwrap.dedent(
        """\
        {"file_name": "file3.txt", "additional_feature": "Test dummy file"}
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


@pytest.fixture
def data_files_with_zip_archives(tmp_path, auto_text_file):
    data_dir = tmp_path / "autofolder_data_dir_with_zip_archives"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = data_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    subdir = archive_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    filename = archive_dir / "file.txt"
    shutil.copyfile(auto_text_file, filename)
    filename2 = subdir / "file2.txt"  # in subdir
    shutil.copyfile(auto_text_file, filename2)

    metadata_filename = archive_dir / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Dummy file"}
        {"file_name": "subdir/file2.txt", "additional_feature": "Second dummy file"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    shutil.make_archive(archive_dir, "zip", archive_dir)
    shutil.rmtree(str(archive_dir))

    data_files_with_zip_archives = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())

    assert len(data_files_with_zip_archives) == 1
    assert len(data_files_with_zip_archives["train"]) == 1
    return data_files_with_zip_archives


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = FolderBasedBuilderConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = FolderBasedBuilderConfig(name="name", data_files=data_files)


def test_inferring_labels_from_data_dirs(data_files_with_labels_no_metadata, cache_dir):
    autofolder = DummyFolderBasedBuilder(
        data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    assert autofolder.info.features["label"] == ClassLabel(names=["class0", "class1"])
    generator = autofolder._generate_examples(**gen_kwargs)
    assert all(example["label"] in {"class0", "class1"} for _, example in generator)


def test_default_folder_builder_not_usable(data_files_with_labels_no_metadata, cache_dir):
    # builder would try to access non-existing attributes of a default `BuilderConfig` class
    # as a custom one is not provided
    with pytest.raises(AttributeError):
        _ = FolderBasedBuilder(
            data_files=data_files_with_labels_no_metadata,
            cache_dir=cache_dir,
        )


# test that AutoFolder is extended for streaming when it's child class is instantiated:
# see line 115 in src/datasets/streaming.py
def test_streaming_patched():
    _ = DummyFolderBasedBuilder(data_dir=".")
    module = importlib.import_module(FolderBasedBuilder.__module__)
    assert hasattr(module, "_patched_for_streaming")
    assert module._patched_for_streaming


@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_labels(
    data_files_with_labels_no_metadata, auto_text_file, drop_metadata, drop_labels, cache_dir
):
    autofolder = DummyFolderBasedBuilder(
        data_files=data_files_with_labels_no_metadata,
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        cache_dir=cache_dir,
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # removing labels explicitly requires drop_labels=True
    assert gen_kwargs["add_labels"] is not bool(drop_labels)
    assert gen_kwargs["add_metadata"] is False
    generator = autofolder._generate_examples(**gen_kwargs)
    if not drop_labels:
        assert all(
            example.keys() == {"base", "label"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"base"} and all(val is not None for val in example.values()) for _, example in generator
        )


@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_metadata(file_with_metadata, drop_metadata, drop_labels, cache_dir):
    file, metadata_file = file_with_metadata
    autofolder = DummyFolderBasedBuilder(
        data_files=[file, metadata_file],
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        cache_dir=cache_dir,
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # since the dataset has metadata, removing the metadata explicitly requires drop_metadata=True
    assert gen_kwargs["add_metadata"] is not bool(drop_metadata)
    # since the dataset has metadata, adding the labels explicitly requires drop_labels=False
    assert gen_kwargs["add_labels"] is False
    generator = autofolder._generate_examples(**gen_kwargs)
    expected_columns = {"base"}
    if gen_kwargs["add_metadata"]:
        expected_columns.add("additional_feature")
    if gen_kwargs["add_labels"]:
        expected_columns.add("label")
    result = [example for _, example in generator]
    assert len(result) == 1
    example = result[0]
    assert example.keys() == expected_columns
    for column in expected_columns:
        assert example[column] is not None


@pytest.mark.parametrize("remote", [True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_data_files_with_different_levels_no_metadata(
    data_files_with_different_levels_no_metadata, drop_labels, remote, cache_dir
):
    data_files = remote_files if remote else data_files_with_different_levels_no_metadata
    autofolder = DummyFolderBasedBuilder(
        data_files=data_files,
        cache_dir=cache_dir,
        drop_labels=drop_labels,
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = autofolder._generate_examples(**gen_kwargs)
    if drop_labels is not False:
        # with None (default) we should drop labels if files are on different levels in dir structure
        assert "label" not in autofolder.info.features
        assert all(example.keys() == {"base"} for _, example in generator)
    else:
        assert "label" in autofolder.info.features
        assert isinstance(autofolder.info.features["label"], ClassLabel)
        assert all(example.keys() == {"base", "label"} for _, example in generator)


@pytest.mark.parametrize("remote", [False, True])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_data_files_with_one_label_no_metadata(data_files_with_one_label_no_metadata, drop_labels, remote, cache_dir):
    data_files = remote_files[:2] if remote else data_files_with_one_label_no_metadata
    autofolder = DummyFolderBasedBuilder(
        data_files=data_files,
        cache_dir=cache_dir,
        drop_labels=drop_labels,
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = autofolder._generate_examples(**gen_kwargs)
    if drop_labels is not False:
        # with None (default) we should drop labels if only one label is found (=if there is a single dir)
        assert "label" not in autofolder.info.features
        assert all(example.keys() == {"base"} for _, example in generator)
    else:
        assert "label" in autofolder.info.features
        assert isinstance(autofolder.info.features["label"], ClassLabel)
        assert all(example.keys() == {"base", "label"} for _, example in generator)


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("n_splits", [1, 2])
def test_data_files_with_metadata_and_splits(
    streaming, cache_dir, n_splits, data_files_with_one_split_and_metadata, data_files_with_two_splits_and_metadata
):
    data_files = data_files_with_one_split_and_metadata if n_splits == 1 else data_files_with_two_splits_and_metadata
    autofolder = DummyFolderBasedBuilder(
        data_files=data_files,
        cache_dir=cache_dir,
    )
    download_manager = StreamingDownloadManager() if streaming else DownloadManager()
    generated_splits = autofolder._split_generators(download_manager)
    for (split, files), generated_split in zip(data_files.items(), generated_splits):
        assert split == generated_split.name
        expected_num_of_examples = len(files) - 1
        generated_examples = list(autofolder._generate_examples(**generated_split.gen_kwargs))
        assert len(generated_examples) == expected_num_of_examples
        assert len({example["base"] for _, example in generated_examples}) == expected_num_of_examples
        assert len({example["additional_feature"] for _, example in generated_examples}) == expected_num_of_examples
        assert all(example["additional_feature"] is not None for _, example in generated_examples)


@pytest.mark.parametrize("streaming", [False, True])
def test_data_files_with_metadata_and_archives(streaming, cache_dir, data_files_with_zip_archives):
    autofolder = DummyFolderBasedBuilder(data_files=data_files_with_zip_archives, cache_dir=cache_dir)
    download_manager = StreamingDownloadManager() if streaming else DownloadManager()
    generated_splits = autofolder._split_generators(download_manager)
    for (split, files), generated_split in zip(data_files_with_zip_archives.items(), generated_splits):
        assert split == generated_split.name
        num_of_archives = len(files)
        expected_num_of_examples = 2 * num_of_archives
        generated_examples = list(autofolder._generate_examples(**generated_split.gen_kwargs))
        assert len(generated_examples) == expected_num_of_examples
        assert len({example["base"] for _, example in generated_examples}) == expected_num_of_examples
        assert len({example["additional_feature"] for _, example in generated_examples}) == expected_num_of_examples
        assert all(example["additional_feature"] is not None for _, example in generated_examples)


def test_data_files_with_wrong_metadata_file_name(cache_dir, tmp_path, auto_text_file):
    data_dir = tmp_path / "data_dir_with_bad_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    metadata_filename = data_dir / "bad_metadata.jsonl"  # bad file
    metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Dummy file"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files_with_bad_metadata = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = autofolder._generate_examples(**gen_kwargs)
    assert all("additional_feature" not in example for _, example in generator)


@pytest.mark.parametrize(
    "malicious_file_name",
    [
        "../outside/secret.txt",  # relative traversal
        "../../outside/secret.txt",  # deeper relative traversal
        "subdir/../../outside/secret.txt",  # traversal hidden after a valid segment
        "dummy/../../../etc/passwd",  # valid segment then escapes past the root (review on #8325)
        "subdir/../../../../outside/secret.txt",  # deep escape after a valid segment
    ],
)
def test_data_files_with_metadata_path_traversal_is_rejected(cache_dir, tmp_path, auto_text_file, malicious_file_name):
    # Regression test for https://github.com/huggingface/datasets/issues/8324
    # A crafted `file_name` must not be able to escape the metadata file's directory.
    secret_dir = tmp_path / "outside"
    secret_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, secret_dir / "secret.txt")

    data_dir = tmp_path / "data_dir_with_traversal_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    metadata_filename = data_dir / "metadata.jsonl"
    metadata = f'{{"file_name": {json.dumps(malicious_file_name)}, "additional_feature": "Malicious file"}}\n'
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    with pytest.raises(ValueError, match="Invalid metadata file_name"):
        list(autofolder._generate_examples(**gen_kwargs))


def test_data_files_with_metadata_absolute_path_is_rejected(cache_dir, tmp_path, auto_text_file):
    # Regression test for https://github.com/huggingface/datasets/issues/8324
    # An absolute `file_name` must not be able to read files outside the dataset directory.
    secret_dir = tmp_path / "outside"
    secret_dir.mkdir(parents=True, exist_ok=True)
    secret_file = secret_dir / "secret.txt"
    shutil.copyfile(auto_text_file, secret_file)

    data_dir = tmp_path / "data_dir_with_absolute_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    metadata_filename = data_dir / "metadata.jsonl"
    metadata = f'{{"file_name": {json.dumps(str(secret_file))}, "additional_feature": "Malicious file"}}\n'
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    with pytest.raises(ValueError, match="Invalid metadata file_name"):
        list(autofolder._generate_examples(**gen_kwargs))


@pytest.mark.parametrize(
    "malicious_file_name",
    [
        "file://../../outside/secret.txt",  # fsspec local scheme + traversal
        "local://../../outside/secret.txt",  # fsspec local scheme + traversal
        "file://../outside/secret.txt",  # scheme where os.path.normpath mangles the "../" away
        "file:///etc/passwd",  # absolute-looking local scheme
        "file://outside/secret.txt",  # scheme without traversal
    ],
)
def test_data_files_with_metadata_url_scheme_is_rejected(cache_dir, tmp_path, auto_text_file, malicious_file_name):
    # Regression test for the review on https://github.com/huggingface/datasets/pull/8325:
    # fsspec schemes such as `file://` / `local://` resolve to local files and previously bypassed
    # the containment check. A `file_name` carrying any URL scheme ("://") must be rejected.
    secret_dir = tmp_path / "outside"
    secret_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, secret_dir / "secret.txt")

    data_dir = tmp_path / "data_dir_with_scheme_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    metadata_filename = data_dir / "metadata.jsonl"
    metadata = f'{{"file_name": {json.dumps(malicious_file_name)}, "additional_feature": "Malicious file"}}\n'
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    with pytest.raises(ValueError, match="Invalid metadata file_name"):
        list(autofolder._generate_examples(**gen_kwargs))


def test_data_files_with_metadata_symlink_escape_is_rejected(cache_dir, tmp_path, auto_text_file):
    # Regression test for the review on https://github.com/huggingface/datasets/pull/8325:
    # the string-based checks (URL scheme / absolute path / ".." traversal) only see a plain,
    # innocent-looking relative `file_name` and let it through. If a subdirectory of the dataset
    # is actually a symlink pointing outside the dataset directory, a reference such as
    # "evil_link/secret.txt" resolves to a file outside the dataset root. Only the realpath-based
    # containment check (`_metadata_reference_is_contained`) catches this, so this test guards that
    # second layer of defense: with the string checks alone the reference would be read.
    secret_dir = tmp_path / "outside"
    secret_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, secret_dir / "secret.txt")

    data_dir = tmp_path / "data_dir_with_symlink_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")

    # A subdirectory of the dataset that is really a symlink escaping the dataset root. Creating
    # symlinks may require privileges (e.g. Windows without Developer Mode); skip when unavailable.
    # The test still runs on Linux CI, where this attack matters.
    evil_link = data_dir / "evil_link"
    try:
        evil_link.symlink_to(secret_dir, target_is_directory=True)
    except (OSError, NotImplementedError) as e:
        pytest.skip(f"symlink creation not available on this platform: {e!r}")

    metadata_filename = data_dir / "metadata.jsonl"
    metadata = '{"file_name": "evil_link/secret.txt", "additional_feature": "Malicious file"}\n'
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # The string checks accept this relative path; only the realpath-based containment check
    # rejects it, with this specific message. Asserting on that message ensures the test would
    # fail (the file would be read) if the containment check were removed.
    with pytest.raises(ValueError, match="the resolved path escapes the dataset directory"):
        list(autofolder._generate_examples(**gen_kwargs))


def test_metadata_reference_containment_across_scheme_forms(tmp_path):
    # Regression test for the review on https://github.com/huggingface/datasets/pull/8325:
    # the containment check must actually run (not be skipped) for URLs and correctly handle
    # chained "::" references. It must work for the four forms `downloaded_metadata_dir` can take:
    #   1. a local path                          -> /path/to/metadata_dir
    #   2. a remote URL                          -> hf://path/to/metadata_dir
    #   3. a chained URL over a local archive    -> zip://metadata_dir::/path/to/archive.zip
    #   4. a chained URL over a remote archive   -> zip://metadata_dir::hf://path/to/archive.zip
    # `os.path.join` is patched to the fsspec-aware `xjoin` once a builder is instantiated, which is
    # exactly how `set_feature` joins the reference at runtime, so use it here too.
    _ = DummyFolderBasedBuilder(data_dir=".")  # triggers the streaming patch of os.path.join
    from datasets.packaged_modules.folder_based_builder import folder_based_builder as fbb

    xjoin = fbb.os.path.join

    # a real local metadata dir (with a real subdir) so realpath-based containment can resolve
    local_dir = tmp_path / "metadata_dir"
    (local_dir / "subdir").mkdir(parents=True, exist_ok=True)
    (tmp_path / "outside").mkdir(parents=True, exist_ok=True)

    forms = {
        "local": local_dir.as_posix(),
        "hf_remote": "hf://datasets/user/repo@main/metadata_dir",
        "zip_local": "zip://metadata_dir::/data/local/archive.zip",
        "zip_remote": "zip://metadata_dir::hf://datasets/user/repo@main/archive.zip",
    }
    for name, metadata_dir in forms.items():
        # a legitimate relative reference must be considered contained
        legit = xjoin(metadata_dir, "subdir/file2.txt")
        assert _metadata_reference_is_contained(metadata_dir, legit), f"legit ref rejected for {name}"

        # a reference pointing at a sibling of the metadata dir must be rejected
        head, _, _ = metadata_dir.partition("::")
        sibling_head = head.rsplit("/", 1)[0] + "/evil_sibling"
        escaping = sibling_head + metadata_dir[len(head) :]
        assert not _metadata_reference_is_contained(metadata_dir, escaping), f"sibling escape allowed for {name}"

        # for chained URLs, tampering with the container part (after "::") must be rejected
        if "::" in metadata_dir:
            tampered = legit.split("::")[0] + "::/attacker/other.zip"
            assert not _metadata_reference_is_contained(metadata_dir, tampered), f"container tamper allowed for {name}"


def test_data_files_with_metadata_legitimate_subdir_reference(cache_dir, tmp_path, auto_text_file):
    # A legitimate `file_name` pointing to a file in a subdirectory of the metadata
    # file's directory must keep working after the path traversal fix (#8324).
    data_dir = tmp_path / "data_dir_with_subdir_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir = data_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    shutil.copyfile(auto_text_file, subdir / "file2.txt")
    metadata_filename = data_dir / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Same-dir file"}
        {"file_name": "subdir/file2.txt", "additional_feature": "Subdir file"}
        {"file_name": "./subdir/file2.txt", "additional_feature": "Subdir file with dot prefix"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    examples = [example for _, example in autofolder._generate_examples(**gen_kwargs)]
    assert len(examples) == 3
    assert all(example["base"] is not None for example in examples)
    assert all(os.path.isfile(example["base"]) for example in examples)


def test_data_files_with_custom_file_name_column_in_metadata_file(cache_dir, tmp_path, auto_text_file):
    data_dir = tmp_path / "data_dir_with_custom_file_name_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    metadata_filename = data_dir / "metadata.jsonl"
    metadata = textwrap.dedent(  # with bad column "bad_file_name" instead of "file_name"
        """\
        {"text_file_name": "file.txt", "additional_feature": "Dummy file"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files_with_bad_metadata = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = autofolder._generate_examples(**gen_kwargs)
    assert all("text" in example and "text_file_name" not in example for _, example in generator)


def test_data_files_with_custom_file_names_column_in_metadata_file_large_string_list(
    cache_dir, tmp_path, auto_text_file
):
    import pyarrow as pa
    import pyarrow.parquet as pq

    data_dir = tmp_path / "data_dir_with_custom_file_names_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    metadata_filename = data_dir / "metadata.parquet"
    pq.write_table(
        pa.Table.from_arrays(
            [
                pa.array([["file.txt"]], type=pa.list_(pa.large_string())),
                pa.array(["Dummy file"], type=pa.large_string()),
            ],
            names=["text_file_names", "additional_feature"],
        ),
        metadata_filename,
    )

    data_files_with_metadata = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files_with_metadata, cache_dir=cache_dir)
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = autofolder._generate_examples(**gen_kwargs)
    examples = [example for _, example in generator]
    assert len(examples) == 1
    assert "text" in examples[0] and "text_file_names" not in examples[0]
    assert len(examples[0]["text"]) == 1 and examples[0]["text"][0].endswith("file.txt")
