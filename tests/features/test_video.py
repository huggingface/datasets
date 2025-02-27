import pytest

from datasets import Dataset, Features, Video

from ..utils import require_decord


@require_decord
@pytest.mark.parametrize(
    "build_example",
    [
        lambda video_path: video_path,
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


@require_decord
def test_dataset_with_video_feature(shared_datadir):
    from decord.ndarray import NDArray
    from torchcodec.decoders import VideoDecoder

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = {"video": [video_path]}
    features = Features({"video": Video()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"video"}
    assert isinstance(item["video"], VideoDecoder)
    assert item["video"][0].shape == (50, 66, 3)
    assert isinstance(item["video"][0], NDArray)
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"video"}
    assert isinstance(batch["video"], list) and all(isinstance(item, VideoDecoder) for item in batch["video"])
    assert batch["video"][0][0].shape == (50, 66, 3)
    assert isinstance(batch["video"][0][0], NDArray)
    column = dset["video"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, VideoDecoder) for item in column)
    assert column[0][0].shape == (50, 66, 3)
    assert isinstance(column[0][0], NDArray)

    # from bytes
    with open(video_path, "rb") as f:
        data = {"video": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"video"}
    assert isinstance(item["video"], VideoDecoder)
    assert item["video"][0].shape == (50, 66, 3)
    assert isinstance(item["video"][0], NDArray)


@require_decord
def test_dataset_with_video_map_and_formatted(shared_datadir):
    import numpy as np
    from torchcodec.decoders import VideoDecoder

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = {"video": [video_path]}
    features = Features({"video": Video()})
    dset = Dataset.from_dict(data, features=features)
    dset = dset.map(lambda x: x).with_format("numpy")
    example = dset[0]
    assert isinstance(example["video"], VideoDecoder)
    assert isinstance(example["video"][0], np.ndarray)

    # from bytes
    with open(video_path, "rb") as f:
        data = {"video": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    dset = dset.map(lambda x: x).with_format("numpy")
    example = dset[0]
    assert isinstance(example["video"], VideoDecoder)
    assert isinstance(example["video"][0], np.ndarray)
