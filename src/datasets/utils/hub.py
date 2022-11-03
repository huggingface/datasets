from typing import Optional
from urllib.parse import quote

from datasets import config


def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    revision = revision or config.HUB_DEFAULT_VERSION
    return config.HUB_DATASETS_URL.format(repo_id=repo_id, path=quote(path), revision=quote(revision))
