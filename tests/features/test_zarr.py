import pickle
import sys
import types
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pyarrow as pa
import pytest

from datasets import Dataset, Features
from datasets.features.zarr import (
    OmeZarrProxy,
    Zarr,
    ZarrArrayProxy,
    ZarrGroupProxy,
    ZarrProxy,
    _extract_repo_id_from_hf_path,
    _get_ome_attr,
    _is_ome_zarr,
    _open_zarr_store,
    _render_array_as_png,
)
from datasets.features.zarr_cache import CHUNK_CACHE, STORE_REGISTRY, cached_array_getitem

from ..utils import require_zarr


@pytest.fixture(autouse=True)
def _clean_zarr_caches():
    CHUNK_CACHE.clear()
    STORE_REGISTRY.clear()
    yield
    CHUNK_CACHE.clear()
    STORE_REGISTRY.clear()


def _create_zarr_array(tmp_path, shape=(10, 20), dtype="float32", chunks=(5, 10)):
    import zarr

    store_path = str(tmp_path / "array.zarr")
    z = zarr.open_array(store_path, mode="w", shape=shape, dtype=dtype, chunks=chunks)
    z[:] = np.arange(np.prod(shape), dtype=dtype).reshape(shape)
    return store_path


def _create_zarr_group(tmp_path):
    import zarr

    store_path = str(tmp_path / "group.zarr")
    root = zarr.open_group(store_path, mode="w")
    root.attrs["description"] = "test group"
    arr = root.create_array("data", shape=(5, 5), dtype="float32", chunks=(5, 5))
    arr[:] = np.ones((5, 5))
    root.create_array("mask", shape=(5, 5), dtype="uint8", chunks=(5, 5))
    root["mask"][:] = np.zeros((5, 5), dtype="uint8")
    return store_path


def _create_ome_zarr(tmp_path):
    import zarr

    store_path = str(tmp_path / "ome.zarr")
    root = zarr.open_group(store_path, mode="w")
    root.attrs["multiscales"] = [
        {
            "version": "0.4",
            "axes": [
                {"name": "y", "type": "space", "unit": "micrometer"},
                {"name": "x", "type": "space", "unit": "micrometer"},
            ],
            "datasets": [
                {"path": "0", "coordinateTransformations": [{"type": "scale", "scale": [1.0, 1.0]}]},
                {"path": "1", "coordinateTransformations": [{"type": "scale", "scale": [2.0, 2.0]}]},
            ],
        }
    ]
    root.attrs["omero"] = {
        "channels": [{"label": "DAPI"}, {"label": "GFP"}],
    }
    arr0 = root.create_array("0", shape=(20, 20), dtype="float32", chunks=(10, 10))
    arr0[:] = np.arange(400, dtype="float32").reshape(20, 20)
    arr1 = root.create_array("1", shape=(10, 10), dtype="float32", chunks=(5, 5))
    arr1[:] = np.arange(100, dtype="float32").reshape(10, 10)
    return store_path


def _create_ome_zarr_v05(tmp_path):
    import zarr

    store_path = str(tmp_path / "ome_v05.zarr")
    root = zarr.open_group(store_path, mode="w")
    root.attrs["ome"] = {
        "version": "0.5",
        "multiscales": [
            {
                "axes": [
                    {"name": "z", "type": "space", "unit": "micrometer"},
                    {"name": "y", "type": "space", "unit": "micrometer"},
                    {"name": "x", "type": "space", "unit": "micrometer"},
                ],
                "datasets": [
                    {"path": "0", "coordinateTransformations": [{"type": "scale", "scale": [5.0, 1.0, 1.0]}]},
                    {"path": "1", "coordinateTransformations": [{"type": "scale", "scale": [5.0, 2.0, 2.0]}]},
                ],
            }
        ],
        "omero": {
            "channels": [{"label": "tdTomato", "color": "FFFFFF"}],
            "id": 1,
            "rdefs": {"defaultT": 0, "defaultZ": 0, "model": "greyscale"},
        },
    }
    arr0 = root.create_array("0", shape=(10, 64, 64), dtype="uint16", chunks=(1, 64, 64))
    arr0[:] = np.arange(40960, dtype="uint16").reshape(10, 64, 64)
    arr1 = root.create_array("1", shape=(10, 32, 32), dtype="uint16", chunks=(1, 32, 32))
    arr1[:] = np.arange(10240, dtype="uint16").reshape(10, 32, 32)
    return store_path


@require_zarr
class TestZarrEncodeExample:
    def test_encode_string(self):
        zarr_feat = Zarr()
        result = zarr_feat.encode_example("/data/scan.zarr")
        assert result == {"path": "/data/scan.zarr"}

    def test_encode_path(self, tmp_path):
        zarr_feat = Zarr()
        result = zarr_feat.encode_example(Path(tmp_path / "scan.zarr"))
        assert result == {"path": str((tmp_path / "scan.zarr").absolute())}

    def test_encode_dict_with_path(self):
        zarr_feat = Zarr()
        result = zarr_feat.encode_example({"path": "/data/scan.zarr"})
        assert result == {"path": "/data/scan.zarr"}

    def test_encode_dict_without_path_raises(self):
        zarr_feat = Zarr()
        with pytest.raises(ValueError, match="must have a 'path' key"):
            zarr_feat.encode_example({"url": "/data/scan.zarr"})

    def test_encode_zarr_array(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path)
        arr = zarr.open_array(store_path, mode="r")
        zarr_feat = Zarr()
        result = zarr_feat.encode_example(arr)
        assert "path" in result
        assert result["path"] is not None

    def test_encode_zarr_group(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        grp = zarr.open_group(store_path, mode="r")
        zarr_feat = Zarr()
        result = zarr_feat.encode_example(grp)
        assert "path" in result
        assert result["path"] is not None

    def test_encode_unsupported_type_raises(self):
        zarr_feat = Zarr()
        with pytest.raises(ValueError, match="must be a string path"):
            zarr_feat.encode_example(42)


@require_zarr
class TestZarrDecodeExample:
    def test_decode_local_array(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        result = zarr_feat.decode_example(encoded)
        assert isinstance(result, ZarrProxy)
        resolved = result._resolve()
        assert isinstance(resolved, ZarrArrayProxy)
        assert result.shape == (10, 20)
        assert result.dtype == np.dtype("float32")
        assert result.ndim == 2
        assert result.chunks == (5, 10)
        np.testing.assert_array_equal(np.asarray(result[:]), np.arange(200, dtype="float32").reshape(10, 20))

    def test_decode_local_group(self, tmp_path):
        store_path = _create_zarr_group(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        result = zarr_feat.decode_example(encoded)
        assert isinstance(result, ZarrProxy)
        resolved = result._resolve()
        assert isinstance(resolved, ZarrGroupProxy)
        assert "data" in result
        assert "mask" in result
        assert sorted(result.keys()) == ["data", "mask"]
        assert result.attrs == {"description": "test group"}

    def test_decode_ome_zarr(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        result = zarr_feat.decode_example(encoded)
        assert isinstance(result, ZarrProxy)
        assert isinstance(result._resolve(), OmeZarrProxy)
        assert result.num_levels == 2
        assert result.shape == (20, 20)
        assert result.dtype == np.dtype("float32")
        assert result.ndim == 2
        assert result.chunks == (10, 10)
        assert result.channel_names == ["DAPI", "GFP"]
        level0 = result.get_level(0)
        assert isinstance(level0, ZarrArrayProxy)
        assert level0.shape == (20, 20)
        level_last = result.get_level(-1)
        assert level_last.shape == (10, 10)
        levels = result.levels
        assert len(levels) == 2

    def test_decode_no_decode(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        zarr_feat = Zarr(decode=False)
        encoded = zarr_feat.encode_example(store_path)
        result = zarr_feat.decode_example(encoded)
        assert result == {"path": store_path}

    def test_decode_missing_zarr_raises(self, tmp_path):
        zarr_feat = Zarr()
        with patch("datasets.features.zarr.config.ZARR_AVAILABLE", False):
            with pytest.raises(ImportError, match="zarr"):
                zarr_feat.decode_example({"path": "/some/path.zarr"})


@require_zarr
class TestZarrStorageOptions:
    def test_decode_example_stores_storage_options(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        zarr_feat = Zarr(storage_options={"simplecache": {"cache_storage": "/tmp/zarr-cache"}})
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        assert proxy._storage_options == {"simplecache": {"cache_storage": "/tmp/zarr-cache"}}

    def test_storage_options_reach_open_zarr_store(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path)
        arr = zarr.open_array(store_path, mode="r")
        zarr_feat = Zarr(storage_options={"anon": True})
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        with patch("datasets.features.zarr._open_zarr_store", return_value=arr) as mock_open:
            assert proxy.shape == (10, 20)
        mock_open.assert_called_once_with(store_path, {}, {"anon": True})

    def test_pickle_roundtrip_preserves_storage_options(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        zarr_feat = Zarr(storage_options={"simplecache": {"cache_storage": "/tmp/zarr-cache"}})
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        restored = pickle.loads(pickle.dumps(proxy))
        assert restored._storage_options == {"simplecache": {"cache_storage": "/tmp/zarr-cache"}}
        np.testing.assert_array_equal(np.asarray(restored[:5, :5]), np.asarray(proxy[:5, :5]))


@require_zarr
class TestAsArray:
    def test_array_proxy_asarray(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        zarr_feat = Zarr()
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        arr = proxy.asarray()
        assert isinstance(arr, np.ndarray)
        np.testing.assert_array_equal(arr, np.arange(200, dtype="float32").reshape(10, 20))

    def test_ome_proxy_asarray(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        assert proxy.asarray().shape == (20, 20)
        assert proxy.asarray(level=-1).shape == (10, 10)

    def test_group_proxy_asarray_raises(self, tmp_path):
        store_path = _create_zarr_group(tmp_path)
        zarr_feat = Zarr()
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        with pytest.raises(TypeError, match="ZarrGroup"):
            proxy.asarray()


@require_zarr
class TestAxisNames:
    def test_v04_axis_names_and_types(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        assert proxy.axis_names == ["y", "x"]
        assert proxy.axis_types == ["space", "space"]

    def test_v05_axis_names_and_types(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        assert proxy.axis_names == ["z", "y", "x"]
        assert proxy.axis_types == ["space", "space", "space"]

    def test_empty_axes(self, tmp_path):
        import zarr

        store_path = str(tmp_path / "noaxes.zarr")
        root = zarr.open_group(store_path, mode="w")
        root.attrs["multiscales"] = [{"datasets": [{"path": "0"}]}]
        root.create_array("0", shape=(4, 4), dtype="uint8")
        grp = zarr.open_group(store_path, mode="r")
        proxy = OmeZarrProxy(grp, store_path)
        assert proxy.axis_names == []
        assert proxy.axis_types == []


def _install_fake_pil(monkeypatch):
    """Install a minimal PIL stub so ``_render_array_as_png`` uses it."""
    fake = types.ModuleType("PIL")

    class _FakeImage:
        def __init__(self, arr):
            self._arr = arr

        def thumbnail(self, size, resample=None):
            pass

        def save(self, buf, format=None):
            buf.write(b"FAKEPNGDATA")

    fake.Image = type(
        "Image",
        (),
        {"LANCZOS": 1, "fromarray": staticmethod(lambda arr, mode=None: _FakeImage(arr))},
    )
    monkeypatch.setitem(sys.modules, "PIL", fake)


@require_zarr
class TestReprHtml:
    def test_ome_proxy_repr_html_embeds_thumbnail(self, tmp_path, monkeypatch):
        _install_fake_pil(monkeypatch)
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        html = proxy._repr_html_()
        assert html is not None
        assert "data:image/png;base64," in html
        assert "RkFLRVBOR0RBVEE=" in html  # base64 of the fake PNG bytes
        assert "shape=(20, 20)" in html

    def test_array_proxy_repr_html_embeds_thumbnail(self, tmp_path, monkeypatch):
        _install_fake_pil(monkeypatch)
        store_path = _create_zarr_array(tmp_path)
        zarr_feat = Zarr()
        proxy = zarr_feat.decode_example(zarr_feat.encode_example(store_path))
        html = proxy._repr_html_()
        assert html is not None
        assert "data:image/png;base64," in html

    def test_zarr_proxy_delegates_repr_html(self, tmp_path, monkeypatch):
        _install_fake_pil(monkeypatch)
        store_path = _create_ome_zarr(tmp_path)
        proxy = ZarrProxy(path=store_path)
        html = proxy._repr_html_()
        assert html is not None
        assert "data:image/png;base64," in html

    def test_1d_array_repr_html_none(self, tmp_path, monkeypatch):
        _install_fake_pil(monkeypatch)
        import zarr

        store_path = str(tmp_path / "oned.zarr")
        z = zarr.open_array(store_path, mode="w", shape=(10,), dtype="float32")
        z[:] = np.arange(10)
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        assert proxy._repr_html_() is None

    def test_render_array_as_png_invalid_inputs(self):
        assert _render_array_as_png(np.zeros((0, 0))) is None
        assert _render_array_as_png(np.zeros(5)) is None
        assert _render_array_as_png(np.array([])) is None


@require_zarr
class TestZarrProxy:
    def test_unresolved_repr(self):
        proxy = ZarrProxy(path="/data/scan.zarr")
        r = repr(proxy)
        assert "ZarrProxy" in r
        assert "/data/scan.zarr" in r

    def test_resolved_repr_array(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        proxy = ZarrProxy(path=store_path)
        proxy.shape  # force resolution
        r = repr(proxy)
        assert "ZarrArrayProxy" in r or "shape" in r

    def test_pickle_roundtrip(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        data = proxy[:5, :5]
        expected = np.asarray(data)

        pickled = pickle.dumps(proxy)
        restored = pickle.loads(pickled)
        assert restored._resolved is None
        result = restored[:5, :5]
        np.testing.assert_array_equal(np.asarray(result), expected)

    def test_getitem_delegates(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        proxy = ZarrProxy(path=store_path)
        result = proxy[0, :5]
        assert result.shape == (5,)


@require_zarr
class TestZarrArrayProxy:
    def test_shape_dtype_ndim_chunks(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(10, 20), dtype="float32", chunks=(5, 10))
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        assert proxy.shape == (10, 20)
        assert proxy.dtype == np.dtype("float32")
        assert proxy.ndim == 2
        assert proxy.chunks == (5, 10)

    def test_getitem(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path)
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        result = proxy[2:5, 3:8]
        assert result.shape == (3, 5)

    def test_len(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(10, 20))
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        assert len(proxy) == 10

    def test_attrs(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path)
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        assert isinstance(proxy.attrs, dict)

    def test_iter_patches_nonoverlapping(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(10, 20), chunks=(5, 10))
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        patches = list(proxy.iter_patches((5, 10)))
        assert len(patches) == 4
        for (y, x), patch in patches:
            assert patch.shape == (5, 10)

    def test_iter_patches_with_stride(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(10, 20), chunks=(5, 10))
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        patches = list(proxy.iter_patches((5, 10), stride=(5, 5)))
        assert len(patches) > 4

    def test_iter_patches_edge_shape(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(7, 13), chunks=(5, 5))
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        patches = list(proxy.iter_patches((5, 5)))
        last_patch = patches[-1][1]
        assert last_patch.shape[0] <= 5
        assert last_patch.shape[1] <= 5

    def test_random_patch(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(20, 30), chunks=(10, 10))
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        rng = np.random.default_rng(42)
        patch = proxy.random_patch((8, 10), rng=rng)
        assert patch.shape == (8, 10)

    def test_iter_patches_raises_too_many_dims(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(10, 20))
        arr = zarr.open_array(store_path, mode="r")
        proxy = ZarrArrayProxy(arr, store_path)
        with pytest.raises(ValueError, match="dimensions"):
            list(proxy.iter_patches((5, 10, 20)))


@require_zarr
class TestZarrGroupProxy:
    def test_keys_and_contains(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        grp = zarr.open_group(store_path, mode="r")
        proxy = ZarrGroupProxy(grp, store_path)
        assert "data" in proxy
        assert "mask" in proxy
        assert sorted(proxy.keys()) == ["data", "mask"]

    def test_getitem_returns_proxy(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        grp = zarr.open_group(store_path, mode="r")
        proxy = ZarrGroupProxy(grp, store_path)
        data_proxy = proxy["data"]
        assert isinstance(data_proxy, ZarrArrayProxy)
        assert data_proxy.shape == (5, 5)

    def test_shape_raises(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        grp = zarr.open_group(store_path, mode="r")
        proxy = ZarrGroupProxy(grp, store_path)
        with pytest.raises(ValueError, match="shape"):
            proxy.shape

    def test_dtype_raises(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        grp = zarr.open_group(store_path, mode="r")
        proxy = ZarrGroupProxy(grp, store_path)
        with pytest.raises(ValueError, match="dtype"):
            proxy.dtype

    def test_ndim_raises(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        grp = zarr.open_group(store_path, mode="r")
        proxy = ZarrGroupProxy(grp, store_path)
        with pytest.raises(ValueError, match="ndim"):
            proxy.ndim

    def test_attrs(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        grp = zarr.open_group(store_path, mode="r")
        proxy = ZarrGroupProxy(grp, store_path)
        assert proxy.attrs == {"description": "test group"}


@require_zarr
class TestOmeZarrProxy:
    def test_multiscales_and_axes(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert isinstance(proxy._resolve(), OmeZarrProxy)
        ms = proxy.multiscales
        assert len(ms) == 1
        axes = proxy.axes
        assert len(axes) == 2
        assert axes[0]["name"] == "y"

    def test_scale(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert proxy.scale == [1.0, 1.0]

    def test_channel_names(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert proxy.channel_names == ["DAPI", "GFP"]

    def test_getitem_default_level0(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        result = proxy[0:5, 0:5]
        assert result.shape == (5, 5)

    def test_len(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert len(proxy) == 20

    def test_thumbnail(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        thumb = proxy.thumbnail(level=-1)
        assert thumb.shape == (10, 10)

    def test_iter_patches_ome(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        patches = list(proxy.iter_patches((10, 10), level=0))
        assert len(patches) == 4
        for (y, x), patch in patches:
            assert patch.shape == (10, 10)

    def test_random_patch_ome(self, tmp_path):
        store_path = _create_ome_zarr(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        rng = np.random.default_rng(0)
        patch = proxy.random_patch((5, 5), level=-1, rng=rng)
        assert patch.shape == (5, 5)


@require_zarr
class TestZarrFeatureCastAndFlatten:
    def test_cast_storage_from_string(self):
        zarr_feat = Zarr()
        arr = pa.array(["/path/a.zarr", "/path/b.zarr"], type=pa.string())
        result = zarr_feat.cast_storage(arr)
        assert result.type == pa.struct({"path": pa.string()})
        assert result.field("path")[0].as_py() == "/path/a.zarr"
        assert result.field("path")[1].as_py() == "/path/b.zarr"

    def test_cast_storage_from_struct(self):
        zarr_feat = Zarr()
        path_arr = pa.array(["/path/a.zarr"], type=pa.string())
        struct_arr = pa.StructArray.from_arrays([path_arr], ["path"])
        result = zarr_feat.cast_storage(struct_arr)
        assert result.type == pa.struct({"path": pa.string()})

    def test_flatten_decode_true(self):
        assert isinstance(Zarr(decode=True).flatten(), Zarr)

    def test_flatten_decode_false(self):
        from datasets.features.features import Value

        result = Zarr(decode=False).flatten()
        assert isinstance(result, dict)
        assert "path" in result
        assert result["path"].dtype == "string"

    def test_embed_storage_preserves_paths(self):
        zarr_feat = Zarr()
        path_arr = pa.array(["/path/a.zarr", "/path/b.zarr"], type=pa.string())
        storage = pa.StructArray.from_arrays([path_arr], ["path"])
        result = zarr_feat.embed_storage(storage)
        assert result is storage
        assert result.field("path")[0].as_py() == "/path/a.zarr"
        assert result.field("path")[1].as_py() == "/path/b.zarr"


@require_zarr
class TestIsOmeZarr:
    def test_ome_zarr_detected(self, tmp_path):
        import zarr

        store_path = _create_ome_zarr(tmp_path)
        root = zarr.open_group(store_path, mode="r")
        assert _is_ome_zarr(root) is True

    def test_plain_group_not_ome(self, tmp_path):
        import zarr

        store_path = _create_zarr_group(tmp_path)
        root = zarr.open_group(store_path, mode="r")
        assert _is_ome_zarr(root) is False


@require_zarr
class TestOmeZarrV05:
    def test_v05_ome_detected(self, tmp_path):
        import zarr

        store_path = _create_ome_zarr_v05(tmp_path)
        root = zarr.open_group(store_path, mode="r")
        assert _is_ome_zarr(root) is True

    def test_v05_multiscales(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert isinstance(proxy._resolve(), OmeZarrProxy)
        assert proxy.num_levels == 2

    def test_v05_axes(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        axes = proxy.axes
        assert len(axes) == 3
        assert axes[0]["name"] == "z"
        assert axes[1]["name"] == "y"
        assert axes[2]["name"] == "x"

    def test_v05_scale(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert proxy.scale == [5.0, 1.0, 1.0]

    def test_v05_channel_names(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert proxy.channel_names == ["tdTomato"]

    def test_v05_shape_dtype(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        assert proxy.shape == (10, 64, 64)
        assert proxy.dtype == np.dtype("uint16")

    def test_v05_get_level(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        level0 = proxy.get_level(0)
        assert isinstance(level0, ZarrArrayProxy)
        assert level0.shape == (10, 64, 64)
        level1 = proxy.get_level(1)
        assert level1.shape == (10, 32, 32)

    def test_v05_thumbnail(self, tmp_path):
        store_path = _create_ome_zarr_v05(tmp_path)
        zarr_feat = Zarr()
        encoded = zarr_feat.encode_example(store_path)
        proxy = zarr_feat.decode_example(encoded)
        thumb = proxy.thumbnail(level=-1)
        assert thumb.shape == (10, 32, 32)


@require_zarr
class TestGetOmeAttr:
    def test_v04_top_level(self):
        attrs = {"multiscales": [{"axes": []}], "omero": {"channels": []}}
        assert _get_ome_attr(attrs, "multiscales") == [{"axes": []}]
        assert _get_ome_attr(attrs, "omero") == {"channels": []}

    def test_v05_namespaced(self):
        attrs = {"ome": {"version": "0.5", "multiscales": [{"axes": []}], "omero": {"channels": [{"label": "DAPI"}]}}}
        assert _get_ome_attr(attrs, "multiscales") == [{"axes": []}]
        assert _get_ome_attr(attrs, "omero") == {"channels": [{"label": "DAPI"}]}

    def test_missing_key(self):
        attrs = {"description": "plain group"}
        assert _get_ome_attr(attrs, "multiscales") is None
        assert _get_ome_attr(attrs, "multiscales", []) == []

    def test_v04_takes_precedence(self):
        attrs = {"multiscales": [{"axes": []}], "ome": {"multiscales": [{"axes": []}, {"axes": []}]}}
        assert len(_get_ome_attr(attrs, "multiscales")) == 1


@require_zarr
class TestExtractRepoId:
    def test_hf_path_with_revision(self):
        assert _extract_repo_id_from_hf_path("hf://datasets/user/repo@main/data.zarr") == "user/repo"

    def test_hf_path_without_revision(self):
        assert _extract_repo_id_from_hf_path("hf://datasets/user/repo/data.zarr") == "user/repo"

    def test_hf_path_short(self):
        assert _extract_repo_id_from_hf_path("hf://datasets/repo") is None

    def test_hf_bucket_path(self):
        assert _extract_repo_id_from_hf_path("hf://buckets/user/my-bucket/data.zarr") is None

    def test_non_hf_path(self):
        assert _extract_repo_id_from_hf_path("/local/path/data.zarr") is None


@require_zarr
class TestOpenZarrStoreHF:
    def test_hf_path_uses_fsspecstore_from_url_with_token(self):
        path = "hf://datasets/user/repo/store.zarr"
        with patch("zarr.storage.FsspecStore.from_url") as mock_from_url, patch("zarr.open") as mock_open:
            mock_store = object()
            mock_result = object()
            mock_from_url.return_value = mock_store
            mock_open.return_value = mock_result

            result = _open_zarr_store(path, token_per_repo_id={"user/repo": "hf_token"})

            assert result is mock_result
            mock_from_url.assert_called_once_with(
                path,
                read_only=True,
                storage_options={"token": "hf_token"},
            )
            mock_open.assert_called_once_with(store=mock_store, mode="r")

    def test_hf_path_uses_fsspecstore_from_url_without_token(self):
        path = "hf://datasets/user/repo/store.zarr"
        with patch("zarr.storage.FsspecStore.from_url") as mock_from_url, patch("zarr.open") as mock_open:
            mock_store = object()
            mock_result = object()
            mock_from_url.return_value = mock_store
            mock_open.return_value = mock_result

            result = _open_zarr_store(path, token_per_repo_id=None)

            assert result is mock_result
            mock_from_url.assert_called_once_with(
                path,
                read_only=True,
                storage_options=None,
            )
            mock_open.assert_called_once_with(store=mock_store, mode="r")

    def test_hf_bucket_path_uses_fsspecstore_from_url_with_token(self):
        path = "hf://buckets/user/my-bucket/store.zarr"
        with patch("zarr.storage.FsspecStore.from_url") as mock_from_url, patch("zarr.open") as mock_open:
            mock_store = object()
            mock_result = object()
            mock_from_url.return_value = mock_store
            mock_open.return_value = mock_result

            result = _open_zarr_store(path, token_per_repo_id={"user/index-repo": "hf_token"})

            assert result is mock_result
            mock_from_url.assert_called_once_with(
                path,
                read_only=True,
                storage_options={"token": "hf_token"},
            )
            mock_open.assert_called_once_with(store=mock_store, mode="r")

    def test_hf_bucket_path_uses_fsspecstore_from_url_without_token(self):
        path = "hf://buckets/user/my-bucket/store.zarr"
        with patch("zarr.storage.FsspecStore.from_url") as mock_from_url, patch("zarr.open") as mock_open:
            mock_store = object()
            mock_result = object()
            mock_from_url.return_value = mock_store
            mock_open.return_value = mock_result

            result = _open_zarr_store(path, token_per_repo_id=None)

            assert result is mock_result
            mock_from_url.assert_called_once_with(
                path,
                read_only=True,
                storage_options=None,
            )
            mock_open.assert_called_once_with(store=mock_store, mode="r")

    def test_hf_path_merges_user_storage_options_with_token(self):
        path = "hf://datasets/user/repo/store.zarr"
        user_options = {"anon": True}
        with patch("zarr.storage.FsspecStore.from_url") as mock_from_url, patch("zarr.open") as mock_open:
            mock_from_url.return_value = object()
            mock_open.return_value = object()

            _open_zarr_store(path, token_per_repo_id={"user/repo": "hf_token"}, storage_options=user_options)

            mock_from_url.assert_called_once_with(
                path,
                read_only=True,
                storage_options={"anon": True, "token": "hf_token"},
            )

    def test_hf_path_user_storage_options_without_token(self):
        path = "hf://datasets/user/repo/store.zarr"
        user_options = {"anon": True}
        with patch("zarr.storage.FsspecStore.from_url") as mock_from_url, patch("zarr.open") as mock_open:
            mock_from_url.return_value = object()
            mock_open.return_value = object()

            _open_zarr_store(path, token_per_repo_id=None, storage_options=user_options)

            mock_from_url.assert_called_once_with(
                path,
                read_only=True,
                storage_options=user_options,
            )

    def test_non_hf_remote_passes_storage_options(self):
        path = "s3://bucket/store.zarr"
        with patch("zarr.storage.FsspecStore.from_url") as mock_from_url, patch("zarr.open") as mock_open:
            mock_from_url.return_value = object()
            mock_open.return_value = object()

            _open_zarr_store(path, storage_options={"anon": True})

            mock_from_url.assert_called_once_with(path, mode="r", storage_options={"anon": True})


@require_zarr
class TestDatasetWithZarrFeature:
    def test_dataset_with_array(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        features = Features({"zarr": Zarr()})
        ds = Dataset.from_dict({"zarr": [store_path]}, features=features)
        item = ds[0]
        assert "zarr" in item
        proxy = item["zarr"]
        assert isinstance(proxy, ZarrProxy)
        assert proxy.shape == (10, 20)

    def test_dataset_batch(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        features = Features({"zarr": Zarr()})
        ds = Dataset.from_dict({"zarr": [store_path]}, features=features)
        batch = ds[:1]
        assert "zarr" in batch
        assert len(batch["zarr"]) == 1

    def test_dataset_column(self, tmp_path):
        store_path = _create_zarr_array(tmp_path)
        features = Features({"zarr": Zarr()})
        ds = Dataset.from_dict({"zarr": [store_path]}, features=features)
        col = ds["zarr"]
        assert len(col) == 1


@require_zarr
class TestZarrStoreRegistryReuse:
    def test_two_proxies_open_store_once(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path)
        with patch("zarr.open", wraps=zarr.open) as mock_open:
            p1 = ZarrProxy(path=store_path)
            p2 = ZarrProxy(path=store_path)
            _ = p1.shape, p2.shape
            assert mock_open.call_count == 1

    def test_different_paths_open_separately(self, tmp_path):
        import zarr

        array_path = _create_zarr_array(tmp_path)
        group_path = _create_zarr_group(tmp_path)
        with patch("zarr.open", wraps=zarr.open) as mock_open:
            ZarrProxy(path=array_path)._resolve()
            ZarrProxy(path=group_path)._resolve()
            assert mock_open.call_count == 2


@require_zarr
class TestZarrChunkCache:
    def test_overlapping_reads_share_chunks(self, tmp_path):
        store_path = _create_zarr_array(tmp_path, shape=(32, 32), dtype="float32", chunks=(16, 16))
        proxy = ZarrProxy(path=store_path)
        expected = np.asarray(proxy[:])
        CHUNK_CACHE.clear()
        first = proxy[0:20, 0:20]
        assert len(CHUNK_CACHE._cache) == 4
        second = proxy[0:20, 0:20]
        assert len(CHUNK_CACHE._cache) == 4
        overlap = proxy[0:20, 5:21]
        assert len(CHUNK_CACHE._cache) == 4
        assert np.array_equal(first, expected[0:20, 0:20])
        assert np.array_equal(second, expected[0:20, 0:20])
        assert np.array_equal(overlap, expected[0:20, 5:21])

    def test_evicts_to_bounded_bytes(self, tmp_path, monkeypatch):
        store_path = _create_zarr_array(tmp_path, shape=(32, 32), dtype="float32", chunks=(16, 16))
        proxy = ZarrProxy(path=store_path)
        monkeypatch.setattr(CHUNK_CACHE, "_max_bytes", 2048)
        result = np.asarray(proxy[:])
        assert CHUNK_CACHE._bytes <= 2048
        assert np.array_equal(result, np.arange(1024, dtype="float32").reshape(32, 32))

    def test_disabled_cache_returns_plain_results(self, tmp_path, monkeypatch):
        store_path = _create_zarr_array(tmp_path)
        proxy = ZarrProxy(path=store_path)
        monkeypatch.setattr(CHUNK_CACHE, "_max_bytes", 0)
        result = proxy[1:5, 2:8]
        assert np.array_equal(result, np.arange(200, dtype="float32").reshape(10, 20)[1:5, 2:8])
        assert len(CHUNK_CACHE._cache) == 0


@require_zarr
class TestZarrCachedSelectionSemantics:
    @pytest.mark.parametrize(
        "key",
        [
            (slice(None), slice(None)),
            (slice(2, 8), slice(1, 4)),
            (slice(None, None, 2), slice(None, None, 3)),
            (5, slice(None)),
            (slice(2, 8), 3),
            (5, 7),
            (Ellipsis,),
            (slice(3), Ellipsis),
        ],
    )
    def test_cached_equals_plain(self, tmp_path, key):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(10, 20), dtype="int32", chunks=(5, 10))
        proxy = ZarrProxy(path=store_path)
        expected = np.asarray(zarr.open(store_path, mode="r")[key])
        got = np.asarray(proxy[key])
        assert got.shape == expected.shape
        assert np.array_equal(got, expected)

    def test_negative_step_propagates_zarr_error(self, tmp_path):
        import zarr

        store_path = _create_zarr_array(tmp_path, shape=(10, 20), dtype="int32", chunks=(5, 10))
        proxy = ZarrProxy(path=store_path)
        key = (slice(None, None, -1), slice(None))
        with pytest.raises(zarr.errors.NegativeStepError):
            proxy[key]
        with pytest.raises(zarr.errors.NegativeStepError):
            zarr.open(store_path, mode="r")[key]
