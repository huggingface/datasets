import posixpath
from pathlib import Path
from unittest.mock import patch

import pytest
from fsspec.implementations.local import AbstractFileSystem, LocalFileSystem, stringify_path
from fsspec.registry import _registry as _fsspec_registry


class MockFileSystem(AbstractFileSystem):
    protocol = "mock"

    def __init__(self, *args, local_root_dir, **kwargs):
        super().__init__()
        self._fs = LocalFileSystem(*args, **kwargs)
        self.local_root_dir = Path(local_root_dir).resolve().as_posix() + "/"

    def mkdir(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.mkdir(path, *args, **kwargs)

    def makedirs(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.makedirs(path, *args, **kwargs)

    def rmdir(self, path):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.rmdir(path)

    def ls(self, path, detail=True, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        out = self._fs.ls(path, detail=detail, *args, **kwargs)
        if detail:
            return [{**info, "name": info["name"][len(self.local_root_dir) :]} for info in out]
        else:
            return [name[len(self.local_root_dir) :] for name in out]

    def info(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        out = dict(self._fs.info(path, *args, **kwargs))
        out["name"] = out["name"][len(self.local_root_dir) :]
        return out

    def cp_file(self, path1, path2, *args, **kwargs):
        path1 = posixpath.join(self.local_root_dir, self._strip_protocol(path1))
        path2 = posixpath.join(self.local_root_dir, self._strip_protocol(path2))
        return self._fs.cp_file(path1, path2, *args, **kwargs)

    def rm_file(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.rm_file(path, *args, **kwargs)

    def rm(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.rm(path, *args, **kwargs)

    def _open(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs._open(path, *args, **kwargs)

    def created(self, path):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.created(path)

    def modified(self, path):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.modified(path)

    @classmethod
    def _strip_protocol(cls, path):
        path = stringify_path(path)
        if path.startswith("mock://"):
            path = path[7:]
        return path


class TmpDirFileSystem(MockFileSystem):
    protocol = "tmp"
    tmp_dir = None

    def __init__(self, *args, **kwargs):
        assert self.tmp_dir is not None, "TmpDirFileSystem.tmp_dir is not set"
        super().__init__(*args, **kwargs, local_root_dir=self.tmp_dir, auto_mkdir=True)

    @classmethod
    def _strip_protocol(cls, path):
        path = stringify_path(path)
        if path.startswith("tmp://"):
            path = path[6:]
        return path


@pytest.fixture
def mock_fsspec():
    _fsspec_registry["mock"] = MockFileSystem
    _fsspec_registry["tmp"] = TmpDirFileSystem
    yield
    del _fsspec_registry["mock"]
    del _fsspec_registry["tmp"]


@pytest.fixture
def mockfs(tmp_path_factory, mock_fsspec):
    local_fs_dir = tmp_path_factory.mktemp("mockfs")
    return MockFileSystem(local_root_dir=local_fs_dir, auto_mkdir=True)


@pytest.fixture
def tmpfs(tmp_path_factory, mock_fsspec):
    tmp_fs_dir = tmp_path_factory.mktemp("tmpfs")
    with patch.object(TmpDirFileSystem, "tmp_dir", tmp_fs_dir):
        yield TmpDirFileSystem()
        TmpDirFileSystem.clear_instance_cache()
