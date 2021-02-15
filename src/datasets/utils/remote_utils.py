import time

import requests

from .logging import get_logger


logger = get_logger(__name__)


class RemoteManager:
    @staticmethod
    def request_with_retry(
        verb: str, url: str, max_retries: int = 0, base_wait_time: float = 0.5, max_wait_time: float = 2, **kwargs
    ) -> requests.Response:
        """Wrapper around requests to retry in case it fails with a ConnectTimeout, with exponential backoff

        Args:
            verb (str): HTTP verb, such as 'GET' or 'HEAD'.
            url (str): The URL of the resource to fetch.
            max_retries (int): Maximum number of retries, defaults to 0 (no retries).
            base_wait_time (float): Duration (in seconds) to wait before retrying the first time. Wait time between
                retries then grows exponentially, capped by max_wait_time.
            max_wait_time (float): Maximum amount of time between two retries, in seconds.
            **kwargs: Params to pass to `requests.request`.
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
