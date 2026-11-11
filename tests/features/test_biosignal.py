"""Tests for the Biosignal feature type."""

import shutil

import numpy as np
import pyarrow as pa
import pytest

import datasets
from datasets import Biosignal, Dataset, Features, Value
from datasets.features.features import require_decoding


require_mne = pytest.mark.skipif(not datasets.config.MNE_AVAILABLE, reason="mne is not installed")
require_mne_bids = pytest.mark.skipif(
    not (datasets.config.MNE_AVAILABLE and datasets.config.MNE_BIDS_AVAILABLE),
    reason="mne and mne_bids are not installed",
)


def _make_raw(ch_type: str = "eeg", sfreq: float = 100.0):
    import mne

    info = mne.create_info(["Ch1", "Ch2"], sfreq=sfreq, ch_types=ch_type)
    data = np.array([[1e-5, -1e-5] * 50, [-2e-5, 2e-5] * 50], dtype=np.float64)
    raw = mne.io.RawArray(data, info, verbose="ERROR")
    raw.info["line_freq"] = 50.0
    return raw


def test_biosignal_storage_and_schema(tmp_path, monkeypatch):
    feat = Biosignal()
    assert feat.pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()}) == feat()
    assert require_decoding(feat) and not require_decoding(Biosignal(decode=False))
    assert Features.from_dict(Features({"b": Biosignal(decode=False)}).to_dict()) == Features(
        {"b": Biosignal(decode=False)}
    )
    assert Biosignal(decode=False).flatten() == {"bytes": Value("binary"), "path": Value("string")}
    assert Biosignal(decode=True).flatten() == Biosignal(decode=True)

    path = tmp_path / "rec.edf"
    path.write_bytes(b"payload")
    assert feat.encode_example(str(path)) == {"path": str(path), "bytes": None}
    assert feat.encode_example(path) == {"path": str(path.absolute()), "bytes": None}
    assert feat.encode_example(bytearray(b"raw")) == {"path": None, "bytes": b"raw"}
    assert feat.encode_example({"path": str(path), "bytes": b"dup"}) == {"path": str(path), "bytes": None}
    assert feat.encode_example({"bytes": b"raw"}) == {"path": None, "bytes": b"raw"}
    with pytest.raises(ValueError, match="should have one of 'path' or 'bytes'"):
        feat.encode_example({"path": None, "bytes": None})
    with pytest.raises(RuntimeError, match="Decoding is disabled"):
        Biosignal(decode=False).decode_example({"path": "x.edf", "bytes": b"y"})

    ds = Dataset.from_dict({"b": [str(path)]}, features=Features({"b": Biosignal(decode=False)}))
    assert ds[0]["b"] == {"bytes": None, "path": str(path)}
    assert feat.cast_storage(pa.array(["a.edf"], type=pa.string())).to_pylist() == [{"bytes": None, "path": "a.edf"}]
    assert feat.cast_storage(pa.array([b"x"], type=pa.binary())).to_pylist() == [{"bytes": b"x", "path": None}]
    storage = pa.array([{"bytes": None, "path": "/data/rec.edf"}, None], type=feat.pa_type)
    assert feat.embed_storage(storage, local_files=False, remote_files=False).to_pylist() == [
        {"bytes": None, "path": "/data/rec.edf"},
        None,
    ]

    monkeypatch.setattr(datasets.config, "MNE_AVAILABLE", False)
    with pytest.raises(ImportError, match="install 'mne'"):
        feat.decode_example({"path": str(path), "bytes": None})


@require_mne
def test_biosignal_local_raw_and_bytes(tmp_path):
    import mne

    raw = _make_raw()
    fif_path = tmp_path / "sample_raw.fif"
    raw.save(str(fif_path), overwrite=True, verbose="ERROR")

    ds = Dataset.from_dict({"biosignal": [str(fif_path)]}, features=Features({"biosignal": Biosignal()}))
    loaded = ds[0]["biosignal"]
    assert isinstance(loaded, mne.io.BaseRaw) and not loaded.preload
    assert Biosignal().decode_example(loaded) is loaded
    np.testing.assert_allclose(loaded.get_data(), raw.get_data(), atol=1e-6)

    cropped = loaded.copy().load_data().crop(tmax=0.49)
    ds_mem = Dataset.from_dict({"biosignal": [cropped]}, features=Features({"biosignal": Biosignal()}))
    assert isinstance(ds_mem.features["biosignal"], Biosignal)
    assert ds_mem[0]["biosignal"].n_times == 50
    np.testing.assert_allclose(ds_mem[0]["biosignal"].get_data(), cropped.get_data(), atol=1e-6)

    edf_path = tmp_path / "sample.edf"
    mne.export.export_raw(str(edf_path), raw, fmt="edf", overwrite=True, verbose="ERROR")
    from_edf_bytes = Biosignal().decode_example({"path": "sample.edf", "bytes": edf_path.read_bytes()})
    np.testing.assert_allclose(from_edf_bytes.get_data(), raw.get_data(), atol=1e-4)

    # operations on the recordings go through map, which encodes the returned raw objects
    mapped = ds.map(lambda x: {"biosignal": x["biosignal"].load_data().pick(["Ch1"]).resample(50.0, verbose="ERROR")})
    assert mapped[0]["biosignal"].ch_names == ["Ch1"] and mapped[0]["biosignal"].info["sfreq"] == 50.0


@require_mne_bids
@pytest.mark.parametrize(
    "fmt,ext,datatype",
    [
        ("BrainVision", ".vhdr", "eeg"),
        ("EDF", ".edf", "eeg"),
        ("BDF", ".bdf", "eeg"),
        ("EEGLAB", ".set", "eeg"),
        ("FIF", ".fif", "meg"),
    ],
)
def test_biosignal_bids_formats_and_embed(tmp_path, fmt, ext, datatype):
    import mne
    import mne_bids

    raw = _make_raw(ch_type="eeg" if datatype == "eeg" else "mag")
    raw.set_annotations(mne.Annotations(onset=[0.1], duration=[0.2], description=["stimulus"]))
    bids_root = tmp_path / "bids_root"
    bp = mne_bids.BIDSPath(
        subject="01",
        session="01",
        task="rest",
        run="01",
        datatype=datatype,
        suffix=datatype,
        extension=ext,
        root=bids_root,
    )
    mne_bids.write_raw_bids(raw, bp, allow_preload=True, format=fmt, overwrite=True, verbose="ERROR")

    ds = Dataset.from_dict({"biosignal": [str(bp.fpath)]}, features=Features({"biosignal": Biosignal()}))
    decoded = ds[0]["biosignal"]
    assert decoded.info["line_freq"] == 50.0 and list(decoded.annotations.description) == ["stimulus"]

    saved_path = tmp_path / "saved_ds"
    ds.save_to_disk(str(saved_path))
    shutil.rmtree(bids_root)
    reloaded = datasets.load_from_disk(str(saved_path))
    assert reloaded.cast_column("biosignal", Biosignal(decode=False))[0]["biosignal"]["path"].endswith(".fif")
    reloaded_raw = reloaded[0]["biosignal"]
    assert reloaded_raw.info["line_freq"] == 50.0 and list(reloaded_raw.annotations.description) == ["stimulus"]
    np.testing.assert_allclose(reloaded_raw.get_data(), raw.get_data(), atol=1e-4)
