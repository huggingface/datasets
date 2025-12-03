"""Tests for memory-safe push_to_hub with large datasets.

Regression tests for https://github.com/huggingface/datasets/issues/XXXX
(OOM when uploading large datasets due to memory accumulation in additions list)
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from datasets import Dataset


class TestPushToHubMemorySafe:
    """Tests for memory-safe push_to_hub implementation."""

    def test_push_to_hub_uses_file_path_not_bytes_in_commit_operation(self):
        """CommitOperationAdd should use file path, not bytes, to enable streaming.

        This is the core fix - by using file paths instead of bytes, the upload
        can stream from disk instead of holding all shard bytes in memory.
        """
        ds = Dataset.from_dict({"x": list(range(100))})

        commit_operations = []

        with patch("datasets.arrow_dataset.HfApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api

            def capture_preupload(repo_id, additions, **kwargs):
                for add in additions:
                    commit_operations.append(add)

            mock_api.preupload_lfs_files = capture_preupload

            # Consume the generator
            list(
                ds._push_parquet_shards_to_hub_single(
                    job_id=0,
                    num_jobs=1,
                    repo_id="test/repo",
                    data_dir="data",
                    split="train",
                    token="fake",
                    revision=None,
                    create_pr=False,
                    num_shards=2,
                    embed_external_files=False,
                    writer_batch_size=1000,
                )
            )

        # Should have captured at least one operation
        assert len(commit_operations) > 0, "No commit operations captured"

        # Each CommitOperationAdd should have a Path or str, not bytes
        for op in commit_operations:
            assert isinstance(op.path_or_fileobj, (str, Path)), (
                f"Expected file path (str or Path), got {type(op.path_or_fileobj).__name__}. "
                "This indicates bytes are being held in memory instead of streamed from disk."
            )

    def test_push_to_hub_cleans_up_temp_files(self):
        """Temp files should be deleted after each shard upload.

        Memory safety requires that temp files are cleaned up after upload
        to avoid disk exhaustion on large datasets.
        """
        ds = Dataset.from_dict({"x": list(range(100))})

        created_temp_files = []

        # Patch at the module level where it's used
        with patch("datasets.arrow_dataset.tempfile") as mock_tempfile:
            # Create real temp files but track them
            real_tempfile = tempfile

            def track_named_temp(*args, **kwargs):
                kwargs["delete"] = False  # We'll delete manually to track
                f = real_tempfile.NamedTemporaryFile(*args, **kwargs)
                created_temp_files.append(Path(f.name))
                return f

            mock_tempfile.NamedTemporaryFile = track_named_temp

            with patch("datasets.arrow_dataset.HfApi") as mock_api_class:
                mock_api = MagicMock()
                mock_api_class.return_value = mock_api
                mock_api.preupload_lfs_files = MagicMock()

                # Consume the generator
                list(
                    ds._push_parquet_shards_to_hub_single(
                        job_id=0,
                        num_jobs=1,
                        repo_id="test/repo",
                        data_dir="data",
                        split="train",
                        token="fake",
                        revision=None,
                        create_pr=False,
                        num_shards=3,
                        embed_external_files=False,
                        writer_batch_size=1000,
                    )
                )

        # All temp files should be cleaned up after the upload completes
        for temp_file in created_temp_files:
            assert not temp_file.exists(), (
                f"Temp file not cleaned up: {temp_file}. This will cause disk exhaustion on large datasets."
            )

    def test_push_to_hub_uploaded_size_still_calculated(self):
        """uploaded_size should still be calculated correctly with file-based approach."""
        ds = Dataset.from_dict({"x": list(range(100))})

        with patch("datasets.arrow_dataset.HfApi") as mock_api_class:
            mock_api = MagicMock()
            mock_api_class.return_value = mock_api
            mock_api.preupload_lfs_files = MagicMock()

            # Collect all yields to get the final result
            results = list(
                ds._push_parquet_shards_to_hub_single(
                    job_id=0,
                    num_jobs=1,
                    repo_id="test/repo",
                    data_dir="data",
                    split="train",
                    token="fake",
                    revision=None,
                    create_pr=False,
                    num_shards=1,
                    embed_external_files=False,
                    writer_batch_size=1000,
                )
            )

        # The function yields (job_id, done, content) tuples
        # Final yield has done=True and content=additions list
        final_result = results[-1]
        assert final_result[1] is True, "Expected final yield to have done=True"

        additions = final_result[2]
        assert len(additions) > 0, "Expected at least one addition"

        # Each addition should have upload_info with size > 0
        for add in additions:
            assert hasattr(add, "upload_info"), "CommitOperationAdd missing upload_info"
            if add.upload_info is not None:
                assert add.upload_info.size > 0, "upload_info.size should be > 0"
