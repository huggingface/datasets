from typing import Optional
from urllib.parse import quote

import huggingface_hub as hfh


def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    return hfh.hf_hub_url(repo_id, quote(path), repo_type="dataset", revision=revision)
