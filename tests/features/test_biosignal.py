"""Tests for the Biosignal feature type."""

import numpy as np
import pyarrow as pa
import pytest

import datasets
from datasets import Biosignal, Dataset, Features, Value


require_mne = pytest.mark.skipif(not datasets.config.MNE_AVAILABLE, reason="mne is not installed")
require_mne_bids = pytest.mark.skipif(
    not (datasets.config.MNE_AVAILABLE and datasets.config.MNE_BIDS_AVAILABLE),
    reason="mne and mne_bids are not installed",
)


def _make_raw(sfreq: float = 100.0):
    import mne

    info = mne.create_info(["Fp1", "Fp2"], sfreq=sfreq, ch_types="eeg")
    data = np.array([[1e-5, -1e-5] * 50, [-2e-5, 2e-5] * 50], dtype=np.float64)
    raw = mne.io.RawArray(data, info, verbose="ERROR")
    raw.info["line_freq"] = 50.0
    return raw


# --------------------------------------------------------------------------
# Storage and encoding (no mne import needed)
# --------------------------------------------------------------------------


def test_storage_type_is_bytes_path_struct():
    assert Biosignal().pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert Biosignal()() == Biosignal().pa_type


def test_encode_example_from_path_and_bytes(tmp_path):
    path = tmp_path / "rec.edf"
    assert Biosignal().encode_example(str(path)) == {"path": str(path), "bytes": None}
    assert Biosignal().encode_example(path) == {"path": str(path.absolute()), "bytes": None}
    assert Biosignal().encode_example(b"raw") == {"path": None, "bytes": b"raw"}


def test_encode_example_rejects_empty_dict():
    with pytest.raises(ValueError, match="should have one of 'path' or 'bytes'"):
        Biosignal().encode_example({"path": None, "bytes": None})


def test_decode_false_returns_raw_and_never_decodes(tmp_path):
    path = str(tmp_path / "rec.edf")
    (tmp_path / "rec.edf").write_bytes(b"payload")
    ds = Dataset.from_dict({"biosignal": [path]}, features=Features({"biosignal": Biosignal(decode=False)}))
    assert ds[0]["biosignal"] == {"bytes": None, "path": path}


def test_decode_example_raises_when_decode_disabled():
    with pytest.raises(RuntimeError, match="Decoding is disabled"):
        Biosignal(decode=False).decode_example({"path": "x.edf", "bytes": b"y"})


def test_flatten_when_not_decoding():
    assert Biosignal(decode=False).flatten() == {
        "bytes": Value("binary"),
        "path": Value("string"),
    }
    assert Biosignal(decode=True).flatten() == Biosignal(decode=True)


def test_feature_roundtrips_through_dict():
    features = Features({"biosignal": Biosignal(preload=True)})
    assert Features.from_dict(features.to_dict()) == features


def test_cast_storage_from_string_and_binary():
    feature = Biosignal()
    from_str = feature.cast_storage(pa.array(["a.edf", "b.edf"], type=pa.string()))
    assert from_str.type == feature.pa_type
    assert from_str.to_pylist() == [{"bytes": None, "path": "a.edf"}, {"bytes": None, "path": "b.edf"}]

    from_bin = feature.cast_storage(pa.array([b"x"], type=pa.binary()))
    assert from_bin.to_pylist() == [{"bytes": b"x", "path": None}]


def test_embed_storage_keeps_path_only_rows_when_embedding_is_off():
    feature = Biosignal()
    storage = pa.array([{"bytes": None, "path": "/data/rec.edf"}, None], type=feature.pa_type)
    embedded = feature.embed_storage(storage, local_files=False, remote_files=False)
    assert embedded.to_pylist() == [{"bytes": None, "path": "rec.edf"}, None]


# --------------------------------------------------------------------------
# Decoding and BIDS integration (requires mne / mne_bids)
# --------------------------------------------------------------------------


@require_mne
def test_biosignal_decodes_local_fif_lazily(tmp_path):
    import mne

    raw = _make_raw()
    fif_path = tmp_path / "sample_raw.fif"
    raw.save(str(fif_path), overwrite=True, verbose="ERROR")

    ds = Dataset.from_dict({"biosignal": [str(fif_path)]}, features=Features({"biosignal": Biosignal(preload=False)}))
    loaded = ds[0]["biosignal"]
    assert isinstance(loaded, mne.io.BaseRaw)
    assert not loaded.preload
    assert loaded.ch_names == ["Fp1", "Fp2"]
    assert loaded.info["sfreq"] == 100.0
    np.testing.assert_allclose(loaded.get_data(), raw.get_data(), atol=1e-6)


@require_mne
def test_biosignal_encodes_and_decodes_mne_raw_instance(tmp_path):
    import mne

    raw = _make_raw()
    fif_path = tmp_path / "orig_raw.fif"
    raw.save(str(fif_path), overwrite=True, verbose="ERROR")
    cropped = mne.io.read_raw_fif(str(fif_path), preload=True, verbose="ERROR").crop(tmax=0.49)

    # Automatic feature inference from mne.io.BaseRaw + preservation of in-memory modifications
    ds = Dataset.from_dict({"biosignal": [cropped]})
    assert isinstance(ds.features["biosignal"], Biosignal)
    loaded = ds[0]["biosignal"]
    assert isinstance(loaded, mne.io.BaseRaw)
    assert loaded.ch_names == ["Fp1", "Fp2"]
    assert loaded.n_times == 50
    np.testing.assert_allclose(loaded.get_data(), cropped.get_data(), atol=1e-6)

    # Also test Dataset._estimate_nbytes accounts for external Biosignal files
    ds_ext = Dataset.from_dict({"biosignal": [str(fif_path)]}, features=Features({"biosignal": Biosignal()}))
    assert ds_ext._estimate_nbytes() >= fif_path.stat().st_size


@require_mne_bids
def test_biosignal_bids_sidecar_and_multifile_embed(tmp_path):
    import mne
    import mne_bids

    raw = _make_raw()
    raw.set_annotations(mne.Annotations(onset=[0.1], duration=[0.2], description=["stimulus"]))
    bids_root = tmp_path / "bids_root"
    bids_path = mne_bids.BIDSPath(
        subject="01",
        session="01",
        task="rest",
        run="01",
        datatype="eeg",
        suffix="eeg",
        extension=".vhdr",
        root=bids_root,
    )
    mne_bids.write_raw_bids(raw, bids_path, allow_preload=True, format="BrainVision", overwrite=True, verbose="ERROR")

    ds = Dataset.from_dict({"biosignal": [str(bids_path.fpath)]}, features=Features({"biosignal": Biosignal()}))
    decoded = ds[0]["biosignal"]
    assert isinstance(decoded, mne.io.BaseRaw)
    assert decoded.info["line_freq"] == 50.0
    assert list(decoded.annotations.description) == ["stimulus"]

    # Embedding storage converts multi-file BIDS BrainVision (.vhdr/.vmrk/.eeg + sidecars) into self-contained bytes
    parquet_path = tmp_path / "embedded.parquet"
    ds.to_parquet(str(parquet_path))
    reloaded = Dataset.from_parquet(str(parquet_path))
    reloaded_raw = reloaded[0]["biosignal"]
    assert isinstance(reloaded_raw, mne.io.BaseRaw)
    assert reloaded_raw.info["line_freq"] == 50.0
    assert list(reloaded_raw.annotations.description) == ["stimulus"]
    np.testing.assert_allclose(reloaded_raw.get_data(), raw.get_data(), atol=1e-5)
