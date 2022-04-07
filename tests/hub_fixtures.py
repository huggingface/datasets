import time
from unittest.mock import patch

import pytest
import requests
from huggingface_hub.hf_api import HfApi


USER = "__DUMMY_TRANSFORMERS_USER__"
FULL_NAME = "Dummy User"
PASS = "__DUMMY_TRANSFORMERS_PASS__"

ENDPOINT_STAGING = "https://moon-staging.huggingface.co"
ENDPOINT_STAGING_DATASETS_URL = ENDPOINT_STAGING + "/datasets/{path}/resolve/{revision}/{name}"


@pytest.fixture(scope="session")
def hf_api():
    return HfApi(endpoint=ENDPOINT_STAGING)


@pytest.fixture(scope="session")
def hf_token(hf_api: HfApi):
    hf_token = hf_api.login(username=USER, password=PASS)
    yield hf_token
    try:
        hf_api.logout(hf_token)
    except requests.exceptions.HTTPError:
        pass


@pytest.fixture(scope="session")
def hf_private_dataset_repo_txt_data_(hf_api: HfApi, hf_token, text_file):
    repo_name = f"repo_txt_data-{int(time.time() * 10e3)}"
    hf_api.create_repo(token=hf_token, name=repo_name, repo_type="dataset", private=True)
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
        hf_api.delete_repo(token=hf_token, name=repo_name, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_txt_data(hf_private_dataset_repo_txt_data_):
    with patch("datasets.config.HF_ENDPOINT", ENDPOINT_STAGING):
        with patch("datasets.config.HUB_DATASETS_URL", ENDPOINT_STAGING_DATASETS_URL):
            yield hf_private_dataset_repo_txt_data_


@pytest.fixture(scope="session")
def hf_private_dataset_repo_zipped_txt_data_(hf_api: HfApi, hf_token, zip_csv_path):
    repo_name = f"repo_zipped_txt_data-{int(time.time() * 10e3)}"
    hf_api.create_repo(token=hf_token, name=repo_name, repo_type="dataset", private=True)
    repo_id = f"{USER}/{repo_name}"
    hf_api.upload_file(
        token=hf_token,
        path_or_fileobj=str(zip_csv_path),
        path_in_repo="data.zip",
        repo_id=repo_id,
        repo_type="dataset",
    )
    yield repo_id
    try:
        hf_api.delete_repo(token=hf_token, name=repo_name, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_zipped_txt_data(hf_private_dataset_repo_zipped_txt_data_):
    with patch("datasets.config.HF_ENDPOINT", ENDPOINT_STAGING):
        with patch("datasets.config.HUB_DATASETS_URL", ENDPOINT_STAGING_DATASETS_URL):
            yield hf_private_dataset_repo_zipped_txt_data_
