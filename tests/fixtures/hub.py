import time
from contextlib import contextmanager
from pathlib import Path

import pytest
import requests
from huggingface_hub.hf_api import HfApi


CI_HUB_USER = "__DUMMY_TRANSFORMERS_USER__"
CI_HUB_USER_FULL_NAME = "Dummy User"
CI_HUB_USER_TOKEN = "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"

CI_HUB_ENDPOINT = "https://hub-ci.huggingface.co"
CI_HUB_DATASETS_URL = CI_HUB_ENDPOINT + "/datasets/{repo_id}/resolve/{revision}/{path}"
CI_HFH_HUGGINGFACE_CO_URL_TEMPLATE = CI_HUB_ENDPOINT + "/{repo_id}/resolve/{revision}/{filename}"
CI_HUB_TOKEN_PATH = Path("~/.huggingface/hub_ci_token").expanduser()


@pytest.fixture
def ci_hfh_hf_hub_url(monkeypatch):
    monkeypatch.setattr(
        "huggingface_hub.file_download.HUGGINGFACE_CO_URL_TEMPLATE", CI_HFH_HUGGINGFACE_CO_URL_TEMPLATE
    )


@pytest.fixture
def ci_hub_config(monkeypatch):
    monkeypatch.setattr("datasets.config.HF_ENDPOINT", CI_HUB_ENDPOINT)
    monkeypatch.setattr("datasets.config.HUB_DATASETS_URL", CI_HUB_DATASETS_URL)


@pytest.fixture
def ci_hub_token_path(monkeypatch):
    monkeypatch.setattr("huggingface_hub.hf_api.HfFolder.path_token", CI_HUB_TOKEN_PATH)


@pytest.fixture(scope="session")
def hf_api():
    return HfApi(endpoint=CI_HUB_ENDPOINT)


@pytest.fixture(scope="session")
def hf_token():
    yield CI_HUB_USER_TOKEN


@pytest.fixture
def cleanup_repo(hf_api):
    def _cleanup_repo(repo_id):
        hf_api.delete_repo(repo_id, token=CI_HUB_USER_TOKEN, repo_type="dataset")

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
    repo_id = f"{CI_HUB_USER}/{repo_name}"
    hf_api.create_repo(repo_id, token=hf_token, repo_type="dataset", private=True)
    hf_api.upload_file(
        token=hf_token,
        path_or_fileobj=str(text_file),
        path_in_repo="data/text_data.txt",
        repo_id=repo_id,
        repo_type="dataset",
    )
    yield repo_id
    try:
        hf_api.delete_repo(repo_id, token=hf_token, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_txt_data(hf_private_dataset_repo_txt_data_, ci_hub_config, ci_hfh_hf_hub_url):
    return hf_private_dataset_repo_txt_data_


@pytest.fixture(scope="session")
def hf_private_dataset_repo_zipped_txt_data_(hf_api: HfApi, hf_token, zip_csv_with_dir_path):
    repo_name = f"repo_zipped_txt_data-{int(time.time() * 10e3)}"
    repo_id = f"{CI_HUB_USER}/{repo_name}"
    hf_api.create_repo(repo_id, token=hf_token, repo_type="dataset", private=True)
    hf_api.upload_file(
        token=hf_token,
        path_or_fileobj=str(zip_csv_with_dir_path),
        path_in_repo="data.zip",
        repo_id=repo_id,
        repo_type="dataset",
    )
    yield repo_id
    try:
        hf_api.delete_repo(repo_id, token=hf_token, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_zipped_txt_data(
    hf_private_dataset_repo_zipped_txt_data_, ci_hub_config, ci_hfh_hf_hub_url
):
    return hf_private_dataset_repo_zipped_txt_data_


@pytest.fixture(scope="session")
def hf_private_dataset_repo_zipped_img_data_(hf_api: HfApi, hf_token, zip_image_path):
    repo_name = f"repo_zipped_img_data-{int(time.time() * 10e3)}"
    repo_id = f"{CI_HUB_USER}/{repo_name}"
    hf_api.create_repo(repo_id, token=hf_token, repo_type="dataset", private=True)
    hf_api.upload_file(
        token=hf_token,
        path_or_fileobj=str(zip_image_path),
        path_in_repo="data.zip",
        repo_id=repo_id,
        repo_type="dataset",
    )
    yield repo_id
    try:
        hf_api.delete_repo(repo_id, token=hf_token, repo_type="dataset")
    except (requests.exceptions.HTTPError, ValueError):  # catch http error and token invalid error
        pass


@pytest.fixture()
def hf_private_dataset_repo_zipped_img_data(
    hf_private_dataset_repo_zipped_img_data_, ci_hub_config, ci_hfh_hf_hub_url
):
    return hf_private_dataset_repo_zipped_img_data_
