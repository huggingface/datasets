import os
import tarfile

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

from datasets import Dataset, Features, Image, Sequence, Value, load_dataset
from datasets.arrow_dataset import concatenate_datasets
from datasets.features.image import image_to_bytes

from ..utils import require_pil


@pytest.fixture
def tar_jpg_path(shared_datadir, tmp_path_factory):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    path = tmp_path_factory.mktemp("data") / "image_data.jpg.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(image_path, arcname=os.path.basename(image_path))
    return path


def iter_archive(archive_path):
    with tarfile.open(archive_path) as tar:
        for tarinfo in tar:
            file_path = tarinfo.name
            file_obj = tar.extractfile(tarinfo)
            yield file_path, file_obj


def test_image_instantiation():
    image = Image()
    assert image.id is None
    assert image.dtype == "PIL.Image.Image"
    assert image.pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert image._type == "Image"


def test_image_feature_type_to_arrow():
    features = Features({"image": Image()})
    assert features.arrow_schema == pa.schema({"image": Image().pa_type})
    features = Features({"struct_containing_an_image": {"image": Image()}})
    assert features.arrow_schema == pa.schema({"struct_containing_an_image": pa.struct({"image": Image().pa_type})})
    features = Features({"sequence_of_images": Sequence(Image())})
    assert features.arrow_schema == pa.schema({"sequence_of_images": pa.list_(Image().pa_type)})


@require_pil
@pytest.mark.parametrize(
    "build_example",
    [
        lambda image_path: image_path,
        lambda image_path: {"path": image_path},
        lambda image_path: {"path": image_path, "bytes": None},
        lambda image_path: {"path": image_path, "bytes": open(image_path, "rb").read()},
        lambda image_path: {"path": None, "bytes": open(image_path, "rb").read()},
        lambda image_path: {"bytes": open(image_path, "rb").read()},
    ],
)
def test_image_feature_encode_example(shared_datadir, build_example):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    image = Image()
    encoded_example = image.encode_example(build_example(image_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = image.decode_example(encoded_example)
    assert isinstance(decoded_example, PIL.Image.Image)


@require_pil
def test_image_decode_example(shared_datadir):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    image = Image()
    decoded_example = image.decode_example({"path": image_path, "bytes": None})

    assert isinstance(decoded_example, PIL.Image.Image)
    assert os.path.samefile(decoded_example.filename, image_path)
    assert decoded_example.size == (640, 480)
    assert decoded_example.mode == "RGB"

    with pytest.raises(RuntimeError):
        Image(decode=False).decode_example(image_path)


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
    assert item["image"].format == "JPEG"
    assert item["image"].size == (640, 480)
    assert item["image"].mode == "RGB"
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"image"}
    assert isinstance(batch["image"], list) and all(isinstance(item, PIL.Image.Image) for item in batch["image"])
    assert os.path.samefile(batch["image"][0].filename, image_path)
    assert batch["image"][0].format == "JPEG"
    assert batch["image"][0].size == (640, 480)
    assert batch["image"][0].mode == "RGB"
    column = dset["image"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, PIL.Image.Image) for item in column)
    assert os.path.samefile(column[0].filename, image_path)
    assert column[0].format == "JPEG"
    assert column[0].size == (640, 480)
    assert column[0].mode == "RGB"


@require_pil
@pytest.mark.parametrize("infer_feature", [False, True])
def test_dataset_with_image_feature_from_pil_image(infer_feature, shared_datadir):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [PIL.Image.open(image_path)]}
    features = Features({"image": Image()}) if not infer_feature else None
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert isinstance(item["image"], PIL.Image.Image)
    assert os.path.samefile(item["image"].filename, image_path)
    assert item["image"].format == "JPEG"
    assert item["image"].size == (640, 480)
    assert item["image"].mode == "RGB"
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"image"}
    assert isinstance(batch["image"], list) and all(isinstance(item, PIL.Image.Image) for item in batch["image"])
    assert os.path.samefile(batch["image"][0].filename, image_path)
    assert batch["image"][0].format == "JPEG"
    assert batch["image"][0].size == (640, 480)
    assert batch["image"][0].mode == "RGB"
    column = dset["image"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, PIL.Image.Image) for item in column)
    assert os.path.samefile(column[0].filename, image_path)
    assert column[0].format == "JPEG"
    assert column[0].size == (640, 480)
    assert column[0].mode == "RGB"


@require_pil
def test_dataset_with_image_feature_from_np_array():
    import PIL.Image

    image_array = np.arange(640 * 480, dtype=np.uint8).reshape(480, 640)
    data = {"image": [image_array]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert isinstance(item["image"], PIL.Image.Image)
    np.testing.assert_array_equal(np.array(item["image"]), image_array)
    assert item["image"].filename == ""
    assert item["image"].format == "PNG"
    assert item["image"].size == (640, 480)
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"image"}
    assert isinstance(batch["image"], list) and all(isinstance(item, PIL.Image.Image) for item in batch["image"])
    np.testing.assert_array_equal(np.array(batch["image"][0]), image_array)
    assert batch["image"][0].filename == ""
    assert batch["image"][0].format == "PNG"
    assert batch["image"][0].size == (640, 480)
    column = dset["image"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, PIL.Image.Image) for item in column)
    np.testing.assert_array_equal(np.array(column[0]), image_array)
    assert column[0].filename == ""
    assert column[0].format == "PNG"
    assert column[0].size == (640, 480)


@require_pil
def test_dataset_with_image_feature_tar_jpg(tar_jpg_path):
    import PIL.Image

    data = {"image": []}
    for file_path, file_obj in iter_archive(tar_jpg_path):
        data["image"].append({"path": file_path, "bytes": file_obj.read()})
        break

    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert isinstance(item["image"], PIL.Image.Image)
    assert item["image"].filename == ""
    assert item["image"].format == "JPEG"
    assert item["image"].size == (640, 480)
    assert item["image"].mode == "RGB"
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"image"}
    assert isinstance(batch["image"], list) and all(isinstance(item, PIL.Image.Image) for item in batch["image"])
    assert batch["image"][0].filename == ""
    assert batch["image"][0].format == "JPEG"
    assert batch["image"][0].size == (640, 480)
    assert batch["image"][0].mode == "RGB"
    column = dset["image"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, PIL.Image.Image) for item in column)
    assert column[0].filename == ""
    assert column[0].format == "JPEG"
    assert column[0].size == (640, 480)
    assert column[0].mode == "RGB"


@require_pil
@pytest.mark.parametrize(
    "build_data",
    [
        lambda image_path: {"image": [image_path]},
        lambda image_path: {"image": [{"path": image_path}]},
        lambda image_path: {"image": [{"path": image_path, "bytes": None}]},
        lambda image_path: {"image": [{"path": image_path, "bytes": open(image_path, "rb").read()}]},
        lambda image_path: {"image": [{"path": None, "bytes": open(image_path, "rb").read()}]},
        lambda image_path: {"image": [{"bytes": open(image_path, "rb").read()}]},
    ],
)
def test_dataset_cast_to_image_features(shared_datadir, build_data):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = build_data(image_path)
    dset = Dataset.from_dict(data)
    item = dset.cast(Features({"image": Image()}))[0]
    assert item.keys() == {"image"}
    assert isinstance(item["image"], PIL.Image.Image)
    item = dset.cast_column("image", Image())[0]
    assert item.keys() == {"image"}
    assert isinstance(item["image"], PIL.Image.Image)


@require_pil
def test_dataset_concatenate_image_features(shared_datadir):
    # we use a different data structure between 1 and 2 to make sure they are compatible with each other
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data1 = {"image": [image_path]}
    dset1 = Dataset.from_dict(data1, features=Features({"image": Image()}))
    data2 = {"image": [{"bytes": open(image_path, "rb").read()}]}
    dset2 = Dataset.from_dict(data2, features=Features({"image": Image()}))
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == len(dset1) + len(dset2)
    assert concatenated_dataset[0]["image"] == dset1[0]["image"]
    assert concatenated_dataset[1]["image"] == dset2[0]["image"]


@require_pil
def test_dataset_concatenate_nested_image_features(shared_datadir):
    # we use a different data structure between 1 and 2 to make sure they are compatible with each other
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    features = Features({"list_of_structs_of_images": [{"image": Image()}]})
    data1 = {"list_of_structs_of_images": [[{"image": image_path}]]}
    dset1 = Dataset.from_dict(data1, features=features)
    data2 = {"list_of_structs_of_images": [[{"image": {"bytes": open(image_path, "rb").read()}}]]}
    dset2 = Dataset.from_dict(data2, features=features)
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == len(dset1) + len(dset2)
    assert (
        concatenated_dataset[0]["list_of_structs_of_images"][0]["image"]
        == dset1[0]["list_of_structs_of_images"][0]["image"]
    )
    assert (
        concatenated_dataset[1]["list_of_structs_of_images"][0]["image"]
        == dset2[0]["list_of_structs_of_images"][0]["image"]
    )


@require_pil
def test_dataset_with_image_feature_map(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path], "caption": ["cats sleeping"]}
    features = Features({"image": Image(), "caption": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    for item in dset._iter(decoded=False):
        assert item.keys() == {"image", "caption"}
        assert item == {"image": {"path": image_path, "bytes": None}, "caption": "cats sleeping"}

    # no decoding

    def process_caption(example):
        example["caption"] = "Two " + example["caption"]
        return example

    processed_dset = dset.map(process_caption)
    for item in processed_dset._iter(decoded=False):
        assert item.keys() == {"image", "caption"}
        assert item == {"image": {"path": image_path, "bytes": None}, "caption": "Two cats sleeping"}

    # decoding example

    def process_image_by_example(example):
        example["mode"] = example["image"].mode
        return example

    decoded_dset = dset.map(process_image_by_example)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"image", "caption", "mode"}
        assert os.path.samefile(item["image"]["path"], image_path)
        assert item["caption"] == "cats sleeping"
        assert item["mode"] == "RGB"

    # decoding batch

    def process_image_by_batch(batch):
        batch["mode"] = [image.mode for image in batch["image"]]
        return batch

    decoded_dset = dset.map(process_image_by_batch, batched=True)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"image", "caption", "mode"}
        assert os.path.samefile(item["image"]["path"], image_path)
        assert item["caption"] == "cats sleeping"
        assert item["mode"] == "RGB"


@require_pil
def test_dataset_with_image_feature_map_change_image(shared_datadir):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    pil_image = Image().decode_example({"path": image_path, "bytes": None})
    data = {"image": [image_path]}
    features = Features({"image": Image()})
    dset = Dataset.from_dict(data, features=features)

    for item in dset._iter(decoded=False):
        assert item.keys() == {"image"}
        assert item == {
            "image": {
                "bytes": None,
                "path": image_path,
            }
        }

    # return pil image

    def process_image_resize_by_example(example):
        example["image"] = example["image"].resize((100, 100))
        return example

    decoded_dset = dset.map(process_image_resize_by_example)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"image"}
        assert item == {"image": {"bytes": image_to_bytes(pil_image.resize((100, 100))), "path": None}}

    def process_image_resize_by_batch(batch):
        batch["image"] = [image.resize((100, 100)) for image in batch["image"]]
        return batch

    decoded_dset = dset.map(process_image_resize_by_batch, batched=True)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"image"}
        assert item == {"image": {"bytes": image_to_bytes(pil_image.resize((100, 100))), "path": None}}

    # return np.ndarray (e.g. when using albumentations)

    def process_image_resize_by_example_return_np_array(example):
        example["image"] = np.array(example["image"].resize((100, 100)))
        return example

    decoded_dset = dset.map(process_image_resize_by_example_return_np_array)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"image"}
        assert item == {
            "image": {
                "bytes": image_to_bytes(PIL.Image.fromarray(np.array(pil_image.resize((100, 100))))),
                "path": None,
            }
        }

    def process_image_resize_by_batch_return_np_array(batch):
        batch["image"] = [np.array(image.resize((100, 100))) for image in batch["image"]]
        return batch

    decoded_dset = dset.map(process_image_resize_by_batch_return_np_array, batched=True)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"image"}
        assert item == {
            "image": {
                "bytes": image_to_bytes(PIL.Image.fromarray(np.array(pil_image.resize((100, 100))))),
                "path": None,
            }
        }


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
        assert item["image"].format == "JPEG"
        assert item["image"].size == (640, 480)
        assert item["image"].mode == "RGB"
        batch = dset[:1]
        assert batch.keys() == {"image"}
        assert len(batch) == 1
        assert isinstance(batch["image"], list) and all(isinstance(item, PIL.Image.Image) for item in batch["image"])
        assert os.path.samefile(batch["image"][0].filename, image_path)
        assert batch["image"][0].format == "JPEG"
        assert batch["image"][0].size == (640, 480)
        assert batch["image"][0].mode == "RGB"
        column = dset["image"]
        assert len(column) == 2
        assert isinstance(column, list) and all(isinstance(item, PIL.Image.Image) for item in column)
        assert os.path.samefile(column[0].filename, image_path)
        assert column[0].format == "JPEG"
        assert column[0].size == (640, 480)
        assert column[0].mode == "RGB"

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["image"]
        assert isinstance(item["image"][0], PIL.Image.Image)
        assert os.path.samefile(item["image"][0].filename, image_path)
        assert item["image"][0].format == "JPEG"
        assert item["image"][0].size == (640, 480)
        assert item["image"][0].mode == "RGB"
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["image"]
        assert isinstance(batch["image"], pd.Series) and all(
            isinstance(item, PIL.Image.Image) for item in batch["image"]
        )
        assert os.path.samefile(batch["image"][0].filename, image_path)
        assert batch["image"][0].format == "JPEG"
        assert batch["image"][0].size == (640, 480)
        assert batch["image"][0].mode == "RGB"
        column = dset["image"]
        assert len(column) == 2
        assert isinstance(column, pd.Series) and all(isinstance(item, PIL.Image.Image) for item in column)
        assert os.path.samefile(column[0].filename, image_path)
        assert column[0].format == "JPEG"
        assert column[0].size == (640, 480)
        assert column[0].mode == "RGB"


# Currently, the JSONL reader doesn't support complex feature types so we create a temporary dataset script
# to test streaming (without uploading the test dataset to the hub).

DATASET_LOADING_SCRIPT_NAME = "__dummy_dataset__"

DATASET_LOADING_SCRIPT_CODE = """
import os

import datasets
from datasets import DatasetInfo, Features, Image, Split, SplitGenerator, Value


class __DummyDataset__(datasets.GeneratorBasedBuilder):

    def _info(self) -> DatasetInfo:
        return DatasetInfo(features=Features({"image": Image(), "caption": Value("string")}))

    def _split_generators(self, dl_manager):
        return [
            SplitGenerator(Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_manager.manual_dir, "train.txt")}),
        ]

    def _generate_examples(self, filepath, **kwargs):
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                image_path, caption = line.split(",")
                yield i, {"image": image_path.strip(), "caption": caption.strip()}
"""


@pytest.fixture
def data_dir(shared_datadir, tmp_path):
    data_dir = tmp_path / "dummy_dataset_data"
    data_dir.mkdir()
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    with open(data_dir / "train.txt", "w") as f:
        f.write(f"{image_path},Two cats sleeping\n")
    return str(data_dir)


@pytest.fixture
def dataset_loading_script_dir(tmp_path):
    script_name = DATASET_LOADING_SCRIPT_NAME
    script_dir = tmp_path / script_name
    script_dir.mkdir()
    script_path = script_dir / f"{script_name}.py"
    with open(script_path, "w") as f:
        f.write(DATASET_LOADING_SCRIPT_CODE)
    return str(script_dir)


@require_pil
@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_with_image_feature(shared_datadir, data_dir, dataset_loading_script_dir, streaming):
    import PIL.Image

    image_path = str(shared_datadir / "test_image_rgb.jpg")
    dset = load_dataset(dataset_loading_script_dir, split="train", data_dir=data_dir, streaming=streaming)
    item = dset[0] if not streaming else next(iter(dset))
    assert item.keys() == {"image", "caption"}
    assert isinstance(item["image"], PIL.Image.Image)
    assert os.path.samefile(item["image"].filename, image_path)
    assert item["image"].format == "JPEG"
    assert item["image"].size == (640, 480)
    assert item["image"].mode == "RGB"


@require_pil
def test_dataset_with_image_feature_undecoded(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image(decode=False)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert item["image"] == {"path": image_path, "bytes": None}
    batch = dset[:1]
    assert batch.keys() == {"image"}
    assert len(batch["image"]) == 1
    assert batch["image"][0] == {"path": image_path, "bytes": None}
    column = dset["image"]
    assert len(column) == 1
    assert column[0] == {"path": image_path, "bytes": None}


@require_pil
def test_formatted_dataset_with_image_feature_undecoded(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image(decode=False)})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"image"}
        assert item["image"] == {"path": image_path, "bytes": None}
        batch = dset[:1]
        assert batch.keys() == {"image"}
        assert len(batch["image"]) == 1
        assert batch["image"][0] == {"path": image_path, "bytes": None}
        column = dset["image"]
        assert len(column) == 1
        assert column[0] == {"path": image_path, "bytes": None}

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["image"]
        assert item["image"][0] == {"path": image_path, "bytes": None}
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["image"]
        assert batch["image"][0] == {"path": image_path, "bytes": None}
        column = dset["image"]
        assert len(column) == 1
        assert column[0] == {"path": image_path, "bytes": None}


@require_pil
def test_dataset_with_image_feature_map_undecoded(shared_datadir):
    image_path = str(shared_datadir / "test_image_rgb.jpg")
    data = {"image": [image_path]}
    features = Features({"image": Image(decode=False)})
    dset = Dataset.from_dict(data, features=features)

    def assert_image_example_undecoded(example):
        assert example["image"] == {"path": image_path, "bytes": None}

    dset.map(assert_image_example_undecoded)

    def assert_image_batch_undecoded(batch):
        for image in batch["image"]:
            assert image == {"path": image_path, "bytes": None}

    dset.map(assert_image_batch_undecoded, batched=True)
