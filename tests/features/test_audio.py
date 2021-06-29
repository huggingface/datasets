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
def test_audio_encode_example(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    audio = Audio()
    encoded_example = audio.encode_example(audio_path)
    assert encoded_example.keys() == {"array", "sample_rate"}
    assert encoded_example["array"].shape == (404622,)  # TODO: (202311, 2)
    assert encoded_example["sample_rate"] == 44100


@pytest.mark.skipif(
    sys.platform == "linux", reason="linux requires libsndfile installed using distribution package manager"
)
def test_dataset_with_audio_feature(shared_datadir):
    audio_path = str(shared_datadir / "test_audio_44100.wav")
    data = {"file": [audio_path]}
    features = Features({"file": Audio()})
    dset = Dataset.from_dict(data, features=features)
    assert dset.shape == (1, 1)
    assert dset.column_names == ["file"]
    assert isinstance(dset[0]["file"], dict)
    assert dset[0]["file"].keys() == {"array", "sample_rate"}
    assert len(dset[0]["file"]["array"]) == 404622  # TODO: to numpy? .shape == (202311, 2)
    assert dset[0]["file"]["sample_rate"] == 44100
