import textwrap
from contextlib import nullcontext as does_not_raise

import pyarrow as pa
import pytest

from datasets import Features, Image
from datasets.packaged_modules.text.text import Text

from ..utils import require_pil


@pytest.fixture
def text_file(tmp_path):
    filename = tmp_path / "text.txt"
    data = textwrap.dedent(
        """\
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

        Second paragraph:
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    return str(filename)


@pytest.fixture
def text_file_with_image(tmp_path, image_file):
    filename = tmp_path / "text_with_image.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(image_file)
    return str(filename)


@pytest.mark.parametrize("keep_linebreaks", [True, False])
def test_text_linebreaks(text_file, keep_linebreaks):
    with open(text_file, encoding="utf-8") as f:
        expected_content = f.read().splitlines(keepends=keep_linebreaks)
    text = Text(keep_linebreaks=keep_linebreaks, encoding="utf-8")
    generator = text._generate_tables([[text_file]])
    generated_content = pa.concat_tables([table for _, table in generator]).to_pydict()["text"]
    assert generated_content == expected_content


@require_pil
def test_text_cast_image(text_file_with_image):
    with open(text_file_with_image, encoding="utf-8") as f:
        image_file = f.read().splitlines()[0]
    text = Text(encoding="utf-8", features=Features({"image": Image()}))
    generator = text._generate_tables([[text_file_with_image]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.schema.field("image").type == Image()()
    generated_content = pa_table.to_pydict()["image"]
    assert generated_content == [{"path": image_file, "bytes": None}]


@pytest.mark.parametrize("sample_by", ["line", "paragraph", "document"])
def test_text_sample_by(sample_by, text_file):
    with open(text_file, encoding="utf-8") as f:
        expected_content = f.read()
    if sample_by == "line":
        expected_content = expected_content.splitlines()
    elif sample_by == "paragraph":
        expected_content = expected_content.split("\n\n")
    elif sample_by == "document":
        expected_content = [expected_content]
    text = Text(sample_by=sample_by, encoding="utf-8", chunksize=100)
    generator = text._generate_tables([[text_file]])
    generated_content = pa.concat_tables([table for _, table in generator]).to_pydict()["text"]
    assert generated_content == expected_content


@pytest.mark.parametrize("only_supported_extensions, raises", [(None, True), (False, True), (True, False)])
def test_text_reads_only_supported_extensions(only_supported_extensions, raises, text_file, image_file):
    config_kwargs = (
        {"only_supported_extensions": only_supported_extensions} if only_supported_extensions is not None else {}
    )
    expectation = pytest.raises(UnicodeDecodeError) if raises else does_not_raise()
    builder = Text(**config_kwargs)
    generator = builder._generate_tables([[text_file, image_file]])
    # If image file is read, it raises UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
    with expectation:
        for _ in generator:
            pass
