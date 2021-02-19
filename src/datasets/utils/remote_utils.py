import copy
import time
from typing import Optional, Union

import requests
from tqdm.auto import tqdm

from .. import __version__, config
from .logging import WARNING, get_logger


logger = get_logger(__name__)


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
    def get(cls, url, proxies=None, resume_size=0, headers=None, cookies=None, max_retries=0, callback=None):
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
            callback (callable, optional): Callback function to be called with each response data chunk.

        Returns:
            generator or type returned by `callback`
        """
        headers = copy.deepcopy(headers) or {}
        headers["user-agent"] = cls.get_datasets_user_agent(user_agent=headers.get("user-agent"))
        if resume_size > 0:
            headers["Range"] = "bytes=%d-" % (resume_size,)
        response = cls.request_with_retry(
            verb="GET",
            url=url,
            stream=True,
            proxies=proxies,
            headers=headers,
            cookies=cookies,
            max_retries=max_retries,
        )
        if response.status_code == 416:  # Range not satisfiable
            return
        if callback:
            content_length = response.headers.get("Content-Length")
            total = resume_size + int(content_length) if content_length is not None else None
            not_verbose = bool(logger.getEffectiveLevel() > WARNING)
            progress = tqdm(
                unit="B",
                unit_scale=True,
                total=total,
                initial=resume_size,
                desc="Downloading",
                disable=not_verbose,
            )
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    progress.update(len(chunk))
                    callback(chunk)
            progress.close()
        else:
            return response.iter_content(chunk_size=1024)

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
