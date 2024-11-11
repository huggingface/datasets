import os
import re
from pathlib import Path
from unittest.mock import patch

import pytest
import zstandard as zstd
from fsspec.registry import _registry as _fsspec_registry
from fsspec.spec import AbstractBufferedFile, AbstractFileSystem
from huggingface_hub.errors import OfflineModeIsEnabled

from datasets.download.download_config import DownloadConfig
from datasets.utils.file_utils import (
    _get_extraction_protocol,
    _prepare_single_hop_path_and_storage_options,
    cached_path,
    fsspec_get,
    fsspec_head,
    get_from_cache,
    xdirname,
    xexists,
    xgetsize,
    xglob,
    xisdir,
    xisfile,
    xjoin,
    xlistdir,
    xnumpy_load,
    xopen,
    xPath,
    xrelpath,
    xsplit,
    xsplitext,
    xwalk,
)
from datasets.utils.hub import hf_dataset_url

from .utils import slow


FILE_CONTENT = """\
    Text data.
    Second line of data."""

FILE_PATH = "file"

TEST_URL = "https://huggingface.co/datasets/hf-internal-testing/dataset_with_script/resolve/main/some_text.txt"
TEST_URL_CONTENT = "foo\nbar\nfoobar"

TEST_GG_DRIVE_FILENAME = "train.tsv"
TEST_GG_DRIVE_URL = "https://drive.google.com/uc?export=download&id=17bOgBDc3hRCoPZ89EYtKDzK-yXAWat94"
TEST_GG_DRIVE_GZIPPED_URL = "https://drive.google.com/uc?export=download&id=1Bt4Garpf0QLiwkJhHJzXaVa0I0H5Qhwz"
TEST_GG_DRIVE_ZIPPED_URL = "https://drive.google.com/uc?export=download&id=1k92sUfpHxKq8PXWRr7Y5aNHXwOCNUmqh"
TEST_GG_DRIVE_CONTENT = """\
pokemon_name, type
Charmander, fire
Squirtle, water
Bulbasaur, grass"""


@pytest.fixture(scope="session")
def zstd_path(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / (FILE_PATH + ".zstd")
    data = bytes(FILE_CONTENT, "utf-8")
    with zstd.open(path, "wb") as f:
        f.write(data)
    return path


@pytest.fixture
def tmpfs_file(tmpfs):
    with open(os.path.join(tmpfs.local_root_dir, FILE_PATH), "w") as f:
        f.write(FILE_CONTENT)
    return FILE_PATH


@pytest.mark.parametrize("compression_format", ["gzip", "xz", "zstd"])
def test_cached_path_extract(compression_format, gz_file, xz_file, zstd_path, tmp_path, text_file):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_path}
    input_path = input_paths[compression_format]
    cache_dir = tmp_path / "cache"
    download_config = DownloadConfig(cache_dir=cache_dir, extract_compressed_file=True)
    extracted_path = cached_path(input_path, download_config=download_config)
    with open(extracted_path) as f:
        extracted_file_content = f.read()
    with open(text_file) as f:
        expected_file_content = f.read()
    assert extracted_file_content == expected_file_content


@pytest.mark.parametrize("default_extracted", [True, False])
@pytest.mark.parametrize("default_cache_dir", [True, False])
def test_extracted_datasets_path(default_extracted, default_cache_dir, xz_file, tmp_path, monkeypatch):
    custom_cache_dir = "custom_cache"
    custom_extracted_dir = "custom_extracted_dir"
    custom_extracted_path = tmp_path / "custom_extracted_path"
    if default_extracted:
        expected = ("downloads" if default_cache_dir else custom_cache_dir, "extracted")
    else:
        monkeypatch.setattr("datasets.config.EXTRACTED_DATASETS_DIR", custom_extracted_dir)
        monkeypatch.setattr("datasets.config.EXTRACTED_DATASETS_PATH", str(custom_extracted_path))
        expected = custom_extracted_path.parts[-2:] if default_cache_dir else (custom_cache_dir, custom_extracted_dir)

    filename = xz_file
    download_config = (
        DownloadConfig(extract_compressed_file=True)
        if default_cache_dir
        else DownloadConfig(cache_dir=tmp_path / custom_cache_dir, extract_compressed_file=True)
    )
    extracted_file_path = cached_path(filename, download_config=download_config)
    assert Path(extracted_file_path).parent.parts[-2:] == expected


def test_cached_path_local(text_file):
    # input absolute path -> output absolute path
    text_file_abs = str(Path(text_file).resolve())
    assert os.path.samefile(cached_path(text_file_abs), text_file_abs)
    # input relative path -> output absolute path
    text_file = __file__
    text_file_abs = str(Path(text_file).resolve())
    text_file_rel = str(Path(text_file).resolve().relative_to(Path(os.getcwd())))
    assert os.path.samefile(cached_path(text_file_rel), text_file_abs)


def test_cached_path_missing_local(tmp_path):
    # absolute path
    missing_file = str(tmp_path.resolve() / "__missing_file__.txt")
    with pytest.raises(FileNotFoundError):
        cached_path(missing_file)
    # relative path
    missing_file = "./__missing_file__.txt"
    with pytest.raises(FileNotFoundError):
        cached_path(missing_file)


def test_get_from_cache_fsspec(tmpfs_file):
    output_path = get_from_cache(f"tmp://{tmpfs_file}")
    with open(output_path) as f:
        output_file_content = f.read()
    assert output_file_content == FILE_CONTENT


@patch("datasets.config.HF_HUB_OFFLINE", True)
def test_cached_path_offline():
    with pytest.raises(OfflineModeIsEnabled):
        cached_path("https://huggingface.co")


@patch("datasets.config.HF_HUB_OFFLINE", True)
def test_fsspec_offline(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.html"
    with pytest.raises(OfflineModeIsEnabled):
        fsspec_get("s3://huggingface.co", temp_file=filename)
    with pytest.raises(OfflineModeIsEnabled):
        fsspec_head("s3://huggingface.co")


@pytest.mark.parametrize(
    "urlpath, download_config, expected_urlpath, expected_storage_options",
    [
        (
            "https://huggingface.co/datasets/hf-internal-testing/dataset_with_script/resolve/main/some_text.txt",
            DownloadConfig(),
            "hf://datasets/hf-internal-testing/dataset_with_script@main/some_text.txt",
            {"hf": {"endpoint": "https://huggingface.co", "token": None}},
        ),
        (
            "https://huggingface.co/datasets/hf-internal-testing/dataset_with_script/resolve/main/some_text.txt",
            DownloadConfig(token="MY-TOKEN"),
            "hf://datasets/hf-internal-testing/dataset_with_script@main/some_text.txt",
            {"hf": {"endpoint": "https://huggingface.co", "token": "MY-TOKEN"}},
        ),
        (
            "https://huggingface.co/datasets/hf-internal-testing/dataset_with_script/resolve/main/some_text.txt",
            DownloadConfig(token="MY-TOKEN", storage_options={"hf": {"on_error": "omit"}}),
            "hf://datasets/hf-internal-testing/dataset_with_script@main/some_text.txt",
            {"hf": {"endpoint": "https://huggingface.co", "token": "MY-TOKEN", "on_error": "omit"}},
        ),
        (
            "https://domain.org/data.txt",
            DownloadConfig(),
            "https://domain.org/data.txt",
            {"https": {"client_kwargs": {"trust_env": True}}},
        ),
        (
            "https://domain.org/data.txt",
            DownloadConfig(storage_options={"https": {"block_size": "omit"}}),
            "https://domain.org/data.txt",
            {"https": {"client_kwargs": {"trust_env": True}, "block_size": "omit"}},
        ),
        (
            "https://domain.org/data.txt",
            DownloadConfig(storage_options={"https": {"client_kwargs": {"raise_for_status": True}}}),
            "https://domain.org/data.txt",
            {"https": {"client_kwargs": {"trust_env": True, "raise_for_status": True}}},
        ),
        (
            "https://domain.org/data.txt",
            DownloadConfig(storage_options={"https": {"client_kwargs": {"trust_env": False}}}),
            "https://domain.org/data.txt",
            {"https": {"client_kwargs": {"trust_env": False}}},
        ),
        (
            "https://raw.githubusercontent.com/data.txt",
            DownloadConfig(storage_options={"https": {"headers": {"x-test": "true"}}}),
            "https://raw.githubusercontent.com/data.txt",
            {
                "https": {
                    "client_kwargs": {"trust_env": True},
                    "headers": {"x-test": "true", "Accept-Encoding": "identity"},
                }
            },
        ),
    ],
)
def test_prepare_single_hop_path_and_storage_options(
    urlpath, download_config, expected_urlpath, expected_storage_options
):
    original_download_config_storage_options = str(download_config.storage_options)
    prepared_urlpath, storage_options = _prepare_single_hop_path_and_storage_options(urlpath, download_config)
    assert prepared_urlpath == expected_urlpath
    assert storage_options == expected_storage_options
    # Check that DownloadConfig.storage_options are not modified:
    assert str(download_config.storage_options) == original_download_config_storage_options


class DummyTestFS(AbstractFileSystem):
    protocol = "mock"
    _file_class = AbstractBufferedFile
    _fs_contents = (
        {"name": "top_level", "type": "directory"},
        {"name": "top_level/second_level", "type": "directory"},
        {"name": "top_level/second_level/date=2019-10-01", "type": "directory"},
        {
            "name": "top_level/second_level/date=2019-10-01/a.parquet",
            "type": "file",
            "size": 100,
        },
        {
            "name": "top_level/second_level/date=2019-10-01/b.parquet",
            "type": "file",
            "size": 100,
        },
        {"name": "top_level/second_level/date=2019-10-02", "type": "directory"},
        {
            "name": "top_level/second_level/date=2019-10-02/a.parquet",
            "type": "file",
            "size": 100,
        },
        {"name": "top_level/second_level/date=2019-10-04", "type": "directory"},
        {
            "name": "top_level/second_level/date=2019-10-04/a.parquet",
            "type": "file",
            "size": 100,
        },
        {"name": "misc", "type": "directory"},
        {"name": "misc/foo.txt", "type": "file", "size": 100},
        {"name": "glob_test", "type": "directory", "size": 0},
        {"name": "glob_test/hat", "type": "directory", "size": 0},
        {"name": "glob_test/hat/^foo.txt", "type": "file", "size": 100},
        {"name": "glob_test/dollar", "type": "directory", "size": 0},
        {"name": "glob_test/dollar/$foo.txt", "type": "file", "size": 100},
        {"name": "glob_test/lbrace", "type": "directory", "size": 0},
        {"name": "glob_test/lbrace/{foo.txt", "type": "file", "size": 100},
        {"name": "glob_test/rbrace", "type": "directory", "size": 0},
        {"name": "glob_test/rbrace/}foo.txt", "type": "file", "size": 100},
    )

    def __getitem__(self, name):
        for item in self._fs_contents:
            if item["name"] == name:
                return item
        raise IndexError(f"{name} not found!")

    def ls(self, path, detail=True, refresh=True, **kwargs):
        if kwargs.pop("strip_proto", True):
            path = self._strip_protocol(path)

        files = not refresh and self._ls_from_cache(path)
        if not files:
            files = [file for file in self._fs_contents if path == self._parent(file["name"])]
            files.sort(key=lambda file: file["name"])
            self.dircache[path.rstrip("/")] = files

        if detail:
            return files
        return [file["name"] for file in files]

    def _open(
        self,
        path,
        mode="rb",
        block_size=None,
        autocommit=True,
        cache_options=None,
        **kwargs,
    ):
        return self._file_class(
            self,
            path,
            mode,
            block_size,
            autocommit,
            cache_options=cache_options,
            **kwargs,
        )


@pytest.fixture
def mock_fsspec2():  # to avoid the name collision with `mock_fsspec` from fixtures/fsspec.py
    _fsspec_registry["mock"] = DummyTestFS
    yield
    del _fsspec_registry["mock"]


def _readd_double_slash_removed_by_path(path_as_posix: str) -> str:
    """Path(...) on an url path like zip://file.txt::http://host.com/data.zip
    converts the :// to :/
    This function readds the ://

    It handles cases like:

    - https://host.com/data.zip
    - C://data.zip
    - zip://file.txt::https://host.com/data.zip
    - zip://file.txt::/Users/username/data.zip
    - zip://file.txt::C://data.zip

    Args:
        path_as_posix (str): output of Path(...).as_posix()

    Returns:
        str: the url path with :// instead of :/
    """
    return re.sub("([A-z]:/)([A-z:])", r"\g<1>/\g<2>", path_as_posix)


@pytest.mark.parametrize(
    "input_path, paths_to_join, expected_path",
    [
        (
            "https://host.com/archive.zip",
            ("file.txt",),
            "https://host.com/archive.zip/file.txt",
        ),
        (
            "zip://::https://host.com/archive.zip",
            ("file.txt",),
            "zip://file.txt::https://host.com/archive.zip",
        ),
        (
            "zip://folder::https://host.com/archive.zip",
            ("file.txt",),
            "zip://folder/file.txt::https://host.com/archive.zip",
        ),
        (
            ".",
            ("file.txt",),
            os.path.join(".", "file.txt"),
        ),
        (
            str(Path().resolve()),
            ("file.txt",),
            str((Path().resolve() / "file.txt")),
        ),
    ],
)
def test_xjoin(input_path, paths_to_join, expected_path):
    output_path = xjoin(input_path, *paths_to_join)
    assert output_path == expected_path
    output_path = xPath(input_path).joinpath(*paths_to_join)
    assert output_path == xPath(expected_path)


@pytest.mark.parametrize(
    "input_path, expected_path",
    [
        (str(Path(__file__).resolve()), str(Path(__file__).resolve().parent)),
        ("https://host.com/archive.zip", "https://host.com"),
        (
            "zip://file.txt::https://host.com/archive.zip",
            "zip://::https://host.com/archive.zip",
        ),
        (
            "zip://folder/file.txt::https://host.com/archive.zip",
            "zip://folder::https://host.com/archive.zip",
        ),
    ],
)
def test_xdirname(input_path, expected_path):
    output_path = xdirname(input_path)
    output_path = _readd_double_slash_removed_by_path(Path(output_path).as_posix())
    assert output_path == _readd_double_slash_removed_by_path(Path(expected_path).as_posix())


@pytest.mark.parametrize(
    "input_path, exists",
    [
        ("tmp_path/file.txt", True),
        ("tmp_path/file_that_doesnt_exist.txt", False),
        ("mock://top_level/second_level/date=2019-10-01/a.parquet", True),
        ("mock://top_level/second_level/date=2019-10-01/file_that_doesnt_exist.parquet", False),
    ],
)
def test_xexists(input_path, exists, tmp_path, mock_fsspec2):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
    assert xexists(input_path) is exists


@pytest.mark.integration
def test_xexists_private(hf_private_dataset_repo_txt_data, hf_token):
    root_url = hf_dataset_url(hf_private_dataset_repo_txt_data, "")
    download_config = DownloadConfig(token=hf_token)
    assert xexists(root_url + "data/text_data.txt", download_config=download_config)
    assert not xexists(root_url + "file_that_doesnt_exist.txt", download_config=download_config)


@pytest.mark.parametrize(
    "input_path, expected_head_and_tail",
    [
        (
            str(Path(__file__).resolve()),
            (str(Path(__file__).resolve().parent), str(Path(__file__).resolve().name)),
        ),
        ("https://host.com/archive.zip", ("https://host.com", "archive.zip")),
        ("zip://file.txt::https://host.com/archive.zip", ("zip://::https://host.com/archive.zip", "file.txt")),
        ("zip://folder::https://host.com/archive.zip", ("zip://::https://host.com/archive.zip", "folder")),
        ("zip://::https://host.com/archive.zip", ("zip://::https://host.com/archive.zip", "")),
    ],
)
def test_xsplit(input_path, expected_head_and_tail):
    output_path, tail = xsplit(input_path)
    expected_path, expected_tail = expected_head_and_tail
    output_path = _readd_double_slash_removed_by_path(Path(output_path).as_posix())
    expected_path = _readd_double_slash_removed_by_path(Path(expected_path).as_posix())
    assert output_path == expected_path
    assert tail == expected_tail


@pytest.mark.parametrize(
    "input_path, expected_path_and_ext",
    [
        (
            str(Path(__file__).resolve()),
            (str(Path(__file__).resolve().with_suffix("")), str(Path(__file__).resolve().suffix)),
        ),
        ("https://host.com/archive.zip", ("https://host.com/archive", ".zip")),
        ("zip://file.txt::https://host.com/archive.zip", ("zip://file::https://host.com/archive.zip", ".txt")),
        ("zip://folder::https://host.com/archive.zip", ("zip://folder::https://host.com/archive.zip", "")),
        ("zip://::https://host.com/archive.zip", ("zip://::https://host.com/archive.zip", "")),
    ],
)
def test_xsplitext(input_path, expected_path_and_ext):
    output_path, ext = xsplitext(input_path)
    expected_path, expected_ext = expected_path_and_ext
    output_path = _readd_double_slash_removed_by_path(Path(output_path).as_posix())
    expected_path = _readd_double_slash_removed_by_path(Path(expected_path).as_posix())
    assert output_path == expected_path
    assert ext == expected_ext


def test_xopen_local(text_path):
    with xopen(text_path, "r", encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert list(f) == list(expected_file)
    with xPath(text_path).open("r", encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert list(f) == list(expected_file)


@pytest.mark.integration
def test_xopen_remote():
    with xopen(TEST_URL, "r", encoding="utf-8") as f:
        assert list(f) == TEST_URL_CONTENT.splitlines(keepends=True)
    with xPath(TEST_URL).open("r", encoding="utf-8") as f:
        assert list(f) == TEST_URL_CONTENT.splitlines(keepends=True)


@pytest.mark.parametrize(
    "input_path, expected_paths",
    [
        ("tmp_path", ["file1.txt", "file2.txt"]),
        ("mock://", ["glob_test", "misc", "top_level"]),
        ("mock://top_level", ["second_level"]),
        ("mock://top_level/second_level/date=2019-10-01", ["a.parquet", "b.parquet"]),
    ],
)
def test_xlistdir(input_path, expected_paths, tmp_path, mock_fsspec2):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        for file in ["file1.txt", "file2.txt"]:
            (tmp_path / file).touch()
    output_paths = sorted(xlistdir(input_path))
    assert output_paths == expected_paths


@pytest.mark.integration
def test_xlistdir_private(hf_private_dataset_repo_zipped_txt_data, hf_token):
    root_url = hf_dataset_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
    download_config = DownloadConfig(token=hf_token)
    assert len(xlistdir("zip://::" + root_url, download_config=download_config)) == 1
    assert len(xlistdir("zip://main_dir::" + root_url, download_config=download_config)) == 2
    with pytest.raises(FileNotFoundError):
        xlistdir("zip://qwertyuiop::" + root_url, download_config=download_config)
    with pytest.raises(FileNotFoundError):
        xlistdir(root_url, download_config=download_config)


@pytest.mark.parametrize(
    "input_path, isdir",
    [
        ("tmp_path", True),
        ("tmp_path/file.txt", False),
        ("mock://", True),
        ("mock://top_level", True),
        ("mock://dir_that_doesnt_exist", False),
    ],
)
def test_xisdir(input_path, isdir, tmp_path, mock_fsspec2):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
    assert xisdir(input_path) == isdir


@pytest.mark.integration
def test_xisdir_private(hf_private_dataset_repo_zipped_txt_data, hf_token):
    root_url = hf_dataset_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
    download_config = DownloadConfig(token=hf_token)
    assert xisdir("zip://::" + root_url, download_config=download_config) is True
    assert xisdir("zip://main_dir::" + root_url, download_config=download_config) is True
    assert xisdir("zip://qwertyuiop::" + root_url, download_config=download_config) is False
    assert xisdir(root_url, download_config=download_config) is False


@pytest.mark.parametrize(
    "input_path, isfile",
    [
        ("tmp_path/file.txt", True),
        ("tmp_path/file_that_doesnt_exist.txt", False),
        ("mock://", False),
        ("mock://top_level/second_level/date=2019-10-01/a.parquet", True),
    ],
)
def test_xisfile(input_path, isfile, tmp_path, mock_fsspec2):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
    assert xisfile(input_path) == isfile


@pytest.mark.integration
def test_xisfile_private(hf_private_dataset_repo_txt_data, hf_token):
    root_url = hf_dataset_url(hf_private_dataset_repo_txt_data, "")
    download_config = DownloadConfig(token=hf_token)
    assert xisfile(root_url + "data/text_data.txt", download_config=download_config) is True
    assert xisfile(root_url + "qwertyuiop", download_config=download_config) is False


@pytest.mark.parametrize(
    "input_path, size",
    [
        ("tmp_path/file.txt", 100),
        ("mock://", 0),
        ("mock://top_level/second_level/date=2019-10-01/a.parquet", 100),
    ],
)
def test_xgetsize(input_path, size, tmp_path, mock_fsspec2):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
        (tmp_path / "file.txt").write_bytes(b"x" * 100)
    assert xgetsize(input_path) == size


@pytest.mark.integration
def test_xgetsize_private(hf_private_dataset_repo_txt_data, hf_token):
    root_url = hf_dataset_url(hf_private_dataset_repo_txt_data, "")
    download_config = DownloadConfig(token=hf_token)
    assert xgetsize(root_url + "data/text_data.txt", download_config=download_config) == 39
    with pytest.raises(FileNotFoundError):
        xgetsize(root_url + "qwertyuiop", download_config=download_config)


@pytest.mark.parametrize(
    "input_path, expected_paths",
    [
        ("tmp_path/*.txt", ["file1.txt", "file2.txt"]),
        ("mock://*", ["mock://glob_test", "mock://misc", "mock://top_level"]),
        ("mock://top_*", ["mock://top_level"]),
        (
            "mock://top_level/second_level/date=2019-10-0[1-4]",
            [
                "mock://top_level/second_level/date=2019-10-01",
                "mock://top_level/second_level/date=2019-10-02",
                "mock://top_level/second_level/date=2019-10-04",
            ],
        ),
        (
            "mock://top_level/second_level/date=2019-10-0[1-4]/*",
            [
                "mock://top_level/second_level/date=2019-10-01/a.parquet",
                "mock://top_level/second_level/date=2019-10-01/b.parquet",
                "mock://top_level/second_level/date=2019-10-02/a.parquet",
                "mock://top_level/second_level/date=2019-10-04/a.parquet",
            ],
        ),
    ],
)
def test_xglob(input_path, expected_paths, tmp_path, mock_fsspec2):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        expected_paths = [str(tmp_path / file) for file in expected_paths]
        for file in ["file1.txt", "file2.txt", "README.md"]:
            (tmp_path / file).touch()
    output_paths = sorted(xglob(input_path))
    assert output_paths == expected_paths


@pytest.mark.integration
def test_xglob_private(hf_private_dataset_repo_zipped_txt_data, hf_token):
    root_url = hf_dataset_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
    download_config = DownloadConfig(token=hf_token)
    assert len(xglob("zip://**::" + root_url, download_config=download_config)) == 3
    assert len(xglob("zip://qwertyuiop/*::" + root_url, download_config=download_config)) == 0


@pytest.mark.parametrize(
    "input_path, expected_outputs",
    [
        ("tmp_path", [("", [], ["file1.txt", "file2.txt", "README.md"])]),
        (
            "mock://top_level/second_level",
            [
                ("mock://top_level/second_level", ["date=2019-10-01", "date=2019-10-02", "date=2019-10-04"], []),
                ("mock://top_level/second_level/date=2019-10-01", [], ["a.parquet", "b.parquet"]),
                ("mock://top_level/second_level/date=2019-10-02", [], ["a.parquet"]),
                ("mock://top_level/second_level/date=2019-10-04", [], ["a.parquet"]),
            ],
        ),
    ],
)
def test_xwalk(input_path, expected_outputs, tmp_path, mock_fsspec2):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        expected_outputs = sorted(
            [
                (str(tmp_path / dirpath).rstrip("/"), sorted(dirnames), sorted(filenames))
                for dirpath, dirnames, filenames in expected_outputs
            ]
        )
        for file in ["file1.txt", "file2.txt", "README.md"]:
            (tmp_path / file).touch()
    outputs = sorted(xwalk(input_path))
    outputs = [(dirpath, sorted(dirnames), sorted(filenames)) for dirpath, dirnames, filenames in outputs]
    assert outputs == expected_outputs


@pytest.mark.integration
def test_xwalk_private(hf_private_dataset_repo_zipped_txt_data, hf_token):
    root_url = hf_dataset_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
    download_config = DownloadConfig(token=hf_token)
    assert len(list(xwalk("zip://::" + root_url, download_config=download_config))) == 2
    assert len(list(xwalk("zip://main_dir::" + root_url, download_config=download_config))) == 1
    assert len(list(xwalk("zip://qwertyuiop::" + root_url, download_config=download_config))) == 0


@pytest.mark.parametrize(
    "input_path, start_path, expected_path",
    [
        ("dir1/dir2/file.txt".replace("/", os.path.sep), "dir1", "dir2/file.txt".replace("/", os.path.sep)),
        ("dir1/dir2/file.txt".replace("/", os.path.sep), "dir1/dir2".replace("/", os.path.sep), "file.txt"),
        ("zip://file.txt::https://host.com/archive.zip", "zip://::https://host.com/archive.zip", "file.txt"),
        (
            "zip://folder/file.txt::https://host.com/archive.zip",
            "zip://::https://host.com/archive.zip",
            "folder/file.txt",
        ),
        (
            "zip://folder/file.txt::https://host.com/archive.zip",
            "zip://folder::https://host.com/archive.zip",
            "file.txt",
        ),
    ],
)
def test_xrelpath(input_path, start_path, expected_path):
    output_path = xrelpath(input_path, start=start_path)
    assert output_path == expected_path


class TestxPath:
    @pytest.mark.parametrize(
        "input_path",
        [
            "https://host.com/archive.zip",
            "zip://file.txt::https://host.com/archive.zip",
            "zip://dir/file.txt::https://host.com/archive.zip",
            "file.txt",
            str(Path().resolve() / "file.txt"),
        ],
    )
    def test_xpath_str(self, input_path):
        assert str(xPath(input_path)) == input_path

    @pytest.mark.parametrize(
        "input_path, expected_path",
        [
            ("https://host.com/archive.zip", "https://host.com/archive.zip"),
            ("zip://file.txt::https://host.com/archive.zip", "zip://file.txt::https://host.com/archive.zip"),
            ("zip://dir/file.txt::https://host.com/archive.zip", "zip://dir/file.txt::https://host.com/archive.zip"),
            ("file.txt", "file.txt"),
            (str(Path().resolve() / "file.txt"), (Path().resolve() / "file.txt").as_posix()),
        ],
    )
    def test_xpath_as_posix(self, input_path, expected_path):
        assert xPath(input_path).as_posix() == expected_path

    @pytest.mark.parametrize(
        "input_path, exists",
        [
            ("tmp_path/file.txt", True),
            ("tmp_path/file_that_doesnt_exist.txt", False),
            ("mock://top_level/second_level/date=2019-10-01/a.parquet", True),
            ("mock://top_level/second_level/date=2019-10-01/file_that_doesnt_exist.parquet", False),
        ],
    )
    def test_xpath_exists(self, input_path, exists, tmp_path, mock_fsspec2):
        if input_path.startswith("tmp_path"):
            input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
            (tmp_path / "file.txt").touch()
        assert xexists(input_path) is exists

    @pytest.mark.parametrize(
        "input_path, pattern, expected_paths",
        [
            ("tmp_path", "*.txt", ["file1.txt", "file2.txt"]),
            ("mock://", "*", ["mock://glob_test", "mock://misc", "mock://top_level"]),
            ("mock://", "top_*", ["mock://top_level"]),
            (
                "mock://top_level/second_level",
                "date=2019-10-0[1-4]",
                [
                    "mock://top_level/second_level/date=2019-10-01",
                    "mock://top_level/second_level/date=2019-10-02",
                    "mock://top_level/second_level/date=2019-10-04",
                ],
            ),
            (
                "mock://top_level/second_level",
                "date=2019-10-0[1-4]/*",
                [
                    "mock://top_level/second_level/date=2019-10-01/a.parquet",
                    "mock://top_level/second_level/date=2019-10-01/b.parquet",
                    "mock://top_level/second_level/date=2019-10-02/a.parquet",
                    "mock://top_level/second_level/date=2019-10-04/a.parquet",
                ],
            ),
        ],
    )
    def test_xpath_glob(self, input_path, pattern, expected_paths, tmp_path, mock_fsspec2):
        if input_path == "tmp_path":
            input_path = tmp_path
            expected_paths = [tmp_path / file for file in expected_paths]
            for file in ["file1.txt", "file2.txt", "README.md"]:
                (tmp_path / file).touch()
        else:
            expected_paths = [Path(file) for file in expected_paths]
        output_paths = sorted(xPath(input_path).glob(pattern))
        assert output_paths == expected_paths

    @pytest.mark.parametrize(
        "input_path, pattern, expected_paths",
        [
            ("tmp_path", "*.txt", ["file1.txt", "file2.txt"]),
            (
                "mock://",
                "date=2019-10-0[1-4]",
                [
                    "mock://top_level/second_level/date=2019-10-01",
                    "mock://top_level/second_level/date=2019-10-02",
                    "mock://top_level/second_level/date=2019-10-04",
                ],
            ),
            (
                "mock://top_level",
                "date=2019-10-0[1-4]",
                [
                    "mock://top_level/second_level/date=2019-10-01",
                    "mock://top_level/second_level/date=2019-10-02",
                    "mock://top_level/second_level/date=2019-10-04",
                ],
            ),
            (
                "mock://",
                "date=2019-10-0[1-4]/*",
                [
                    "mock://top_level/second_level/date=2019-10-01/a.parquet",
                    "mock://top_level/second_level/date=2019-10-01/b.parquet",
                    "mock://top_level/second_level/date=2019-10-02/a.parquet",
                    "mock://top_level/second_level/date=2019-10-04/a.parquet",
                ],
            ),
            (
                "mock://top_level",
                "date=2019-10-0[1-4]/*",
                [
                    "mock://top_level/second_level/date=2019-10-01/a.parquet",
                    "mock://top_level/second_level/date=2019-10-01/b.parquet",
                    "mock://top_level/second_level/date=2019-10-02/a.parquet",
                    "mock://top_level/second_level/date=2019-10-04/a.parquet",
                ],
            ),
        ],
    )
    def test_xpath_rglob(self, input_path, pattern, expected_paths, tmp_path, mock_fsspec2):
        if input_path == "tmp_path":
            input_path = tmp_path
            dir_path = tmp_path / "dir"
            dir_path.mkdir()
            expected_paths = [dir_path / file for file in expected_paths]
            for file in ["file1.txt", "file2.txt", "README.md"]:
                (dir_path / file).touch()
        else:
            expected_paths = [Path(file) for file in expected_paths]
        output_paths = sorted(xPath(input_path).rglob(pattern))
        assert output_paths == expected_paths

    @pytest.mark.parametrize(
        "input_path, expected_path",
        [
            ("https://host.com/archive.zip", "https://host.com"),
            ("zip://file.txt::https://host.com/archive.zip", "zip://::https://host.com/archive.zip"),
            ("zip://dir/file.txt::https://host.com/archive.zip", "zip://dir::https://host.com/archive.zip"),
            ("file.txt", ""),
            (str(Path().resolve() / "file.txt"), str(Path().resolve())),
        ],
    )
    def test_xpath_parent(self, input_path, expected_path):
        assert xPath(input_path).parent == xPath(expected_path)

    @pytest.mark.parametrize(
        "input_path, expected",
        [
            ("https://host.com/archive.zip", "archive.zip"),
            ("zip://file.txt::https://host.com/archive.zip", "file.txt"),
            ("zip://dir/file.txt::https://host.com/archive.zip", "file.txt"),
            ("file.txt", "file.txt"),
            (str(Path().resolve() / "file.txt"), "file.txt"),
        ],
    )
    def test_xpath_name(self, input_path, expected):
        assert xPath(input_path).name == expected

    @pytest.mark.parametrize(
        "input_path, expected",
        [
            ("https://host.com/archive.zip", "archive"),
            ("zip://file.txt::https://host.com/archive.zip", "file"),
            ("zip://dir/file.txt::https://host.com/archive.zip", "file"),
            ("file.txt", "file"),
            (str(Path().resolve() / "file.txt"), "file"),
        ],
    )
    def test_xpath_stem(self, input_path, expected):
        assert xPath(input_path).stem == expected

    @pytest.mark.parametrize(
        "input_path, expected",
        [
            ("https://host.com/archive.zip", ".zip"),
            ("zip://file.txt::https://host.com/archive.zip", ".txt"),
            ("zip://dir/file.txt::https://host.com/archive.zip", ".txt"),
            ("file.txt", ".txt"),
            (str(Path().resolve() / "file.txt"), ".txt"),
        ],
    )
    def test_xpath_suffix(self, input_path, expected):
        assert xPath(input_path).suffix == expected

    @pytest.mark.parametrize(
        "input_path, suffix, expected",
        [
            ("https://host.com/archive.zip", ".ann", "https://host.com/archive.ann"),
            ("zip://file.txt::https://host.com/archive.zip", ".ann", "zip://file.ann::https://host.com/archive.zip"),
            (
                "zip://dir/file.txt::https://host.com/archive.zip",
                ".ann",
                "zip://dir/file.ann::https://host.com/archive.zip",
            ),
            ("file.txt", ".ann", "file.ann"),
            (str(Path().resolve() / "file.txt"), ".ann", str(Path().resolve() / "file.ann")),
        ],
    )
    def test_xpath_with_suffix(self, input_path, suffix, expected):
        assert xPath(input_path).with_suffix(suffix) == xPath(expected)


@pytest.mark.parametrize(
    "urlpath, expected_protocol",
    [
        ("zip://train-00000.json.gz::https://foo.bar/data.zip", "gzip"),
        ("https://foo.bar/train.json.gz?dl=1", "gzip"),
        ("http://opus.nlpl.eu/download.php?f=Bianet/v1/moses/en-ku.txt.zip", "zip"),
        ("https://github.com/user/what-time-is-it/blob/master/gutenberg_time_phrases.zip?raw=true", "zip"),
        ("https://github.com/user/repo/blob/master/data/morph_train.tsv?raw=true", None),
        ("https://repo.org/bitstream/handle/20.500.12185/346/annotated_corpus.zip?sequence=3&isAllowed=y", "zip"),
        ("https://zenodo.org/record/2787612/files/SICK.zip?download=1", "zip"),
    ],
)
def test_get_extraction_protocol(urlpath, expected_protocol):
    assert _get_extraction_protocol(urlpath) == expected_protocol


@pytest.mark.parametrize(
    "urlpath, expected_protocol",
    [
        (TEST_GG_DRIVE_GZIPPED_URL, "gzip"),
        (TEST_GG_DRIVE_ZIPPED_URL, "zip"),
    ],
)
@slow  # otherwise it spams Google Drive and the CI gets banned
def test_get_extraction_protocol_gg_drive(urlpath, expected_protocol):
    assert _get_extraction_protocol(urlpath) == expected_protocol


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive():
    with xopen(TEST_GG_DRIVE_URL) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


def test_xnumpy_load(tmp_path):
    import numpy as np

    expected_x = np.arange(10)
    npy_path = tmp_path / "data-x.npy"
    np.save(npy_path, expected_x)
    x = xnumpy_load(npy_path)
    assert np.array_equal(x, expected_x)

    npz_path = tmp_path / "data.npz"
    np.savez(npz_path, x=expected_x)
    with xnumpy_load(npz_path) as f:
        x = f["x"]
    assert np.array_equal(x, expected_x)
