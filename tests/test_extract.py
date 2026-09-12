import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import get_context
from pathlib import Path
from threading import Event
from unittest.mock import patch

import pytest

from datasets.utils._filelock import FileLock
from datasets.utils.extract import (
    Bzip2Extractor,
    ExtractManager,
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


@pytest.fixture
def two_member_zip(tmp_path):
    archive = tmp_path / "input.zip"
    with zipfile.ZipFile(archive, "w") as zip_file:
        zip_file.writestr("a.txt", "first")
        zip_file.writestr("b.txt", "second")
    return archive


@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
@pytest.mark.parametrize("sibling_type", ["file", "directory", "symlink"])
def test_extractor_preserves_unrelated_siblings(tmp_path, two_member_zip, gz_file, compression_format, sibling_type):
    input_path = two_member_zip if compression_format == "zip" else gz_file
    output_path = tmp_path / "output"
    unrelated_file = tmp_path / "unrelated.txt"
    unrelated_file.write_text("unrelated user data")
    siblings = [tmp_path / "output.old", tmp_path / "output.incomplete"]
    for sibling in siblings:
        if sibling_type == "directory":
            sibling.mkdir()
            (sibling / "data.txt").write_text("unrelated user data")
        elif sibling_type == "symlink":
            sibling.symlink_to(unrelated_file)
        else:
            sibling.write_text("unrelated user data")

    # Exercise both initial publication and retirement of an existing output.
    for _ in range(2):
        Extractor.extract(input_path, output_path, compression_format)
        for sibling in siblings:
            assert sibling.exists(), "deleted an unrelated sibling"
            if sibling_type == "directory":
                assert (sibling / "data.txt").read_text() == "unrelated user data"
            else:
                assert sibling.read_text() == "unrelated user data"
                assert sibling.is_symlink() == (sibling_type == "symlink")
        assert unrelated_file.read_text() == "unrelated user data"


@pytest.mark.skipif(os.name == "nt", reason="requires POSIX directory and file permissions")
@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
@pytest.mark.parametrize("readonly_target", ["directory", "lock"])
def test_extract_manager_readonly_cache(tmp_path, two_member_zip, gz_file, compression_format, readonly_target):
    input_path = str(two_member_zip if compression_format == "zip" else gz_file)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    output_path = Path(manager.extract(input_path))
    lock_path = output_path.with_suffix(".lock")
    lock_path.unlink(missing_ok=True)
    if readonly_target == "directory":
        readonly_path = output_path.parent
        mode = 0o555
    else:
        lock_path.write_text("unheld lock")
        readonly_path = lock_path
        mode = 0o444
    original_mode = readonly_path.stat().st_mode
    readonly_path.chmod(mode)
    try:
        if os.access(readonly_path, os.W_OK):
            pytest.skip("requires a user that cannot write chmod-protected paths")
        assert manager.extract(input_path) == str(output_path)
        Extractor.extract(input_path, output_path, compression_format, force_extract=False)
        if compression_format == "zip":
            assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}
        else:
            assert output_path.stat().st_size > 0
        with pytest.raises(PermissionError):
            manager.extract(input_path, force_extract=True)
    finally:
        readonly_path.chmod(original_mode)


@pytest.mark.parametrize("path_type", ["trailing_separator", "pathlib", "relative"])
def test_extractor_output_path(tmp_path, monkeypatch, two_member_zip, path_type):
    output_path = tmp_path / "output"
    if path_type == "trailing_separator":
        argument = str(output_path) + os.sep
    elif path_type == "relative":
        monkeypatch.chdir(tmp_path)
        argument = "output"
    else:
        argument = output_path
    for _ in range(2):
        Extractor.extract(two_member_zip, argument, "zip")
        assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}


def test_extractor_output_with_symlink_parent(tmp_path, gz_file, text_file):
    target = tmp_path / "real" / "child"
    target.mkdir(parents=True)
    alias = tmp_path / "alias"
    alias.symlink_to(target, target_is_directory=True)
    output_path = alias / ".." / "output"
    unrelated_path = tmp_path / "output"
    unrelated_path.write_text("unrelated user data")

    Extractor.extract(gz_file, output_path, "gzip")

    assert unrelated_path.read_text() == "unrelated user data"
    assert output_path.read_bytes() == text_file.read_bytes()


@pytest.mark.skipif(os.name == "nt", reason="requires POSIX directory permissions")
@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
def test_extractor_unlistable_output_parent(tmp_path, two_member_zip, gz_file, text_file, compression_format):
    input_path = two_member_zip if compression_format == "zip" else gz_file
    output_dir = tmp_path / "unlistable"
    output_dir.mkdir()
    original_mode = output_dir.stat().st_mode
    output_dir.chmod(0o333)
    output_path = output_dir / "output"
    try:
        if os.access(output_dir, os.R_OK):
            pytest.skip("requires a user that cannot read chmod-protected directories")
        Extractor.extract(input_path, output_path, compression_format)
        if compression_format == "zip":
            assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}
        else:
            assert output_path.read_bytes() == text_file.read_bytes()
    finally:
        output_dir.chmod(original_mode)


@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
def test_extractor_long_output_basename(tmp_path, two_member_zip, gz_file, text_file, compression_format):
    input_path = two_member_zip if compression_format == "zip" else gz_file
    output_path = tmp_path / ("x" * 250)
    for _ in range(2):
        Extractor.extract(input_path, output_path, compression_format)
        if compression_format == "zip":
            assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}
        else:
            assert output_path.read_bytes() == text_file.read_bytes()


def test_extract_manager_concurrent_cache_reuse(tmp_path, monkeypatch, two_member_zip):
    archive = two_member_zip

    first_member_extracted = Event()
    release_extraction = Event()
    second_observed = Event()
    extraction_calls = []
    original_acquire = FileLock.acquire

    def acquire(self, *args, **kwargs):
        if first_member_extracted.is_set():
            second_observed.set()
        return original_acquire(self, *args, **kwargs)

    def extract(input_path, output_path):
        extraction_calls.append(input_path)
        with zipfile.ZipFile(input_path) as zip_file:
            zip_file.extract("a.txt", output_path)
            first_member_extracted.set()
            assert release_extraction.wait(60), "timed out waiting to finish extraction"
            zip_file.extract("b.txt", output_path)

    monkeypatch.setattr(FileLock, "acquire", acquire)
    monkeypatch.setattr(ZipExtractor, "extract", staticmethod(extract))
    first_manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    second_manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(first_manager.extract, str(archive))
        try:
            assert first_member_extracted.wait(60), "first extraction did not start"
            second = pool.submit(second_manager.extract, str(archive))
            # Observe either the second caller trying to acquire the lock, or
            # returning early from the cache check without acquiring it.
            second.add_done_callback(lambda future: second_observed.set())
            assert second_observed.wait(60), "second extraction did not start"
            assert not second.done(), "returned an incomplete extraction cache"
            assert not Path(first_manager._get_output_path(str(archive))).exists()
        finally:
            release_extraction.set()
        output_path = first.result(timeout=60)
        assert second.result(timeout=60) == output_path

    assert (Path(output_path) / "a.txt").read_text() == "first"
    assert (Path(output_path) / "b.txt").read_text() == "second"
    assert extraction_calls == [str(archive)]


def _extract_in_process(
    archive, cache_dir, first_member_extracted, release_extraction, second_observed, calls, results
):
    original_acquire = FileLock.acquire

    def acquire(self, *args, **kwargs):
        if first_member_extracted.is_set():
            second_observed.set()
        return original_acquire(self, *args, **kwargs)

    def extract(input_path, output_path):
        with calls.get_lock():
            calls.value += 1
        with zipfile.ZipFile(input_path) as zip_file:
            zip_file.extract("a.txt", output_path)
            first_member_extracted.set()
            assert release_extraction.wait(60), "timed out waiting to finish extraction"
            zip_file.extract("b.txt", output_path)

    with patch.object(FileLock, "acquire", acquire), patch.object(ZipExtractor, "extract", staticmethod(extract)):
        output_path = ExtractManager(cache_dir=cache_dir).extract(archive)
        second_observed.set()  # Also observe a premature cache hit without a lock.
        results.put((output_path, {p.name: p.read_text() for p in Path(output_path).iterdir()}))


def test_extract_manager_concurrent_processes(tmp_path, two_member_zip):
    # Spawn also exercises independent imports and works on Windows.
    context = get_context("spawn")
    first_member_extracted = context.Event()
    release_extraction = context.Event()
    second_observed = context.Event()
    calls = context.Value("i", 0)
    results = context.Queue()
    cache_dir = str(tmp_path / "cache")
    args = (
        str(two_member_zip),
        cache_dir,
        first_member_extracted,
        release_extraction,
        second_observed,
        calls,
        results,
    )
    processes = [context.Process(target=_extract_in_process, args=args) for _ in range(2)]
    output_path = ExtractManager(cache_dir=cache_dir)._get_output_path(str(two_member_zip))
    try:
        processes[0].start()
        assert first_member_extracted.wait(60), "first extraction did not start"
        processes[1].start()
        assert second_observed.wait(60), "second extraction did not start"
        assert not Path(output_path).exists(), "partial extraction was published"
        release_extraction.set()
        expected = (output_path, {"a.txt": "first", "b.txt": "second"})
        assert results.get(timeout=60) == expected
        assert results.get(timeout=60) == expected
        for process in processes:
            process.join(timeout=60)
            assert process.exitcode == 0
        assert calls.value == 1
    finally:
        release_extraction.set()
        for process in processes:
            if process.pid is not None:
                if process.is_alive():
                    process.terminate()
                process.join(timeout=60)
        results.close()
        results.join_thread()


def _extract_and_crash(input_path, output_path, compression_format, staging_path):
    def extract(input_path, output_path):
        if compression_format == "zip":
            Path(output_path).mkdir(exist_ok=True)
            (Path(output_path) / "stale.txt").write_text("left over from a crashed extraction")
        else:
            Path(output_path).write_text("partial data")
        staging_path.send(str(output_path))
        staging_path.close()
        os._exit(17)  # Skip Python cleanup and release the file lock by exiting.

    with patch.object(Extractor.extractors[compression_format], "extract", staticmethod(extract)):
        Extractor.extract(input_path, output_path, compression_format)


@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
def test_extract_manager_discards_incomplete(tmp_path, compression_format, two_member_zip, gz_file, text_file):
    input_path = str(two_member_zip if compression_format == "zip" else gz_file)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    output_path = Path(manager._get_output_path(input_path))
    context = get_context("spawn")
    receive_path, send_path = context.Pipe(duplex=False)
    process = context.Process(
        target=_extract_and_crash, args=(input_path, str(output_path), compression_format, send_path)
    )
    try:
        process.start()
        send_path.close()
        assert receive_path.poll(60), "extraction did not start"
        incomplete_path = Path(receive_path.recv())
        process.join(timeout=60)
        assert process.exitcode == 17
    finally:
        if process.pid is not None:
            if process.is_alive():
                process.terminate()
            process.join(timeout=60)
        receive_path.close()
        send_path.close()
    assert incomplete_path.exists()
    assert not output_path.exists(), "crashed extraction published partial data"

    # Cleanup for a different output in the same parent must leave this staging alone.
    Extractor.extract(input_path, output_path.parent / "other-output", compression_format)
    assert incomplete_path.exists()

    assert manager.extract(input_path) == str(output_path)
    if compression_format == "zip":
        assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}
    else:
        assert output_path.read_bytes() == text_file.read_bytes()
    assert not incomplete_path.exists()


@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
@pytest.mark.parametrize("force_extract", [False, True])
def test_extract_manager_interrupted_extraction(
    tmp_path, monkeypatch, two_member_zip, gz_file, text_file, compression_format, force_extract
):
    input_path = str(two_member_zip if compression_format == "zip" else gz_file)
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    output_path = Path(manager._get_output_path(input_path))
    if force_extract:
        manager.extract(input_path)

    def extract_then_fail(input_path, output_path):
        if compression_format == "zip":
            with zipfile.ZipFile(input_path) as zip_file:
                zip_file.extract("a.txt", output_path)
        else:
            Path(output_path).write_bytes(b"partial data")
        raise RuntimeError("interrupted extraction")

    with monkeypatch.context() as patch_extractor:
        patch_extractor.setattr(Extractor.extractors[compression_format], "extract", staticmethod(extract_then_fail))
        with pytest.raises(RuntimeError, match="interrupted extraction"):
            manager.extract(input_path, force_extract=force_extract)

    if force_extract:
        if compression_format == "zip":
            assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}
        else:
            assert output_path.read_bytes() == text_file.read_bytes()
    else:
        assert not output_path.exists(), "failed extraction left a partial final cache"

    assert manager.extract(input_path) == str(output_path)
    if compression_format == "zip":
        assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}
    else:
        assert output_path.read_bytes() == text_file.read_bytes()


@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
def test_extractor_force_extract_default(tmp_path, compression_format, zip_file, gz_file):
    input_path = {"zip": zip_file, "gzip": gz_file}[compression_format]
    output_path = tmp_path / "extracted"
    Extractor.extract(input_path, output_path, compression_format)
    extracted_file = next(output_path.iterdir()) if output_path.is_dir() else output_path
    original = extracted_file.read_bytes()
    extracted_file.write_bytes(b"changed")

    Extractor.extract(input_path, output_path, compression_format, force_extract=False)
    assert extracted_file.read_bytes() == b"changed"
    Extractor.extract(input_path, output_path, compression_format)
    assert extracted_file.read_bytes() == original


def test_extract_manager_interrupted_cache_removal(tmp_path, monkeypatch, two_member_zip):
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    output_path = Path(manager.extract(str(two_member_zip)))

    def remove_then_fail(path, *args, **kwargs):
        (Path(path) / "b.txt").unlink()
        raise RuntimeError("interrupted cache removal")

    with monkeypatch.context() as patch_removal:
        patch_removal.setattr(shutil, "rmtree", remove_then_fail)
        with pytest.raises(RuntimeError, match="interrupted cache removal"):
            manager.extract(str(two_member_zip), force_extract=True)

    # Retire the old directory before deleting it so an interrupted deletion
    # cannot leave a partial directory at the final cache path either.
    if output_path.exists():
        assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}
    assert manager.extract(str(two_member_zip)) == str(output_path)
    assert {p.name: p.read_text() for p in output_path.iterdir()} == {"a.txt": "first", "b.txt": "second"}


@pytest.mark.parametrize("compression_format", ["zip", "gzip"])
def test_extract_manager_force_extract(tmp_path, compression_format, zip_file, gz_file):
    input_path = {"zip": zip_file, "gzip": gz_file}[compression_format]
    manager = ExtractManager(cache_dir=str(tmp_path / "cache"))
    output_path = Path(manager.extract(input_path))
    extracted_file = next(output_path.iterdir()) if output_path.is_dir() else output_path
    original = extracted_file.read_bytes()
    extracted_file.write_bytes(b"changed")

    assert manager.extract(input_path) == str(output_path)
    assert extracted_file.read_bytes() == b"changed"
    assert manager.extract(input_path, force_extract=True) == str(output_path)
    assert extracted_file.read_bytes() == original


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
