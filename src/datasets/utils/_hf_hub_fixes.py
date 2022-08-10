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
    """
    The huggingface_hub.HfApi.create_repo parameters changed in 0.5.0 and some of them were deprecated.
    This function checks the huggingface_hub version to call the right parameters.

    Args:
        hf_api (`huggingface_hub.HfApi`): Hub client
        name (`str`): name of the repository (without the namespace)
        token (`str`, *optional*): user or organization token. Defaults to None.
        organization (`str`, *optional*): namespace for the repository: the username or organization name.
            By default it uses the namespace associated to the token used.
        private (`bool`, *optional*):
            Whether the model repo should be private.
        repo_type (`str`, *optional*):
            Set to `"dataset"` or `"space"` if uploading to a dataset or
            space, `None` or `"model"` if uploading to a model. Default is
            `None`.
        exist_ok (`bool`, *optional*, defaults to `False`):
            If `True`, do not raise an error if repo already exists.
        space_sdk (`str`, *optional*):
            Choice of SDK to use if repo_type is "space". Can be
            "streamlit", "gradio", or "static".

    Returns:
        `str`: URL to the newly created repo.
    """
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


def delete_repo(
    hf_api: HfApi,
    name: str,
    token: Optional[str] = None,
    organization: Optional[str] = None,
    repo_type: Optional[str] = None,
) -> str:
    """
    The huggingface_hub.HfApi.delete_repo parameters changed in 0.5.0 and some of them were deprecated.
    This function checks the huggingface_hub version to call the right parameters.

    Args:
        hf_api (`huggingface_hub.HfApi`): Hub client
        name (`str`): name of the repository (without the namespace)
        token (`str`, *optional*): user or organization token. Defaults to None.
        organization (`str`, *optional*): namespace for the repository: the username or organization name.
            By default it uses the namespace associated to the token used.
        repo_type (`str`, *optional*):
            Set to `"dataset"` or `"space"` if uploading to a dataset or
            space, `None` or `"model"` if uploading to a model. Default is
            `None`.

    Returns:
        `str`: URL to the newly created repo.
    """
    if version.parse(huggingface_hub.__version__) < version.parse("0.5.0"):
        return hf_api.delete_repo(
            name=name,
            organization=organization,
            token=token,
            repo_type=repo_type,
        )
    else:  # the `organization` parameter is deprecated in huggingface_hub>=0.5.0
        return hf_api.delete_repo(
            repo_id=f"{organization}/{name}",
            token=token,
            repo_type=repo_type,
        )
