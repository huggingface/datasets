import lzma
import textwrap

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


@pytest.fixture(scope="session")
def xml_file(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.xml"
    data = textwrap.dedent(
        """\
    <?xml version="1.0" encoding="UTF-8" ?>
    <tmx version="1.4">
      <header segtype="sentence" srclang="ca" />
      <body>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 1</seg></tuv>
          <tuv xml:lang="en"><seg>Content 1</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 2</seg></tuv>
          <tuv xml:lang="en"><seg>Content 2</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 3</seg></tuv>
          <tuv xml:lang="en"><seg>Content 3</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 4</seg></tuv>
          <tuv xml:lang="en"><seg>Content 4</seg></tuv>
        </tu>
        <tu>
          <tuv xml:lang="ca"><seg>Contingut 5</seg></tuv>
          <tuv xml:lang="en"><seg>Content 5</seg></tuv>
        </tu>
      </body>
    </tmx>"""
    )
    with open(filename, "w") as f:
        f.write(data)
    return filename
