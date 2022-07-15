import shutil
import textwrap

import numpy as np
import pytest

from datasets import ClassLabel, Features, Image, Value
from datasets.data_files import DataFilesDict, get_data_patterns_locally
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.imagefolder.imagefolder import ImageFolder
from datasets.streaming import extend_module_for_streaming

from ..utils import require_pil


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "imagefolder_cache_dir")


@pytest.fixture
def data_files_with_labels_no_metadata(tmp_path, image_file):
    data_dir = tmp_path / "data_files_with_labels_no_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "cat"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    # data dirs can be nested but imagefolder should care only about the last part of the path:
    subdir_class_1 = data_dir / "subdir" / "dog"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    image_filename = subdir_class_0 / "image_cat.jpg"
    shutil.copyfile(image_file, image_filename)
    image_filename2 = subdir_class_1 / "image_dog.jpg"
    shutil.copyfile(image_file, image_filename2)

    data_files_with_labels_no_metadata = DataFilesDict.from_local_or_remote(
        get_data_patterns_locally(str(data_dir)), str(data_dir)
    )

    return data_files_with_labels_no_metadata


@pytest.fixture
def image_files_with_labels_and_duplicated_label_key_in_metadata(tmp_path, image_file):
    data_dir = tmp_path / "image_files_with_labels_and_label_key_in_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "cat"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "dog"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    image_filename = subdir_class_0 / "image_cat.jpg"
    shutil.copyfile(image_file, image_filename)
    image_filename2 = subdir_class_1 / "image_dog.jpg"
    shutil.copyfile(image_file, image_filename2)

    image_metadata_filename = tmp_path / data_dir / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "cat/image_cat.jpg", "caption": "Nice image of a cat", "label": "Cat"}
        {"file_name": "dog/image_dog.jpg", "caption": "Nice image of a dog", "label": "Dog"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)

    return str(image_filename), str(image_filename2), str(image_metadata_filename)


@pytest.fixture
def image_file_with_metadata(tmp_path, image_file):
    image_filename = tmp_path / "image_rgb.jpg"
    shutil.copyfile(image_file, image_filename)
    image_metadata_filename = tmp_path / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb.jpg", "caption": "Nice image"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)
    return str(image_filename), str(image_metadata_filename)


@pytest.fixture
def image_files_with_metadata_that_misses_one_image(tmp_path, image_file):
    image_filename = tmp_path / "image_rgb.jpg"
    shutil.copyfile(image_file, image_filename)
    image_filename2 = tmp_path / "image_rgb2.jpg"
    shutil.copyfile(image_file, image_filename2)
    image_metadata_filename = tmp_path / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb.jpg", "caption": "Nice image"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)
    return str(image_filename), str(image_filename2), str(image_metadata_filename)


@pytest.fixture
def data_files_with_one_split_and_metadata(tmp_path, image_file):
    data_dir = tmp_path / "imagefolder_data_dir_with_metadata_one_split"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir = data_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    image_filename = data_dir / "image_rgb.jpg"
    shutil.copyfile(image_file, image_filename)
    image_filename2 = data_dir / "image_rgb2.jpg"
    shutil.copyfile(image_file, image_filename2)
    image_filename3 = subdir / "image_rgb3.jpg"  # in subdir
    shutil.copyfile(image_file, image_filename3)

    image_metadata_filename = data_dir / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb.jpg", "caption": "Nice image"}
        {"file_name": "image_rgb2.jpg", "caption": "Nice second image"}
        {"file_name": "subdir/image_rgb3.jpg", "caption": "Nice third image"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)
    data_files_with_one_split_and_metadata = DataFilesDict.from_local_or_remote(
        get_data_patterns_locally(data_dir), data_dir
    )
    assert len(data_files_with_one_split_and_metadata) == 1
    assert len(data_files_with_one_split_and_metadata["train"]) == 4
    return data_files_with_one_split_and_metadata


@pytest.fixture
def data_files_with_two_splits_and_metadata(tmp_path, image_file):
    data_dir = tmp_path / "imagefolder_data_dir_with_metadata_two_splits"
    data_dir.mkdir(parents=True, exist_ok=True)
    train_dir = data_dir / "train"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir = data_dir / "test"
    test_dir.mkdir(parents=True, exist_ok=True)

    image_filename = train_dir / "image_rgb.jpg"  # train image
    shutil.copyfile(image_file, image_filename)
    image_filename2 = train_dir / "image_rgb2.jpg"  # train image
    shutil.copyfile(image_file, image_filename2)
    image_filename3 = test_dir / "image_rgb3.jpg"  # test image
    shutil.copyfile(image_file, image_filename3)

    train_image_metadata_filename = train_dir / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb.jpg", "caption": "Nice train image"}
        {"file_name": "image_rgb2.jpg", "caption": "Nice second train image"}
        """
    )
    with open(train_image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)
    test_image_metadata_filename = test_dir / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb3.jpg", "caption": "Nice test image"}
        """
    )
    with open(test_image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)
    data_files_with_two_splits_and_metadata = DataFilesDict.from_local_or_remote(
        get_data_patterns_locally(data_dir), data_dir
    )
    assert len(data_files_with_two_splits_and_metadata) == 2
    assert len(data_files_with_two_splits_and_metadata["train"]) == 3
    assert len(data_files_with_two_splits_and_metadata["test"]) == 2
    return data_files_with_two_splits_and_metadata


@pytest.fixture
def data_files_with_zip_archives(tmp_path, image_file):
    from PIL import Image, ImageOps

    data_dir = tmp_path / "imagefolder_data_dir_with_zip_archives"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = data_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    subdir = archive_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    image_filename = archive_dir / "image_rgb.jpg"
    shutil.copyfile(image_file, image_filename)
    image_filename2 = subdir / "image_rgb2.jpg"  # in subdir
    # make sure they're two different images
    # Indeed we won't be able to compare the image.filename, since the archive is not extracted in streaming mode
    ImageOps.flip(Image.open(image_file)).save(image_filename2)

    image_metadata_filename = archive_dir / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb.jpg", "caption": "Nice image"}
        {"file_name": "subdir/image_rgb2.jpg", "caption": "Nice second image"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)

    shutil.make_archive(archive_dir, "zip", archive_dir)
    shutil.rmtree(str(archive_dir))

    data_files_with_zip_archives = DataFilesDict.from_local_or_remote(get_data_patterns_locally(data_dir), data_dir)

    assert len(data_files_with_zip_archives) == 1
    assert len(data_files_with_zip_archives["train"]) == 1
    return data_files_with_zip_archives


@require_pil
# check that labels are inferred correctly from dir names
def test_generate_examples_with_labels(data_files_with_labels_no_metadata, cache_dir):
    # there are no metadata.jsonl files in this test case
    imagefolder = ImageFolder(data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False)
    imagefolder.download_and_prepare()
    assert imagefolder.info.features == Features({"image": Image(), "label": ClassLabel(names=["cat", "dog"])})
    dataset = list(imagefolder.as_dataset()["train"])
    label_feature = imagefolder.info.features["label"]

    assert dataset[0]["label"] == label_feature._str2int["cat"]
    assert dataset[1]["label"] == label_feature._str2int["dog"]


@require_pil
@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_duplicated_label_key(
    image_files_with_labels_and_duplicated_label_key_in_metadata, drop_metadata, drop_labels, cache_dir, caplog
):
    cat_image_file, dog_image_file, image_metadata_file = image_files_with_labels_and_duplicated_label_key_in_metadata
    imagefolder = ImageFolder(
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        data_files=[cat_image_file, dog_image_file, image_metadata_file],
        cache_dir=cache_dir,
    )
    if drop_labels is False:
        # infer labels from directories even if metadata files are found
        imagefolder.download_and_prepare()
        warning_in_logs = any("ignoring metadata columns" in record.msg.lower() for record in caplog.records)
        assert warning_in_logs if drop_metadata is not True else not warning_in_logs
        dataset = imagefolder.as_dataset()["train"]
        assert imagefolder.info.features["label"] == ClassLabel(names=["cat", "dog"])
        assert all(example["label"] in imagefolder.info.features["label"]._str2int.values() for example in dataset)
    else:
        imagefolder.download_and_prepare()
        dataset = imagefolder.as_dataset()["train"]
        if drop_metadata is not True:
            # labels are from metadata
            assert imagefolder.info.features["label"] == Value("string")
            assert all(example["label"] in ["Cat", "Dog"] for example in dataset)
        else:
            # drop both labels and metadata
            assert imagefolder.info.features == Features({"image": Image()})
            assert all(example.keys() == {"image"} for example in dataset)


@require_pil
@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_labels(image_file, drop_metadata, drop_labels):
    imagefolder = ImageFolder(drop_metadata=drop_metadata, drop_labels=drop_labels, data_files={"train": [image_file]})
    gen_kwargs = imagefolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # removing the labels explicitly requires drop_labels=True
    assert gen_kwargs["add_labels"] is not bool(drop_labels)
    assert gen_kwargs["add_metadata"] is False
    generator = imagefolder._generate_examples(**gen_kwargs)
    if not drop_labels:
        assert all(
            example.keys() == {"image", "label"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"image"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_pil
@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_metadata(image_file_with_metadata, drop_metadata, drop_labels):
    image_file, image_metadata_file = image_file_with_metadata
    imagefolder = ImageFolder(
        drop_metadata=drop_metadata, drop_labels=drop_labels, data_files={"train": [image_file, image_metadata_file]}
    )
    gen_kwargs = imagefolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # since the dataset has metadata, removing the metadata explicitly requires drop_metadata=True
    assert gen_kwargs["add_metadata"] is not bool(drop_metadata)
    # since the dataset has metadata, adding the labels explicitly requires drop_labels=False
    assert gen_kwargs["add_labels"] is (drop_labels is False)
    generator = imagefolder._generate_examples(**gen_kwargs)
    expected_columns = {"image"}
    if gen_kwargs["add_metadata"]:
        expected_columns.add("caption")
    if gen_kwargs["add_labels"]:
        expected_columns.add("label")
    result = [example for _, example in generator]
    assert len(result) == 1
    example = result[0]
    assert example.keys() == expected_columns
    for column in expected_columns:
        assert example[column] is not None


@require_pil
@pytest.mark.parametrize("drop_metadata", [None, True, False])
def test_generate_examples_with_metadata_in_wrong_location(image_file, image_file_with_metadata, drop_metadata):
    _, image_metadata_file = image_file_with_metadata
    imagefolder = ImageFolder(drop_metadata=drop_metadata, data_files={"train": [image_file, image_metadata_file]})
    gen_kwargs = imagefolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = imagefolder._generate_examples(**gen_kwargs)
    if not drop_metadata:
        with pytest.raises(ValueError):
            list(generator)
    else:
        assert all(
            example.keys() == {"image"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_pil
@pytest.mark.parametrize("drop_metadata", [None, True, False])
def test_generate_examples_with_metadata_that_misses_one_image(
    image_files_with_metadata_that_misses_one_image, drop_metadata
):
    image_file, image_file2, image_metadata_file = image_files_with_metadata_that_misses_one_image
    if not drop_metadata:
        features = Features({"image": Image(), "caption": Value("string")})
    else:
        features = Features({"image": Image()})
    imagefolder = ImageFolder(
        drop_metadata=drop_metadata,
        features=features,
        data_files={"train": [image_file, image_file2, image_metadata_file]},
    )
    gen_kwargs = imagefolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = imagefolder._generate_examples(**gen_kwargs)
    if not drop_metadata:
        with pytest.raises(ValueError):
            list(generator)
    else:
        assert all(
            example.keys() == {"image"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_pil
@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("n_splits", [1, 2])
def test_data_files_with_metadata_and_splits(
    streaming, cache_dir, n_splits, data_files_with_one_split_and_metadata, data_files_with_two_splits_and_metadata
):
    data_files = data_files_with_one_split_and_metadata if n_splits == 1 else data_files_with_two_splits_and_metadata
    imagefolder = ImageFolder(data_files=data_files, cache_dir=cache_dir)
    imagefolder.download_and_prepare()
    datasets = imagefolder.as_streaming_dataset() if streaming else imagefolder.as_dataset()
    for split, data_files in data_files.items():
        expected_num_of_images = len(data_files) - 1  # don't count the metadata file
        assert split in datasets
        dataset = list(datasets[split])
        assert len(dataset) == expected_num_of_images
        # make sure each sample has its own image and metadata
        assert len(set(example["image"].filename for example in dataset)) == expected_num_of_images
        assert len(set(example["caption"] for example in dataset)) == expected_num_of_images
        assert all(example["caption"] is not None for example in dataset)


@require_pil
@pytest.mark.parametrize("streaming", [False, True])
def test_data_files_with_metadata_and_archives(streaming, cache_dir, data_files_with_zip_archives):
    if streaming:
        extend_module_for_streaming(ImageFolder.__module__)
    imagefolder = ImageFolder(data_files=data_files_with_zip_archives, cache_dir=cache_dir)
    imagefolder.download_and_prepare()
    datasets = imagefolder.as_streaming_dataset() if streaming else imagefolder.as_dataset()
    for split, data_files in data_files_with_zip_archives.items():
        num_of_archives = len(data_files)  # the metadata file is inside the archive
        expected_num_of_images = 2 * num_of_archives
        assert split in datasets
        dataset = list(datasets[split])
        assert len(dataset) == expected_num_of_images
        # make sure each sample has its own image and metadata
        assert len(set([np.array(example["image"])[0, 0, 0] for example in dataset])) == expected_num_of_images
        assert len(set(example["caption"] for example in dataset)) == expected_num_of_images
        assert all(example["caption"] is not None for example in dataset)


@require_pil
def test_data_files_with_wrong_metadata_file_name(cache_dir, tmp_path, image_file):
    data_dir = tmp_path / "data_dir_with_bad_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(image_file, data_dir / "image_rgb.jpg")
    image_metadata_filename = data_dir / "bad_metadata.jsonl"  # bad file
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb.jpg", "caption": "Nice image"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)

    data_files_with_bad_metadata = DataFilesDict.from_local_or_remote(get_data_patterns_locally(data_dir), data_dir)
    imagefolder = ImageFolder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    imagefolder.download_and_prepare()
    dataset = imagefolder.as_dataset(split="train")
    # check that there are no metadata, since the metadata file name doesn't have the right name
    assert "caption" not in dataset.column_names


@require_pil
def test_data_files_with_wrong_image_file_name_column_in_metadata_file(cache_dir, tmp_path, image_file):
    data_dir = tmp_path / "data_dir_with_bad_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(image_file, data_dir / "image_rgb.jpg")
    image_metadata_filename = data_dir / "metadata.jsonl"
    image_metadata = textwrap.dedent(  # with bad column "bad_file_name" instead of "file_name"
        """\
        {"bad_file_name": "image_rgb.jpg", "caption": "Nice image"}
        """
    )
    with open(image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)

    data_files_with_bad_metadata = DataFilesDict.from_local_or_remote(get_data_patterns_locally(data_dir), data_dir)
    imagefolder = ImageFolder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    with pytest.raises(ValueError) as exc_info:
        imagefolder.download_and_prepare()
    assert "`file_name` must be present" in str(exc_info.value)
