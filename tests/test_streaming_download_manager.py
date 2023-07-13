import json
import os
import re
from pathlib import Path

import pytest
from fsspec.registry import _registry as _fsspec_registry
from fsspec.spec import AbstractBufferedFile, AbstractFileSystem

from datasets.download.download_config import DownloadConfig
from datasets.download.streaming_download_manager import (
    StreamingDownloadManager,
    _get_extraction_protocol,
    xbasename,
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
from datasets.filesystems import COMPRESSION_FILESYSTEMS
from datasets.utils.hub import hf_hub_url

from .utils import require_lz4, require_zstandard, slow


TEST_URL = "https://huggingface.co/datasets/lhoestq/test/raw/main/some_text.txt"
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
def mock_fsspec():
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
    from datasets.download.streaming_download_manager import xdirname

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
def test_xexists(input_path, exists, tmp_path, mock_fsspec):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
    assert xexists(input_path) is exists


@pytest.mark.integration
def test_xexists_private(hf_private_dataset_repo_txt_data, hf_token):
    root_url = hf_hub_url(hf_private_dataset_repo_txt_data, "")
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
def test_xlistdir(input_path, expected_paths, tmp_path, mock_fsspec):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        for file in ["file1.txt", "file2.txt"]:
            (tmp_path / file).touch()
    output_paths = sorted(xlistdir(input_path))
    assert output_paths == expected_paths


@pytest.mark.integration
def test_xlistdir_private(hf_private_dataset_repo_zipped_txt_data, hf_token):
    root_url = hf_hub_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
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
def test_xisdir(input_path, isdir, tmp_path, mock_fsspec):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
    assert xisdir(input_path) == isdir


@pytest.mark.integration
def test_xisdir_private(hf_private_dataset_repo_zipped_txt_data, hf_token):
    root_url = hf_hub_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
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
def test_xisfile(input_path, isfile, tmp_path, mock_fsspec):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
    assert xisfile(input_path) == isfile


@pytest.mark.integration
def test_xisfile_private(hf_private_dataset_repo_txt_data, hf_token):
    root_url = hf_hub_url(hf_private_dataset_repo_txt_data, "")
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
def test_xgetsize(input_path, size, tmp_path, mock_fsspec):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        (tmp_path / "file.txt").touch()
        (tmp_path / "file.txt").write_bytes(b"x" * 100)
    assert xgetsize(input_path) == size


@pytest.mark.integration
def test_xgetsize_private(hf_private_dataset_repo_txt_data, hf_token):
    root_url = hf_hub_url(hf_private_dataset_repo_txt_data, "")
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
def test_xglob(input_path, expected_paths, tmp_path, mock_fsspec):
    if input_path.startswith("tmp_path"):
        input_path = input_path.replace("/", os.sep).replace("tmp_path", str(tmp_path))
        expected_paths = [str(tmp_path / file) for file in expected_paths]
        for file in ["file1.txt", "file2.txt", "README.md"]:
            (tmp_path / file).touch()
    output_paths = sorted(xglob(input_path))
    assert output_paths == expected_paths


@pytest.mark.integration
def test_xglob_private(hf_private_dataset_repo_zipped_txt_data, hf_token):
    root_url = hf_hub_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
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
def test_xwalk(input_path, expected_outputs, tmp_path, mock_fsspec):
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
    root_url = hf_hub_url(hf_private_dataset_repo_zipped_txt_data, "data.zip")
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
    def test_xpath_exists(self, input_path, exists, tmp_path, mock_fsspec):
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
    def test_xpath_glob(self, input_path, pattern, expected_paths, tmp_path, mock_fsspec):
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
    def test_xpath_rglob(self, input_path, pattern, expected_paths, tmp_path, mock_fsspec):
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


@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_dummy_path(urlpath):
    dl_manager = StreamingDownloadManager()
    assert dl_manager.download(urlpath) == urlpath


def test_streaming_dl_manager_download(text_path):
    dl_manager = StreamingDownloadManager()
    out = dl_manager.download(text_path)
    assert out == text_path
    with xopen(out, encoding="utf-8") as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize("urlpath", [r"C:\\foo\bar.txt", "/foo/bar.txt", "https://f.oo/bar.txt"])
def test_streaming_dl_manager_download_and_extract_no_extraction(urlpath):
    dl_manager = StreamingDownloadManager()
    assert dl_manager.download_and_extract(urlpath) == urlpath


def test_streaming_dl_manager_extract(text_gz_path, text_path):
    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.extract(text_gz_path)
    path = os.path.basename(text_gz_path)
    path = path[: path.rindex(".")]
    assert output_path == f"gzip://{path}::{text_gz_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


def test_streaming_dl_manager_download_and_extract_with_extraction(text_gz_path, text_path):
    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.download_and_extract(text_gz_path)
    path = os.path.basename(text_gz_path)
    path = path[: path.rindex(".")]
    assert output_path == f"gzip://{path}::{text_gz_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_path, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


@pytest.mark.parametrize(
    "input_path, filename, expected_path",
    [("https://domain.org/archive.zip", "filename.jsonl", "zip://filename.jsonl::https://domain.org/archive.zip")],
)
def test_streaming_dl_manager_download_and_extract_with_join(input_path, filename, expected_path):
    dl_manager = StreamingDownloadManager()
    extracted_path = dl_manager.download_and_extract(input_path)
    output_path = xjoin(extracted_path, filename)
    assert output_path == expected_path


@pytest.mark.parametrize("compression_fs_class", COMPRESSION_FILESYSTEMS)
def test_streaming_dl_manager_extract_all_supported_single_file_compression_types(
    compression_fs_class, gz_file, xz_file, zstd_file, bz2_file, lz4_file, text_file
):
    input_paths = {"gzip": gz_file, "xz": xz_file, "zstd": zstd_file, "bz2": bz2_file, "lz4": lz4_file}
    input_path = input_paths[compression_fs_class.protocol]
    if input_path is None:
        reason = f"for '{compression_fs_class.protocol}' compression protocol, "
        if compression_fs_class.protocol == "lz4":
            reason += require_lz4.kwargs["reason"]
        elif compression_fs_class.protocol == "zstd":
            reason += require_zstandard.kwargs["reason"]
        pytest.skip(reason)
    dl_manager = StreamingDownloadManager()
    output_path = dl_manager.extract(input_path)
    path = os.path.basename(input_path)
    path = path[: path.rindex(".")]
    assert output_path == f"{compression_fs_class.protocol}://{path}::{input_path}"
    fsspec_open_file = xopen(output_path, encoding="utf-8")
    with fsspec_open_file as f, open(text_file, encoding="utf-8") as expected_file:
        assert f.read() == expected_file.read()


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
def test_streaming_dl_manager_get_extraction_protocol(urlpath, expected_protocol):
    assert _get_extraction_protocol(urlpath) == expected_protocol


@pytest.mark.parametrize(
    "urlpath, expected_protocol",
    [
        (TEST_GG_DRIVE_GZIPPED_URL, "gzip"),
        (TEST_GG_DRIVE_ZIPPED_URL, "zip"),
    ],
)
@slow  # otherwise it spams Google Drive and the CI gets banned
def test_streaming_dl_manager_get_extraction_protocol_gg_drive(urlpath, expected_protocol):
    assert _get_extraction_protocol(urlpath) == expected_protocol


@pytest.mark.parametrize(
    "urlpath",
    [
        "zip://train-00000.tar.gz::https://foo.bar/data.zip",
        "https://foo.bar/train.tar.gz",
        "https://foo.bar/train.tgz",
        "https://foo.bar/train.tar",
    ],
)
def test_streaming_dl_manager_extract_throws(urlpath):
    with pytest.raises(NotImplementedError):
        _ = StreamingDownloadManager().extract(urlpath)


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive():
    with xopen(TEST_GG_DRIVE_URL) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive_no_extract():
    urlpath = StreamingDownloadManager().download_and_extract(TEST_GG_DRIVE_URL)
    with xopen(urlpath) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive_gzipped():
    urlpath = StreamingDownloadManager().download_and_extract(TEST_GG_DRIVE_GZIPPED_URL)
    with xopen(urlpath) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


@slow  # otherwise it spams Google Drive and the CI gets banned
@pytest.mark.integration
def test_streaming_gg_drive_zipped():
    urlpath = StreamingDownloadManager().download_and_extract(TEST_GG_DRIVE_ZIPPED_URL)
    all_files = list(xglob(xjoin(urlpath, "*")))
    assert len(all_files) == 1
    assert xbasename(all_files[0]) == TEST_GG_DRIVE_FILENAME
    with xopen(all_files[0]) as f:
        assert f.read() == TEST_GG_DRIVE_CONTENT


def _test_jsonl(path, file):
    assert path.endswith(".jsonl")
    for num_items, line in enumerate(file, start=1):
        item = json.loads(line.decode("utf-8"))
        assert item.keys() == {"col_1", "col_2", "col_3"}
    assert num_items == 4


@pytest.mark.parametrize("archive_jsonl", ["tar_jsonl_path", "zip_jsonl_path"])
def test_iter_archive_path(archive_jsonl, request):
    archive_jsonl_path = request.getfixturevalue(archive_jsonl)
    dl_manager = StreamingDownloadManager()
    archive_iterable = dl_manager.iter_archive(archive_jsonl_path)
    num_jsonl = 0
    for num_jsonl, (path, file) in enumerate(archive_iterable, start=1):
        _test_jsonl(path, file)
    assert num_jsonl == 2
    # do it twice to make sure it's reset correctly
    num_jsonl = 0
    for num_jsonl, (path, file) in enumerate(archive_iterable, start=1):
        _test_jsonl(path, file)
    assert num_jsonl == 2


@pytest.mark.parametrize("archive_nested_jsonl", ["tar_nested_jsonl_path", "zip_nested_jsonl_path"])
def test_iter_archive_file(archive_nested_jsonl, request):
    archive_nested_jsonl_path = request.getfixturevalue(archive_nested_jsonl)
    dl_manager = StreamingDownloadManager()
    files_iterable = dl_manager.iter_archive(archive_nested_jsonl_path)
    num_tar, num_jsonl = 0, 0
    for num_tar, (path, file) in enumerate(files_iterable, start=1):
        for num_jsonl, (subpath, subfile) in enumerate(dl_manager.iter_archive(file), start=1):
            _test_jsonl(subpath, subfile)
    assert num_tar == 1
    assert num_jsonl == 2
    # do it twice to make sure it's reset correctly
    num_tar, num_jsonl = 0, 0
    for num_tar, (path, file) in enumerate(files_iterable, start=1):
        for num_jsonl, (subpath, subfile) in enumerate(dl_manager.iter_archive(file), start=1):
            _test_jsonl(subpath, subfile)
    assert num_tar == 1
    assert num_jsonl == 2


def test_iter_files(data_dir_with_hidden_files):
    dl_manager = StreamingDownloadManager()
    for num_file, file in enumerate(dl_manager.iter_files(data_dir_with_hidden_files), start=1):
        assert os.path.basename(file) == ("test.txt" if num_file == 1 else "train.txt")
    assert num_file == 2


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
