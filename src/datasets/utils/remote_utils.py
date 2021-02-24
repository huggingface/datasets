import copy
import json
import os
import re
import shutil
import tempfile
import time
import urllib
from contextlib import contextmanager
from functools import partial
from typing import Optional, Union

import requests
from tqdm.auto import tqdm

from .. import __version__, config
from .filelock import FileLock
from .logging import WARNING, get_logger


logger = get_logger(__name__)


class RemoteManager:
    @staticmethod
    def fetch(remote_resource, cache_path, resume_download, cache_dir):
        # Prevent parallel downloads of the same file with a lock.
        lock_path = cache_path + ".lock"
        with FileLock(lock_path):

            if resume_download:
                incomplete_path = cache_path + ".incomplete"

                @contextmanager
                def _resumable_file_manager():
                    with open(incomplete_path, "a+b") as f:
                        yield f

                temp_file_manager = _resumable_file_manager
                if os.path.exists(incomplete_path):
                    resume_size = os.stat(incomplete_path).st_size
                else:
                    resume_size = 0
            else:
                temp_file_manager = partial(tempfile.NamedTemporaryFile, dir=cache_dir, delete=False)
                resume_size = 0

            # Download to temporary file, then copy to cache dir once finished.
            # Otherwise you get corrupt cache entries if the download gets interrupted.
            remote_resource.resume_size = resume_size
            with remote_resource.open() as remote_file, temp_file_manager() as temp_file:
                logger.info(
                    "%s not found in cache or force_download set to True, downloading to %s",
                    remote_resource.url,
                    temp_file.name,
                )
                # GET file object
                remote_file.fetch(temp_file)

            logger.info("storing %s in cache at %s", remote_resource.url, cache_path)
            shutil.move(temp_file.name, cache_path)

            logger.info("creating metadata file for %s", cache_path)
            meta = {"url": remote_resource.url, "etag": remote_resource.etag}
            meta_path = cache_path + ".json"
            with open(meta_path, "w", encoding="utf-8") as meta_file:
                json.dump(meta, meta_file)


class RemoteResource:
    def __new__(cls, url, *args, **kwargs):
        cls = FtpResource if urllib.parse.urlparse(url).scheme == "ftp" else HttpResource
        return super().__new__(cls)

    def __init__(self, url):
        self.url = url
        self.scheme = urllib.parse.urlparse(url).scheme


class FtpResource(RemoteResource):
    def __init__(self, url, timeout=2.0, **kwargs):
        super().__init__(url)
        self.timeout = timeout

    def open(self):
        return FtpFile(self)

    def exists(self):
        return FtpClient.head(self.url)


class HttpResource(RemoteResource):
    def __init__(
        self,
        url,
        cookies=None,
        headers=None,
        max_retries=0,
        proxies=None,
        use_etag=True,
        etag_timeout=10,
        etag=None,
        resume_size=0,
        **kwargs,
    ):
        super().__init__(url)
        self.cookies = cookies
        self.headers = headers
        self.max_retries = max_retries
        self.proxies = proxies
        self.resume_size = resume_size
        self.use_etag = use_etag
        self.etag_timeout = etag_timeout
        self.etag = etag

        self.response = None

    def open(self):
        return HttpFile(self)

    def exists(self):
        connected = False
        try:
            response = HttpClient.head(
                self.url,
                allow_redirects=True,
                proxies=self.proxies,
                timeout=self.etag_timeout,
                max_retries=self.max_retries,
                headers=self.headers,
            )
            self.response = response
            if response.status_code == 200:  # ok
                self.etag = response.headers.get("ETag") if self.use_etag else None
                for k, v in response.cookies.items():
                    # In some edge cases, we need to get a confirmation token
                    if k.startswith("download_warning") and "drive.google.com" in self.url:
                        self.url += "&confirm=" + v
                        self.cookies = response.cookies
                connected = True
            # In some edge cases, head request returns 400 but the connection is actually ok
            elif (
                (response.status_code == 400 and "firebasestorage.googleapis.com" in self.url)
                or (response.status_code == 405 and "drive.google.com" in self.url)
                or (
                    response.status_code == 403
                    and re.match(r"^https?://github.com/.*?/.*?/releases/download/.*?/.*?$", self.url)
                )
            ):
                connected = True
                logger.info("Couldn't get ETag version for url {}".format(self.url))
        except (EnvironmentError, requests.exceptions.Timeout):
            # not connected
            pass
        return connected


class RemoteFile:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class FtpFile(RemoteFile):
    def __init__(self, path):
        super().__init__(path)
        self.file = FtpClient.get(self.path.url, timeout=self.path.timeout)

    def fetch(self, dst_file):
        logger.info(f"Getting through FTP {self.path.url} into {dst_file.name}")
        shutil.copyfileobj(self.file, dst_file)


class HttpFile(RemoteFile):
    def __init__(self, path):
        super().__init__(path)
        self.file = HttpClient.get(
            self.path.url,
            cookies=self.path.cookies,
            headers=self.path.headers,
            max_retries=self.path.max_retries,
            proxies=self.path.proxies,
            resume_size=self.path.resume_size,
        )

    def fetch(self, dst_file):
        if self.file.status_code == 416:  # Range not satisfiable
            return
        content_length = self.file.headers.get("Content-Length")
        total = self.path.resume_size + int(content_length) if content_length is not None else None
        not_verbose = bool(logger.getEffectiveLevel() > WARNING)
        progress = tqdm(
            unit="B",
            unit_scale=True,
            total=total,
            initial=self.path.resume_size,
            desc="Downloading",
            disable=not_verbose,
        )
        logger.info(f"Getting through HTTP {self.path.url} into {dst_file.name}")
        for chunk in self.file.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                progress.update(len(chunk))
                dst_file.write(chunk)
        progress.close()


class HttpClient:
    @staticmethod
    def request_with_retry(
        verb: str, url: str, max_retries: int = 0, base_wait_time: float = 0.5, max_wait_time: float = 2, **params
    ) -> requests.Response:
        """Wrapper around `requests` to retry in case it fails with a ConnectTimeout, with exponential backoff.

        Args:
            verb (str): HTTP verb, such as 'GET' or 'HEAD'.
            url (str): The URL of the resource to fetch.
            max_retries (int): Maximum number of retries, defaults to 0 (no retries).
            base_wait_time (float): Duration (in seconds) to wait before retrying the first time. Wait time between
                retries then grows exponentially, capped by max_wait_time.
            max_wait_time (float): Maximum amount of time between two retries, in seconds.
            **params: Params to pass to `requests.request`.

        Returns:
            requests.Response
        """
        tries, success = 0, False
        while not success:
            tries += 1
            try:
                response = requests.request(verb.upper(), url, **params)
                success = True
            except requests.exceptions.ConnectTimeout as err:
                if tries > max_retries:
                    raise err
                else:
                    logger.info(f"{verb} request to {url} timed out, retrying... [{tries / max_retries}]")
                    sleep_time = max(max_wait_time, base_wait_time * 2 ** (tries - 1))  # Exponential backoff
                    time.sleep(sleep_time)
        return response

    @classmethod
    def head(
        cls, url, proxies=None, headers=None, cookies=None, allow_redirects=True, timeout=10, max_retries=0
    ) -> requests.Response:
        """Wrapper around `requests` HEAD.

        Args:
            url (str): The URL of the resource to fetch.
            proxies (dict): Parameter passed to `requests.request` with the protocol to the URL of the proxy.
            headers (dict, optional): Parameter passed to `requests.request` with the HTTP Headers to be sent with the
                Request.
            cookies (dict, optional): Parameter passed to `requests.request` with the cookies to be sent with the
                Request.
            allow_redirects (bool, default=True): Parameter passed to `requests.request` to enable/disable
                redirections.
            timeout (float, default=10): Parameter passed to `requests.request` to indicate how many seconds to wait
                for the server to send data before giving up.
            max_retries (int, default=0): Maximum number of retries, defaults to 0 (no retries).

        Returns:
            requests.Response
        """
        headers = copy.deepcopy(headers) or {}
        headers["user-agent"] = cls.get_datasets_user_agent(user_agent=headers.get("user-agent"))
        response = cls.request_with_retry(
            verb="HEAD",
            url=url,
            proxies=proxies,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
            timeout=timeout,
            max_retries=max_retries,
        )
        return response

    @classmethod
    def get(cls, url, proxies=None, resume_size=0, headers=None, cookies=None, max_retries=0):
        """Wrapper around `requests` GET.

        Args:
            url (str): The URL of the resource to fetch.
            proxies (dict): Parameter passed to `requests.request` with the protocol to the URL of the proxy.
            resume_size (int): Part of the resource to be returned, passed to Range HTTP request Header as bytes range
                start.
            headers (dict, optional): Parameter passed to `requests.request` with the HTTP Headers to be sent with the
                Request.
            cookies (dict, optional): Parameter passed to `requests.request` with the cookies to be sent with the
                Request.
            max_retries (int, default=0): Maximum number of retries, defaults to 0 (no retries).

        Returns:
            requests.Response
        """
        headers = copy.deepcopy(headers) or {}
        headers["user-agent"] = cls.get_datasets_user_agent(user_agent=headers.get("user-agent"))
        if resume_size > 0:
            headers["Range"] = "bytes=%d-" % (resume_size,)
        return cls.request_with_retry(
            verb="GET",
            url=url,
            stream=True,
            proxies=proxies,
            headers=headers,
            cookies=cookies,
            max_retries=max_retries,
        )

    @staticmethod
    def get_datasets_user_agent(user_agent: Optional[Union[str, dict]] = None) -> str:
        ua = "datasets/{}; python/{}".format(__version__, config.PY_VERSION)
        ua += "; pyarrow/{}".format(config.PYARROW_VERSION)
        if config.TORCH_AVAILABLE:
            ua += "; torch/{}".format(config.TORCH_VERSION)
        if config.TF_AVAILABLE:
            ua += "; tensorflow/{}".format(config.TF_VERSION)
        if config.BEAM_AVAILABLE:
            ua += "; apache_beam/{}".format(config.BEAM_VERSION)
        if isinstance(user_agent, dict):
            ua += "; " + "; ".join("{}/{}".format(k, v) for k, v in user_agent.items())
        elif isinstance(user_agent, str):
            ua += "; " + user_agent
        return ua


class FtpClient:
    @staticmethod
    def head(url, timeout=2.0):
        """Wrapper around `urllib.request` to get the first byte of a remote resource.

        Args:
            url (str): The URL of the resource to fetch.
            timeout (float): Parameter passed to `urllib.request.urlopen` to indicate timeout seconds for blocking
                operations like the connection attempt.

        Returns:
            bytes
        """
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                r.read(1)
        except Exception:
            return False
        return True

    @staticmethod
    def get(url, timeout=2.0):
        """Wrapper around `urllib.request` to get a remote resource.

        Args:
            url (str): The URL of the resource to fetch.
            timeout (float): Parameter passed to `urllib.request.urlopen` to indicate timeout seconds for blocking
                operations like the connection attempt.

        Returns:
            urllib.response.addinfourl
        """
        try:
            return urllib.request.urlopen(url, timeout=timeout)
        except urllib.error.URLError as e:
            raise ConnectionError(e)
