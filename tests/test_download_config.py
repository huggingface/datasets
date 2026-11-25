import datasets.config
from datasets.download.download_config import DownloadConfig
from datasets.utils.file_utils import _prepare_single_hop_path_and_storage_options


def test_download_config_preserves_hf_token_in_storage_options():
    user_storage_options = {"hf": {"token": "hf_secret_token", "endpoint": "https://mirror.example.org"}}
    config = DownloadConfig(storage_options=user_storage_options)

    assert config.token == "hf_secret_token"
    assert config.storage_options["hf"]["token"] == "hf_secret_token"
    assert config.storage_options["hf"]["endpoint"] == "https://mirror.example.org"

    _, prepared_storage_options = _prepare_single_hop_path_and_storage_options(
        "hf://datasets/org/private/train.parquet", config
    )
    assert prepared_storage_options == {"hf": {"endpoint": "https://mirror.example.org", "token": "hf_secret_token"}}


def test_download_config_preserves_false_hf_token_in_storage_options():
    config = DownloadConfig(storage_options={"hf": {"token": False}})

    assert config.token is False
    assert config.storage_options["hf"]["token"] is False


def test_download_config_explicit_token_overrides_storage_options_without_mutating_caller():
    user_storage_options = {"hf": {"token": "hf_old_token", "on_error": "omit"}}
    config = DownloadConfig(token="hf_explicit_token", storage_options=user_storage_options)

    assert config.token == "hf_explicit_token"
    assert config.storage_options["hf"] == {"token": "hf_explicit_token", "on_error": "omit"}
    assert user_storage_options == {"hf": {"token": "hf_old_token", "on_error": "omit"}}


def test_download_config_does_not_mutate_non_hf_caller_storage_options():
    user_storage_options = {"key": "aws_key", "secret": "aws_secret"}
    config = DownloadConfig(storage_options=user_storage_options)

    assert user_storage_options == {"key": "aws_key", "secret": "aws_secret"}
    assert config.storage_options["key"] == "aws_key"
    assert config.storage_options["secret"] == "aws_secret"
    assert config.storage_options["hf"] == {"endpoint": datasets.config.HF_ENDPOINT, "token": None}


def test_download_config_setattr_and_copy():
    config = DownloadConfig(storage_options={"hf": {"token": "hf_initial"}})
    copied = config.copy()

    config.token = None
    assert config.token is None
    assert config.storage_options["hf"]["token"] is None
    assert copied.token == "hf_initial"
    assert copied.storage_options["hf"]["token"] == "hf_initial"
