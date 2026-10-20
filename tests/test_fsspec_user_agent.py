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
