import os

import pytest

from datasets.utils.extract import (
    Bzip2Extractor,
    Extractor,
    GzipExtractor,
    Lz4Extractor,
    SevenZipExtractor,
    TarExtractor,
    XzExtractor,
    ZipExtractor,
    ZstdExtractor,
)

from .utils import require_lz4, require_py7zr, require_zstandard


@pytest.mark.parametrize(
    "compression_format, is_archive",
    [
        ("7z", True),
        ("bz2", False),
        ("gzip", False),
        ("lz4", False),
        ("tar", True),
        ("xz", False),
        ("zip", True),
        ("zstd", False),
    ],
)
def test_base_extractors(
    compression_format,
    is_archive,
    bz2_file,
    gz_file,
    lz4_file,
    seven_zip_file,
    tar_file,
    xz_file,
    zip_file,
    zstd_file,
    tmp_path,
    text_file,
):
    input_paths_and_base_extractors = {
        "7z": (seven_zip_file, SevenZipExtractor),
        "bz2": (bz2_file, Bzip2Extractor),
        "gzip": (gz_file, GzipExtractor),
        "lz4": (lz4_file, Lz4Extractor),
        "tar": (tar_file, TarExtractor),
        "xz": (xz_file, XzExtractor),
        "zip": (zip_file, ZipExtractor),
        "zstd": (zstd_file, ZstdExtractor),
    }
    input_path, base_extractor = input_paths_and_base_extractors[compression_format]
    if input_path is None:
        reason = f"for '{compression_format}' compression_format, "
        if compression_format == "7z":
            reason += require_py7zr.kwargs["reason"]
        elif compression_format == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_format == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    assert base_extractor.is_extractable(input_path)
    output_path = tmp_path / ("extracted" if is_archive else "extracted.txt")
    base_extractor.extract(input_path, output_path)
    if is_archive:
        assert output_path.is_dir()
        for file_path in output_path.iterdir():
            assert file_path.name == text_file.name
            extracted_file_content = file_path.read_text(encoding="utf-8")
    else:
        extracted_file_content = output_path.read_text(encoding="utf-8")
    expected_file_content = text_file.read_text(encoding="utf-8")
    assert extracted_file_content == expected_file_content


@pytest.mark.parametrize(
    "compression_format, is_archive",
    [
        ("7z", True),
        ("bz2", False),
        ("gzip", False),
        ("lz4", False),
        ("tar", True),
        ("xz", False),
        ("zip", True),
        ("zstd", False),
    ],
)
def test_extractor(
    compression_format,
    is_archive,
    bz2_file,
    gz_file,
    lz4_file,
    seven_zip_file,
    tar_file,
    xz_file,
    zip_file,
    zstd_file,
    tmp_path,
    text_file,
):
    input_paths = {
        "7z": seven_zip_file,
        "bz2": bz2_file,
        "gzip": gz_file,
        "lz4": lz4_file,
        "tar": tar_file,
        "xz": xz_file,
        "zip": zip_file,
        "zstd": zstd_file,
    }
    input_path = input_paths[compression_format]
    if input_path is None:
        reason = f"for '{compression_format}' compression_format, "
        if compression_format == "7z":
            reason += require_py7zr.kwargs["reason"]
        elif compression_format == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_format == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    extractor_format = Extractor.infer_extractor_format(input_path)
    assert extractor_format is not None
    output_path = tmp_path / ("extracted" if is_archive else "extracted.txt")
    Extractor.extract(input_path, output_path, extractor_format)
    if is_archive:
        assert output_path.is_dir()
        for file_path in output_path.iterdir():
            assert file_path.name == text_file.name
            extracted_file_content = file_path.read_text(encoding="utf-8")
    else:
        extracted_file_content = output_path.read_text(encoding="utf-8")
    expected_file_content = text_file.read_text(encoding="utf-8")
    assert extracted_file_content == expected_file_content


@pytest.fixture
def tar_file_with_dot_dot(tmp_path, text_file):
    import tarfile

    directory = tmp_path / "data_dot_dot"
    directory.mkdir()
    path = directory / "tar_file_with_dot_dot.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(text_file, arcname=os.path.join("..", text_file.name))
    return path


@pytest.fixture
def tar_file_with_sym_link(tmp_path):
    import tarfile

    directory = tmp_path / "data_sym_link"
    directory.mkdir()
    path = directory / "tar_file_with_sym_link.tar"
    os.symlink("..", directory / "subdir", target_is_directory=True)
    with tarfile.TarFile(path, "w") as f:
        f.add(str(directory / "subdir"), arcname="subdir")  # str required by os.readlink on Windows and Python < 3.8
    return path


@pytest.fixture
def tar_file_with_sibling_prefix(tmp_path, text_file):
    # A member like "../extracted_evil/x" escapes into a *sibling* of the output
    # directory whose name starts with the output directory's name, which a plain
    # startswith(base) check used to allow.
    import tarfile

    directory = tmp_path / "data_sibling_prefix"
    directory.mkdir()
    path = directory / "tar_file_with_sibling_prefix.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(text_file, arcname="../extracted_evil/" + text_file.name)
    return path


@pytest.mark.parametrize(
    "insecure_tar_file, error_log",
    [
        ("tar_file_with_dot_dot", "illegal path"),
        ("tar_file_with_sym_link", "Symlink"),
        ("tar_file_with_sibling_prefix", "illegal path"),
    ],
)
def test_tar_extract_insecure_files(
    insecure_tar_file,
    error_log,
    tar_file_with_dot_dot,
    tar_file_with_sym_link,
    tar_file_with_sibling_prefix,
    tmp_path,
    caplog,
):
    insecure_tar_files = {
        "tar_file_with_dot_dot": tar_file_with_dot_dot,
        "tar_file_with_sym_link": tar_file_with_sym_link,
        "tar_file_with_sibling_prefix": tar_file_with_sibling_prefix,
    }
    input_path = insecure_tar_files[insecure_tar_file]
    output_path = tmp_path / "extracted"
    TarExtractor.extract(input_path, output_path)
    assert caplog.text
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert error_log in record.msg


@pytest.fixture
def tar_file_with_device_and_fifo(tmp_path, text_file):
    import tarfile

    directory = tmp_path / "data_device_fifo"
    directory.mkdir()
    path = directory / "tar_file_with_device_and_fifo.tar"
    with tarfile.TarFile(path, "w") as f:
        device = tarfile.TarInfo("devnode")
        device.type = tarfile.CHRTYPE
        device.devmajor, device.devminor = 1, 3
        f.addfile(device)
        fifo = tarfile.TarInfo("myfifo")
        fifo.type = tarfile.FIFOTYPE
        f.addfile(fifo)
        f.add(text_file, arcname=text_file.name)
    return path


def test_tar_extract_device_and_fifo_members_are_skipped(tar_file_with_device_and_fifo, tmp_path, text_file, caplog):
    # Regression test for https://github.com/huggingface/datasets/issues/9101:
    # device/FIFO members must be skipped instead of aborting the extraction
    # (device) or being materialised in the output directory (FIFO).
    output_path = tmp_path / "extracted"
    TarExtractor.extract(tar_file_with_device_and_fifo, output_path)
    assert not (output_path / "devnode").exists()
    assert not (output_path / "myfifo").exists()
    extracted_file = output_path / text_file.name
    assert extracted_file.read_text(encoding="utf-8") == text_file.read_text(encoding="utf-8")
    assert caplog.text
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "unsupported file type" in record.msg


@pytest.fixture
def tar_file_with_hardlinks_to_special_members(tmp_path, text_file):
    import tarfile

    directory = tmp_path / "data_hardlink_special"
    directory.mkdir()
    path = directory / "tar_file_with_hardlinks_to_special_members.tar"
    with tarfile.TarFile(path, "w") as f:
        device = tarfile.TarInfo("devnode")
        device.type = tarfile.CHRTYPE
        device.devmajor, device.devminor = 1, 3
        f.addfile(device)
        dev_alias = tarfile.TarInfo("dev_alias")
        dev_alias.type = tarfile.LNKTYPE
        dev_alias.linkname = "devnode"
        f.addfile(dev_alias)
        fifo = tarfile.TarInfo("myfifo")
        fifo.type = tarfile.FIFOTYPE
        f.addfile(fifo)
        fifo_alias = tarfile.TarInfo("fifo_alias")
        fifo_alias.type = tarfile.LNKTYPE
        fifo_alias.linkname = "myfifo"
        f.addfile(fifo_alias)
        chain_alias = tarfile.TarInfo("chain_alias")
        chain_alias.type = tarfile.LNKTYPE
        chain_alias.linkname = "fifo_alias"
        f.addfile(chain_alias)
        f.add(text_file, arcname=text_file.name)
        good_alias = tarfile.TarInfo("good_alias")
        good_alias.type = tarfile.LNKTYPE
        good_alias.linkname = text_file.name
        f.addfile(good_alias)
    return path


def test_tar_extract_hardlinks_to_special_members_are_skipped(
    tar_file_with_hardlinks_to_special_members, tmp_path, text_file, caplog
):
    # Regression test for https://github.com/huggingface/datasets/issues/9101:
    # a hard link to a skipped device/FIFO member must be skipped too — tarfile's
    # link fallback would otherwise re-extract the target member at the link
    # path, bypassing safemembers. A hard link to a regular file must still work.
    output_path = tmp_path / "extracted"
    TarExtractor.extract(tar_file_with_hardlinks_to_special_members, output_path)
    for blocked_name in ("devnode", "dev_alias", "myfifo", "fifo_alias", "chain_alias"):
        assert not (output_path / blocked_name).exists()
    extracted_file = output_path / text_file.name
    assert extracted_file.read_text(encoding="utf-8") == text_file.read_text(encoding="utf-8")
    good_alias = output_path / "good_alias"
    assert good_alias.read_text(encoding="utf-8") == text_file.read_text(encoding="utf-8")
    assert caplog.text
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "unsupported file type" in record.msg


@pytest.fixture
def tar_file_with_duplicate_name_link_chain(tmp_path, text_file):
    import tarfile

    directory = tmp_path / "data_duplicate_link_chain"
    directory.mkdir()
    path = directory / "tar_file_with_duplicate_name_link_chain.tar"
    with tarfile.TarFile(path, "w") as f:
        # A FIFO 'a', a link 'b' -> 'a', then a *regular* file also named 'a',
        # then a link 'c' -> 'b'. tarfile resolves each link against the
        # members preceding that link, so 'c' resolves (via 'b') to the FIFO
        # 'a', not to the later regular 'a' — 'c' must be blocked too.
        fifo = tarfile.TarInfo("a")
        fifo.type = tarfile.FIFOTYPE
        f.addfile(fifo)
        link_b = tarfile.TarInfo("b")
        link_b.type = tarfile.LNKTYPE
        link_b.linkname = "a"
        f.addfile(link_b)
        f.add(text_file, arcname="a")
        link_c = tarfile.TarInfo("c")
        link_c.type = tarfile.LNKTYPE
        link_c.linkname = "b"
        f.addfile(link_c)
        f.add(text_file, arcname=text_file.name)
    return path


def test_tar_extract_duplicate_name_link_chain_is_blocked(
    tar_file_with_duplicate_name_link_chain, tmp_path, text_file, caplog
):
    # Regression test for https://github.com/huggingface/datasets/issues/9101:
    # a later regular file sharing the FIFO's name must not whitewash the
    # link chain that tarfile resolves to the earlier FIFO member.
    output_path = tmp_path / "extracted"
    TarExtractor.extract(tar_file_with_duplicate_name_link_chain, output_path)
    assert not (output_path / "b").exists()
    assert not (output_path / "c").exists()
    extracted_file = output_path / "a"
    assert extracted_file.read_text(encoding="utf-8") == text_file.read_text(encoding="utf-8")
    assert (output_path / text_file.name).read_text(encoding="utf-8") == text_file.read_text(encoding="utf-8")
    assert caplog.text
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert "unsupported file type" in record.msg


@pytest.fixture
def tar_file_with_valid_duplicate_name_links(tmp_path, text_file):
    import tarfile

    directory = tmp_path / "data_valid_duplicate_links"
    directory.mkdir()
    path = directory / "tar_file_with_valid_duplicate_name_links.tar"
    with tarfile.TarFile(path, "w") as f:
        # A regular file 'a', a link 'b' -> 'a', a link also named 'a' -> 'b',
        # and a link 'c' -> 'a'. Every step resolves backward to the original
        # regular file; the repeated name is not a cycle.
        f.add(text_file, arcname="a")
        link_b = tarfile.TarInfo("b")
        link_b.type = tarfile.LNKTYPE
        link_b.linkname = "a"
        f.addfile(link_b)
        link_a = tarfile.TarInfo("a")
        link_a.type = tarfile.LNKTYPE
        link_a.linkname = "b"
        f.addfile(link_a)
        link_c = tarfile.TarInfo("c")
        link_c.type = tarfile.LNKTYPE
        link_c.linkname = "a"
        f.addfile(link_c)
        f.add(text_file, arcname=text_file.name)
    return path


def test_tar_extract_valid_duplicate_name_links_are_kept(
    tar_file_with_valid_duplicate_name_links, tmp_path, text_file, caplog
):
    # Regression test for https://github.com/huggingface/datasets/issues/9101:
    # hard links whose chains resolve backward to the same regular file must
    # be kept, even when a name repeats along the chain.
    output_path = tmp_path / "extracted"
    TarExtractor.extract(tar_file_with_valid_duplicate_name_links, output_path)
    expected_content = text_file.read_text(encoding="utf-8")
    for name in ("a", "b", "c"):
        assert (output_path / name).read_text(encoding="utf-8") == expected_content
    assert (output_path / text_file.name).read_text(encoding="utf-8") == expected_content
    assert not caplog.text


@pytest.fixture
def tar_file_with_hardlink_to_symlink(tmp_path, text_file):
    import tarfile

    directory = tmp_path / "data_hardlink_to_symlink"
    directory.mkdir()
    path = directory / "tar_file_with_hardlink_to_symlink.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(text_file, arcname=text_file.name)
        sym = tarfile.TarInfo("sym")
        sym.type = tarfile.SYMTYPE
        sym.linkname = text_file.name
        f.addfile(sym)
        alias = tarfile.TarInfo("alias")
        alias.type = tarfile.LNKTYPE
        alias.linkname = "sym"
        f.addfile(alias)
    return path


def test_tar_extract_hardlink_to_safe_symlink_is_kept(tar_file_with_hardlink_to_symlink, tmp_path, text_file, caplog):
    # Regression test for https://github.com/huggingface/datasets/issues/9101:
    # a hard link to an in-bounds symlink that was itself extracted must be
    # kept; it only re-creates the already-approved symlink.
    output_path = tmp_path / "extracted"
    TarExtractor.extract(tar_file_with_hardlink_to_symlink, output_path)
    expected_content = text_file.read_text(encoding="utf-8")
    assert (output_path / text_file.name).read_text(encoding="utf-8") == expected_content
    assert (output_path / "sym").read_text(encoding="utf-8") == expected_content
    assert (output_path / "alias").read_text(encoding="utf-8") == expected_content
    assert not caplog.text


def test_tar_extract_long_hardlink_chain_is_fast(tmp_path):
    # Regression test for https://github.com/huggingface/datasets/issues/9101:
    # validating a long hard-link chain must stay (near-)linear, not
    # quadratic — each link's resolved verdict is memoized per position.
    import io
    import tarfile
    import time

    n_links = 4000
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode="w") as f:
        first = tarfile.TarInfo("a0")
        first.size = 5
        f.addfile(first, io.BytesIO(b"hello"))
        for i in range(1, n_links):
            link = tarfile.TarInfo(f"a{i}")
            link.type = tarfile.LNKTYPE
            link.linkname = f"a{i - 1}"
            f.addfile(link)
    bio.seek(0)
    with tarfile.open(fileobj=bio) as tf:
        start = time.monotonic()
        members = list(TarExtractor.safemembers(tf, tmp_path))
        elapsed = time.monotonic() - start
    assert len(members) == n_links
    # Without memoization this takes ~8s (quadratic); memoized it is ~0.4s.
    assert elapsed < 2.0


def test_is_zipfile_false_positive(tmpdir):
    # We should have less false positives than zipfile.is_zipfile
    # We do that by checking only the magic number
    not_a_zip_file = tmpdir / "not_a_zip_file"
    # From: https://github.com/python/cpython/pull/5053
    data = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
        b"\x00\x02\x08\x06\x00\x00\x00\x99\x81\xb6'\x00\x00\x00\x15I"
        b"DATx\x01\x01\n\x00\xf5\xff\x00PK\x05\x06\x00PK\x06\x06\x07"
        b"\xac\x01N\xc6|a\r\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    with not_a_zip_file.open("wb") as f:
        f.write(data)
    # zipfile.is_zipfile(str(not_a_zip_file)) could be a false positive for `zipfile`
    assert not ZipExtractor.is_extractable(not_a_zip_file)  # but we're right
