from typing import Optional
from urllib.parse import quote

import huggingface_hub.file_download

from .. import config
from .py_utils import temporary_assignment


@temporary_assignment(
    huggingface_hub.file_download,
    "HUGGINGFACE_CO_URL_TEMPLATE",
    config.HUB_DATASETS_URL.replace("{path}", "{filename}"),
)
def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    revision = revision or config.HUB_DEFAULT_VERSION
    # As config.HUB_DATASETS_URL contains "/datasets/", no need to pass repo_type="dataset"
    return huggingface_hub.file_download.hf_hub_url(repo_id, quote(path), revision=revision)
