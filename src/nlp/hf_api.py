# coding=utf-8
# Copyright 2019-present, the HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import io
import os
from os.path import expanduser
from typing import Dict, List, Optional, Tuple

import requests
from tqdm import tqdm


ENDPOINT = "https://huggingface.co"


class S3Obj:
    """
    Data structure that represents a file belonging to the current user.
    """

    def __init__(self, filename: str, LastModified: str, ETag: str, Size: int, **kwargs):
        self.filename = filename
        self.LastModified = LastModified
        self.ETag = ETag
        self.Size = Size

    def __repr__(self):
        return f"nlp.S3Obj(filename='{self.filename}')"


class PresignedUrl:
    def __init__(self, write: str, access: str, type: str, **kwargs):
        self.write = write
        self.access = access
        self.type = type  # mime-type to send to S3.

    def __repr__(self):
        return f"nlp.PresignedUrl(write='{self.write}', access='{self.access}', type='{self.type}')"


class S3Object:
    """
    Data structure that represents a public file accessible on our S3.
    """

    def __init__(
        self,
        key: str,  # S3 object key
        etag: str,
        lastModified: str,
        size: int,
        rfilename: str,  # filename relative to config.json
        **kwargs,
    ):
        self.key = key
        self.etag = etag
        self.lastModified = lastModified
        self.size = size
        self.rfilename = rfilename
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"nlp.S3Object('{self.rfilename}')"


class ObjectInfo:
    """
    Info about a public dataset or Metric accessible from our S3.
    """

    def __init__(
        self,
        id: str,
        key: str,
        lastModified: Optional[str] = None,
        description: Optional[str] = None,
        citation: Optional[str] = None,
        size: Optional[int] = None,
        etag: Optional[str] = None,
        siblings: List[Dict] = None,
        author: str = None,
        **kwargs,
    ):
        self.id = id  # id of dataset
        self.key = key  # S3 object key of config.json
        self.lastModified = lastModified
        self.description = description
        self.citation = citation
        self.size = size
        self.etag = etag
        self.siblings = siblings  # list of files that constitute the dataset
        self.author = author
        self.siblings = [S3Object(**x) for x in self.siblings] if self.siblings else None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        single_line_description = self.description.replace("\n", "")
        return f"nlp.ObjectInfo(id='{self.id}', description='{single_line_description}', files={self.siblings})"


class HfApi:
    ALLOWED_FILE_TYPES = ["datasets", "metrics"]

    def __init__(self, endpoint=None):
        """Create Api using a specific endpoint and also the file types ('datasets' or 'metrics')"""
        self.endpoint = endpoint if endpoint is not None else ENDPOINT

    def login(self, username: str, password: str) -> str:
        """
        Call HF API to sign in a user and get a token if credentials are valid.

        Outputs:
            token if credentials are valid

        Throws:
            requests.exceptions.HTTPError if credentials are invalid
        """
        path = "{}/api/login".format(self.endpoint)
        r = requests.post(path, json={"username": username, "password": password})
        r.raise_for_status()
        d = r.json()
        return d["token"]

    def whoami(self, token: str) -> Tuple[str, List[str]]:
        """
        Call HF API to know "whoami"
        """
        path = "{}/api/whoami".format(self.endpoint)
        r = requests.get(path, headers={"authorization": "Bearer {}".format(token)})
        r.raise_for_status()
        d = r.json()
        return d["user"], d["orgs"]

    def logout(self, token: str) -> None:
        """
        Call HF API to log out.
        """
        path = "{}/api/logout".format(self.endpoint)
        r = requests.post(path, headers={"authorization": "Bearer {}".format(token)})
        r.raise_for_status()

    def presign(
        self, token: str, filename: str, organization: Optional[str] = None, file_types: Optional[str] = None
    ) -> PresignedUrl:
        """
        Call HF API to get a presigned url to upload `filename` to S3.
        """
        assert file_types in self.ALLOWED_FILE_TYPES, "Please specify file types from {}".format(
            self.ALLOWED_FILE_TYPES
        )
        path = "{}/api/{}/presign".format(self.endpoint, file_types)
        r = requests.post(
            path,
            headers={"authorization": "Bearer {}".format(token)},
            json={"filename": filename, "organization": organization},
        )
        r.raise_for_status()
        d = r.json()
        return PresignedUrl(**d)

    def presign_and_upload(
        self,
        token: str,
        filename: str,
        filepath: str,
        organization: Optional[str] = None,
        file_types: Optional[str] = None,
    ) -> str:
        """
        Get a presigned url, then upload file to S3.

        Outputs:
            url: Read-only url for the stored file on S3.
        """
        urls = self.presign(token, filename=filename, organization=organization, file_types=file_types)
        # streaming upload:
        # https://2.python-requests.org/en/master/user/advanced/#streaming-uploads
        #
        # Even though we presign with the correct content-type,
        # the client still has to specify it when uploading the file.
        with open(filepath, "rb") as f:
            pf = TqdmProgressFileReader(f)
            data = f if pf.total_size > 0 else ""

            r = requests.put(urls.write, data=data, headers={"content-type": urls.type})
            r.raise_for_status()
            pf.close()
        return urls.access

    def list_objs(
        self, token: str, organization: Optional[str] = None, file_types: Optional[str] = None
    ) -> List[S3Obj]:
        """
        Call HF API to list all stored files for user (or one of their organizations).
        """
        assert file_types in self.ALLOWED_FILE_TYPES, "Please specify file types from {}".format(
            self.ALLOWED_FILE_TYPES
        )
        path = "{}/api/{}/listObjs".format(self.endpoint, file_types)
        params = {"organization": organization} if organization is not None else None
        r = requests.get(path, params=params, headers={"authorization": "Bearer {}".format(token)})
        r.raise_for_status()
        d = r.json()
        return [S3Obj(**x) for x in d]

    def delete_obj(
        self, token: str, filename: str, organization: Optional[str] = None, file_types: Optional[str] = None
    ):
        """
        Call HF API to delete a file stored by user
        """
        assert file_types in self.ALLOWED_FILE_TYPES, "Please specify file types from {}".format(
            self.ALLOWED_FILE_TYPES
        )
        path = "{}/api/{}/deleteObj".format(self.endpoint, file_types)
        r = requests.delete(
            path,
            headers={"authorization": "Bearer {}".format(token)},
            json={"filename": filename, "organization": organization},
        )
        r.raise_for_status()

    def dataset_list(self, with_community_datasets=True) -> List[ObjectInfo]:
        """
        Get the public list of all the datasets on huggingface, including the community datasets
        """
        path = "{}/api/datasets".format(self.endpoint)
        r = requests.get(path)
        r.raise_for_status()
        d = r.json()
        datasets = [ObjectInfo(**x) for x in d]
        if not with_community_datasets:
            datasets = [d for d in datasets if "/" not in d.id]
        return datasets

    def metric_list(self, with_community_metrics=True) -> List[ObjectInfo]:
        """
        Get the public list of all the metrics on huggingface, including the community metrics
        """
        path = "{}/api/metrics".format(self.endpoint)
        r = requests.get(path)
        r.raise_for_status()
        d = r.json()
        metrics = [ObjectInfo(**x) for x in d]
        if not with_community_metrics:
            metrics = [m for m in metrics if "/" not in m.id]
        return metrics


class TqdmProgressFileReader:
    """
    Wrap an io.BufferedReader `f` (such as the output of `open(…, "rb")`)
    and override `f.read()` so as to display a tqdm progress bar.

    see github.com/huggingface/transformers/pull/2078#discussion_r354739608
    for implementation details.
    """

    def __init__(self, f: io.BufferedReader):
        self.f = f
        self.total_size = os.fstat(f.fileno()).st_size
        self.pbar = tqdm(total=self.total_size, leave=False)
        self.read = f.read
        f.read = self._read

    def _read(self, n=-1):
        self.pbar.update(n)
        return self.read(n)

    def close(self):
        self.pbar.close()


class HfFolder:
    path_token = expanduser("~/.huggingface/token")

    @classmethod
    def save_token(cls, token):
        """
        Save token, creating folder as needed.
        """
        os.makedirs(os.path.dirname(cls.path_token), exist_ok=True)
        with open(cls.path_token, "w+") as f:
            f.write(token)

    @classmethod
    def get_token(cls):
        """
        Get token or None if not existent.
        """
        try:
            with open(cls.path_token, "r") as f:
                return f.read()
        except FileNotFoundError:
            pass

    @classmethod
    def delete_token(cls):
        """
        Delete token.
        Do not fail if token does not exist.
        """
        try:
            os.remove(cls.path_token)
        except FileNotFoundError:
            pass
