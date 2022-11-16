from typing import Optional
from urllib.parse import quote

import huggingface_hub as hfh
from packaging import version


def hf_hub_url(repo_id: str, path: str, revision: Optional[str] = None) -> str:
    if version.parse(hfh.__version__).release < version.parse("0.11.0").release:
        # old versions of hfh don't url-encode the file path
        path = quote(path)
    return hfh.hf_hub_url(repo_id, path, repo_type="dataset", revision=revision)
