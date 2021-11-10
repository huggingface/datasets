import pytest

from datasets import Dataset
from datasets.features import Features, Image
from datasets.features.features import Value
from datasets.features.image import convert_pil_image_to_bytes


try:
    import PIL.Image

    PIL_AVAILABLE = True
except ImportError:
    PIL = None
    PIL.Image = None
    PIL_AVAILABLE = False


require_pil = pytest.mark.skipif(
    not PIL_AVAILABLE,
    reason="Test requires 'Pillow': `pip install Pillow",
)


def test_image_instantiation():
    image = Image()
    assert image.id is None
    assert image.dtype == "dict"
    assert image.pa_type is None
    assert image._type == "Image"


@require_pil
def test_image_decode_example(shared_datadir):
    image_path = str(shared_datadir / f"test_image_rgb.jpg")
    image = Image()
    decoded_example = image.decode_example(image_path)
    assert decoded_example.keys() == {"path", "image"}
    assert decoded_example["path"] == image_path

    assert isinstance(decoded_example["image"], PIL.Image.Image)
    assert decoded_example["image"].size == (640, 480)
    assert decoded_example["image"].mode == "RGB"


@require_pil
def test_dataset_with_image_feature(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert item["image"].keys() == {"path", "image"}
    assert item["image"]["path"] == image_path
    assert item["image"]["image"].size == (640, 480)
    assert item["image"]["image"].mode == "RGB"
    batch = dset[:1]
    assert batch.keys() == {"image"}
    assert len(batch["image"]) == 1
    assert batch["image"][0].keys() == {"path", "image"}
    assert batch["image"][0]["path"] == image_path
    assert batch["image"][0]["image"].size == (640, 480)
    assert batch["image"][0]["image"].mode == "RGB"
    column = dset["image"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "image"}
    assert column[0]["path"] == image_path
    assert column[0]["image"].size == (640, 480)
    assert column[0]["image"].mode == "RGB"


@require_pil
def test_dataset_with_image_feature_map(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    pil_image = Image().decode_example(image_path)["image"]
    data = {"image": [image_path], "caption": ["cats sleeping"]}
    features = Features({"image": Image(), "caption": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    for item in dset:
        assert item.keys() == {"image", "caption"}
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
        example["mode"] = example["image"]["image"].mode
        return example

    decoded_dset = dset.map(process_image_by_example)
    for item in decoded_dset:
        assert item.keys() == {"image", "caption", "mode"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] == image_path
        assert item["image"]["bytes"] == convert_pil_image_to_bytes(pil_image)
        assert item["caption"] == "cats sleeping"
        assert item["mode"] == "RGB"

    # decoding batch

    def process_image_by_batch(batch):
        modes = []
        for image in batch["image"]:
            modes.append(image["image"].mode)
        batch["mode"] = modes
        return batch

    decoded_dset = dset.map(process_image_by_batch, batched=True)
    for item in decoded_dset:
        assert item.keys() == {"image", "caption", "mode"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] == image_path
        assert item["image"]["bytes"] == convert_pil_image_to_bytes(pil_image)
        assert item["caption"] == "cats sleeping"
        assert item["mode"] == "RGB"


@require_pil
def test_dataset_with_image_feature_map_change_image(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    pil_image = Image().decode_example(image_path)["image"]
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)

    def process_image_resize_by_example(example):
        example["image"]["image"] = example["image"]["image"].resize((100, 100))
        return example

    decoded_dset = dset.map(process_image_resize_by_example)
    for item in decoded_dset:
        assert item.keys() == {"image"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] == image_path
        assert item["image"]["bytes"] == convert_pil_image_to_bytes(pil_image.resize((100, 100)))

    def process_image_resize_by_batch(batch):
        images = []
        for image in batch["image"]:
            image["image"] = image["image"].resize((100, 100))
            images.append(image)
        batch["image"] = images
        return batch

    decoded_dset = dset.map(process_image_resize_by_batch, batched=True)
    for item in decoded_dset:
        assert item.keys() == {"image"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] == image_path  # old path
        assert item["image"]["bytes"] == convert_pil_image_to_bytes(pil_image.resize((100, 100)))

    # return a list of images

    def process_image_resize_by_batch(batch):
        batch["image"] = [image["image"].resize((100, 100)) for image in batch["image"]]
        return batch

    decoded_dset = dset.map(process_image_resize_by_batch, batched=True)
    for item in decoded_dset:
        assert item.keys() == {"image"}
        assert item["image"].keys() == {"path", "bytes"}
        assert item["image"]["path"] is None  # delete path information
        assert item["image"]["bytes"] == convert_pil_image_to_bytes(pil_image.resize((100, 100)))


@pytest.mark.skip(reason="TODO: Support formatting with Pandas")
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
