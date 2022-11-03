from typing import Optional
from urllib.parse import quote

import huggingface_hub as hfh

from datasets import config


def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    revision = revision or config.HUB_DEFAULT_VERSION
    hfh.constants.HUGGINGFACE_CO_URL_TEMPLATE = config.HUB_DATASETS_URL.replace(
        "/datasets/{repo_id}/resolve/{revision}/{path}", "/{repo_id}/resolve/{revision}/{filename}"
    )
    return hfh.hf_hub_url(repo_id, quote(path), repo_type="dataset", revision=revision)
