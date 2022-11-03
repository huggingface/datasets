from typing import Optional
from urllib.parse import quote

import huggingface_hub.file_download

from datasets import config


def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    revision = revision or config.HUB_DEFAULT_VERSION
    return huggingface_hub.file_download.hf_hub_url(repo_id, quote(path), repo_type="dataset", revision=revision)
