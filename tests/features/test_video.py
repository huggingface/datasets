import pytest

from datasets import Column, Dataset, Features, Video

from ..utils import require_torchvision


@require_torchvision
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
    from torchvision.io import VideoReader

    video_path = str(shared_datadir / "test_video_66x50.mov")
    video = Video()
    encoded_example = video.encode_example(build_example(video_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = video.decode_example(encoded_example)
    assert isinstance(decoded_example, VideoReader)


@require_torchvision
def test_dataset_with_video_feature(shared_datadir):
    import torch
    from torchvision.io import VideoReader

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = {"video": [video_path]}
    features = Features({"video": Video()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"video"}
    assert isinstance(item["video"], VideoReader)
    assert next(item["video"])["data"].shape == (3, 50, 66)
    assert isinstance(next(item["video"])["data"], torch.Tensor)
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"video"}
    assert isinstance(batch["video"], list) and all(isinstance(item, VideoReader) for item in batch["video"])
    assert next(batch["video"][0])["data"].shape == (3, 50, 66)
    assert isinstance(next(batch["video"][0])["data"], torch.Tensor)
    column = dset["video"]
    assert len(column) == 1
    assert isinstance(column, Column) and all(isinstance(item, VideoReader) for item in column)
    assert next(column[0])["data"].shape == (3, 50, 66)
    assert isinstance(next(column[0])["data"], torch.Tensor)

    # from bytes
    with open(video_path, "rb") as f:
        data = {"video": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"video"}
    assert isinstance(item["video"], VideoReader)
    assert next(item["video"])["data"].shape == (3, 50, 66)
    assert isinstance(next(item["video"])["data"], torch.Tensor)


@require_torchvision
def test_dataset_with_video_map_and_formatted(shared_datadir):
    from torchvision.io import VideoReader

    video_path = str(shared_datadir / "test_video_66x50.mov")
    data = {"video": [video_path]}
    features = Features({"video": Video()})
    dset = Dataset.from_dict(data, features=features)
    dset = dset.map(lambda x: x).with_format("numpy")
    example = dset[0]
    assert isinstance(example["video"], VideoReader)
    # assert isinstance(example["video"][0], np.ndarray)

    # from bytes
    with open(video_path, "rb") as f:
        data = {"video": [f.read()]}
    dset = Dataset.from_dict(data, features=features)
    dset = dset.map(lambda x: x).with_format("numpy")
    example = dset[0]
    assert isinstance(example["video"], VideoReader)
    # assert isinstance(example["video"][0], np.ndarray)
