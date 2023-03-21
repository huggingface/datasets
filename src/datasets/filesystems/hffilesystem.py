from pathlib import PurePosixPath
from typing import Optional

import fsspec
from fsspec import AbstractFileSystem
from huggingface_hub.hf_api import DatasetInfo

from ..utils.file_utils import get_authentication_headers_for_url
from ..utils.hub import hf_hub_url


class HfFileSystem(AbstractFileSystem):
    """Interface to files in a Hugging face repository"""

    root_marker = ""
    protocol = "hf-legacy"  # "hf://"" is reserved for hffs

    def __init__(
        self,
        repo_info: Optional[DatasetInfo] = None,
        token: Optional[str] = None,
        **kwargs,
    ):
        """
        The file system can be instantiated using a huggingface_hub.hf_api.DatasetInfo object,
        and can be used to list and open files from a Hugging Face dataset repository with fsspec.

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
            self.dir_cache = {}
            for hf_file in self.repo_info.siblings:
                # TODO(QL): add sizes
                self.dir_cache[hf_file.rfilename] = {
                    "name": hf_file.rfilename,
                    "size": None,
                    "type": "file",
                }
                self.dir_cache.update(
                    {
                        str(d): {"name": str(d), "size": None, "type": "directory"}
                        for d in list(PurePosixPath(hf_file.rfilename).parents)[:-1]
                    }
                )

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
            client_kwargs={"trust_env": True},  # Enable reading proxy env variables.
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
        path = PurePosixPath(path.strip("/"))
        paths = {}
        for p, f in self.dir_cache.items():
            p = PurePosixPath(p.strip("/"))
            root = p.parent
            if root == path:
                paths[str(p)] = f
        out = list(paths.values())
        if detail:
            return out
        else:
            return sorted(f["name"] for f in out)
