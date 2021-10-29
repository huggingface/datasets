from importlib.util import find_spec

import pytest

from datasets import Dataset
from datasets.features import Image, Features


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
@pytest.mark.parametrize("format", "jpg", "png", "bmp", "gif"])
def test_image_decode_example(shared_datadir, format):
    image_path = str(shared_datadir / f"test_image_rgb.{format}")
    image = Image()
    decoded_example = image.decode_example(image_path)
    assert decoded_example.keys() == {"path", "array", "mode"}
    assert decoded_example["path"] == image_path
    assert decoded_example["mode"] == "RGB" if format != "gif" else "P"
    assert decoded_example["array"].shape == (3, 480, 640) if format != "gif" else (1, 480, 640)


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
    features = Features({"audio": Image()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"image"}
    assert item["image"].keys() == {"path", "array", "mode"}
    assert item["image"]["path"] == image_path
    assert item["image"]["array"].shape == (3, 480, 640)
    assert item["image"]["mode"] == 44100
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_path
    assert batch["audio"][0]["array"].shape == (202311,)
    assert batch["audio"][0]["sampling_rate"] == 44100
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_path
    assert column[0]["array"].shape == (202311,)
    assert column[0]["sampling_rate"] == 44100


# @require_sndfile
# def test_resampling_at_loading_dataset_with_audio_feature(shared_datadir):
#     audio_path = str(shared_datadir / "test_audio_44100.wav")
#     data = {"audio": [audio_path]}
#     features = Features({"audio": Audio(sampling_rate=16000)})
#     dset = Dataset.from_dict(data, features=features)
#     item = dset[0]
#     assert item.keys() == {"audio"}
#     assert item["audio"].keys() == {"path", "array", "sampling_rate"}
#     assert item["audio"]["path"] == audio_path
#     assert item["audio"]["array"].shape == (73401,)
#     assert item["audio"]["sampling_rate"] == 16000
#     batch = dset[:1]
#     assert batch.keys() == {"audio"}
#     assert len(batch["audio"]) == 1
#     assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
#     assert batch["audio"][0]["path"] == audio_path
#     assert batch["audio"][0]["array"].shape == (73401,)
#     assert batch["audio"][0]["sampling_rate"] == 16000
#     column = dset["audio"]
#     assert len(column) == 1
#     assert column[0].keys() == {"path", "array", "sampling_rate"}
#     assert column[0]["path"] == audio_path
#     assert column[0]["array"].shape == (73401,)
#     assert column[0]["sampling_rate"] == 16000


# @require_sndfile
# def test_resampling_after_loading_dataset_with_audio_feature(shared_datadir):
#     audio_path = str(shared_datadir / "test_audio_44100.wav")
#     data = {"audio": [audio_path]}
#     features = Features({"audio": Audio()})
#     dset = Dataset.from_dict(data, features=features)
#     item = dset[0]
#     assert item["audio"]["sampling_rate"] == 44100
#     dset = dset.cast_column("audio", Audio(sampling_rate=16000))
#     item = dset[0]
#     assert item.keys() == {"audio"}
#     assert item["audio"].keys() == {"path", "array", "sampling_rate"}
#     assert item["audio"]["path"] == audio_path
#     assert item["audio"]["array"].shape == (73401,)
#     assert item["audio"]["sampling_rate"] == 16000
#     batch = dset[:1]
#     assert batch.keys() == {"audio"}
#     assert len(batch["audio"]) == 1
#     assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
#     assert batch["audio"][0]["path"] == audio_path
#     assert batch["audio"][0]["array"].shape == (73401,)
#     assert batch["audio"][0]["sampling_rate"] == 16000
#     column = dset["audio"]
#     assert len(column) == 1
#     assert column[0].keys() == {"path", "array", "sampling_rate"}
#     assert column[0]["path"] == audio_path
#     assert column[0]["array"].shape == (73401,)
#     assert column[0]["sampling_rate"] == 16000


# @require_sox
# @require_sndfile
# def test_resampling_after_loading_dataset_with_audio_feature_mp3(shared_datadir):
#     audio_path = str(shared_datadir / "test_audio_44100.mp3")
#     data = {"audio": [audio_path]}
#     features = Features({"audio": Audio()})
#     dset = Dataset.from_dict(data, features=features)
#     item = dset[0]
#     assert item["audio"]["sampling_rate"] == 44100
#     dset = dset.cast_column("audio", Audio(sampling_rate=16000))
#     item = dset[0]
#     assert item.keys() == {"audio"}
#     assert item["audio"].keys() == {"path", "array", "sampling_rate"}
#     assert item["audio"]["path"] == audio_path
#     assert item["audio"]["array"].shape == (39707,)
#     assert item["audio"]["sampling_rate"] == 16000
#     batch = dset[:1]
#     assert batch.keys() == {"audio"}
#     assert len(batch["audio"]) == 1
#     assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
#     assert batch["audio"][0]["path"] == audio_path
#     assert batch["audio"][0]["array"].shape == (39707,)
#     assert batch["audio"][0]["sampling_rate"] == 16000
#     column = dset["audio"]
#     assert len(column) == 1
#     assert column[0].keys() == {"path", "array", "sampling_rate"}
#     assert column[0]["path"] == audio_path
#     assert column[0]["array"].shape == (39707,)
#     assert column[0]["sampling_rate"] == 16000


# @require_sndfile
# def test_dataset_with_audio_feature_map_is_not_decoded(shared_datadir):
#     audio_path = str(shared_datadir / "test_audio_44100.wav")
#     data = {"audio": [audio_path], "text": ["Hello"]}
#     features = Features({"audio": Audio(), "text": Value("string")})
#     dset = Dataset.from_dict(data, features=features)

#     for item in dset:
#         assert item.keys() == {"audio", "text"}
#         assert item == {"audio": audio_path, "text": "Hello"}

#     def process_text(example):
#         example["text"] = example["text"] + " World!"
#         return example

#     processed_dset = dset.map(process_text)
#     for item in processed_dset:
#         assert item.keys() == {"audio", "text"}
#         assert item == {"audio": audio_path, "text": "Hello World!"}


# @require_sndfile
# def test_dataset_with_audio_feature_map_is_decoded(shared_datadir):
#     audio_path = str(shared_datadir / "test_audio_44100.wav")
#     data = {"audio": [audio_path], "text": ["Hello"]}
#     features = Features({"audio": Audio(), "text": Value("string")})
#     dset = Dataset.from_dict(data, features=features)

#     def process_audio_sampling_rate_by_example(example):
#         example["double_sampling_rate"] = 2 * example["audio"]["sampling_rate"]
#         return example

#     decoded_dset = dset.map(process_audio_sampling_rate_by_example)
#     for item in decoded_dset:
#         assert item.keys() == {"audio", "text", "double_sampling_rate"}
#         assert item["double_sampling_rate"] == 88200

#     def process_audio_sampling_rate_by_batch(batch):
#         double_sampling_rates = []
#         for audio in batch["audio"]:
#             double_sampling_rates.append(2 * audio["sampling_rate"])
#         batch["double_sampling_rate"] = double_sampling_rates
#         return batch

#     decoded_dset = dset.map(process_audio_sampling_rate_by_batch, batched=True)
#     for item in decoded_dset:
#         assert item.keys() == {"audio", "text", "double_sampling_rate"}
#         assert item["double_sampling_rate"] == 88200


# @require_sndfile
# def test_formatted_dataset_with_audio_feature(shared_datadir):
#     audio_path = str(shared_datadir / "test_audio_44100.wav")
#     data = {"audio": [audio_path, audio_path]}
#     features = Features({"audio": Audio()})
#     dset = Dataset.from_dict(data, features=features)
#     with dset.formatted_as("numpy"):
#         item = dset[0]
#         assert item.keys() == {"audio"}
#         assert item["audio"].keys() == {"path", "array", "sampling_rate"}
#         assert item["audio"]["path"] == audio_path
#         assert item["audio"]["array"].shape == (202311,)
#         assert item["audio"]["sampling_rate"] == 44100
#         batch = dset[:1]
#         assert batch.keys() == {"audio"}
#         assert len(batch["audio"]) == 1
#         assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
#         assert batch["audio"][0]["path"] == audio_path
#         assert batch["audio"][0]["array"].shape == (202311,)
#         assert batch["audio"][0]["sampling_rate"] == 44100
#         column = dset["audio"]
#         assert len(column) == 2
#         assert column[0].keys() == {"path", "array", "sampling_rate"}
#         assert column[0]["path"] == audio_path
#         assert column[0]["array"].shape == (202311,)
#         assert column[0]["sampling_rate"] == 44100

#     with dset.formatted_as("pandas"):
#         item = dset[0]
#         assert item.shape == (1, 1)
#         assert item.columns == ["audio"]
#         assert item["audio"][0].keys() == {"path", "array", "sampling_rate"}
#         assert item["audio"][0]["path"] == audio_path
#         assert item["audio"][0]["array"].shape == (202311,)
#         assert item["audio"][0]["sampling_rate"] == 44100
#         item = dset[:1]
#         assert item.shape == (1, 1)
#         assert item.columns == ["audio"]
#         assert item["audio"][0].keys() == {"path", "array", "sampling_rate"}
#         assert item["audio"][0]["path"] == audio_path
#         assert item["audio"][0]["array"].shape == (202311,)
#         assert item["audio"][0]["sampling_rate"] == 44100
#         column = dset["audio"]
#         assert len(column) == 2
#         assert column[0].keys() == {"path", "array", "sampling_rate"}
#         assert column[0]["path"] == audio_path
#         assert column[0]["array"].shape == (202311,)
#         assert column[0]["sampling_rate"] == 44100


# @require_sndfile
# def test_dataset_with_audio_feature_loaded_from_cache():
#     # load first time
#     ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean")
#     # load from cache
#     ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")
#     assert isinstance(ds, Dataset)
