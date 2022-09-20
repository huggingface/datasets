import os
import tarfile
from contextlib import nullcontext
from unittest.mock import patch

import pyarrow as pa
import pytest

from datasets import Dataset, concatenate_datasets, load_dataset
from datasets.features import Audio, Features, Sequence, Value

from ..utils import (
    require_libsndfile_with_opus,
    require_sndfile,
    require_sox,
    require_torchaudio,
    require_torchaudio_latest,
)


@pytest.fixture()
def tar_wav_path(shared_datadir, tmp_path_factory):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    path = tmp_path_factory.mktemp("data") / "audio_data.wav.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(audio_path, arcname=os.path.basename(audio_path))
    return path


@pytest.fixture()
def tar_mp3_path(shared_datadir, tmp_path_factory):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    path = tmp_path_factory.mktemp("data") / "audio_data.mp3.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(audio_path, arcname=os.path.basename(audio_path))
    return path


def iter_archive(archive_path):
    with tarfile.open(archive_path) as tar:
        for tarinfo in tar:
            file_path = tarinfo.name
            file_obj = tar.extractfile(tarinfo)
            yield file_path, file_obj


def test_audio_instantiation():
    audio = Audio()
    assert audio.sampling_rate is None
    assert audio.mono is True
    assert audio.id is None
    assert audio.dtype == "dict"
    assert audio.pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert audio._type == "Audio"


def test_audio_feature_type_to_arrow():
    features = Features({"audio": Audio()})
    assert features.arrow_schema == pa.schema({"audio": Audio().pa_type})
    features = Features({"struct_containing_an_audio": {"audio": Audio()}})
    assert features.arrow_schema == pa.schema({"struct_containing_an_audio": pa.struct({"audio": Audio().pa_type})})
    features = Features({"sequence_of_audios": Sequence(Audio())})
    assert features.arrow_schema == pa.schema({"sequence_of_audios": pa.list_(Audio().pa_type)})


@pytest.mark.parametrize(
    "build_example",
    [
        lambda audio_path: audio_path,
        lambda audio_path: {"path": audio_path},
        lambda audio_path: {"path": audio_path, "bytes": None},
        lambda audio_path: {"path": audio_path, "bytes": open(audio_path, "rb").read()},
        lambda audio_path: {"path": None, "bytes": open(audio_path, "rb").read()},
        lambda audio_path: {"bytes": open(audio_path, "rb").read()},
        lambda audio_path: {"array": [0.1, 0.2, 0.3], "sampling_rate": 16_000},
    ],
)
def test_audio_feature_encode_example(shared_datadir, build_example):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio()
    encoded_example = audio.encode_example(build_example(audio_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = audio.decode_example(encoded_example)
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}


@pytest.mark.parametrize(
    "build_example",
    [
        lambda audio_path: {"path": audio_path, "sampling_rate": 16_000},
        lambda audio_path: {"path": audio_path, "bytes": None, "sampling_rate": 16_000},
        lambda audio_path: {"path": audio_path, "bytes": open(audio_path, "rb").read(), "sampling_rate": 16_000},
        lambda audio_path: {"array": [0.1, 0.2, 0.3], "sampling_rate": 16_000},
    ],
)
def test_audio_feature_encode_example_pcm(shared_datadir, build_example):
    audio_path = str(shared_datadir / "test_audio_16000.pcm")
    audio = Audio(sampling_rate=16_000)
    encoded_example = audio.encode_example(build_example(audio_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = audio.decode_example(encoded_example)
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}


@require_sndfile
def test_audio_decode_example(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio()
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (202311,)
    assert decoded_example["sampling_rate"] == 44100

    with pytest.raises(RuntimeError):
        Audio(decode=False).decode_example(audio_path)


@require_sndfile
def test_audio_resampling(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio(sampling_rate=16000)
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (73401,)
    assert decoded_example["sampling_rate"] == 16000


@require_sox
@require_torchaudio
def test_audio_decode_example_mp3(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio = Audio()
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (109440,)
    assert decoded_example["sampling_rate"] == 44100


@pytest.mark.torchaudio_latest
@require_torchaudio_latest
@pytest.mark.parametrize("torchaudio_failed", [False, True])
def test_audio_decode_example_mp3_torchaudio_latest(shared_datadir, torchaudio_failed):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio = Audio()

    with patch("torchaudio.load") if torchaudio_failed else nullcontext() as load_mock, pytest.warns(
        UserWarning, match=r"Decoding mp3 with `librosa` instead of `torchaudio`.+?"
    ) if torchaudio_failed else nullcontext():

        if torchaudio_failed:
            load_mock.side_effect = RuntimeError()

        decoded_example = audio.decode_example(audio.encode_example(audio_path))
        assert decoded_example["path"] == audio_path
        assert decoded_example["array"].shape == (110592,)
        assert decoded_example["sampling_rate"] == 44100


@require_libsndfile_with_opus
def test_audio_decode_example_opus(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_48000.opus")
    audio = Audio()
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (48000,)
    assert decoded_example["sampling_rate"] == 48000


@pytest.mark.parametrize("sampling_rate", [16_000, 48_000])
def test_audio_decode_example_pcm(shared_datadir, sampling_rate):
    audio_path = str(shared_datadir / "test_audio_16000.pcm")
    audio_input = {"path": audio_path, "sampling_rate": 16_000}
    audio = Audio(sampling_rate=sampling_rate)
    decoded_example = audio.decode_example(audio.encode_example(audio_input))
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] is None
    assert decoded_example["array"].shape == (16208 * sampling_rate // 16_000,)
    assert decoded_example["sampling_rate"] == sampling_rate


@require_sox
@require_torchaudio
def test_audio_resampling_mp3_different_sampling_rates(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio_path2 = str(shared_datadir / "test_audio_16000.mp3")
    audio = Audio(sampling_rate=48000)

    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (119119,)
    assert decoded_example["sampling_rate"] == 48000

    decoded_example = audio.decode_example(audio.encode_example(audio_path2))
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path2
    assert decoded_example["array"].shape == (120960,)
    assert decoded_example["sampling_rate"] == 48000


@pytest.mark.torchaudio_latest
@require_torchaudio_latest
@pytest.mark.parametrize("torchaudio_failed", [False, True])
def test_audio_resampling_mp3_different_sampling_rates_torchaudio_latest(shared_datadir, torchaudio_failed):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio_path2 = str(shared_datadir / "test_audio_16000.mp3")
    audio = Audio(sampling_rate=48000)

    # if torchaudio>=0.12 failed, mp3 must be decoded anyway (with librosa)
    with patch("torchaudio.load") if torchaudio_failed else nullcontext() as load_mock, pytest.warns(
        UserWarning, match=r"Decoding mp3 with `librosa` instead of `torchaudio`.+?"
    ) if torchaudio_failed else nullcontext():
        if torchaudio_failed:
            load_mock.side_effect = RuntimeError()

        decoded_example = audio.decode_example(audio.encode_example(audio_path))
        assert decoded_example.keys() == {"path", "array", "sampling_rate"}
        assert decoded_example["path"] == audio_path
        assert decoded_example["array"].shape == (120373,)
        assert decoded_example["sampling_rate"] == 48000

        decoded_example = audio.decode_example(audio.encode_example(audio_path2))
        assert decoded_example.keys() == {"path", "array", "sampling_rate"}
        assert decoded_example["path"] == audio_path2
        assert decoded_example["array"].shape == (122688,)
        assert decoded_example["sampling_rate"] == 48000


@require_sndfile
def test_dataset_with_audio_feature(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_path
    assert item["audio"]["array"].shape == (202311,)
    assert item["audio"]["sampling_rate"] == 44100
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


@require_sndfile
def test_dataset_with_audio_feature_tar_wav(tar_wav_path):
    audio_filename = "test_audio_44100.wav"
    data = {"audio": []}
    for file_path, file_obj in iter_archive(tar_wav_path):
        data["audio"].append({"path": file_path, "bytes": file_obj.read()})
        break
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_filename
    assert item["audio"]["array"].shape == (202311,)
    assert item["audio"]["sampling_rate"] == 44100
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_filename
    assert batch["audio"][0]["array"].shape == (202311,)
    assert batch["audio"][0]["sampling_rate"] == 44100
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_filename
    assert column[0]["array"].shape == (202311,)
    assert column[0]["sampling_rate"] == 44100


@require_sox
@require_torchaudio
def test_dataset_with_audio_feature_tar_mp3(tar_mp3_path):
    audio_filename = "test_audio_44100.mp3"
    data = {"audio": []}
    for file_path, file_obj in iter_archive(tar_mp3_path):
        data["audio"].append({"path": file_path, "bytes": file_obj.read()})
        break
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_filename
    assert item["audio"]["array"].shape == (109440,)
    assert item["audio"]["sampling_rate"] == 44100
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_filename
    assert batch["audio"][0]["array"].shape == (109440,)
    assert batch["audio"][0]["sampling_rate"] == 44100
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_filename
    assert column[0]["array"].shape == (109440,)
    assert column[0]["sampling_rate"] == 44100


@pytest.mark.torchaudio_latest
@require_torchaudio_latest
def test_dataset_with_audio_feature_tar_mp3_torchaudio_latest(tar_mp3_path):
    # no test for librosa here because it doesn't support file-like objects, only paths
    audio_filename = "test_audio_44100.mp3"
    data = {"audio": []}
    for file_path, file_obj in iter_archive(tar_mp3_path):
        data["audio"].append({"path": file_path, "bytes": file_obj.read()})
        break
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_filename
    assert item["audio"]["array"].shape == (110592,)
    assert item["audio"]["sampling_rate"] == 44100
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_filename
    assert batch["audio"][0]["array"].shape == (110592,)
    assert batch["audio"][0]["sampling_rate"] == 44100
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_filename
    assert column[0]["array"].shape == (110592,)
    assert column[0]["sampling_rate"] == 44100


@require_sndfile
def test_dataset_with_audio_feature_with_none():
    data = {"audio": [None]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"] is None
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"audio"}
    assert isinstance(batch["audio"], list) and all(item is None for item in batch["audio"])
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column, list) and all(item is None for item in column)

    # nested tests

    data = {"audio": [[None]]}
    features = Features({"audio": Sequence(Audio())})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert all(i is None for i in item["audio"])

    data = {"nested": [{"audio": None}]}
    features = Features({"nested": {"audio": Audio()}})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"nested"}
    assert item["nested"].keys() == {"audio"}
    assert item["nested"]["audio"] is None


@require_sndfile
def test_resampling_at_loading_dataset_with_audio_feature(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(sampling_rate=16000)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_path
    assert item["audio"]["array"].shape == (73401,)
    assert item["audio"]["sampling_rate"] == 16000
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_path
    assert batch["audio"][0]["array"].shape == (73401,)
    assert batch["audio"][0]["sampling_rate"] == 16000
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_path
    assert column[0]["array"].shape == (73401,)
    assert column[0]["sampling_rate"] == 16000


@require_sox
@require_torchaudio
def test_resampling_at_loading_dataset_with_audio_feature_mp3(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(sampling_rate=16000)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_path
    assert item["audio"]["array"].shape == (39707,)
    assert item["audio"]["sampling_rate"] == 16000
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_path
    assert batch["audio"][0]["array"].shape == (39707,)
    assert batch["audio"][0]["sampling_rate"] == 16000
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_path
    assert column[0]["array"].shape == (39707,)
    assert column[0]["sampling_rate"] == 16000


@pytest.mark.torchaudio_latest
@require_torchaudio_latest
@pytest.mark.parametrize("torchaudio_failed", [False, True])
def test_resampling_at_loading_dataset_with_audio_feature_mp3_torchaudio_latest(shared_datadir, torchaudio_failed):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(sampling_rate=16000)})
    dset = Dataset.from_dict(data, features=features)

    # if torchaudio>=0.12 failed, mp3 must be decoded anyway (with librosa)
    with patch("torchaudio.load") if torchaudio_failed else nullcontext() as load_mock, pytest.warns(
        UserWarning, match=r"Decoding mp3 with `librosa` instead of `torchaudio`.+?"
    ) if torchaudio_failed else nullcontext():
        if torchaudio_failed:
            load_mock.side_effect = RuntimeError()

        item = dset[0]
        assert item.keys() == {"audio"}
        assert item["audio"].keys() == {"path", "array", "sampling_rate"}
        assert item["audio"]["path"] == audio_path
        assert item["audio"]["array"].shape == (40125,)
        assert item["audio"]["sampling_rate"] == 16000
        batch = dset[:1]
        assert batch.keys() == {"audio"}
        assert len(batch["audio"]) == 1
        assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
        assert batch["audio"][0]["path"] == audio_path
        assert batch["audio"][0]["array"].shape == (40125,)
        assert batch["audio"][0]["sampling_rate"] == 16000
        column = dset["audio"]
        assert len(column) == 1
        assert column[0].keys() == {"path", "array", "sampling_rate"}
        assert column[0]["path"] == audio_path
        assert column[0]["array"].shape == (40125,)
        assert column[0]["sampling_rate"] == 16000


@require_sndfile
def test_resampling_after_loading_dataset_with_audio_feature(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item["audio"]["sampling_rate"] == 44100
    dset = dset.cast_column("audio", Audio(sampling_rate=16000))
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_path
    assert item["audio"]["array"].shape == (73401,)
    assert item["audio"]["sampling_rate"] == 16000
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_path
    assert batch["audio"][0]["array"].shape == (73401,)
    assert batch["audio"][0]["sampling_rate"] == 16000
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_path
    assert column[0]["array"].shape == (73401,)
    assert column[0]["sampling_rate"] == 16000


@require_sox
@require_torchaudio
def test_resampling_after_loading_dataset_with_audio_feature_mp3(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item["audio"]["sampling_rate"] == 44100
    dset = dset.cast_column("audio", Audio(sampling_rate=16000))
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_path
    assert item["audio"]["array"].shape == (39707,)
    assert item["audio"]["sampling_rate"] == 16000
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
    assert batch["audio"][0]["path"] == audio_path
    assert batch["audio"][0]["array"].shape == (39707,)
    assert batch["audio"][0]["sampling_rate"] == 16000
    column = dset["audio"]
    assert len(column) == 1
    assert column[0].keys() == {"path", "array", "sampling_rate"}
    assert column[0]["path"] == audio_path
    assert column[0]["array"].shape == (39707,)
    assert column[0]["sampling_rate"] == 16000


@pytest.mark.torchaudio_latest
@require_torchaudio_latest
@pytest.mark.parametrize("torchaudio_failed", [False, True])
def test_resampling_after_loading_dataset_with_audio_feature_mp3_torchaudio_latest(shared_datadir, torchaudio_failed):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)

    # if torchaudio>=0.12 failed, mp3 must be decoded anyway (with librosa)
    with patch("torchaudio.load") if torchaudio_failed else nullcontext() as load_mock, pytest.warns(
        UserWarning, match=r"Decoding mp3 with `librosa` instead of `torchaudio`.+?"
    ) if torchaudio_failed else nullcontext():
        if torchaudio_failed:
            load_mock.side_effect = RuntimeError()

        item = dset[0]
        assert item["audio"]["sampling_rate"] == 44100
        dset = dset.cast_column("audio", Audio(sampling_rate=16000))
        item = dset[0]
        assert item.keys() == {"audio"}
        assert item["audio"].keys() == {"path", "array", "sampling_rate"}
        assert item["audio"]["path"] == audio_path
        assert item["audio"]["array"].shape == (40125,)
        assert item["audio"]["sampling_rate"] == 16000
        batch = dset[:1]
        assert batch.keys() == {"audio"}
        assert len(batch["audio"]) == 1
        assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
        assert batch["audio"][0]["path"] == audio_path
        assert batch["audio"][0]["array"].shape == (40125,)
        assert batch["audio"][0]["sampling_rate"] == 16000
        column = dset["audio"]
        assert len(column) == 1
        assert column[0].keys() == {"path", "array", "sampling_rate"}
        assert column[0]["path"] == audio_path
        assert column[0]["array"].shape == (40125,)
        assert column[0]["sampling_rate"] == 16000


@pytest.mark.parametrize(
    "build_data",
    [
        lambda audio_path: {"audio": [audio_path]},
        lambda audio_path: {"audio": [{"path": audio_path}]},
        lambda audio_path: {"audio": [{"path": audio_path, "bytes": None}]},
        lambda audio_path: {"audio": [{"path": audio_path, "bytes": open(audio_path, "rb").read()}]},
        lambda audio_path: {"audio": [{"path": None, "bytes": open(audio_path, "rb").read()}]},
        lambda audio_path: {"audio": [{"bytes": open(audio_path, "rb").read()}]},
    ],
)
def test_dataset_cast_to_audio_features(shared_datadir, build_data):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = build_data(audio_path)
    dset = Dataset.from_dict(data)
    item = dset.cast(Features({"audio": Audio()}))[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    item = dset.cast_column("audio", Audio())[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}


def test_dataset_concatenate_audio_features(shared_datadir):
    # we use a different data structure between 1 and 2 to make sure they are compatible with each other
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data1 = {"audio": [audio_path]}
    dset1 = Dataset.from_dict(data1, features=Features({"audio": Audio()}))
    data2 = {"audio": [{"bytes": open(audio_path, "rb").read()}]}
    dset2 = Dataset.from_dict(data2, features=Features({"audio": Audio()}))
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == len(dset1) + len(dset2)
    assert concatenated_dataset[0]["audio"]["array"].shape == dset1[0]["audio"]["array"].shape
    assert concatenated_dataset[1]["audio"]["array"].shape == dset2[0]["audio"]["array"].shape


def test_dataset_concatenate_nested_audio_features(shared_datadir):
    # we use a different data structure between 1 and 2 to make sure they are compatible with each other
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    features = Features({"list_of_structs_of_audios": [{"audio": Audio()}]})
    data1 = {"list_of_structs_of_audios": [[{"audio": audio_path}]]}
    dset1 = Dataset.from_dict(data1, features=features)
    data2 = {"list_of_structs_of_audios": [[{"audio": {"bytes": open(audio_path, "rb").read()}}]]}
    dset2 = Dataset.from_dict(data2, features=features)
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == len(dset1) + len(dset2)
    assert (
        concatenated_dataset[0]["list_of_structs_of_audios"][0]["audio"]["array"].shape
        == dset1[0]["list_of_structs_of_audios"][0]["audio"]["array"].shape
    )
    assert (
        concatenated_dataset[1]["list_of_structs_of_audios"][0]["audio"]["array"].shape
        == dset2[0]["list_of_structs_of_audios"][0]["audio"]["array"].shape
    )


@require_sndfile
def test_dataset_with_audio_feature_map_is_not_decoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path], "text": ["Hello"]}
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    expected_audio = features.encode_batch(data)["audio"][0]
    for item in dset._iter(decoded=False):
        assert item.keys() == {"audio", "text"}
        assert item == {"audio": expected_audio, "text": "Hello"}

    def process_text(example):
        example["text"] = example["text"] + " World!"
        return example

    processed_dset = dset.map(process_text)
    for item in processed_dset._iter(decoded=False):
        assert item.keys() == {"audio", "text"}
        assert item == {"audio": expected_audio, "text": "Hello World!"}


@require_sndfile
def test_dataset_with_audio_feature_map_is_decoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path], "text": ["Hello"]}
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    def process_audio_sampling_rate_by_example(example):
        example["double_sampling_rate"] = 2 * example["audio"]["sampling_rate"]
        return example

    decoded_dset = dset.map(process_audio_sampling_rate_by_example)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"audio", "text", "double_sampling_rate"}
        assert item["double_sampling_rate"] == 88200

    def process_audio_sampling_rate_by_batch(batch):
        double_sampling_rates = []
        for audio in batch["audio"]:
            double_sampling_rates.append(2 * audio["sampling_rate"])
        batch["double_sampling_rate"] = double_sampling_rates
        return batch

    decoded_dset = dset.map(process_audio_sampling_rate_by_batch, batched=True)
    for item in decoded_dset._iter(decoded=False):
        assert item.keys() == {"audio", "text", "double_sampling_rate"}
        assert item["double_sampling_rate"] == 88200


@require_sndfile
def test_formatted_dataset_with_audio_feature(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path, audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"audio"}
        assert item["audio"].keys() == {"path", "array", "sampling_rate"}
        assert item["audio"]["path"] == audio_path
        assert item["audio"]["array"].shape == (202311,)
        assert item["audio"]["sampling_rate"] == 44100
        batch = dset[:1]
        assert batch.keys() == {"audio"}
        assert len(batch["audio"]) == 1
        assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
        assert batch["audio"][0]["path"] == audio_path
        assert batch["audio"][0]["array"].shape == (202311,)
        assert batch["audio"][0]["sampling_rate"] == 44100
        column = dset["audio"]
        assert len(column) == 2
        assert column[0].keys() == {"path", "array", "sampling_rate"}
        assert column[0]["path"] == audio_path
        assert column[0]["array"].shape == (202311,)
        assert column[0]["sampling_rate"] == 44100

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["audio"]
        assert item["audio"][0].keys() == {"path", "array", "sampling_rate"}
        assert item["audio"][0]["path"] == audio_path
        assert item["audio"][0]["array"].shape == (202311,)
        assert item["audio"][0]["sampling_rate"] == 44100
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["audio"]
        assert batch["audio"][0].keys() == {"path", "array", "sampling_rate"}
        assert batch["audio"][0]["path"] == audio_path
        assert batch["audio"][0]["array"].shape == (202311,)
        assert batch["audio"][0]["sampling_rate"] == 44100
        column = dset["audio"]
        assert len(column) == 2
        assert column[0].keys() == {"path", "array", "sampling_rate"}
        assert column[0]["path"] == audio_path
        assert column[0]["array"].shape == (202311,)
        assert column[0]["sampling_rate"] == 44100


@pytest.fixture
def jsonl_audio_dataset_path(shared_datadir, tmp_path_factory):
    import json

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = [{"audio": audio_path, "text": "Hello world!"}]
    path = str(tmp_path_factory.mktemp("data") / "audio_dataset.jsonl")
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return path


@require_sndfile
@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_with_audio_feature(streaming, jsonl_audio_dataset_path, shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data_files = jsonl_audio_dataset_path
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = load_dataset("json", split="train", data_files=data_files, features=features, streaming=streaming)
    item = dset[0] if not streaming else next(iter(dset))
    assert item.keys() == {"audio", "text"}
    assert item["audio"].keys() == {"path", "array", "sampling_rate"}
    assert item["audio"]["path"] == audio_path
    assert item["audio"]["array"].shape == (202311,)
    assert item["audio"]["sampling_rate"] == 44100


@require_sndfile
@pytest.mark.integration
def test_dataset_with_audio_feature_loaded_from_cache():
    # load first time
    ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean")
    # load from cache
    ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")
    assert isinstance(ds, Dataset)


def test_dataset_with_audio_feature_undecoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(decode=False)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"] == {"path": audio_path, "bytes": None}
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert batch["audio"][0] == {"path": audio_path, "bytes": None}
    column = dset["audio"]
    assert len(column) == 1
    assert column[0] == {"path": audio_path, "bytes": None}


def test_formatted_dataset_with_audio_feature_undecoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(decode=False)})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"audio"}
        assert item["audio"] == {"path": audio_path, "bytes": None}
        batch = dset[:1]
        assert batch.keys() == {"audio"}
        assert len(batch["audio"]) == 1
        assert batch["audio"][0] == {"path": audio_path, "bytes": None}
        column = dset["audio"]
        assert len(column) == 1
        assert column[0] == {"path": audio_path, "bytes": None}

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["audio"]
        assert item["audio"][0] == {"path": audio_path, "bytes": None}
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["audio"]
        assert batch["audio"][0] == {"path": audio_path, "bytes": None}
        column = dset["audio"]
        assert len(column) == 1
        assert column[0] == {"path": audio_path, "bytes": None}


def test_dataset_with_audio_feature_map_undecoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(decode=False)})
    dset = Dataset.from_dict(data, features=features)

    def assert_audio_example_undecoded(example):
        assert example["audio"] == {"path": audio_path, "bytes": None}

    dset.map(assert_audio_example_undecoded)

    def assert_audio_batch_undecoded(batch):
        for audio in batch["audio"]:
            assert audio == {"path": audio_path, "bytes": None}

    dset.map(assert_audio_batch_undecoded, batched=True)
