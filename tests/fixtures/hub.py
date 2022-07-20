import os.path
import time
from contextlib import contextmanager
from unittest.mock import patch

import pytest
import requests
from huggingface_hub.hf_api import HfApi, HfFolder

from datasets.utils._hf_hub_fixes import create_repo, delete_repo


USER = "__DUMMY_TRANSFORMERS_USER__"
FULL_NAME = "Dummy User"
TOKEN = "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"

ENDPOINT_STAGING = "https://hub-ci.huggingface.co"
ENDPOINT_STAGING_DATASETS_URL = ENDPOINT_STAGING + "/datasets/{repo_id}/resolve/{revision}/{path}"

STAGING_TOKEN_PATH = os.path.expanduser("~/.huggingface/staging_token")


@pytest.fixture
def staging_hub_config(monkeypatch):
    monkeypatch.setattr("datasets.config.HF_ENDPOINT", ENDPOINT_STAGING)
    monkeypatch.setattr("datasets.config.HUB_DATASETS_URL", ENDPOINT_STAGING_DATASETS_URL)


@pytest.fixture
def staging_token_path(monkeypatch):
    monkeypatch.setattr("huggingface_hub.hf_api.HfFolder.path_token", STAGING_TOKEN_PATH)


@pytest.fixture
def set_staging_access_token(staging_hub_config, staging_token_path):
    _api = HfApi(endpoint=ENDPOINT_STAGING)
    _api.set_access_token(TOKEN)
    HfFolder.save_token(TOKEN)
    yield
    HfFolder.delete_token()
    _api.unset_access_token()


@pytest.fixture(scope="session")
def hf_api():
    return HfApi(endpoint=ENDPOINT_STAGING)


@pytest.fixture(scope="session")
def hf_token(hf_api: HfApi):
    hf_api.set_access_token(TOKEN)
    HfFolder.save_token(TOKEN)

    yield TOKEN
    try:
        hf_api.unset_access_token()
    except requests.exceptions.HTTPError:
        pass


@pytest.fixture
def cleanup_repo(hf_api):
    def _cleanup_repo(repo_id):
        organization, name = repo_id.split("/")
        delete_repo(hf_api=hf_api, name=name, organization=organization, token=TOKEN, repo_type="dataset")

    return _cleanup_repo


@pytest.fixture
def temporary_repo(cleanup_repo):
    @contextmanager
    def _temporary_repo(repo_id):
        try:
            yield repo_id
        finally:
            cleanup_repo(repo_id)

    return _temporary_repo


@pytest.fixture(scope="session")
def hf_private_dataset_repo_txt_data_(hf_api: HfApi, hf_token, text_file):
    repo_name = f"repo_txt_data-{int(time.time() * 10e3)}"
    create_repo(hf_api, repo_name, token=hf_token, organization=USER, repo_type="dataset", private=True)
    repo_id = f"{USER}/{repo_name}"
    hf_api.upload_file(
        token=hf_token,
        path_or_fileobj=str(text_file),
        path_in_repo="data/text_data.txt",
        repo_id=repo_id,
        repo_type="dataset",
    )
    yield repo_id
    try:
        delete_repo(hf_api, repo_name, token=hf_token, organization=USER, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_txt_data(hf_private_dataset_repo_txt_data_):
    with patch("datasets.config.HF_ENDPOINT", ENDPOINT_STAGING):
        with patch("datasets.config.HUB_DATASETS_URL", ENDPOINT_STAGING_DATASETS_URL):
            yield hf_private_dataset_repo_txt_data_


@pytest.fixture(scope="session")
def hf_private_dataset_repo_zipped_txt_data_(hf_api: HfApi, hf_token, zip_csv_with_dir_path):
    repo_name = f"repo_zipped_txt_data-{int(time.time() * 10e3)}"
    create_repo(hf_api, repo_name, token=hf_token, organization=USER, repo_type="dataset", private=True)
    repo_id = f"{USER}/{repo_name}"
    hf_api.upload_file(
        token=hf_token,
        path_or_fileobj=str(zip_csv_with_dir_path),
        path_in_repo="data.zip",
        repo_id=repo_id,
        repo_type="dataset",
    )
    yield repo_id
    try:
        delete_repo(hf_api, repo_name, token=hf_token, organization=USER, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_zipped_txt_data(hf_private_dataset_repo_zipped_txt_data_):
    with patch("datasets.config.HF_ENDPOINT", ENDPOINT_STAGING):
        with patch("datasets.config.HUB_DATASETS_URL", ENDPOINT_STAGING_DATASETS_URL):
            yield hf_private_dataset_repo_zipped_txt_data_


@pytest.fixture(scope="session")
def hf_private_dataset_repo_zipped_img_data_(hf_api: HfApi, hf_token, zip_image_path):
    repo_name = f"repo_zipped_img_data-{int(time.time() * 10e3)}"
    create_repo(hf_api, repo_name, token=hf_token, organization=USER, repo_type="dataset", private=True)
    repo_id = f"{USER}/{repo_name}"
    hf_api.upload_file(
        token=hf_token,
        path_or_fileobj=str(zip_image_path),
        path_in_repo="data.zip",
        repo_id=repo_id,
        repo_type="dataset",
    )
    yield repo_id
    try:
        delete_repo(hf_api, repo_name, token=hf_token, organization=USER, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_zipped_img_data(hf_private_dataset_repo_zipped_img_data_):
    with patch("datasets.config.HF_ENDPOINT", ENDPOINT_STAGING):
        with patch("datasets.config.HUB_DATASETS_URL", ENDPOINT_STAGING_DATASETS_URL):
            yield hf_private_dataset_repo_zipped_img_data_
