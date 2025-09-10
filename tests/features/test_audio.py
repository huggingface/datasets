import os
import tarfile
from itertools import product

import numpy as np
import pyarrow as pa
import pytest

from datasets import Column, Dataset, concatenate_datasets, load_dataset
from datasets.features import Audio, Features, List, Value

from ..utils import require_torchcodec


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
    assert audio.id is None
    assert audio.stream_index is None

    assert audio.dtype == "dict"
    assert audio.pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert audio._type == "Audio"


def test_audio_feature_type_to_arrow():
    features = Features({"audio": Audio()})
    assert features.arrow_schema == pa.schema({"audio": Audio().pa_type})
    features = Features({"struct_containing_an_audio": {"audio": Audio()}})
    assert features.arrow_schema == pa.schema({"struct_containing_an_audio": pa.struct({"audio": Audio().pa_type})})
    features = Features({"sequence_of_audios": List(Audio())})
    assert features.arrow_schema == pa.schema({"sequence_of_audios": pa.list_(Audio().pa_type)})


@require_torchcodec
@pytest.mark.parametrize(
    "build_example",
    [
        lambda audio_path: audio_path,
        lambda audio_path: open(audio_path, "rb").read(),
        lambda audio_path: {"path": audio_path},
        lambda audio_path: {"path": audio_path, "bytes": None},
        lambda audio_path: {"path": audio_path, "bytes": open(audio_path, "rb").read()},
        lambda audio_path: {"path": None, "bytes": open(audio_path, "rb").read()},
        lambda audio_path: {"bytes": open(audio_path, "rb").read()},
        lambda audio_path: {"array": np.array([0.1, 0.2, 0.3]), "sampling_rate": 16_000},
    ],
)
def test_audio_feature_encode_example(shared_datadir, build_example):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio()
    encoded_example = audio.encode_example(build_example(audio_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = audio.decode_example(encoded_example)
    assert isinstance(decoded_example, AudioDecoder)


@require_torchcodec
@pytest.mark.parametrize(
    "build_example",
    [
        lambda audio_path: {"path": audio_path, "sampling_rate": 16_000},
        lambda audio_path: {"path": audio_path, "bytes": None, "sampling_rate": 16_000},
        lambda audio_path: {"path": audio_path, "bytes": open(audio_path, "rb").read(), "sampling_rate": 16_000},
        lambda audio_path: {"array": np.array([0.1, 0.2, 0.3]), "sampling_rate": 16_000},
    ],
)
def test_audio_feature_encode_example_pcm(shared_datadir, build_example):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_16000.pcm")
    audio = Audio(sampling_rate=16_000)
    encoded_example = audio.encode_example(build_example(audio_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = audio.decode_example(encoded_example)
    assert isinstance(decoded_example, AudioDecoder)


sample_rates = [16_000, 48_000]


@require_torchcodec
@pytest.mark.parametrize(
    "in_sample_rate,out_sample_rate",
    list(product(sample_rates, sample_rates)),
)
def test_audio_feature_encode_example_audiodecoder(shared_datadir, in_sample_rate, out_sample_rate):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio(sampling_rate=out_sample_rate)
    example = AudioDecoder(audio_path, sample_rate=in_sample_rate)
    encoded_example = audio.encode_example(example)
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None
    decoded_example = audio.decode_example(encoded_example)
    assert isinstance(decoded_example, AudioDecoder)


@require_torchcodec
def test_audio_decode_example(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio()
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)

    with pytest.raises(RuntimeError):
        Audio(decode=False).decode_example(audio_path)


@require_torchcodec
def test_audio_resampling(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio(sampling_rate=16000)
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 73401)


@require_torchcodec
def test_audio_decode_example_mp3(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio = Audio()
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    print("decoded_example", decoded_example)
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 110592)


@require_torchcodec
def test_audio_decode_example_opus(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_48000.opus")
    audio = Audio()
    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert samples.sample_rate == 48000
    assert samples.data.shape == (1, 48000)


@require_torchcodec
@pytest.mark.parametrize("sampling_rate", [16_000, 48_000])
def test_audio_decode_example_pcm(shared_datadir, sampling_rate):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_16000.pcm")
    audio_input = {"path": audio_path, "sampling_rate": 16_000}
    audio = Audio(sampling_rate=sampling_rate)
    decoded_example = audio.decode_example(audio.encode_example(audio_input))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert samples.sample_rate == sampling_rate
    assert samples.data.shape == (1, 16208 * sampling_rate // 16_000)


@require_torchcodec
def test_audio_resampling_mp3_different_sampling_rates(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio_path2 = str(shared_datadir / "test_audio_16000.mp3")
    audio = Audio(sampling_rate=48000)

    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert samples.sample_rate == 48000
    assert samples.data.shape == (2, 120373)

    decoded_example = audio.decode_example(audio.encode_example(audio_path2))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert samples.sample_rate == 48000
    assert samples.data.shape == (2, 122688)


@require_torchcodec
def test_backwards_compatibility(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio_path2 = str(shared_datadir / "test_audio_16000.mp3")
    audio = Audio(sampling_rate=48000)

    decoded_example = audio.decode_example(audio.encode_example(audio_path))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert decoded_example["sampling_rate"] == samples.sample_rate
    assert decoded_example["array"].ndim == 1  # mono
    assert abs(decoded_example["array"].shape[0] - samples.data.shape[1]) < 2  # can have off by one error

    decoded_example = audio.decode_example(audio.encode_example(audio_path2))
    assert isinstance(decoded_example, AudioDecoder)
    samples = decoded_example.get_all_samples()
    assert decoded_example["sampling_rate"] == samples.sample_rate
    assert decoded_example["array"].ndim == 1  # mono
    assert abs(decoded_example["array"].shape[0] - samples.data.shape[1]) < 2  # can have off by one error


@require_torchcodec
def test_dataset_with_audio_feature(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert isinstance(batch["audio"][0], AudioDecoder)
    samples = batch["audio"][0].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column[0], AudioDecoder)
    samples = column[0].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)


@require_torchcodec
def test_dataset_with_audio_feature_tar_wav(tar_wav_path):
    from torchcodec.decoders import AudioDecoder

    audio_filename = "test_audio_44100.wav"
    data = {"audio": []}
    for file_path, file_obj in iter_archive(tar_wav_path):
        data["audio"].append({"path": file_path, "bytes": file_obj.read()})
        break
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)
    assert item["audio"].metadata.path == audio_filename
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert isinstance(batch["audio"][0], AudioDecoder)
    samples = batch["audio"][0].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)
    assert batch["audio"][0].metadata.path == audio_filename
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column[0], AudioDecoder)
    samples = column[0].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)


@require_torchcodec
def test_dataset_with_audio_feature_tar_mp3(tar_mp3_path):
    from torchcodec.decoders import AudioDecoder

    audio_filename = "test_audio_44100.mp3"
    data = {"audio": []}
    for file_path, file_obj in iter_archive(tar_mp3_path):
        data["audio"].append({"path": file_path, "bytes": file_obj.read()})
        break
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 110592)
    assert item["audio"].metadata.path == audio_filename
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert isinstance(batch["audio"][0], AudioDecoder)
    samples = batch["audio"][0].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 110592)
    assert batch["audio"][0].metadata.path == audio_filename
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column[0], AudioDecoder)
    samples = column[0].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 110592)


@require_torchcodec
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
    assert isinstance(column, Column) and all(item is None for item in column)

    # nested tests

    data = {"audio": [[None]]}
    features = Features({"audio": List(Audio())})
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


@require_torchcodec
def test_resampling_at_loading_dataset_with_audio_feature(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(sampling_rate=16000)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 73401)
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert isinstance(batch["audio"][0], AudioDecoder)
    samples = batch["audio"][0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 73401)
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column[0], AudioDecoder)
    samples = column[0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 73401)


@require_torchcodec
def test_resampling_at_loading_dataset_with_audio_feature_mp3(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio(sampling_rate=16000)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 40124)
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert isinstance(batch["audio"][0], AudioDecoder)
    samples = batch["audio"][0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 40124)
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column[0], AudioDecoder)
    samples = column[0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 40124)


@require_torchcodec
def test_resampling_after_loading_dataset_with_audio_feature(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 44100
    dset = dset.cast_column("audio", Audio(sampling_rate=16000))
    item = dset[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 73401)
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert isinstance(batch["audio"][0], AudioDecoder)
    samples = batch["audio"][0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 73401)
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column[0], AudioDecoder)
    samples = column[0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 73401)


@require_torchcodec
def test_resampling_after_loading_dataset_with_audio_feature_mp3(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 44100
    dset = dset.cast_column("audio", Audio(sampling_rate=16000))
    item = dset[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 40124)
    batch = dset[:1]
    assert batch.keys() == {"audio"}
    assert len(batch["audio"]) == 1
    assert isinstance(batch["audio"][0], AudioDecoder)
    samples = batch["audio"][0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 40124)
    column = dset["audio"]
    assert len(column) == 1
    assert isinstance(column[0], AudioDecoder)
    samples = column[0].get_all_samples()
    assert samples.sample_rate == 16000
    assert samples.data.shape == (2, 40124)


@require_torchcodec
@pytest.mark.parametrize(
    "build_data",
    [
        lambda audio_path: {"audio": [audio_path]},
        lambda audio_path: {"audio": [open(audio_path, "rb").read()]},
        lambda audio_path: {"audio": [{"path": audio_path}]},
        lambda audio_path: {"audio": [{"path": audio_path, "bytes": None}]},
        lambda audio_path: {"audio": [{"path": audio_path, "bytes": open(audio_path, "rb").read()}]},
        lambda audio_path: {"audio": [{"path": None, "bytes": open(audio_path, "rb").read()}]},
        lambda audio_path: {"audio": [{"bytes": open(audio_path, "rb").read()}]},
    ],
)
def test_dataset_cast_to_audio_features(shared_datadir, build_data):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = build_data(audio_path)
    dset = Dataset.from_dict(data)
    item = dset.cast(Features({"audio": Audio()}))[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)
    item = dset.cast_column("audio", Audio())[0]
    assert item.keys() == {"audio"}
    assert isinstance(item["audio"], AudioDecoder)


@require_torchcodec
def test_dataset_concatenate_audio_features(shared_datadir):
    # we use a different data structure between 1 and 2 to make sure they are compatible with each other
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data1 = {"audio": [audio_path]}
    dset1 = Dataset.from_dict(data1, features=Features({"audio": Audio()}))
    data2 = {"audio": [{"bytes": open(audio_path, "rb").read()}]}
    dset2 = Dataset.from_dict(data2, features=Features({"audio": Audio()}))
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == len(dset1) + len(dset2)
    assert (
        concatenated_dataset[0]["audio"].get_all_samples().data.shape == dset1[0]["audio"].get_all_samples().data.shape
    )
    assert (
        concatenated_dataset[1]["audio"].get_all_samples().data.shape == dset2[0]["audio"].get_all_samples().data.shape
    )


@require_torchcodec
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
        concatenated_dataset[0]["list_of_structs_of_audios"][0]["audio"].get_all_samples().data.shape
        == dset1[0]["list_of_structs_of_audios"][0]["audio"].get_all_samples().data.shape
    )
    assert (
        concatenated_dataset[1]["list_of_structs_of_audios"][0]["audio"].get_all_samples().data.shape
        == dset2[0]["list_of_structs_of_audios"][0]["audio"].get_all_samples().data.shape
    )


@require_torchcodec
def test_dataset_with_audio_feature_map_is_not_decoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path], "text": ["Hello"]}
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    expected_audio = features.encode_batch(data)["audio"][0]
    for item in dset.cast_column("audio", Audio(decode=False)):
        assert item.keys() == {"audio", "text"}
        assert item == {"audio": expected_audio, "text": "Hello"}

    def process_text(example):
        example["text"] = example["text"] + " World!"
        return example

    processed_dset = dset.map(process_text)
    for item in processed_dset.cast_column("audio", Audio(decode=False)):
        assert item.keys() == {"audio", "text"}
        assert item == {"audio": expected_audio, "text": "Hello World!"}


@require_torchcodec
def test_dataset_with_audio_feature_map_is_decoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path], "text": ["Hello"]}
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    def process_audio_sampling_rate_by_example(example):
        sample_rate = example["audio"].get_all_samples().sample_rate
        example["double_sampling_rate"] = 2 * sample_rate
        return example

    decoded_dset = dset.map(process_audio_sampling_rate_by_example)
    for item in decoded_dset.cast_column("audio", Audio(decode=False)):
        assert item.keys() == {"audio", "text", "double_sampling_rate"}
        assert item["double_sampling_rate"] == 88200

    def process_audio_sampling_rate_by_batch(batch):
        double_sampling_rates = []
        for audio in batch["audio"]:
            double_sampling_rates.append(2 * audio.get_all_samples().sample_rate)
        batch["double_sampling_rate"] = double_sampling_rates
        return batch

    decoded_dset = dset.map(process_audio_sampling_rate_by_batch, batched=True)
    for item in decoded_dset.cast_column("audio", Audio(decode=False)):
        assert item.keys() == {"audio", "text", "double_sampling_rate"}
        assert item["double_sampling_rate"] == 88200


@require_torchcodec
def test_formatted_dataset_with_audio_feature(shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path, audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"audio"}
        assert isinstance(item["audio"], AudioDecoder)
        samples = item["audio"].get_all_samples()
        assert samples.sample_rate == 44100
        assert samples.data.shape == (2, 202311)
        batch = dset[:1]
        assert batch.keys() == {"audio"}
        assert len(batch["audio"]) == 1
        assert isinstance(batch["audio"][0], AudioDecoder)
        samples = batch["audio"][0].get_all_samples()
        assert samples.sample_rate == 44100
        assert samples.data.shape == (2, 202311)
        column = dset["audio"]
        assert len(column) == 2
        assert isinstance(column[0], AudioDecoder)
        samples = column[0].get_all_samples()
        assert samples.sample_rate == 44100
        assert samples.data.shape == (2, 202311)

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["audio"]
        assert isinstance(item["audio"][0], AudioDecoder)
        samples = item["audio"][0].get_all_samples()
        assert samples.sample_rate == 44100
        assert samples.data.shape == (2, 202311)
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["audio"]
        assert isinstance(batch["audio"][0], AudioDecoder)
        samples = batch["audio"][0].get_all_samples()
        assert samples.sample_rate == 44100
        assert samples.data.shape == (2, 202311)
        column = dset["audio"]
        assert len(column) == 2
        assert isinstance(column[0], AudioDecoder)
        samples = column[0].get_all_samples()
        assert samples.sample_rate == 44100
        assert samples.data.shape == (2, 202311)


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


@require_torchcodec
@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_with_audio_feature(streaming, jsonl_audio_dataset_path, shared_datadir):
    from torchcodec.decoders import AudioDecoder

    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data_files = jsonl_audio_dataset_path
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = load_dataset("json", split="train", data_files=data_files, features=features, streaming=streaming)
    item = dset[0] if not streaming else next(iter(dset))
    assert item.keys() == {"audio", "text"}
    assert isinstance(item["audio"], AudioDecoder)
    samples = item["audio"].get_all_samples()
    assert samples.sample_rate == 44100
    assert samples.data.shape == (2, 202311)
    assert item["audio"].metadata.path == audio_path


@require_torchcodec
@pytest.mark.integration
def test_dataset_with_audio_feature_loaded_from_cache():
    # load first time
    ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean")
    # load from cache
    ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
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


def test_audio_embed_storage(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    example = {"bytes": None, "path": audio_path}
    storage = pa.array([example], type=pa.struct({"bytes": pa.binary(), "path": pa.string()}))
    embedded_storage = Audio().embed_storage(storage)
    embedded_example = embedded_storage.to_pylist()[0]
    assert embedded_example == {"bytes": open(audio_path, "rb").read(), "path": "test_audio_44100.wav"}
