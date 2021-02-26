import pytest
import requests

from .utils import RequestWouldHangIndefinitlyError, offline


def test_offline_with_timeout():
    with offline(connection_times_out=True):
        with pytest.raises(RequestWouldHangIndefinitlyError):
            requests.request("GET", "https://huggingface.co")
        with pytest.raises(requests.exceptions.ConnectTimeout):
            requests.request("GET", "https://huggingface.co", timeout=1.0)


def test_offline_with_connection_error():
    with offline(connection_times_out=False):
        with pytest.raises(requests.exceptions.ConnectionError):
            requests.request("GET", "https://huggingface.co")
