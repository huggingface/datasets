from typing import Optional
from urllib.parse import quote

import huggingface_hub.file_download

from datasets import config


def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    revision = revision or config.HUB_DEFAULT_VERSION
    huggingface_hub.file_download.HUGGINGFACE_CO_URL_TEMPLATE = config.HUB_DATASETS_URL.replace(
        "/datasets/{repo_id}/resolve/{revision}/{path}", "/{repo_id}/resolve/{revision}/{filename}"
    )
    return huggingface_hub.file_download.hf_hub_url(repo_id, quote(path), repo_type="dataset", revision=revision)
