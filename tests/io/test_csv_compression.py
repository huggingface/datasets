import bz2
import gzip
import io
import lzma
import tarfile
import zipfile

import pandas as pd
import pytest
from packaging.version import Version

from datasets import Dataset


@pytest.mark.parametrize("num_proc", [None, 2])
@pytest.mark.parametrize("batch_size", [1, 3, 10])
@pytest.mark.parametrize("codec", ["gzip", "bz2", "xz", "zip", "tar", "zstd"])
@pytest.mark.parametrize("kind", ["explicit", "infer", "dict", "buffer"])
def test_csv_compression(tmp_path, num_proc, batch_size, codec, kind):
    if codec == "tar" and Version(pd.__version__) < Version("1.5.0"):
        pytest.skip("pandas added tar compression in 1.5.0")
    if codec == "zstd":
        if Version(pd.__version__) < Version("1.4.0"):
            pytest.skip("pandas added zstd compression in 1.4.0")
        zstandard = pytest.importorskip("zstandard")
    dataset = Dataset.from_dict({"text": ["hello", "café, tea", "line\nbreak", "last"], "n": [1, 2, 3, 4]})
    suffix = {"gzip": "gz", "bz2": "bz2", "xz": "xz", "zip": "zip", "tar": "tar", "zstd": "zst"}[codec]
    path = tmp_path / "new-directory" / f"out.csv.{suffix}"
    compression = codec
    if kind == "dict":
        compression = {"method": codec}
        if codec == "gzip":
            compression.update(compresslevel=1, mtime=1)
        elif codec == "bz2":
            compression.update(compresslevel=1)
        elif codec == "zstd":
            compression.update(level=1)
        elif codec in ["zip", "tar"]:
            compression.update(archive_name="data.csv")
    kwargs = {} if kind == "infer" else {"compression": compression}
    target = io.BytesIO() if kind == "buffer" else path
    written = dataset.to_csv(target, batch_size=batch_size, num_proc=num_proc, **kwargs)
    if kind == "buffer":
        assert not target.closed
        raw = target.getvalue()
    else:
        raw = path.read_bytes()
    if codec == "gzip":
        assert raw[:2] == b"\x1f\x8b"
        decoded = gzip.decompress(raw)
        if kind == "dict":
            assert int.from_bytes(raw[4:8], "little") == 1
    elif codec == "bz2":
        assert raw[:3] == b"BZh"
        decoded = bz2.decompress(raw)
    elif codec == "xz":
        assert raw[:6] == b"\xfd7zXZ\x00"
        decoded = lzma.decompress(raw)
    elif codec == "zstd":
        assert raw[:4] == b"\x28\xb5\x2f\xfd"
        with zstandard.ZstdDecompressor().stream_reader(io.BytesIO(raw)) as stream:
            decoded = stream.read()
    elif codec == "zip":
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            assert len(archive.namelist()) == 1
            if kind == "dict":
                assert archive.namelist() == ["data.csv"]
            decoded = archive.read(archive.namelist()[0])
    else:
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            assert len(archive.getmembers()) == 1
            if kind == "dict":
                assert archive.getnames() == ["data.csv"]
            decoded = archive.extractfile(archive.getmembers()[0]).read()
    expected = dataset.to_pandas().to_csv(index=False).encode()
    assert decoded == expected
    assert written == len(expected)
    assert pd.read_csv(io.BytesIO(decoded)).to_dict("list") == dataset.to_dict()


@pytest.mark.parametrize("compression", [None, "infer"])
@pytest.mark.parametrize("header,index", [(True, False), (False, False), (["TEXT", "N"], True)])
@pytest.mark.parametrize("path_kind", ["str", "path", "uri", "buffer"])
def test_csv_plain_controls(tmp_path, compression, header, index, path_kind):
    dataset = Dataset.from_dict({"text": ["a", "b", "c"], "n": [1, 2, 3]})
    path = tmp_path / ("out.csv.gz" if compression is None else "out.csv")
    target = {"str": str(path), "path": path, "uri": path.as_uri(), "buffer": io.BytesIO()}[path_kind]
    kwargs = {"header": header, "index": index, "compression": compression}
    written = dataset.to_csv(target, batch_size=2, **kwargs)
    raw = target.getvalue() if path_kind == "buffer" else path.read_bytes()
    # Dataset index is batch-local, matching the existing writer's behavior.
    expected = b"".join(
        dataset.select(range(i, min(i + 2, len(dataset))))
        .to_pandas()
        .to_csv(index=index, header=header if i == 0 else False)
        .encode()
        for i in range(0, len(dataset), 2)
    )
    assert raw == expected
    assert written == len(expected)
    if path_kind == "buffer":
        assert not target.closed


def test_csv_caller_owned_append(tmp_path):
    dataset = Dataset.from_dict({"text": ["a", "b"]})
    path = tmp_path / "out.csv"
    dataset.to_csv(path)
    with path.open("ab") as stream:
        assert dataset.to_csv(stream, header=False, batch_size=1) == 4
        assert not stream.closed
    assert path.read_bytes() == b"text\na\nb\na\nb\n"


@pytest.mark.parametrize("suffix,decoder", [("gz", gzip.decompress), ("bz2", bz2.decompress), ("xz", lzma.decompress)])
@pytest.mark.skipif(Version(pd.__version__) < Version("1.5.0"), reason="pandas added tar compression in 1.5.0")
def test_csv_compressed_tar(tmp_path, suffix, decoder):
    dataset = Dataset.from_dict({"text": ["a", "b", "c"]})
    path = tmp_path / f"out.tar.{suffix}"
    dataset.to_csv(path, batch_size=1)
    with tarfile.open(fileobj=io.BytesIO(decoder(path.read_bytes())), mode="r:") as archive:
        assert len(archive.getmembers()) == 1
        assert archive.extractfile(archive.getmembers()[0]).read() == b"text\na\nb\nc\n"


@pytest.mark.parametrize("storage_compression", [None, "infer", "gzip", "bz2"])
@pytest.mark.parametrize("suffix", ["csv", "csv.gz"])
@pytest.mark.parametrize("compression_kwargs", [{}, {"compression": None}, {"compression": "infer"}])
def test_csv_storage_compression(tmp_path, storage_compression, suffix, compression_kwargs):
    dataset = Dataset.from_dict({"text": ["ordinary", "data"]})
    path = tmp_path / f"out.{suffix}"
    options = {"compression": storage_compression}
    assert dataset.to_csv(path, storage_options=options, batch_size=1, **compression_kwargs) == 19
    raw = path.read_bytes()
    if storage_compression == "gzip" or (storage_compression == "infer" and suffix.endswith("gz")):
        raw = gzip.decompress(raw)
    elif storage_compression == "bz2":
        raw = bz2.decompress(raw)
    assert raw == b"text\nordinary\ndata\n"
    assert options == {"compression": storage_compression}


@pytest.mark.parametrize("compression", ["gzip", "bz2", {"method": "gzip", "mtime": 1}])
def test_csv_conflicting_compression(tmp_path, compression):
    dataset = Dataset.from_dict({"text": ["ordinary", "data"]})
    path = tmp_path / "out.csv.gz"
    path.write_bytes(b"existing file")
    with pytest.raises(ValueError, match="compression.*storage_options"):
        dataset.to_csv(path, compression=compression, storage_options={"compression": "gzip"})
    assert path.read_bytes() == b"existing file"


def test_csv_buffer_storage_options_ignored():
    dataset = Dataset.from_dict({"text": ["ordinary", "data"]})
    buffer = io.BytesIO()
    dataset.to_csv(buffer, compression={"method": "gzip", "mtime": 1}, storage_options={"compression": "bz2"})
    assert not buffer.closed
    assert gzip.decompress(buffer.getvalue()) == b"text\nordinary\ndata\n"
