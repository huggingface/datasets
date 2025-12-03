"""Tests for embed_array_storage with sliced/sharded arrays.

Regression tests for https://github.com/huggingface/datasets/issues/XXXX
(SIGKILL in embed_array_storage when processing sliced/sharded Arrow tables)
"""

import pyarrow as pa

from datasets.features import Image, List
from datasets.table import embed_array_storage

from ..utils import require_nibabel


class TestEmbedArrayStorageSliced:
    """Tests for embed_array_storage with sliced/sharded arrays."""

    def test_embed_array_storage_sliced_list_image(self, shared_datadir):
        """embed_array_storage should work on sliced ListArray with Image.

        This is a regression test for SIGKILL when processing sharded datasets
        with Sequence(Image()) or similar nested types.
        """
        image_file = str(shared_datadir / "test_image_rgb.jpg")

        # Create a ListArray with 4 items
        array = pa.array(
            [
                [{"bytes": None, "path": image_file}],
                [{"bytes": None, "path": image_file}, {"bytes": None, "path": image_file}],
                [],
                [{"bytes": None, "path": image_file}],
            ],
            type=pa.list_(Image.pa_type),
        )

        # Slice it (simulates ds.shard() or ds.select())
        sliced = array.slice(1, 2)  # Items 1 and 2

        # Verify the array is actually sliced (this is the problematic case)
        assert sliced.offset == 1, "Expected sliced array to have non-zero offset"

        # This should NOT crash with SIGKILL
        embedded = embed_array_storage(sliced, List(Image()))

        # The fix should make the result contiguous (offset = 0)
        assert embedded.offset == 0, "Result should be contiguous after fix"
        assert len(embedded) == 2
        # Item 0 of sliced = Item 1 of original (has 2 images)
        assert len(embedded[0].as_py()) == 2
        # Item 1 of sliced = Item 2 of original (empty list)
        assert len(embedded[1].as_py()) == 0

    @require_nibabel
    def test_embed_array_storage_sliced_list_nifti(self, shared_datadir):
        """embed_array_storage should work on sliced ListArray with Nifti.

        This is the specific case that crashed in the ARC dataset upload.
        """
        from datasets.features.nifti import Nifti

        nifti_path = str(shared_datadir / "test_nifti.nii.gz")

        # Create a ListArray with 4 items (Sequence(Nifti()))
        array = pa.array(
            [
                [{"bytes": None, "path": nifti_path}],
                [{"bytes": None, "path": nifti_path}, {"bytes": None, "path": nifti_path}],
                [],  # Empty list - this also triggered the crash
                [{"bytes": None, "path": nifti_path}],
            ],
            type=pa.list_(Nifti.pa_type),
        )

        # Slice it (simulates ds.shard())
        sliced = array.slice(1, 2)

        # Verify the array is actually sliced
        assert sliced.offset == 1, "Expected sliced array to have non-zero offset"

        # This should NOT crash with SIGKILL
        embedded = embed_array_storage(sliced, List(Nifti()))

        assert len(embedded) == 2
        # Verify bytes were embedded
        assert embedded[0].as_py()[0]["bytes"] is not None

    def test_embed_array_storage_sliced_large_list(self, shared_datadir):
        """embed_array_storage should work on sliced LargeListArray."""
        image_file = str(shared_datadir / "test_image_rgb.jpg")

        # Create a LargeListArray with 4 items
        from datasets.features import LargeList

        array = pa.array(
            [
                [{"bytes": None, "path": image_file}],
                [{"bytes": None, "path": image_file}, {"bytes": None, "path": image_file}],
                [],
                [{"bytes": None, "path": image_file}],
            ],
            type=pa.large_list(Image.pa_type),
        )

        # Slice it
        sliced = array.slice(1, 2)

        # Verify the array is actually sliced
        assert sliced.offset == 1, "Expected sliced array to have non-zero offset"

        # This should NOT crash with SIGKILL
        embedded = embed_array_storage(sliced, LargeList(Image()))

        assert len(embedded) == 2
