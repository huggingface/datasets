from pathlib import PurePath
from typing import Optional

import fsspec
from fsspec import AbstractFileSystem
from huggingface_hub.hf_api import DatasetInfo

from ..utils.file_utils import get_authentication_headers_for_url, hf_hub_url


class HfFileSystem(AbstractFileSystem):
    """Interface to files in a Hugging face repository"""

    root_marker = ""
    protocol = "hf"

    def __init__(
        self,
        repo_info: Optional[str] = None,
        token: Optional[str] = None,
        **kwargs,
    ):
        """
        The compressed file system can be instantiated from any compressed file.
        It reads the contents of compressed file as a filesystem with one file inside, as if it was an archive.

        The single file inside the filesystem is named after the compresssed file,
        without the compression extension at the end of the filename.

        Args:
            repo_info (:obj:``DatasetInfo``, `optional`):
                Dataset repository info from huggingface_hub.HfApi().dataset_info(...)
            token (:obj:``str``, `optional`):
                Hugging Face token. Will default to the locally saved token if not provided.
        """
        super().__init__(self, **kwargs)
        self.repo_info = repo_info
        self.token = token
        self.dir_cache = None

    def _get_dirs(self):
        if self.dir_cache is None:
            self.dir_cache = {
                hf_file.rfilename: {"name": hf_file.rfilename, "size": 0 or None, "type": "file"}  # TODO(QL): add size
                for hf_file in self.repo_info.siblings
            }

    def _open(
        self,
        path: str,
        mode: str = "rb",
        **kwargs,
    ):
        if not isinstance(self.repo_info, DatasetInfo):
            raise NotImplementedError(f"Open is only implemented for dataset repositories, but got {self.repo_info}")
        url = hf_hub_url(self.repo_info.id, path, revision=self.repo_info.sha)
        return fsspec.open(
            url,
            mode=mode,
            headers=get_authentication_headers_for_url(url, use_auth_token=self.token),
        ).open()

    def info(self, path, **kwargs):
        self._get_dirs()
        path = self._strip_protocol(path)
        if path in self.dir_cache:
            return self.dir_cache[path]
        else:
            raise FileNotFoundError(path)

    def ls(self, path, detail=False, **kwargs):
        self._get_dirs()
        path = PurePath(path.strip("/"))
        paths = {}
        for p, f in self.dir_cache.items():
            p = PurePath(p.strip("/"))
            root = p.parent
            if root == path:
                # file is in directory -> return file
                paths[str(p)] = f
            elif path in p.parents:
                # file is in subdirectory -> return first intermediate directory
                ppath = str(path / p.relative_to(path).parts[0])
                paths[ppath] = {"name": ppath + "/", "size": 0, "type": "directory"}
        out = list(paths.values())
        if detail:
            return out
        else:
            return list(sorted(f["name"] for f in out))
