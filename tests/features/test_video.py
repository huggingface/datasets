from pathlib import Path

import pytest

from datasets import Column, Dataset, Features, Value, Video, load_dataset, load_from_disk

from ..utils import require_torch, require_torchcodec


@require_torch
@pytest.mark.parametrize("device", [None, "cpu", "cuda:1"])
@pytest.mark.parametrize("as_torch_device", [False, True])
def test_video_device_serialization(shared_datadir, tmp_path, device, as_torch_device):
    import torch

    device_arg = torch.device(device) if as_torch_device and device is not None else device
    features = Features({"video": Video(decode=False, device=device_arg)})
    video_bytes = (shared_datadir / "test_video_66x50.mov").read_bytes()
    dset = Dataset.from_dict({"video": [video_bytes]}, features=features)
    expected_features = Features({"video": Video(decode=False, device=device)})

    assert dset.features == expected_features
    assert Features.from_arrow_schema(dset.data.schema) == expected_features
    dataset_path = str(tmp_path / "video-dataset")
    dset.save_to_disk(dataset_path)
    restored = load_from_disk(dataset_path)
    assert restored.features == expected_features
    assert restored.features["video"].device == device
    assert restored[0] == {"video": {"bytes": video_bytes, "path": None}}


@require_torchcodec
@pytest.mark.parametrize(
    "build_example",
    [
        lambda video_path: video_path,
        lambda video_path: Path(video_path),
        lambda video_path: open(video_path, "rb").read(),
        lambda video_path: {"path": video_path},
        lambda video_path: {"path": video_path, "bytes": None},
        lambda video_path: {"path": video_path, "bytes": open(video_path, "rb").read()},
        lambda video_path: {"path": None, "bytes": open(video_path, "rb").read()},
        lambda video_path: {"bytes": open(video_path, "rb").read()},
    ],
)
def test_video_feature_encode_example(shared_datadir, build_example):
    from torchcodec.decoders import VideoDecoder

    video_path = str(shared_datadir / "test_video_66x50.mov")
    video = Video()
    encoded_example = video.encode_example(build_example(video_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = video.decode_example(encoded_example)
    assert isinstance(decoded_example, VideoDecoder)


@require_torchcodec
def test_dataset_with_video_feature(shared_datadir):
    import torch
    from torchcodec.decoders import VideoDecoder

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = {"video": [video_path]}
    features = Features({"video": Video()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"video"}
    assert isinstance(item["video"], VideoDecoder)
    assert item["video"].get_frame_at(0).data.shape == (3, 50, 66)
    assert isinstance(item["video"].get_frame_at(0).data, torch.Tensor)
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"video"}
    assert isinstance(batch["video"], list) and all(isinstance(item, VideoDecoder) for item in batch["video"])
    assert batch["video"][0].get_frame_at(0).data.shape == (3, 50, 66)
    assert isinstance(batch["video"][0].get_frame_at(0).data, torch.Tensor)
    column = dset["video"]
    assert len(column) == 1

    assert isinstance(column, Column) and all(isinstance(item, VideoDecoder) for item in column)
    assert next(iter(column)).get_frame_at(0).data.shape == (3, 50, 66)
    assert isinstance(next(iter(column)).get_frame_at(0).data, torch.Tensor)

    # from bytes
    with open(video_path, "rb") as f:
        data = {"video": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"video"}
    assert isinstance(item["video"], VideoDecoder)
    assert item["video"].get_frame_at(0).data.shape == (3, 50, 66)
    assert isinstance(item["video"].get_frame_at(0).data, torch.Tensor)


@require_torchcodec
def test_dataset_with_video_map_and_formatted(shared_datadir):
    from torchcodec.decoders import VideoDecoder

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = {"video": [video_path]}
    features = Features({"video": Video()})
    dset = Dataset.from_dict(data, features=features)
    dset = dset.map(lambda x: x).with_format("numpy")
    example = dset[0]
    assert isinstance(example["video"], VideoDecoder)
    # assert isinstance(example["video"][0], np.ndarray)

    # from bytes
    with open(video_path, "rb") as f:
        data = {"video": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    dset = dset.map(lambda x: x).with_format("numpy")
    example = dset[0]
    assert isinstance(example["video"], VideoDecoder)
    # assert isinstance(example["video"][0], np.ndarray)


# Dataset casting and mapping
@require_torchcodec
def test_dataset_with_video_feature_map_is_decoded(shared_datadir):
    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = {"video": [video_path], "text": ["Hello"]}
    features = Features({"video": Video(), "text": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    def process_audio_sampling_rate_by_example(example):
        begin_stream_seconds = example["video"].metadata.begin_stream_seconds
        example["double_begin_stream_seconds"] = 2 * begin_stream_seconds
        return example

    decoded_dset = dset.map(process_audio_sampling_rate_by_example)
    for item in decoded_dset.cast_column("video", Video(decode=False)):
        assert item.keys() == {"video", "text", "double_begin_stream_seconds"}
        assert item["double_begin_stream_seconds"] == 0.0

    def process_audio_sampling_rate_by_batch(batch):
        double_fps = []
        for video in batch["video"]:
            double_fps.append(2 * video.metadata.begin_stream_seconds)
        batch["double_begin_stream_seconds"] = double_fps
        return batch

    decoded_dset = dset.map(process_audio_sampling_rate_by_batch, batched=True)
    for item in decoded_dset.cast_column("video", Video(decode=False)):
        assert item.keys() == {"video", "text", "double_begin_stream_seconds"}
        assert item["double_begin_stream_seconds"] == 0.0


@pytest.fixture
def jsonl_video_dataset_path(shared_datadir, tmp_path_factory):
    import json

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = [{"video": video_path, "text": "Hello world!"}]
    path = str(tmp_path_factory.mktemp("data") / "video_dataset.jsonl")
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return path


@require_torchcodec
@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_with_video_feature(streaming, jsonl_video_dataset_path, shared_datadir):
    from torchcodec.decoders import VideoDecoder

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data_files = jsonl_video_dataset_path
    features = Features({"video": Video(), "text": Value("string")})
    dset = load_dataset("json", split="train", data_files=data_files, features=features, streaming=streaming)
    item = dset[0] if not streaming else next(iter(dset))
    assert item.keys() == {"video", "text"}
    assert isinstance(item["video"], VideoDecoder)
    assert item["video"].get_frame_at(0).data.shape == (3, 50, 66)
    assert item["video"].metadata.path == video_path
