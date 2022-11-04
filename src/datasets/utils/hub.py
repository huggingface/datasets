from typing import Optional
from urllib.parse import quote

import huggingface_hub as hfh

from datasets import config


def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    revision = revision or config.HUB_DEFAULT_VERSION
    return hfh.hf_hub_url(repo_id, quote(path), repo_type="dataset", revision=revision)
