import time
from functools import partial

from huggingface_hub import HfApi, hf_hub_url
from huggingface_hub.hf_api import RepoFile
from packaging import version
from requests import ConnectionError, HTTPError

from .. import config
from . import logging


logger = logging.get_logger(__name__)

# Retry `preupload_lfs_files` in `huggingface_hub<0.20.0` on the "500 (Internal Server Error)" and "503 (Service Unavailable)" HTTP errors
if config.HF_HUB_VERSION.release < version.parse("0.20.0").release:

    def preupload_lfs_files(hf_api: HfApi, **kwargs):
        max_retries = 5
        base_wait_time = 1
        max_wait_time = 8
        retry = 0
        while True:
            try:
                hf_api.preupload_lfs_files(**kwargs)
            except (RuntimeError, HTTPError, ConnectionError) as err:
                if isinstance(err, RuntimeError):
                    if isinstance(err.__cause__, (HTTPError, ConnectionError)):
                        err = err.__cause__
                    else:
                        raise err
                if retry >= max_retries or err.response and err.response.status_code not in [500, 503]:
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


# `list_files_info` is deprecated in favor of `list_repo_tree` in `huggingface_hub>=0.20.0`
if config.HF_HUB_VERSION.release < version.parse("0.20.0").release:

    def list_files_info(hf_api: HfApi, **kwargs):
        yield from hf_api.list_files_info(**kwargs)
else:

    def list_files_info(hf_api: HfApi, **kwargs):
        kwargs = {**kwargs, "recursive": True}
        for repo_path in hf_api.list_repo_tree(**kwargs):
            if isinstance(repo_path, RepoFile):
                yield repo_path


# bakckward compatibility
hf_hub_url = partial(hf_hub_url, repo_type="dataset")
