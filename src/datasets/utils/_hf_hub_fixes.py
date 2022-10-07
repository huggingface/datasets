from typing import List, Optional, Union

import huggingface_hub
from huggingface_hub import HfApi, HfFolder
from huggingface_hub.hf_api import DatasetInfo
from packaging import version


def create_repo(
    hf_api: HfApi,
    repo_id: str,
    token: Optional[str] = None,
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
        repo_id (`str`): A namespace (user or an organization) and a repo name separated by a `/`.
        token (`str`, *optional*): user or organization token. Defaults to None.
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
        organization, name = repo_id.split("/")
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
            repo_id=repo_id,
            token=token,
            private=private,
            repo_type=repo_type,
            exist_ok=exist_ok,
            space_sdk=space_sdk,
        )


def delete_repo(
    hf_api: HfApi,
    repo_id: str,
    token: Optional[str] = None,
    repo_type: Optional[str] = None,
) -> str:
    """
    The huggingface_hub.HfApi.delete_repo parameters changed in 0.5.0 and some of them were deprecated.
    This function checks the huggingface_hub version to call the right parameters.

    Args:
        hf_api (`huggingface_hub.HfApi`): Hub client
        repo_id (`str`): A namespace (user or an organization) and a repo name separated by a `/`.
        token (`str`, *optional*): user or organization token. Defaults to None.
        repo_type (`str`, *optional*):
            Set to `"dataset"` or `"space"` if uploading to a dataset or
            space, `None` or `"model"` if uploading to a model. Default is
            `None`.

    Returns:
        `str`: URL to the newly created repo.
    """
    if version.parse(huggingface_hub.__version__) < version.parse("0.5.0"):
        organization, name = repo_id.split("/")
        return hf_api.delete_repo(
            name=name,
            organization=organization,
            token=token,
            repo_type=repo_type,
        )
    else:  # the `organization` parameter is deprecated in huggingface_hub>=0.5.0
        return hf_api.delete_repo(
            repo_id=repo_id,
            token=token,
            repo_type=repo_type,
        )


def dataset_info(
    hf_api: HfApi,
    repo_id: str,
    *,
    revision: Optional[str] = None,
    timeout: Optional[float] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
) -> DatasetInfo:
    """
    The huggingface_hub.HfApi.dataset_info parameters changed in 0.10.0 and some of them were deprecated.
    This function checks the huggingface_hub version to call the right parameters.

    Args:
        hf_api (`huggingface_hub.HfApi`): Hub client
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated
            by a `/`.
        revision (`str`, *optional*):
            The revision of the dataset repository from which to get the
            information.
        timeout (`float`, *optional*):
            Whether to set a timeout for the request to the Hub.
        use_auth_token (`bool` or `str`, *optional*):
            Whether to use the `auth_token` provided from the
            `huggingface_hub` cli. If not logged in, a valid `auth_token`
            can be passed in as a string.
    Returns:
        [`hf_api.DatasetInfo`]: The dataset repository information.
    <Tip>
    Raises the following errors:
        - [`~utils.RepositoryNotFoundError`]
            If the repository to download from cannot be found. This may be because it doesn't exist,
            or because it is set to `private` and you do not have access.
        - [`~utils.RevisionNotFoundError`]
            If the revision to download from cannot be found.
    </Tip>
    """
    if version.parse(huggingface_hub.__version__) < version.parse("0.10.0"):
        if use_auth_token is False:
            token = "no-token"
        elif isinstance(use_auth_token, str):
            token = use_auth_token
        else:
            token = HfFolder.get_token() or "no-token"
        return hf_api.dataset_info(
            repo_id,
            revision=revision,
            token=token,
            timeout=timeout,
        )
    else:  # the `token` parameter is deprecated in huggingface_hub>=0.10.0
        return hf_api.dataset_info(repo_id, revision=revision, timeout=timeout, use_auth_token=use_auth_token)


def list_repo_files(
    hf_api: HfApi,
    repo_id: str,
    revision: Optional[str] = None,
    repo_type: Optional[str] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    timeout: Optional[float] = None,
) -> List[str]:
    """
    The huggingface_hub.HfApi.list_repo_files parameters changed in 0.10.0 and some of them were deprecated.
    This function checks the huggingface_hub version to call the right parameters.
    """
    if version.parse(huggingface_hub.__version__) < version.parse("0.10.0"):
        return hf_api.list_repo_files(
            repo_id, revision=revision, repo_type=repo_type, token=use_auth_token, timeout=timeout
        )
    else:  # the `token` parameter is deprecated in huggingface_hub>=0.10.0
        return hf_api.list_repo_files(
            repo_id, revision=revision, repo_type=repo_type, use_auth_token=use_auth_token, timeout=timeout
        )
