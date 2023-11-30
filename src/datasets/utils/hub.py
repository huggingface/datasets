import time
from functools import partial

from huggingface_hub import HfApi, hf_hub_url
from packaging import version
from requests import HTTPError

from .. import config
from . import logging


logger = logging.get_logger(__name__)

# Retry `preupload_lfs_files` in `huggingface_hub<0.20.0` on the "500 (Internal Server Error)" and "503 (Service Unavailable)" HTTP errors
if config.HF_HUB_VERSION < version.parse("0.20.0"):

    def preupload_lfs_files(hf_api: HfApi, **kwargs):
        max_retries = 5
        base_wait_time = 1
        max_wait_time = 8
        status_codes = [500, 503]
        retry = 0
        while True:
            try:
                hf_api.preupload_lfs_files(**kwargs)
            except (RuntimeError, HTTPError) as err:
                if isinstance(err, RuntimeError) and isinstance(err.__cause__, HTTPError):
                    err = err.__cause__
                if retry >= max_retries or err.response.status_code not in status_codes:
                    raise err
                else:
                    sleep_time = min(max_wait_time, base_wait_time * 2**retry)  # Exponential backoff
                    logger.info(
                        f"{hf_api.preupload_lfs_files} timed out, retrying in {sleep_time}s... [{retry/max_retries}]"
                    )
                    time.sleep(sleep_time)
                    retry += 1
            else:
                break
else:

    def preupload_lfs_files(hf_api: HfApi, **kwargs):
        hf_api.preupload_lfs_files(**kwargs)


# bakckward compatibility
hf_hub_url = partial(hf_hub_url, repo_type="dataset")
