import os
import shutil
import textwrap

import numpy as np
import pytest

from datasets import Features, Image, Value
from datasets.data_files import DataFilesDict, get_patterns_locally
from datasets.packaged_modules.imagefolder.imagefolder import ImageFolder
from datasets.streaming import extend_module_for_streaming

from ..utils import require_pil


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "imagefolder_cache_dir")


@pytest.fixture
def image_file():
    return os.path.join(os.path.dirname(__file__), "..", "features", "data", "test_image_rgb.jpg")


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
def data_files_with_one_split_and_metadata(tmp_path, image_file):
    data_dir = tmp_path / "imagefolder_data_dir_with_metadata"
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
        get_patterns_locally(data_dir), data_dir
    )
    assert len(data_files_with_one_split_and_metadata) == 1
    assert len(data_files_with_one_split_and_metadata["train"]) == 4
    return data_files_with_one_split_and_metadata


@pytest.fixture
def data_files_with_two_splits_and_metadata(tmp_path, image_file):
    data_dir = tmp_path / "imagefolder_data_dir_with_metadata"
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
    train_image_metadata_filename = test_dir / "metadata.jsonl"
    image_metadata = textwrap.dedent(
        """\
        {"file_name": "image_rgb3.jpg", "caption": "Nice test image"}
        """
    )
    with open(train_image_metadata_filename, "w", encoding="utf-8") as f:
        f.write(image_metadata)
    data_files_with_two_splits_and_metadata = DataFilesDict.from_local_or_remote(
        get_patterns_locally(data_dir), data_dir
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

    data_files_with_zip_archives = DataFilesDict.from_local_or_remote(get_patterns_locally(data_dir), data_dir)

    assert len(data_files_with_zip_archives) == 1
    assert len(data_files_with_zip_archives["train"]) == 1
    return data_files_with_zip_archives


@require_pil
@pytest.mark.parametrize("drop_labels", [True, False])
def test_generate_examples_drop_labels(image_file, drop_labels):
    imagefolder = ImageFolder(drop_labels=drop_labels)
    generator = imagefolder._generate_examples([(image_file, image_file)], None, "train")
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
@pytest.mark.parametrize("drop_metadata", [True, False])
def test_generate_examples_drop_metadata(image_file_with_metadata, drop_metadata):
    image_file, image_metadata_file = image_file_with_metadata
    if not drop_metadata:
        features = Features({"image": Image(), "label": Value("string"), "caption": Value("string")})
    else:
        features = Features({"image": Image(), "label": Value("string")})
    imagefolder = ImageFolder(drop_metadata=drop_metadata, features=features)
    generator = imagefolder._generate_examples(
        [(image_file, image_file)], {"train": [(image_metadata_file, image_metadata_file)]}, "train"
    )
    if not drop_metadata:
        assert all(
            example.keys() == {"image", "label", "caption"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"image", "label"} and all(val is not None for val in example.values())
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

    data_files_with_bad_metadata = DataFilesDict.from_local_or_remote(get_patterns_locally(data_dir), data_dir)
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

    data_files_with_bad_metadata = DataFilesDict.from_local_or_remote(get_patterns_locally(data_dir), data_dir)
    imagefolder = ImageFolder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    with pytest.raises(ValueError) as exc_info:
        imagefolder.download_and_prepare()
    assert "`file_name` must be present" in str(exc_info.value)
