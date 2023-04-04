import re
from glob import has_magic
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
        self.root_results = {}

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

    def _glob(self, path, **kwargs):
        """
        **copied with minor revisions from https://github.com/fsspec/filesystem_spec/blob/master/fsspec/spec.py, with BSD 3-Clause License**
        Find files by glob-matching.
        If the path ends with '/' and does not contain "*", it is essentially
        the same as ``ls(path)``, returning only files.
        We support ``"**"``,
        ``"?"`` and ``"[..]"``. We do not support ^ for pattern negation.
        Search path names that contain embedded characters special to this
        implementation of glob may not produce expected results;
        e.g., 'foo/bar/*starredfilename*'.
        kwargs are passed to ``ls``.
        """

        ends = path.endswith("/")
        path = self._strip_protocol(path)
        indstar = path.find("*") if path.find("*") >= 0 else len(path)
        indques = path.find("?") if path.find("?") >= 0 else len(path)
        indbrace = path.find("[") if path.find("[") >= 0 else len(path)

        ind = min(indstar, indques, indbrace)

        detail = kwargs.pop("detail", False)

        if not has_magic(path):
            root = path
            depth = 1
            if ends:
                path += "/*"
            elif self.exists(path):
                if not detail:
                    return [path]
                else:
                    return {path: self.info(path)}
            else:
                if not detail:
                    return []  # glob of non-existent returns empty
                else:
                    return {}
        elif "/" in path[:ind]:
            ind2 = path[:ind].rindex("/")
            root = path[: ind2 + 1]
            depth = None if "**" in path else path[ind2 + 1 :].count("/") + 1
        else:
            root = ""
            depth = None if "**" in path else path[ind + 1 :].count("/") + 1

        if self.dir_cache is not None:
            allpaths = self.dir_cache
        else:
            allpaths = self.find(root, maxdepth=depth, withdirs=True, detail=True, **kwargs)

        # Escape characters special to python regex, leaving our supported
        # special characters in place.
        # See https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html
        # for shell globbing details.
        pattern = (
            "^"
            + (
                path.replace("\\", r"\\")
                .replace(".", r"\.")
                .replace("+", r"\+")
                .replace("//", "/")
                .replace("(", r"\(")
                .replace(")", r"\)")
                .replace("|", r"\|")
                .replace("^", r"\^")
                .replace("$", r"\$")
                .replace("{", r"\{")
                .replace("}", r"\}")
                .rstrip("/")
                .replace("?", ".")
            )
            + "$"
        )
        pattern = re.sub("[*]{2}", "=PLACEHOLDER=", pattern)
        pattern = re.sub("[*]", "[^/]*", pattern)
        pattern = re.compile(pattern.replace("=PLACEHOLDER=", ".*"))

        out = {p: allpaths[p] for p in sorted(allpaths) if pattern.match(p.replace("//", "/").rstrip("/"))}
        if detail:
            return out
        else:
            return list(out)
