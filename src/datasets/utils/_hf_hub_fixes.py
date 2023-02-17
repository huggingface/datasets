from pathlib import Path
from typing import Any, BinaryIO, List, Optional, Union

import huggingface_hub
from huggingface_hub import HfApi, HfFolder
from huggingface_hub.hf_api import DatasetInfo
from packaging import version

from . import logging


logger = logging.get_logger(__name__)


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


def get_repo_id_from_repo_url(repo_url: Union[str, Any]) -> str:
    """
    In 0.12.0 the output of `huggingface_hub.hf_api.create_repo` change output from `str` containing the
    repo_url, to `RepoUrl` object. This function checks the huggingface_hub version to get the repo_id from
    the repo_url, in the correct way.

    Args:
        repo_url (`str` or `huggingface_hub.hf_api.RepoUrl`): URL to the repo.

    Returns:
        `str`: repo_id, the ID of the repository to push to in the following format: `<user>/<dataset_name>` or
            `<org>/<dataset_name>`.
    """
    if version.parse(huggingface_hub.__version__) < version.parse("0.12.0"):
        from urllib.parse import urlparse

        repo_id = urlparse(repo_url).path[:1]
        return repo_id
    else:
        return repo_url.repo_id


def create_pr_it_does_not_exist(
    hf_api: HfApi,
    repo_id: str,
    token: Optional[str] = None,
    private: Optional[bool] = False,
    repo_type: Optional[str] = "dataset",
    create_pr: Optional[bool] = False,
    branch: Optional[str] = None,
) -> str:
    """
    This function creates a PR for a dataset if it does not exist safely. The RepositoryNotFoundError was introduced in
    huggingface_hub 0.7.0. This function checks the huggingface_hub version to call the right parameters.
    The `create_pr` parameter was introduced in huggingface_hub 0.9.0. This function checks the huggingface_hub version
    to call the right parameters.

    Args:
        hf_api (`huggingface_hub.HfApi`): Hub client
        repo_id (`str`): The ID of the repository to push to in the following format: `<user>/<dataset_name>` or
            `<org>/<dataset_name>`.
        token (`str`, *optional*): user or organization token. Defaults to None.
        private (`bool`, *optional*):
            Whether the model repo should be private.
        repo_type (`str`, *optional*):
            Set to `"dataset"` or `"space"` if uploading to a dataset or
            space, `None` or `"model"` if uploading to a model. Default is
            `None`.
        create_pr (`bool`, *optional*):
            Whether to create a PR if the branch does not exist. Defaults to False.
        branch (`str`, *optional*):
            The branch to create the PR on. Defaults to None.
    """
    # By version huggingface_hub 0.7.0 HTTPError was replaced by RepositoryNotFoundError
    # so we need to check the version to use the right exception
    if version.parse(huggingface_hub.__version__) < version.parse("0.7.0"):
        from requests.exceptions import HTTPError

        repo_not_found_exception = HTTPError
    else:
        from huggingface_hub.hf_api import RepositoryNotFoundError

        repo_not_found_exception = RepositoryNotFoundError

    # Try to find the repo before creating it
    try:
        hf_api.repo_info(repo_id, token=token)

    except repo_not_found_exception:
        repo_url = create_repo(
            hf_api=hf_api, repo_id=repo_id, private=private, token=token, exist_ok=True, repo_type=repo_type
        )
        repo_id = get_repo_id_from_repo_url(repo_url)

    # Try to find PR branch if branch is supplied
    if create_pr and branch is not None:
        if version.parse(huggingface_hub.__version__) < version.parse("0.9.0"):
            raise ValueError(
                "Using `create_pr` requires `huggingface-hub>=0.9.0`. Please use a more recent version of `huggingface-hub`."
            )
        else:
            from huggingface_hub import get_repo_discussions

            for discussion in get_repo_discussions(repo_id, repo_type="dataset"):
                if discussion.is_pull_request and discussion.git_reference == branch:
                    create_pr = False
                    break
            else:
                raise ValueError("Provided branch not found")

    # Create PR if we didn't find it before
    if create_pr:
        from huggingface_hub import create_pull_request

        pr = create_pull_request(
            repo_id,
            repo_type="dataset",
            title=f"Add {repo_id} dataset",
            token=token,
        )
        branch = pr.git_reference
        create_pr = False
        logger.info(f"Created PR {branch} for {repo_id} dataset")


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


def upload_file(
    hf_api: HfApi,
    path_or_fileobj: Union[str, Path, bytes, BinaryIO],
    path_in_repo: str,
    repo_id: str,
    token: Optional[str] = None,
    repo_type: Optional[str] = None,
    revision: Optional[str] = None,
    commit_message: Optional[str] = None,
    commit_description: Optional[str] = None,
    create_pr: Optional[bool] = None,
    parent_commit: Optional[str] = None,
) -> List[str]:
    """
    Several new parameters for huggingface_hub.HfApi.upload_file were introduced in 0.8.1 and some of them were deprecated.
    """
    if create_pr is not None and version.parse(huggingface_hub.__version__) < version.parse("0.8.1"):
        raise TypeError(
            "The `create_pr` parameter is not supported in huggingface_hub<0.8.1. Please update huggingface_hub to >=0.8.1 to use this parameter, or exclude `create_pr` from the keyword arguments."
        )
    else:
        return hf_api.upload_file(
            path_or_fileobj=path_or_fileobj,
            path_in_repo=path_in_repo,
            repo_id=repo_id,
            token=token,
            repo_type=repo_type,
            revision=revision,
            commit_message=commit_message,
            commit_description=commit_description,
            create_pr=create_pr,
            parent_commit=parent_commit,
        )


def get_repo_discussions(
    hf_api: HfApi,
    repo_id: str,
    repo_type: Optional[str] = None,
    token: Optional[str] = None,
) -> Any:
    """
    The method `huggingface_hub.HfApi.get_repo_discussions` was introduced in 0.9.0, this function checks the version before calling it.

    Args:
        hf_api (`huggingface_hub.HfApi`): Hub client
        repo_id (`str`):
            The ID of the repository to push to in the following format: `<user>/<dataset_name>` or
            `<org>/<dataset_name>`. Also accepts `<dataset_name>`, which will default to the namespace
            of the logged-in user.
        repo_type (`str`, *optional*):
            The type of repository to push to. Can be either `dataset` or `model`.
        token (`str`, *optional*):
            The token to use to authenticate to the Hugging Face Hub. If not provided, will use the token
            stored in your `~/.huggingface` folder.
    Returns:
        Iterator[`huggingface_hub.hf_api.Discussion`]: The discussion(s) of the repository.

    Raises:
        TypeError: If the version of huggingface_hub is <0.9.0
    """
    if version.parse(huggingface_hub.__version__) < version.parse("0.9.0"):
        raise TypeError(
            "The method `get_repo_discussions` was introduced in huggingface_hub 0.9.0. Please update huggingface_hub to >=0.9.0 to use this method."
        )
    else:
        return hf_api.get_repo_discussions(
            repo_id=repo_id,
            repo_type=repo_type,
            token=token,
        )
