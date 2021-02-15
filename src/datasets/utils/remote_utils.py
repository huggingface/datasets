import copy
import time
from typing import Optional, Union

import pyarrow as pa
import requests

from .. import __version__, config
from .logging import get_logger


logger = get_logger(__name__)


class RemoteManager:
    @staticmethod
    def request_with_retry(
        verb: str, url: str, max_retries: int = 0, base_wait_time: float = 0.5, max_wait_time: float = 2, **kwargs
    ) -> requests.Response:
        """Wrapper around requests to retry in case it fails with a ConnectTimeout, with exponential backoff.

        Args:
            verb (str): HTTP verb, such as 'GET' or 'HEAD'.
            url (str): The URL of the resource to fetch.
            max_retries (int): Maximum number of retries, defaults to 0 (no retries).
            base_wait_time (float): Duration (in seconds) to wait before retrying the first time. Wait time between
                retries then grows exponentially, capped by max_wait_time.
            max_wait_time (float): Maximum amount of time between two retries, in seconds.
            **kwargs: Params to pass to `requests.request`.

        Returns:
            requests.Response
        """
        tries, success = 0, False
        while not success:
            tries += 1
            try:
                response = requests.request(verb.upper(), url, **kwargs)
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
    def http_head(
        cls, url, proxies=None, headers=None, cookies=None, allow_redirects=True, timeout=10, max_retries=0
    ) -> requests.Response:
        """Wrapper around requests HEAD.

        Args:
            url (str): The URL of the resource to fetch.
            proxies:
            headers:
            cookies:
            allow_redirects:
            timeout:
            max_retries:

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

    @staticmethod
    def get_datasets_user_agent(user_agent: Optional[Union[str, dict]] = None) -> str:
        ua = "datasets/{}; python/{}".format(__version__, config.PY_VERSION)
        ua += "; pyarrow/{}".format(pa.__version__)
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
