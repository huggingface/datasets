import posixpath
from pathlib import Path

import fsspec
import pytest
from fsspec.implementations.local import AbstractFileSystem, LocalFileSystem, stringify_path


class MockFileSystem(AbstractFileSystem):
    protocol = "mock"

    def __init__(self, *args, local_root_dir, **kwargs):
        super().__init__()
        self._fs = LocalFileSystem(*args, **kwargs)
        self.local_root_dir = Path(local_root_dir).as_posix()

    def mkdir(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.mkdir(path, *args, **kwargs)

    def makedirs(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.makedirs(path, *args, **kwargs)

    def rmdir(self, path):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.rmdir(path)

    def ls(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.ls(path, *args, **kwargs)

    def glob(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.glob(path, *args, **kwargs)

    def info(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.info(path, *args, **kwargs)

    def lexists(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.lexists(path, *args, **kwargs)

    def cp_file(self, path1, path2, *args, **kwargs):
        path1 = posixpath.join(self.local_root_dir, self._strip_protocol(path1))
        path2 = posixpath.join(self.local_root_dir, self._strip_protocol(path2))
        return self._fs.cp_file(path1, path2, *args, **kwargs)

    def get_file(self, path1, path2, *args, **kwargs):
        path1 = posixpath.join(self.local_root_dir, self._strip_protocol(path1))
        path2 = posixpath.join(self.local_root_dir, self._strip_protocol(path2))
        return self._fs.get_file(path1, path2, *args, **kwargs)

    def put_file(self, path1, path2, *args, **kwargs):
        path1 = posixpath.join(self.local_root_dir, self._strip_protocol(path1))
        path2 = posixpath.join(self.local_root_dir, self._strip_protocol(path2))
        return self._fs.put_file(path1, path2, *args, **kwargs)

    def mv_file(self, path1, path2, *args, **kwargs):
        path1 = posixpath.join(self.local_root_dir, self._strip_protocol(path1))
        path2 = posixpath.join(self.local_root_dir, self._strip_protocol(path2))
        return self._fs.mv_file(path1, path2, *args, **kwargs)

    def rm_file(self, path):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.rm_file(path)

    def rm(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.rm(path, *args, **kwargs)

    def _open(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs._open(path, *args, **kwargs)

    def open(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.open(path, *args, **kwargs)

    def touch(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.touch(path, *args, **kwargs)

    def created(self, path):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.created(path)

    def modified(self, path):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.modified(path)

    @classmethod
    def _parent(cls, path):
        return LocalFileSystem._parent(path)

    @classmethod
    def _strip_protocol(cls, path):
        path = stringify_path(path)
        if path.startswith("mock://"):
            path = path[7:]
        return path

    def chmod(self, path, *args, **kwargs):
        path = posixpath.join(self.local_root_dir, self._strip_protocol(path))
        return self._fs.mkdir(path, *args, **kwargs)


@pytest.fixture
def mock_fsspec(monkeypatch):
    monkeypatch.setitem(fsspec.registry.target, "mock", MockFileSystem)


@pytest.fixture
def mockfs(tmp_path_factory, mock_fsspec):
    local_fs_dir = tmp_path_factory.mktemp("mockfs")
    return MockFileSystem(local_root_dir=local_fs_dir)
