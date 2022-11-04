from typing import Optional
from urllib.parse import quote

import huggingface_hub as hfh

from .. import config
from .py_utils import temporary_assignment


@temporary_assignment(
    hfh.constants, "HUGGINGFACE_CO_URL_TEMPLATE", config.HUB_DATASETS_URL.replace("{path}", "{filename}")
)
def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    revision = revision or config.HUB_DEFAULT_VERSION
    return hfh.hf_hub_url(repo_id, quote(path), repo_type="dataset", revision=revision)
