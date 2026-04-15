import pickle
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
)

from ..utils import require_zarr


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

    def test_embed_storage(self):
        zarr_feat = Zarr()
        path_arr = pa.array(["/path/a.zarr"], type=pa.string())
        storage = pa.StructArray.from_arrays([path_arr], ["path"])
        result = zarr_feat.embed_storage(storage)
        assert result is storage


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
