import sys

import pytest

from datasets import Dataset
from datasets.features import Audio, Features


def test_audio_instantiation():
    audio = Audio()
    assert audio.id is None
    assert audio.dtype == "dict"
    assert audio.pa_type is None
    assert audio._type == "Audio"


@pytest.mark.skipif(
    sys.platform == "linux", reason="linux requires libsndfile installed using distribution package manager"
)
def test_audio_decode_example(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio()
    decoded_example = audio.decode_example(audio_path)
    assert decoded_example.keys() == {"array", "sampling_rate"}
    assert decoded_example["array"].shape == (202311,)
    assert decoded_example["sampling_rate"] == 44100


@pytest.mark.skipif(
    sys.platform == "linux", reason="linux requires libsndfile installed using distribution package manager"
)
def test_dataset_with_audio_feature(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"audio": [audio_path]}
    features = Features({"audio": Audio()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"audio"}
    assert item["audio"].keys() == {"array", "sampling_rate"}
    assert item["audio"]["array"].shape == (202311,)
    assert item["audio"]["sampling_rate"] == 44100
