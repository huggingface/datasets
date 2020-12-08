import lzma

import pytest


FILE_CONTENT = """\
    Text data.
    Second line of data."""


@pytest.fixture(scope="session")
def text_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.txt"
    data = FILE_CONTENT
    with open(filename, "w") as f:
        f.write(data)
    return filename


@pytest.fixture(scope="session")
def xz_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.xz"
    data = bytes(FILE_CONTENT, "utf-8")
    with lzma.open(filename, "wb") as f:
        f.write(data)
    return filename
