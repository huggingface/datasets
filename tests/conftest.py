import lzma

import pytest


@pytest.fixture(scope="session")
def file_content(tmp_path_factory):
    content = """\
    Text data.
    Second line of data."""
    return content


@pytest.fixture(scope="session")
def xz_file(tmp_path_factory, file_content):
    filename = tmp_path_factory.mktemp("data") / "file.xz"
    data = bytes(file_content, "utf-8")
    with lzma.open(filename, "wb") as f:
        f.write(data)
    return filename
