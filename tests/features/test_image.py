from importlib.util import find_spec

import pytest

from datasets import Dataset
from datasets.features import Features, Image
from datasets.features.features import Value


require_pil = pytest.mark.skipif(
    find_spec("PIL") is None,
    reason="Test requires 'Pillow': `pip install Pillow",
)


@require_pil
def test_image_instantiation():
    image = Image()
    assert image.id is None
    assert image.dtype == "dict"
    assert image.pa_type is None
    assert image._type == "Image"
    assert image.mode is None

    assert Image(mode="RGB").mode == "RGB"

    with pytest.raises(ValueError):
        Image(mode="dummy_mode")


@require_pil
def test_image_decode_example(shared_datadir):
    image_path = str(shared_datadir / f"test_image_rgb.jpg")
    image = Image()
    decoded_example = image.decode_example(image_path)
    assert decoded_example.keys() == {"path", "array", "mode"}
    assert decoded_example["path"] == image_path
    assert decoded_example["mode"] == "RGB"
    assert decoded_example["array"].shape == (3, 480, 640)


@require_pil
def test_image_change_mode(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    # convert to a greyscale (single-channel) image
    image = Image(mode="L")
    decoded_example = image.decode_example(image_path)
    assert decoded_example.keys() == {"path", "array", "mode"}
    assert decoded_example["path"] == image_path
    assert decoded_example["array"].shape == (1, 480, 640)
    assert decoded_example["mode"] == "L"


@require_pil
def test_dataset_with_image_feature(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert item["image"].keys() == {"path", "array", "mode"}
    assert item["image"]["path"] == image_path
    assert item["image"]["array"].shape == (3, 480, 640)
    assert item["image"]["mode"] == "RGB"
    batch = dset[:1]
    assert batch.keys() == {"image"}
    assert len(batch["image"]) == 1
    assert batch["image"][0].keys() == {"path", "array", "mode"}
    assert batch["image"][0]["path"] == image_path
    assert batch["image"][0]["array"].shape == (3, 480, 640)
    assert batch["image"][0]["mode"] == "RGB"
    column = dset["image"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "mode"}
    assert column[0]["path"] == image_path
    assert column[0]["array"].shape == (3, 480, 640)
    assert column[0]["mode"] == "RGB"


@require_pil
def test_change_mode_on_dataset_with_image_feature(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image(mode="L")})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert item["image"].keys() == {"path", "array", "mode"}
    assert item["image"]["path"] == image_path
    assert item["image"]["array"].shape == (1, 480, 640)
    assert item["image"]["mode"] == "L"
    batch = dset[:1]
    assert batch.keys() == {"image"}
    assert len(batch["image"]) == 1
    assert batch["image"][0].keys() == {"path", "array", "mode"}
    assert batch["image"][0]["path"] == image_path
    assert batch["image"][0]["array"].shape == (1, 480, 640)
    assert batch["image"][0]["mode"] == "L"
    column = dset["image"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "mode"}
    assert column[0]["path"] == image_path
    assert column[0]["array"].shape == (1, 480, 640)
    assert column[0]["mode"] == "L"


@require_pil
def test_cast_column_on_dataset_with_image_feature(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item["image"]["mode"] == "RGB"
    dset = dset.cast_column("image", Image(mode="L"))
    item = dset[0]
    assert item["image"]["mode"] == "L"


@require_pil
def test_dataset_with_image_feature_map(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path], "caption": ["cats sleeping"]}
    features = Features({"image": Image(), "caption": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    for item in dset:
        assert item.keys() == {"image", "caption"}
        assert item == {"image": image_path, "caption": "cats sleeping"}

    # no decoding

    def process_caption(example):
        example["caption"] = "Two " + example["caption"]
        return example

    processed_dset = dset.map(process_caption)
    for item in processed_dset:
        assert item.keys() == {"image", "caption"}
        assert item == {"image": image_path, "caption": "Two cats sleeping"}

    # decoding example

    def process_image_mode_by_example(example):
        example["mode_lowercase"] = example["image"]["mode"].lower()
        return example

    decoded_dset = dset.map(process_image_mode_by_example)
    for item in decoded_dset:
        assert item.keys() == {"image", "caption", "mode_lowercase"}
        assert item["mode_lowercase"] == "rgb"

    # decoding batch

    def process_image_mode_by_batch(batch):
        modes_lowercase = []
        for image in batch["image"]:
            modes_lowercase.append(image["mode"].lower())
        batch["mode_lowercase"] = modes_lowercase
        return batch

    decoded_dset = dset.map(process_image_mode_by_batch, batched=True)
    for item in decoded_dset:
        assert item.keys() == {"image", "caption", "mode_lowercase"}
        assert item["mode_lowercase"] == "rgb"


@require_pil
def test_formatted_dataset_with_image_feature(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path, image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"image"}
        assert item["image"].keys() == {"path", "array", "mode"}
        assert item["image"]["path"] == image_path
        assert item["image"]["array"].shape == (3, 480, 640)
        assert item["image"]["mode"] == "RGB"
        batch = dset[:1]
        assert batch.keys() == {"image"}
        assert len(batch["image"]) == 1
        assert batch["image"][0].keys() == {"path", "array", "mode"}
        assert batch["image"][0]["path"] == image_path
        assert batch["image"][0]["array"].shape == (3, 480, 640)
        assert batch["image"][0]["mode"] == "RGB"
        column = dset["image"]
        assert len(column) == 2
        assert column[0].keys() == {"path", "array", "mode"}
        assert column[0]["path"] == image_path
        assert column[0]["array"].shape == (3, 480, 640)
        assert column[0]["mode"] == "RGB"

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["image"]
        assert item["image"][0].keys() == {"path", "array", "mode"}
        assert item["image"][0]["path"] == image_path
        assert item["image"][0]["array"].shape == (3, 480, 640)
        assert item["image"][0]["mode"] == "RGB"
        item = dset[:1]
        assert item.shape == (1, 1)
        assert item.columns == ["image"]
        assert item["image"][0].keys() == {"path", "array", "mode"}
        assert item["image"][0]["path"] == image_path
        assert item["image"][0]["array"].shape == (3, 480, 640)
        assert item["image"][0]["mode"] == "RGB"
        column = dset["image"]
        assert len(column) == 2
        assert column[0].keys() == {"path", "array", "mode"}
        assert column[0]["path"] == image_path
        assert column[0]["array"].shape == (3, 480, 640)
        assert column[0]["mode"] == "RGB"
