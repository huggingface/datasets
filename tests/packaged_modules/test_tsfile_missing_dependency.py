import pytest

from datasets import load_dataset


def test_tsfile_missing_dependency_message(tmp_path):
    tsfile_path = tmp_path / "sample.tsfile"
    tsfile_path.write_bytes(b"fake tsfile content")

    with pytest.raises(ImportError, match=r"To support loading TSFile datasets, please install 'tsfile'\."):
        load_dataset("tsfile", data_files=str(tsfile_path))