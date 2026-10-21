from datasets.download.download_config import DownloadConfig
from datasets.utils.file_utils import (
    _prepare_single_hop_path_and_storage_options,
    get_datasets_user_agent,
)


def test_http_user_agent_is_forwarded():
    config = DownloadConfig(user_agent="my-application/1.0")

    _, options = _prepare_single_hop_path_and_storage_options(
        "https://example.com/data.jsonl",
        config,
    )

    assert options["https"]["headers"]["user-agent"] == (get_datasets_user_agent(config.user_agent))


def test_explicit_user_agent_header_takes_precedence():
    config = DownloadConfig(
        user_agent="my-application/1.0",
        storage_options={
            "https": {
                "headers": {"user-agent": "custom-agent/2.0"},
            }
        },
    )

    _, options = _prepare_single_hop_path_and_storage_options(
        "https://example.com/data.jsonl",
        config,
    )

    assert options["https"]["headers"]["user-agent"] == "custom-agent/2.0"


def test_existing_headers_are_preserved():
    config = DownloadConfig(
        user_agent="my-application/1.0",
        storage_options={
            "https": {
                "headers": {"Authorization": "Bearer test-token"},
            }
        },
    )

    _, options = _prepare_single_hop_path_and_storage_options(
        "https://example.com/data.jsonl", config
    )

    headers = options["https"]["headers"]
    assert headers["Authorization"] == "Bearer test-token"
    assert headers["user-agent"] == get_datasets_user_agent(config.user_agent)


def test_user_agent_header_is_case_insensitive():
    config = DownloadConfig(
        user_agent="my-application/1.0",
        storage_options={
            "https": {
                "headers": {"User-Agent": "explicit-agent/2.0"},
            }
        },
    )

    _, options = _prepare_single_hop_path_and_storage_options(
        "https://example.com/data.jsonl", config
    )

    assert options["https"]["headers"] == {"User-Agent": "explicit-agent/2.0"}


def test_no_custom_user_agent_does_not_add_headers():
    config = DownloadConfig(user_agent=None)

    _, options = _prepare_single_hop_path_and_storage_options(
        "https://example.com/data.jsonl", config
    )

    assert "headers" not in options["https"]
