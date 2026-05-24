import os
import tempfile

import numpy as np
import pytest

from datasets.config import ZARR_AVAILABLE
from datasets.utils.zarr_utils import (
    ZarrCollator,
    _calculate_shard_shape,
    _count_files,
    _total_chunks,
)

require_zarr = pytest.mark.skipif(not ZARR_AVAILABLE, reason="test requires zarr")


def _create_v2_array(path, shape=(100, 200), dtype="float32", chunks=(10, 20)):
    import zarr

    arr = zarr.open_array(str(path), mode="w", shape=shape, dtype=dtype, chunks=chunks)
    arr[:] = np.arange(np.prod(shape), dtype=dtype).reshape(shape)
    return arr


def _create_v2_group(path):
    import zarr

    root = zarr.open_group(str(path), mode="w")
    root.attrs["description"] = "test group"
    arr1 = root.create_array("data", shape=(50, 100), dtype="float32", chunks=(10, 20))
    arr1[:] = np.ones((50, 100), dtype="float32")
    arr2 = root.create_array("mask", shape=(50, 100), dtype="uint8", chunks=(10, 20))
    arr2[:] = np.zeros((50, 100), dtype="uint8")
    return root


def _create_ome_v2(path):
    import zarr

    root = zarr.open_group(str(path), mode="w")
    root.attrs["multiscales"] = [
        {
            "version": "0.4",
            "datasets": [
                {"path": "0", "coordinateTransformations": [{"type": "scale", "scale": [1.0, 1.0]}]},
                {"path": "1", "coordinateTransformations": [{"type": "scale", "scale": [2.0, 2.0]}]},
            ],
        }
    ]
    a0 = root.create_array("0", shape=(100, 200), dtype="float32", chunks=(10, 20))
    a0[:] = np.arange(20000, dtype="float32").reshape(100, 200)
    a1 = root.create_array("1", shape=(50, 100), dtype="float32", chunks=(10, 20))
    a1[:] = np.arange(5000, dtype="float32").reshape(50, 100)
    return root


class TestCountFiles:
    def test_empty_dir(self, tmp_path):
        assert _count_files(str(tmp_path)) == 0

    def test_simple_files(self, tmp_path):
        (tmp_path / "file1.txt").write_text("hello")
        (tmp_path / "file2.txt").write_text("world")
        assert _count_files(str(tmp_path)) == 2

    def test_nested_dirs(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "file1.txt").write_text("hello")
        (tmp_path / "file2.txt").write_text("world")
        assert _count_files(str(tmp_path)) == 2


class TestTotalChunks:
    def test_exact_division(self):
        assert _total_chunks((100, 200), (10, 20)) == 10 * 10

    def test_non_divisible(self):
        assert _total_chunks((100, 100), (30, 30)) == 4 * 4

    def test_single_element(self):
        assert _total_chunks((1,), (1,)) == 1


class TestCalculateShardShape:
    def test_under_limit_returns_chunks(self):
        result = _calculate_shard_shape((100, 200), (10, 20), file_limit=10000, num_arrays=1)
        assert result == (10, 20)

    def test_over_limit_grows_shard(self):
        result = _calculate_shard_shape((1000, 2000), (10, 20), file_limit=100, num_arrays=1)
        total = _total_chunks((1000, 2000), result)
        assert total <= 100

    def test_multiple_arrays(self):
        result = _calculate_shard_shape((100, 200), (10, 20), file_limit=100, num_arrays=5)
        total = _total_chunks((100, 200), result)
        assert total <= 20


@require_zarr
class TestRechunkToV3:
    def test_rechunk_array(self, tmp_path):
        from datasets.utils.zarr_utils import _rechunk_to_v3

        src = tmp_path / "src.zarr"
        _create_v2_array(src, shape=(50, 100), chunks=(10, 20))

        dst = str(tmp_path / "dst.zarr")
        _rechunk_to_v3(str(src), dst, file_limit=50)

        import zarr

        result = zarr.open(dst, mode="r")
        arr = result["data"] if isinstance(result, zarr.Group) else result
        np.testing.assert_array_equal(np.asarray(arr[:]), np.arange(5000, dtype="float32").reshape(50, 100))

    def test_rechunk_preserves_data(self, tmp_path):
        from datasets.utils.zarr_utils import _rechunk_to_v3

        src = tmp_path / "src.zarr"
        _create_v2_array(src, shape=(30, 40), chunks=(5, 10))

        dst = str(tmp_path / "dst.zarr")
        _rechunk_to_v3(str(src), dst, file_limit=1000)

        import zarr

        result = zarr.open(dst, mode="r")
        arr = result["data"] if isinstance(result, zarr.Group) else result
        expected = np.arange(1200, dtype="float32").reshape(30, 40)
        np.testing.assert_array_equal(np.asarray(arr[:]), expected)

    def test_rechunk_group(self, tmp_path):
        from datasets.utils.zarr_utils import _rechunk_to_v3

        src = tmp_path / "src_group.zarr"
        _create_v2_group(src)

        dst = str(tmp_path / "dst_group.zarr")
        _rechunk_to_v3(str(src), dst, file_limit=50)

        import zarr

        result = zarr.open(dst, mode="r")
        assert "data" in result
        assert "mask" in result
        assert result.attrs.get("description") == "test group"

    def test_rechunk_ome_preserves_multiscales(self, tmp_path):
        from datasets.utils.zarr_utils import _rechunk_to_v3

        src = tmp_path / "src_ome.zarr"
        _create_ome_v2(src)

        dst = str(tmp_path / "dst_ome.zarr")
        _rechunk_to_v3(str(src), dst, file_limit=50)

        import zarr

        result = zarr.open_group(dst, mode="r")
        assert "multiscales" in result.attrs
        assert "0" in result
        assert "1" in result


@require_zarr
class TestPushToHubZarr:
    def test_rejects_non_directory(self, tmp_path):
        file_path = tmp_path / "not_a_dir.txt"
        file_path.write_text("hello")
        from datasets.utils.zarr_utils import push_to_hub_zarr

        with pytest.raises(ValueError, match="must be a directory"):
            push_to_hub_zarr(str(file_path), repo_id="test/repo")

    def test_small_store_direct_upload(self, tmp_path):
        from unittest.mock import MagicMock, patch

        from datasets.utils.zarr_utils import push_to_hub_zarr

        src = tmp_path / "small.zarr"
        _create_v2_array(src, shape=(10, 10), chunks=(5, 5))

        with patch("huggingface_hub.HfApi") as mock_api_cls, patch(
            "huggingface_hub.create_repo"
        ):
            mock_api = MagicMock()
            mock_api.upload_folder.return_value = "https://huggingface.co/test/repo"
            mock_api_cls.return_value = mock_api

            url = push_to_hub_zarr(str(src), repo_id="test/repo", file_limit=50000)
            assert url == "https://huggingface.co/test/repo"
            mock_api.upload_folder.assert_called_once()
            mock_api.upload_large_folder.assert_not_called()

    def test_large_store_triggers_rechunk(self, tmp_path):
        from unittest.mock import MagicMock, patch

        from datasets.utils.zarr_utils import push_to_hub_zarr

        src = tmp_path / "large.zarr"
        _create_v2_array(src, shape=(20, 20), chunks=(5, 5))

        with patch("huggingface_hub.HfApi") as mock_api_cls, patch(
            "huggingface_hub.create_repo"
        ):
            mock_api = MagicMock()
            mock_api_cls.return_value = mock_api

            original_count = _count_files(str(src))
            url = push_to_hub_zarr(str(src), repo_id="test/repo", file_limit=max(1, original_count - 1))
            assert url == "https://huggingface.co/datasets/test/repo"
            mock_api.upload_large_folder.assert_called_once()
            call_kwargs = mock_api.upload_large_folder.call_args[1]
            assert call_kwargs["folder_path"] != str(src)

    def test_explicit_folder_strategy_uses_upload_folder(self, tmp_path):
        from unittest.mock import MagicMock, patch

        from datasets.utils.zarr_utils import push_to_hub_zarr

        src = tmp_path / "small.zarr"
        _create_v2_array(src, shape=(10, 10), chunks=(5, 5))

        with patch("huggingface_hub.HfApi") as mock_api_cls, patch("huggingface_hub.create_repo"):
            mock_api = MagicMock()
            mock_api.upload_folder.return_value = "https://huggingface.co/test/repo"
            mock_api_cls.return_value = mock_api

            url = push_to_hub_zarr(
                str(src),
                repo_id="test/repo",
                file_limit=50000,
                upload_strategy="folder",
            )
            assert url == "https://huggingface.co/test/repo"
            mock_api.upload_folder.assert_called_once()
            mock_api.upload_large_folder.assert_not_called()

    def test_explicit_large_folder_strategy_uses_upload_large_folder(self, tmp_path):
        from unittest.mock import MagicMock, patch

        from datasets.utils.zarr_utils import push_to_hub_zarr

        src = tmp_path / "small.zarr"
        _create_v2_array(src, shape=(10, 10), chunks=(5, 5))

        with patch("huggingface_hub.HfApi") as mock_api_cls, patch("huggingface_hub.create_repo"):
            mock_api = MagicMock()
            mock_api_cls.return_value = mock_api

            url = push_to_hub_zarr(
                str(src),
                repo_id="test/repo",
                file_limit=50000,
                upload_strategy="large_folder",
            )
            assert url == "https://huggingface.co/datasets/test/repo"
            mock_api.upload_large_folder.assert_called_once()
            mock_api.upload_folder.assert_not_called()

    def test_auto_strategy_with_path_in_repo_falls_back_to_upload_folder(self, tmp_path):
        from unittest.mock import MagicMock, patch

        from datasets.utils.zarr_utils import push_to_hub_zarr

        src = tmp_path / "large.zarr"
        _create_v2_array(src, shape=(20, 20), chunks=(5, 5))

        with patch("huggingface_hub.HfApi") as mock_api_cls, patch("huggingface_hub.create_repo"):
            mock_api = MagicMock()
            mock_api.upload_folder.return_value = "https://huggingface.co/test/repo"
            mock_api_cls.return_value = mock_api

            original_count = _count_files(str(src))
            url = push_to_hub_zarr(
                str(src),
                repo_id="test/repo",
                file_limit=max(1, original_count - 1),
                path_in_repo="nested/path",
            )

            assert url == "https://huggingface.co/test/repo"
            mock_api.upload_folder.assert_called_once()
            mock_api.upload_large_folder.assert_not_called()
            call_kwargs = mock_api.upload_folder.call_args[1]
            assert call_kwargs["path_in_repo"] == "nested/path"

    def test_explicit_large_folder_with_path_in_repo_falls_back_to_upload_folder(self, tmp_path):
        from unittest.mock import MagicMock, patch

        from datasets.utils.zarr_utils import push_to_hub_zarr

        src = tmp_path / "small.zarr"
        _create_v2_array(src, shape=(10, 10), chunks=(5, 5))

        with patch("huggingface_hub.HfApi") as mock_api_cls, patch("huggingface_hub.create_repo"):
            mock_api = MagicMock()
            mock_api.upload_folder.return_value = "https://huggingface.co/test/repo"
            mock_api_cls.return_value = mock_api

            url = push_to_hub_zarr(
                str(src),
                repo_id="test/repo",
                upload_strategy="large_folder",
                path_in_repo="nested/path",
            )

            assert url == "https://huggingface.co/test/repo"
            mock_api.upload_folder.assert_called_once()
            mock_api.upload_large_folder.assert_not_called()
            call_kwargs = mock_api.upload_folder.call_args[1]
            assert call_kwargs["path_in_repo"] == "nested/path"

    def test_invalid_upload_strategy_raises(self, tmp_path):
        from datasets.utils.zarr_utils import push_to_hub_zarr

        src = tmp_path / "small.zarr"
        _create_v2_array(src, shape=(10, 10), chunks=(5, 5))

        with pytest.raises(ValueError, match="upload_strategy"):
            push_to_hub_zarr(
                str(src),
                repo_id="test/repo",
                upload_strategy="invalid",
            )


@require_zarr
class TestZarrCollator:
    def test_collator_array_no_patch(self, tmp_path):
        from datasets.features.zarr import ZarrProxy

        store_path = str(tmp_path / "arr.zarr")
        _create_v2_array(tmp_path / "arr.zarr", shape=(10, 20), chunks=(5, 10))

        proxy = ZarrProxy(path=store_path)
        batch = [{"zarr": proxy}]
        collator = ZarrCollator(patch_size=None, column_name="zarr")
        result = collator(batch)
        assert "pixel_values" in result

    def test_collator_array_random_patch(self, tmp_path):
        from datasets.features.zarr import ZarrProxy

        store_path = str(tmp_path / "arr.zarr")
        _create_v2_array(tmp_path / "arr.zarr", shape=(30, 40), chunks=(5, 10))

        proxy = ZarrProxy(path=store_path)
        batch = [{"zarr": proxy}]
        collator = ZarrCollator(patch_size=(8, 8), column_name="zarr")
        result = collator(batch)
        assert "pixel_values" in result
        pv = result["pixel_values"]
        assert pv.shape[-2:] == (8, 8) or (len(pv.shape) >= 2 and pv.shape[-2:] == (8, 8))

    def test_collator_ome_with_level(self, tmp_path):
        from datasets.features.zarr import ZarrProxy

        store_path = str(tmp_path / "ome.zarr")
        _create_ome_v2(tmp_path / "ome.zarr")

        proxy = ZarrProxy(path=store_path)
        batch = [{"zarr": proxy}]
        collator = ZarrCollator(patch_size=(10, 10), level=-1, column_name="zarr")
        result = collator(batch)
        assert "pixel_values" in result

    def test_collator_group_raises(self, tmp_path):
        from datasets.features.zarr import ZarrProxy

        store_path = str(tmp_path / "grp.zarr")
        _create_v2_group(tmp_path / "grp.zarr")

        proxy = ZarrProxy(path=store_path)
        batch = [{"zarr": proxy}]
        collator = ZarrCollator(patch_size=(5, 5), column_name="zarr")
        with pytest.raises(TypeError, match="ZarrGroup"):
            collator(batch)

    def test_collator_with_labels(self, tmp_path):
        from datasets.features.zarr import ZarrProxy

        store_path = str(tmp_path / "arr.zarr")
        _create_v2_array(tmp_path / "arr.zarr", shape=(10, 20), chunks=(5, 10))

        proxy = ZarrProxy(path=store_path)
        batch = [{"zarr": proxy, "label": 0}]
        collator = ZarrCollator(patch_size=(5, 5), column_name="zarr", label_column="label")
        result = collator(batch)
        assert "labels" in result


@require_zarr
class TestLoadZarrDataset:
    def test_load_zarr_dataset_basic(self, tmp_path):
        from datasets.utils.zarr_utils import load_zarr_dataset

        _create_v2_array(tmp_path / "scan1.zarr", shape=(10, 20), chunks=(5, 10))
        _create_v2_array(tmp_path / "scan2.zarr", shape=(15, 30), chunks=(5, 10))

        ds = load_zarr_dataset(str(tmp_path))
        assert len(ds) == 2
        assert "zarr" in ds.features
        assert "label" not in ds.features

    def test_load_zarr_dataset_with_labels(self, tmp_path):
        from datasets.utils.zarr_utils import load_zarr_dataset

        healthy = tmp_path / "healthy"
        healthy.mkdir()
        diseased = tmp_path / "diseased"
        diseased.mkdir()
        _create_v2_array(healthy / "scan1.zarr", shape=(10, 20), chunks=(5, 10))
        _create_v2_array(diseased / "scan2.zarr", shape=(15, 30), chunks=(5, 10))

        ds = load_zarr_dataset(str(tmp_path), drop_labels=False)
        assert len(ds) == 2
        assert "label" in ds.features
        assert set(ds["label"]) == {0, 1}
        assert set(ds.features["label"].names) == {"diseased", "healthy"}

    def test_load_zarr_dataset_no_zarr_raises(self, tmp_path):
        from datasets.utils.zarr_utils import load_zarr_dataset

        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        with pytest.raises(FileNotFoundError, match="No .zarr"):
            load_zarr_dataset(str(empty_dir))

    def test_load_zarr_dataset_proxy_access(self, tmp_path):
        from datasets.utils.zarr_utils import load_zarr_dataset

        _create_v2_array(tmp_path / "scan.zarr", shape=(10, 20), chunks=(5, 10))

        ds = load_zarr_dataset(str(tmp_path))
        proxy = ds[0]["zarr"]
        assert proxy.shape == (10, 20)
        assert proxy.dtype == np.dtype("float32")
