import json
import tarfile

import numpy as np
import pytest

from datasets import Audio, DownloadManager, Features, Image, Value
from datasets.packaged_modules.webdataset.webdataset import WebDataset

from ..utils import require_pil, require_sndfile


@pytest.fixture
def image_wds_file(tmp_path, image_file):
    json_file = tmp_path / "data.json"
    filename = tmp_path / "file.tar"
    num_examples = 3
    with json_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"caption": "this is an image"}))
    with tarfile.open(str(filename), "w") as f:
        for example_idx in range(num_examples):
            f.add(json_file, f"{example_idx:05d}.json")
            f.add(image_file, f"{example_idx:05d}.jpg")
    return str(filename)


@pytest.fixture
def audio_wds_file(tmp_path, audio_file):
    json_file = tmp_path / "data.json"
    filename = tmp_path / "file.tar"
    num_examples = 3
    with json_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"transcript": "this is a transcript"}))
    with tarfile.open(str(filename), "w") as f:
        for example_idx in range(num_examples):
            f.add(json_file, f"{example_idx:05d}.json")
            f.add(audio_file, f"{example_idx:05d}.wav")
    return str(filename)


@pytest.fixture
def bad_wds_file(tmp_path, image_file, text_file):
    json_file = tmp_path / "data.json"
    filename = tmp_path / "bad_file.tar"
    with json_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"caption": "this is an image"}))
    with tarfile.open(str(filename), "w") as f:
        f.add(image_file)
        f.add(json_file)
    return str(filename)


@require_pil
def test_image_webdataset(image_wds_file):
    import PIL.Image

    data_files = {"train": [image_wds_file]}
    webdataset = WebDataset(data_files=data_files)
    split_generators = webdataset._split_generators(DownloadManager())
    assert webdataset.info.features == Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            "json": {"caption": Value("string")},
            "jpg": Image(),
        }
    )
    assert len(split_generators) == 1
    split_generator = split_generators[0]
    assert split_generator.name == "train"
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)
    _, examples = zip(*generator)
    assert len(examples) == 3
    assert isinstance(examples[0]["json"], dict)
    assert isinstance(examples[0]["json"]["caption"], str)
    assert isinstance(examples[0]["jpg"], dict)  # keep encoded to avoid unecessary copies
    encoded = webdataset.info.features.encode_example(examples[0])
    decoded = webdataset.info.features.decode_example(encoded)
    assert isinstance(decoded["json"], dict)
    assert isinstance(decoded["json"]["caption"], str)
    assert isinstance(decoded["jpg"], PIL.Image.Image)


@require_sndfile
def test_audio_webdataset(audio_wds_file):
    data_files = {"train": [audio_wds_file]}
    webdataset = WebDataset(data_files=data_files)
    split_generators = webdataset._split_generators(DownloadManager())
    assert webdataset.info.features == Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            "json": {"transcript": Value("string")},
            "wav": Audio(),
        }
    )
    assert len(split_generators) == 1
    split_generator = split_generators[0]
    assert split_generator.name == "train"
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)
    _, examples = zip(*generator)
    assert len(examples) == 3
    assert isinstance(examples[0]["json"], dict)
    assert isinstance(examples[0]["json"]["transcript"], str)
    assert isinstance(examples[0]["wav"], dict)
    assert isinstance(examples[0]["wav"]["bytes"], bytes)  # keep encoded to avoid unecessary copies
    encoded = webdataset.info.features.encode_example(examples[0])
    decoded = webdataset.info.features.decode_example(encoded)
    assert isinstance(decoded["json"], dict)
    assert isinstance(decoded["json"]["transcript"], str)
    assert isinstance(decoded["wav"], dict)
    assert isinstance(decoded["wav"]["array"], np.ndarray)


def test_webdataset_errors_on_bad_file(bad_wds_file):
    data_files = {"train": [bad_wds_file]}
    webdataset = WebDataset(data_files=data_files)
    with pytest.raises(ValueError):
        webdataset._split_generators(DownloadManager())


@require_pil
def test_webdataset_with_features(image_wds_file):
    import PIL.Image

    data_files = {"train": [image_wds_file]}
    features = Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            "json": {"caption": Value("string"), "additional_field": Value("int64")},
            "jpg": Image(),
        }
    )
    webdataset = WebDataset(data_files=data_files, features=features)
    split_generators = webdataset._split_generators(DownloadManager())
    assert webdataset.info.features == features
    split_generator = split_generators[0]
    assert split_generator.name == "train"
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)
    _, example = next(iter(generator))
    encoded = webdataset.info.features.encode_example(example)
    decoded = webdataset.info.features.decode_example(encoded)
    assert decoded["json"]["additional_field"] is None
    assert isinstance(decoded["json"], dict)
    assert isinstance(decoded["json"]["caption"], str)
    assert isinstance(decoded["jpg"], PIL.Image.Image)
