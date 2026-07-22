from pathlib import Path

import pytest

from datasets import Column, Dataset, Features, Value, Video, load_dataset

from ..utils import require_torchcodec


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


@pytest.fixture
def video_with_audio_path(tmp_path):
    """Synthesize a tiny video with an audio stream so we can exercise the
    populated-audio path of the wrapped VideoDecoder."""
    import torch
    from torchcodec.encoders import Encoder

    sample_rate = 8000
    num_channels = 1
    num_frames = 5
    frame_rate = 10
    height, width = 32, 32

    encoder = Encoder()
    video_stream = encoder.add_video(height=height, width=width, frame_rate=frame_rate)
    audio_stream = encoder.add_audio(sample_rate=sample_rate, num_channels=num_channels)
    path = tmp_path / "video_with_audio.mp4"
    with encoder.open_file(str(path)):
        video_stream.add_frames(torch.zeros((num_frames, 3, height, width), dtype=torch.uint8))
        audio_stream.add_samples(torch.zeros((num_channels, sample_rate), dtype=torch.float32))
    return str(path)


@require_torchcodec
class TestVideoDecoderAudio:
    """Tests for the `audio` property added to the wrapped VideoDecoder."""

    def test_audio_is_none_for_video_only_source(self, shared_datadir):
        from datasets.features._torchcodec import VideoDecoder

        video_path = str(shared_datadir / "test_video_66x50.mov")
        decoder = VideoDecoder(video_path)
        assert decoder.audio is None

    def test_audio_property_returns_wrapped_audio_decoder(self, video_with_audio_path):
        import numpy as np

        from datasets.features._torchcodec import AudioDecoder, VideoDecoder

        decoder = VideoDecoder(video_with_audio_path)
        audio = decoder.audio
        assert isinstance(audio, AudioDecoder)
        # The wrapped AudioDecoder exposes array/sampling_rate via __getitem__.
        assert isinstance(audio["array"], np.ndarray)
        assert audio["sampling_rate"] == 8000

    def test_audio_for_bytes_source(self, video_with_audio_path):
        from datasets.features._torchcodec import AudioDecoder, VideoDecoder

        with open(video_with_audio_path, "rb") as f:
            data = f.read()
        decoder = VideoDecoder(data)
        assert isinstance(decoder.audio, AudioDecoder)

    def test_audio_for_file_like_source(self, video_with_audio_path):
        from datasets.features._torchcodec import AudioDecoder, VideoDecoder

        with open(video_with_audio_path, "rb") as f:
            decoder = VideoDecoder(f)
        # Video frames must still be decodable even though the audio decoder
        # also consumed the same source.
        assert decoder.get_frame_at(0).data.shape[0] == 3
        assert isinstance(decoder.audio, AudioDecoder)

    def test_audio_sample_rate_kwarg(self, video_with_audio_path):
        from datasets.features._torchcodec import VideoDecoder

        decoder = VideoDecoder(video_with_audio_path, audio_sample_rate=16000)
        assert decoder.audio is not None
        assert decoder.audio["sampling_rate"] == 16000

    def test_audio_is_none_for_tensor_source(self, shared_datadir):
        import torch

        from datasets.features._torchcodec import VideoDecoder

        video_path = str(shared_datadir / "test_video_66x50.mov")
        data = torch.frombuffer(Path(video_path).read_bytes(), dtype=torch.uint8)
        decoder = VideoDecoder(data)
        assert decoder.audio is None

    def test_audio_is_cached(self, shared_datadir):
        from datasets.features._torchcodec import VideoDecoder

        video_path = str(shared_datadir / "test_video_66x50.mov")
        decoder = VideoDecoder(video_path)
        # Two accesses must return the same (cached) object — None included.
        assert decoder.audio is decoder.audio

    def test_file_like_source_is_normalized_to_bytes(self, shared_datadir):
        from datasets.features._torchcodec import VideoDecoder

        video_path = str(shared_datadir / "test_video_66x50.mov")
        with open(video_path, "rb") as f:
            decoder = VideoDecoder(f)
        # File-likes share a cursor with the audio decoder, so they must be
        # read into bytes up-front. Decoding a frame after construction proves
        # the video stream is still readable.
        assert decoder.get_frame_at(0).data.shape == (3, 50, 66)
        assert decoder.audio is None

    def test_video_feature_forwards_audio_kwargs(self, shared_datadir):
        from datasets.features._torchcodec import VideoDecoder

        video_path = str(shared_datadir / "test_video_66x50.mov")
        feature = Video(audio_stream_index=0, audio_sample_rate=16000, audio_num_channels=1)
        decoded = feature.decode_example({"path": video_path, "bytes": None})
        assert isinstance(decoded, VideoDecoder)
        assert decoded._audio_stream_index == 0
        assert decoded._audio_sample_rate == 16000
        assert decoded._audio_num_channels == 1

    def test_video_feature_default_audio_kwargs(self):
        feature = Video()
        assert feature.audio_stream_index is None
        assert feature.audio_sample_rate is None
        assert feature.audio_num_channels is None
