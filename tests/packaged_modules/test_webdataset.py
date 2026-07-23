import json
import re
import tarfile
from pathlib import Path

import pytest

from datasets import Audio, DownloadManager, Features, Image, List, Value, Video
from datasets.packaged_modules.webdataset.webdataset import WebDataset
from datasets.utils.track import tracked_str

from ..utils import (
    require_numpy1_on_windows,
    require_pil,
    require_torch,
    require_torchcodec,
)


@pytest.fixture
def gzipped_text_wds_file(tmp_path, text_gz_path):
    filename = tmp_path / "file.tar"
    num_examples = 3
    with tarfile.open(str(filename), "w") as f:
        for example_idx in range(num_examples):
            f.add(text_gz_path, f"{example_idx:05d}.txt.gz")
    return str(filename)


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
def upper_lower_case_file(tmp_path):
    tar_path = tmp_path / "file.tar"
    num_examples = 3
    variants = [
        ("INFO1", "json"),
        ("info2", "json"),
        ("info3", "JSON"),
        ("info3", "json"),  # should probably remove if testing on a case insensitive filesystem
    ]
    with tarfile.open(tar_path, "w") as tar:
        for example_idx in range(num_examples):
            example_name = f"{example_idx:05d}_{'a' if example_idx % 2 else 'A'}"
            for tag, ext in variants:
                caption_path = tmp_path / f"{example_name}.{tag}.{ext}"
                caption_text = {"caption": f"caption for {example_name}.{tag}.{ext}"}
                caption_path.write_text(json.dumps(caption_text), encoding="utf-8")
                tar.add(caption_path, arcname=f"{example_name}.{tag}.{ext}")
    return str(tar_path)


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
def video_wds_file(tmp_path):
    json_file = tmp_path / "data.json"
    filename = tmp_path / "file.tar"
    video_file = Path(__file__).resolve().parents[1] / "features" / "data" / "test_video_66x50.mov"
    num_examples = 3
    with json_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"caption": "this is a video"}))
    with tarfile.open(str(filename), "w") as f:
        for example_idx in range(num_examples):
            f.add(json_file, f"{example_idx:05d}.json")
            f.add(video_file, f"{example_idx:05d}.mov")
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


@pytest.fixture
def corrupted_wds_file(tmp_path):
    filename = tmp_path / "corrupted.tar"
    filename.touch()
    return str(filename)


@pytest.fixture
def valid_text_wds_file(tmp_path):
    data_file = tmp_path / "valid.txt"
    data_file.write_text("valid", encoding="utf-8")
    filename = tmp_path / "valid.tar"
    with tarfile.open(filename, "w") as tar:
        tar.add(data_file, arcname="00000.txt")
    return str(filename)


@pytest.fixture
def truncated_wds_file(tmp_path):
    data_file = tmp_path / "data.txt"
    data_file.write_bytes(b"x" * 1024)
    filename = tmp_path / "truncated.tar"
    with tarfile.open(filename, "w") as tar:
        tar.add(data_file, arcname="00000.txt")
    filename.write_bytes(filename.read_bytes()[:612])
    return str(filename)


@pytest.fixture
def tensor_wds_file(tmp_path, tensor_file):
    json_file = tmp_path / "data.json"
    filename = tmp_path / "file.tar"
    num_examples = 3
    with json_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"text": "this is a text"}))
    with tarfile.open(str(filename), "w") as f:
        for example_idx in range(num_examples):
            f.add(json_file, f"{example_idx:05d}.json")
            f.add(tensor_file, f"{example_idx:05d}.pth")
    return str(filename)


@require_pil
def test_gzipped_text_webdataset(gzipped_text_wds_file, text_path):
    data_files = {"train": [gzipped_text_wds_file]}
    webdataset = WebDataset(data_files=data_files)
    split_generators = webdataset._split_generators(DownloadManager())
    assert webdataset.info.features == Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            "txt.gz": Value("string"),
        }
    )
    assert len(split_generators) == 1
    split_generator = split_generators[0]
    assert split_generator.name == "train"
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)
    _, examples = zip(*generator)
    assert len(examples) == 3
    assert isinstance(examples[0]["txt.gz"], str)
    with open(text_path, "r") as f:
        assert examples[0]["txt.gz"].replace("\r\n", "\n") == f.read().replace("\r\n", "\n")


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


def test_upper_lower_case(upper_lower_case_file):
    variants = [
        ("INFO1", "json"),
        ("info2", "json"),
        ("info3", "JSON"),
        ("info3", "json"),
    ]

    data_files = {"train": [upper_lower_case_file]}
    webdataset = WebDataset(data_files=data_files)
    split_generators = webdataset._split_generators(DownloadManager())

    variant_keys = [f"{tag}.{ext}" for tag, ext in variants]
    assert webdataset.info.features == Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            **{k: {"caption": Value("string")} for k in variant_keys},
        }
    )

    assert len(split_generators) == 1
    split_generator = split_generators[0]
    assert split_generator.name == "train"
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)
    _, examples = zip(*generator)

    assert len(examples) == 3
    for example_idx, example in enumerate(examples):
        example_name = example["__key__"]
        expected_example_name = f"{example_idx:05d}_{'a' if example_idx % 2 else 'A'}"

        assert example_name == expected_example_name
        for key in variant_keys:
            assert isinstance(example[key], dict)
            assert example[key]["caption"] == f"caption for {example_name}.{key}"

        encoded = webdataset.info.features.encode_example(example)
        decoded = webdataset.info.features.decode_example(encoded)
        for key in variant_keys:
            assert decoded[key]["caption"] == example[key]["caption"]


@require_pil
def test_image_webdataset_missing_keys(image_wds_file):
    import PIL.Image

    data_files = {"train": [image_wds_file]}
    features = Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            "json": {"caption": Value("string")},
            "jpg": Image(),
            "jpeg": Image(),  # additional field
            "txt": Value("string"),  # additional field
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
    assert isinstance(decoded["json"], dict)
    assert isinstance(decoded["json"]["caption"], str)
    assert isinstance(decoded["jpg"], PIL.Image.Image)
    assert decoded["jpeg"] is None
    assert decoded["txt"] is None


@require_torchcodec
def test_audio_webdataset(audio_wds_file):
    from torchcodec.decoders import AudioDecoder

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
    assert isinstance(decoded["wav"], AudioDecoder)


def test_video_webdataset(video_wds_file):
    data_files = {"train": [video_wds_file]}
    webdataset = WebDataset(data_files=data_files)
    split_generators = webdataset._split_generators(DownloadManager())
    assert webdataset.info.features == Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            "json": {"caption": Value("string")},
            "mov": Video(),
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
    assert isinstance(examples[0]["mov"], dict)


def test_webdataset_errors_on_bad_file(bad_wds_file):
    data_files = {"train": [bad_wds_file]}
    webdataset = WebDataset(data_files=data_files)
    with pytest.raises(ValueError):
        webdataset._split_generators(DownloadManager())


def test_webdataset_read_error_includes_tar_path_during_feature_inference(corrupted_wds_file):
    webdataset = WebDataset(data_files={"train": [corrupted_wds_file]})

    with pytest.raises(tarfile.ReadError, match=re.escape(corrupted_wds_file)) as raised:
        webdataset._split_generators(DownloadManager())

    assert isinstance(raised.value.__cause__, tarfile.ReadError)


def test_webdataset_read_error_identifies_corrupt_shard_after_valid_shard(valid_text_wds_file, corrupted_wds_file):
    features = Features({"__key__": Value("string"), "__url__": Value("string"), "txt": Value("string")})
    webdataset = WebDataset(data_files={"train": [valid_text_wds_file, corrupted_wds_file]}, features=features)
    split_generator = webdataset._split_generators(DownloadManager())[0]
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)

    _, first_example = next(generator)
    assert first_example["__url__"] == valid_text_wds_file

    with pytest.raises(tarfile.ReadError, match=re.escape(corrupted_wds_file)) as raised:
        next(generator)

    assert isinstance(raised.value.__cause__, tarfile.ReadError)


def test_webdataset_read_error_includes_tar_path_while_reading_member(truncated_wds_file):
    features = Features({"__key__": Value("string"), "__url__": Value("string"), "txt": Value("string")})
    webdataset = WebDataset(data_files={"train": [truncated_wds_file]}, features=features)
    split_generator = webdataset._split_generators(DownloadManager())[0]

    with pytest.raises(tarfile.ReadError, match=re.escape(truncated_wds_file)) as raised:
        next(webdataset._generate_examples(**split_generator.gen_kwargs))

    assert isinstance(raised.value.__cause__, tarfile.ReadError)


def test_webdataset_read_error_includes_path_and_tracked_origin(corrupted_wds_file):
    origin = "hf://datasets/org/name@main/data/corrupted.tar"
    tar_path = tracked_str(corrupted_wds_file)
    tar_path.set_origin(origin)
    tar_iterator = DownloadManager().iter_archive(str(tar_path))

    with pytest.raises(tarfile.ReadError) as raised:
        next(WebDataset._get_pipeline_from_tar(tar_path, tar_iterator))

    message = str(raised.value)
    assert corrupted_wds_file in message
    assert origin in message
    assert message.startswith(f"Failed to read TAR archive {corrupted_wds_file!r} (origin={origin}):")


def test_webdataset_read_error_strips_userinfo_and_query_from_origin(corrupted_wds_file):
    origin = "https://user:pass@example.com/bucket/file.tar?X-Amz-Signature=abc&Expires=1"
    safe_origin = "https://example.com/bucket/file.tar"
    tar_path = tracked_str(corrupted_wds_file)
    tar_path.set_origin(origin)
    tar_iterator = DownloadManager().iter_archive(str(tar_path))

    with pytest.raises(tarfile.ReadError) as raised:
        next(WebDataset._get_pipeline_from_tar(tar_path, tar_iterator))

    message = str(raised.value)
    assert corrupted_wds_file in message
    assert safe_origin in message
    assert "user:pass" not in message
    assert "X-Amz-Signature" not in message
    assert message.startswith(f"Failed to read TAR archive {corrupted_wds_file!r} (origin={safe_origin}):")


def test_webdataset_read_error_omits_origin_when_same_as_path(corrupted_wds_file):
    tar_path = tracked_str(corrupted_wds_file)
    tar_path.set_origin(corrupted_wds_file)
    tar_iterator = DownloadManager().iter_archive(str(tar_path))

    with pytest.raises(tarfile.ReadError) as raised:
        next(WebDataset._get_pipeline_from_tar(tar_path, tar_iterator))

    message = str(raised.value)
    assert corrupted_wds_file in message
    assert "origin=" not in message


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


@require_numpy1_on_windows
@require_torch
def test_tensor_webdataset(tensor_wds_file):
    import torch

    data_files = {"train": [tensor_wds_file]}
    webdataset = WebDataset(data_files=data_files)
    split_generators = webdataset._split_generators(DownloadManager())
    assert webdataset.info.features == Features(
        {
            "__key__": Value("string"),
            "__url__": Value("string"),
            "json": {"text": Value("string")},
            "pth": List(Value("float32")),
        }
    )
    assert len(split_generators) == 1
    split_generator = split_generators[0]
    assert split_generator.name == "train"
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)
    _, examples = zip(*generator)
    assert len(examples) == 3
    assert isinstance(examples[0]["json"], dict)
    assert isinstance(examples[0]["json"]["text"], str)
    assert isinstance(examples[0]["pth"], torch.Tensor)  # keep encoded to avoid unecessary copies
    encoded = webdataset.info.features.encode_example(examples[0])
    decoded = webdataset.info.features.decode_example(encoded)
    assert isinstance(decoded["json"], dict)
    assert isinstance(decoded["json"]["text"], str)
    assert isinstance(decoded["pth"], list)
