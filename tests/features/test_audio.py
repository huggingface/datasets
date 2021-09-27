import sys
from ctypes.util import find_library
from importlib.util import find_spec

import pytest

from datasets import Dataset
from datasets.features import Audio, Features, Value


pytestmark = pytest.mark.audio


require_sndfile = pytest.mark.skipif(
    # In Windows and OS X, soundfile installs sndfile
    (sys.platform != "linux" and find_spec("soundfile") is None)
    # In Linux, soundfile throws RuntimeError if sndfile not installed with distribution package manager
    or (sys.platform == "linux" and find_library("sndfile") is None),
    reason="Test requires 'sndfile': `pip install soundfile`; "
    "Linux requires sndfile installed with distribution package manager, e.g.: `sudo apt-get install libsndfile1`",
)
require_sox = pytest.mark.skipif(
    find_library("sox") is None,
    reason="Test requires 'sox'; only available in non-Windows, e.g.: `sudo apt-get install sox`",
)
require_torchaudio = pytest.mark.skipif(find_spec("torchaudio") is None, reason="Test requires 'torchaudio'")


def test_audio_instantiation():
    audio = Audio()
    assert audio.id is None
    assert audio.dtype == "dict"
    assert audio.pa_type is None
    assert audio._type == "Audio"


@require_sndfile
def test_audio_decode_example(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio()
    decoded_example = audio.decode_example(audio_path)
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (202311,)
    assert decoded_example["sampling_rate"] == 44100


@require_sndfile
def test_audio_resampling(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio(sampling_rate=16000)
    decoded_example = audio.decode_example(audio_path)
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (73401,)
    assert decoded_example["sampling_rate"] == 16000


@require_sox
@require_torchaudio
def test_audio_decode_example_mp3(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.mp3")
    audio = Audio()
    decoded_example = audio.decode_example(audio_path)
    assert decoded_example.keys() == {"path", "array", "sampling_rate"}
    assert decoded_example["path"] == audio_path
    assert decoded_example["array"].shape == (109440,)
    assert decoded_example["sampling_rate"] == 44100


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


@require_sndfile
def test_dataset_with_audio_feature_map_is_not_decoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path], "text": ["Hello"]}
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    for item in dset:
        assert item.keys() == {"audio", "text"}
        assert item == {"audio": audio_path, "text": "Hello"}

    def process_text(example):
        example["text"] = example["text"] + " World!"
        return example

    processed_dset = dset.map(process_text)
    for item in processed_dset:
        assert item.keys() == {"audio", "text"}
        assert item == {"audio": audio_path, "text": "Hello World!"}


@require_sndfile
def test_dataset_with_audio_feature_map_is_decoded(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path], "text": ["Hello"]}
    features = Features({"audio": Audio(), "text": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    def process_audio_sampling_rate(example):
        example["double_sampling_rate"] = 2 * example["audio"]["sampling_rate"]
        return example

    decoded_dset = dset.map(process_audio_sampling_rate)
    for item in decoded_dset:
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

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["audio"]
        assert item["audio"][0].keys() == {"path", "array", "sampling_rate"}
        assert item["audio"][0]["path"] == audio_path
        assert item["audio"][0]["array"].shape == (202311,)
        assert item["audio"][0]["sampling_rate"] == 44100
