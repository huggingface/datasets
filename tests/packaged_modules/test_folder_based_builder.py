import importlib
import shutil
import textwrap

import pytest

from datasets import ClassLabel, DownloadManager, Features, Value
from datasets.data_files import DataFilesDict, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.folder_based_builder.folder_based_builder import (
    FolderBasedBuilder,
    FolderBasedBuilderConfig,
)
from datasets.tasks import TextClassification


remote_files = [
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/hallo.txt",
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/hello.txt",
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/class1/bonjour.txt",
    "https://huggingface.co/datasets/hf-internal-testing/textfolder/resolve/main/class1/bonjour2.txt",
]


class DummyFolderBasedBuilder(FolderBasedBuilder):
    BASE_FEATURE = dict
    BASE_COLUMN_NAME = "base"
    BUILDER_CONFIG_CLASS = FolderBasedBuilderConfig
    EXTENSIONS = [".txt"]
    CLASSIFICATION_TASK = TextClassification(text_column="base", label_column="label")


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


@pytest.fixture()
def files_with_metadata_that_misses_one_sample(tmp_path, auto_text_file):
    filename = tmp_path / "file.txt"
    shutil.copyfile(auto_text_file, filename)
    filename2 = tmp_path / "file2.txt"
    shutil.copyfile(auto_text_file, filename2)
    metadata_filename = tmp_path / "metadata.jsonl"
    metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Dummy file"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)
    return str(filename), str(filename2), str(metadata_filename)


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


def test_inferring_labels_from_data_dirs(data_files_with_labels_no_metadata, cache_dir):
    autofolder = DummyFolderBasedBuilder(
        data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    assert autofolder.info.features == Features({"base": {}, "label": ClassLabel(names=["class0", "class1"])})
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
    _ = DummyFolderBasedBuilder()
    module = importlib.import_module(FolderBasedBuilder.__module__)
    assert hasattr(module, "_patched_for_streaming")
    assert module._patched_for_streaming


@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_duplicated_label_key(
    files_with_labels_and_duplicated_label_key_in_metadata, drop_metadata, drop_labels, cache_dir, caplog
):
    class0_file, class1_file, metadata_file = files_with_labels_and_duplicated_label_key_in_metadata
    autofolder = DummyFolderBasedBuilder(
        data_files=[class0_file, class1_file, metadata_file],
        cache_dir=cache_dir,
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = autofolder._generate_examples(**gen_kwargs)
    if drop_labels is False:
        # infer labels from directories even if metadata files are found
        warning_in_logs = any("ignoring metadata columns" in record.msg.lower() for record in caplog.records)
        assert warning_in_logs if drop_metadata is not True else not warning_in_logs
        assert autofolder.info.features["label"] == ClassLabel(names=["class0", "class1"])
        assert all(example["label"] in ["class0", "class1"] for _, example in generator)

    else:
        if drop_metadata is not True:
            # labels are from metadata
            assert autofolder.info.features["label"] == Value("string")
            assert all(example["label"] in ["CLASS_0", "CLASS_1"] for _, example in generator)
        else:
            # drop both labels and metadata
            assert autofolder.info.features == Features({"base": {}})
            assert all(example.keys() == {"base"} for _, example in generator)


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
    assert gen_kwargs["add_labels"] is (drop_labels is False)
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


@pytest.mark.parametrize("drop_metadata", [None, True, False])
def test_data_files_with_metadata_that_misses_one_sample(
    files_with_metadata_that_misses_one_sample, drop_metadata, cache_dir
):
    file, file2, metadata_file = files_with_metadata_that_misses_one_sample
    if not drop_metadata:
        features = Features({"base": None, "additional_feature": Value("string")})
    else:
        features = Features({"base": None})
    autofolder = DummyFolderBasedBuilder(
        data_files=[file, file2, metadata_file],
        drop_metadata=drop_metadata,
        features=features,
        cache_dir=cache_dir,
    )
    gen_kwargs = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = autofolder._generate_examples(**gen_kwargs)
    if not drop_metadata:
        with pytest.raises(ValueError):
            list(generator)
    else:
        assert all(
            example.keys() == {"base"} and all(val is not None for val in example.values()) for _, example in generator
        )


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


def test_data_files_with_wrong_file_name_column_in_metadata_file(cache_dir, tmp_path, auto_text_file):
    data_dir = tmp_path / "data_dir_with_bad_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(auto_text_file, data_dir / "file.txt")
    metadata_filename = data_dir / "metadata.jsonl"
    metadata = textwrap.dedent(  # with bad column "bad_file_name" instead of "file_name"
        """\
        {"bad_file_name": "file.txt", "additional_feature": "Dummy file"}
        """
    )
    with open(metadata_filename, "w", encoding="utf-8") as f:
        f.write(metadata)

    data_files_with_bad_metadata = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    autofolder = DummyFolderBasedBuilder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    with pytest.raises(ValueError) as exc_info:
        _ = autofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    assert "`file_name` must be present" in str(exc_info.value)
