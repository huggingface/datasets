from typing import Optional

import huggingface_hub
from huggingface_hub import HfApi
from packaging import version


def create_repo(
    hf_api: HfApi,
    name: str,
    token: Optional[str] = None,
    organization: Optional[str] = None,
    private: Optional[bool] = None,
    repo_type: Optional[str] = None,
    exist_ok: Optional[bool] = False,
    space_sdk: Optional[str] = None,
) -> str:
    if version.parse(huggingface_hub.__version__) < version.parse("0.5.0"):
        return hf_api.create_repo(
            name=name,
            organization=organization,
            token=token,
            private=private,
            repo_type=repo_type,
            exist_ok=exist_ok,
            space_sdk=space_sdk,
        )
    else:  # the `organization` parameter is deprecated in huggingface_hub>=0.5.0
        return hf_api.create_repo(
            repo_id=f"{organization}/{name}",
            token=token,
            private=private,
            repo_type=repo_type,
            exist_ok=exist_ok,
            space_sdk=space_sdk,
        )
