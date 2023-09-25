import pytest
import requests

from datasets.utils.file_utils import http_head

from .utils import OfflineSimulationMode, RequestWouldHangIndefinitelyError, offline


@pytest.mark.integration
def test_offline_with_timeout():
    with offline(OfflineSimulationMode.CONNECTION_TIMES_OUT):
        with pytest.raises(RequestWouldHangIndefinitelyError):
            requests.request("GET", "https://huggingface.co")
        with pytest.raises(requests.exceptions.ConnectTimeout):
            requests.request("GET", "https://huggingface.co", timeout=1.0)


@pytest.mark.integration
def test_offline_with_connection_error():
    with offline(OfflineSimulationMode.CONNECTION_FAILS):
        with pytest.raises(requests.exceptions.ConnectionError):
            requests.request("GET", "https://huggingface.co")


def test_offline_with_datasets_offline_mode_enabled():
    with offline(OfflineSimulationMode.HF_DATASETS_OFFLINE_SET_TO_1):
        with pytest.raises(ConnectionError):
            http_head("https://huggingface.co")
