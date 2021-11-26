import os

import pandas as pd
import pytest

from datasets import Dataset, load_dataset
from datasets.features import Features, Image
from datasets.features.features import Value
from datasets.features.image import image_to_bytes

from ..utils import require_pil


def test_image_instantiation():
    image = Image()
    assert image.id is None
    assert image.dtype == "dict"
    assert image.pa_type is None
    assert image._type == "Image"


@require_pil
def test_image_decode_example(shared_datadir):
    import PIL.Image

    image_path = str(shared_datadir / f"test_image_rgb.jpg")
    image = Image()
    decoded_example = image.decode_example(image_path)

    assert isinstance(decoded_example, PIL.Image.Image)
    assert os.path.samefile(decoded_example.filename, image_path)
    assert decoded_example.size == (640, 480)
    assert decoded_example.mode == "RGB"


@require_pil
def test_dataset_with_image_feature(shared_datadir):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)

    item = dset[0]
    assert item.keys() == {"image"}
    assert isinstance(item["image"], PIL.Image.Image)
    assert os.path.samefile(item["image"].filename, image_path)
    assert item["image"].size == (640, 480)
    assert item["image"].mode == "RGB"

    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"image"}
    assert isinstance(batch["image"], list) and all(isinstance(item, PIL.Image.Image) for item in batch["image"])
    assert os.path.samefile(batch["image"][0].filename, image_path)
    assert batch["image"][0].size == (640, 480)
    assert batch["image"][0].mode == "RGB"

    column = dset["image"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, PIL.Image.Image) for item in column)
    assert os.path.samefile(column[0].filename, image_path)
    assert column[0].size == (640, 480)
    assert column[0].mode == "RGB"


@require_pil
def test_dataset_with_image_feature_map(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    pil_image = Image().decode_example(image_path)
    data = {"image": [image_path], "caption": ["cats sleeping"]}
    features = Features({"image": Image(), "caption": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    for item in dset:
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] == image_path
        assert item["image"]["bytes"] is None
        assert item["caption"] == "cats sleeping"

    # no decoding

    def process_caption(example):
        example["caption"] = "Two " + example["caption"]
        return example

    processed_dset = dset.map(process_caption)
    for item in processed_dset:
        assert item.keys() == {"image", "caption"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] == image_path
        assert item["image"]["bytes"] is None
        assert item["caption"] == "Two cats sleeping"

    # decoding example

    def process_image_by_example(example):
        example["mode"] = example["image"].mode
        return example

    decoded_dset = dset.map(process_image_by_example)
    for item in decoded_dset:
        assert item.keys() == {"image", "caption", "mode"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] is None
        assert item["image"]["bytes"] == image_to_bytes(pil_image)
        assert item["caption"] == "cats sleeping"
        assert item["mode"] == "RGB"

    # decoding batch

    def process_image_by_batch(batch):
        batch["mode"] = [image.mode for image in batch["image"]]
        return batch

    decoded_dset = dset.map(process_image_by_batch, batched=True)
    for item in decoded_dset:
        assert item.keys() == {"image", "caption", "mode"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] is None
        assert item["image"]["bytes"] == image_to_bytes(pil_image)
        assert item["caption"] == "cats sleeping"
        assert item["mode"] == "RGB"


@require_pil
def test_dataset_with_image_feature_map_change_image(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    pil_image = Image().decode_example(image_path)
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)

    def process_image_resize_by_example(example):
        example["image"] = example["image"].resize((100, 100))
        return example

    decoded_dset = dset.map(process_image_resize_by_example)
    for item in decoded_dset:
        assert item.keys() == {"image"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] is None
        assert item["image"]["bytes"] == image_to_bytes(pil_image.resize((100, 100)))

    def process_image_resize_by_batch(batch):
        batch["image"] = [image.resize((100, 100)) for image in batch["image"]]
        return batch

    decoded_dset = dset.map(process_image_resize_by_batch, batched=True)
    for item in decoded_dset:
        assert item.keys() == {"image"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] is None
        assert item["image"]["bytes"] == image_to_bytes(pil_image.resize((100, 100)))

    # return a list of images

    def process_image_resize_by_batch(batch):
        batch["image"] = [image.resize((100, 100)) for image in batch["image"]]
        return batch

    decoded_dset = dset.map(process_image_resize_by_batch, batched=True)
    for item in decoded_dset:
        assert item.keys() == {"image"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] is None
        assert item["image"]["bytes"] == image_to_bytes(pil_image.resize((100, 100)))


@require_pil
def test_formatted_dataset_with_image_feature(shared_datadir):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path, image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"image"}
        assert isinstance(item["image"], PIL.Image.Image)
        assert os.path.samefile(item["image"].filename, image_path)
        assert item["image"].size == (640, 480)
        assert item["image"].mode == "RGB"
        batch = dset[:1]
        assert batch.keys() == {"image"}
        assert len(batch) == 1
        assert isinstance(batch["image"], list) and all(isinstance(item, PIL.Image.Image) for item in batch["image"])
        assert os.path.samefile(batch["image"][0].filename, image_path)
        assert batch["image"][0].size == (640, 480)
        assert batch["image"][0].mode == "RGB"
        column = dset["image"]
        assert len(column) == 2
        assert isinstance(column, list) and all(isinstance(item, PIL.Image.Image) for item in column)
        assert os.path.samefile(column[0].filename, image_path)
        assert column[0].size == (640, 480)
        assert column[0].mode == "RGB"

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["image"]
        assert isinstance(item["image"][0], PIL.Image.Image)
        assert os.path.samefile(item["image"][0].filename, image_path)
        assert item["image"][0].size == (640, 480)
        assert item["image"][0].mode == "RGB"
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["image"]
        assert isinstance(batch["image"], pd.Series) and all(
            isinstance(item, PIL.Image.Image) for item in batch["image"]
        )
        assert os.path.samefile(batch["image"][0].filename, image_path)
        assert batch["image"][0].size == (640, 480)
        assert batch["image"][0].mode == "RGB"
        column = dset["image"]
        assert len(column) == 2
        assert isinstance(column, pd.Series) and all(isinstance(item, PIL.Image.Image) for item in column)
        assert os.path.samefile(column[0].filename, image_path)
        assert column[0].size == (640, 480)
        assert column[0].mode == "RGB"


@pytest.fixture
def jsonl_image_dataset_path(shared_datadir, tmp_path_factory):
    import json

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = [{"image": image_path, "caption": "Two cats sleeping"}]
    path = str(tmp_path_factory.mktemp("data") / "image_dataset.jsonl")
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return path


@pytest.mark.skip(reason="TODO: fix issues with ExtensionType cast in json module")
@require_pil
@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_with_audio_feature(streaming, jsonl_image_dataset_path, shared_datadir):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data_files = jsonl_image_dataset_path
    features = Features({"image": Image(), "caption": Value("string")})
    dset = load_dataset("json", split="train", data_files=data_files, features=features, streaming=streaming)
    item = dset[0] if not streaming else next(iter(dset))
    assert item.keys() == {"image", "caption"}
    assert isinstance(item["image"], PIL.Image.Image)
    assert os.path.samefile(item["image"].filename, image_path)
    assert item["image"].size == (640, 480)
    assert item["image"].mode == "RGB"
