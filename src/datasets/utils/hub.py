from functools import partial

from huggingface_hub import HfApi, hf_hub_url
from packaging import version
from requests import HTTPError

from .. import config
from .file_utils import _retry


# `huggingface_hub` in version < 0.20.0 does not retry a failed LFS upload on the "500 (Internal Server Error)" and "504 (Gateway Timeout)" HTTP errors
if config.HF_HUB_VERSION < version.parse("0.20.0"):

    def preupload_lfs_files(hf_api: HfApi, **kwargs):
        _retry(
            hf_api.preupload_lfs_files,
            func_kwargs=kwargs,
            exceptions=HTTPError,
            status_codes=[500, 504],
            max_retries=5,
            base_wait_time=1,
            max_wait_time=8,
        )
else:

    def preupload_lfs_files(hf_api: HfApi, **kwargs):
        hf_api.preupload_lfs_files(**kwargs)


# bakckward compatibility
hf_hub_url = partial(hf_hub_url, repo_type="dataset")
