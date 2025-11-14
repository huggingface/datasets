from unittest import TestCase

import pytest

from datasets import Dataset, Features
from datasets.features import Midi


class TestMidiFeature(TestCase):
    def test_audio_feature_type(self):
        midi = Midi()
        assert midi.dtype == "dict"
        assert midi.pa_type.names == ["bytes", "path"]

    def test_audio_feature_encode_example(self):
        midi = Midi()

        # Test with path
        encoded = midi.encode_example("path/to/midi.mid")
        assert encoded == {"bytes": None, "path": "path/to/midi.mid"}

        # Test with bytes
        encoded = midi.encode_example(b"fake_midi_bytes")
        assert encoded == {"bytes": b"fake_midi_bytes", "path": None}

        # Test with dict containing notes
        notes_data = {"notes": [[60, 64, 0.0, 1.0], [62, 64, 1.0, 2.0]], "tempo": 120.0, "resolution": 480}
        encoded = midi.encode_example(notes_data)
        assert "bytes" in encoded
        assert encoded["path"] is None

    def test_audio_feature_decode_example(self):
        midi = Midi()

        # Test decode with bytes
        fake_midi_bytes = b"MThd\x00\x00\x00\x06\x00\x01\x00\x02\x00\xdcMTrk\x00\x00\x00\x13\x00\xffQ\x03\x07\xa1 \x00\xffX\x04\x04\x02\x18\x08\x01\xff/\x00MTrk\x00\x00\x00\x16\x00\xc0\x00\x00\x90<@\x838<\x00\x00>@\x838>\x00\x01\xff/\x00"
        decoded = midi.decode_example({"bytes": fake_midi_bytes, "path": None})
        assert "notes" in decoded
        assert "tempo" in decoded
        assert "resolution" in decoded
        assert "instruments" in decoded

    def test_audio_feature_with_dataset(self):
        features = Features({"midi": Midi()})
        data = {"midi": ["fake_path1.mid", "fake_path2.mid"]}

        dataset = Dataset.from_dict(data, features=features)
        assert "midi" in dataset.column_names
        assert dataset.features["midi"].dtype == "dict"

    def test_audio_feature_decode_false(self):
        midi = Midi(decode=False)
        encoded = midi.encode_example("path/to/midi.mid")
        assert encoded == {"bytes": None, "path": "path/to/midi.mid"}

    def test_audio_feature_resolution(self):
        midi = Midi(resolution=960)
        assert midi.resolution == 960

    def test_audio_feature_flatten(self):
        midi = Midi(decode=False)
        flattened = midi.flatten()
        assert "bytes" in flattened  # type: ignore
        assert "path" in flattened  # type: ignore

    def test_audio_feature_decode_error(self):
        midi = Midi(decode=False)
        with pytest.raises(RuntimeError):
            midi.decode_example({"bytes": b"fake", "path": None})
