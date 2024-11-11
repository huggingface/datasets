from tempfile import NamedTemporaryFile

import huggingface_hub
import pytest
import requests
from packaging import version

from datasets.utils.file_utils import fsspec_get, fsspec_head

from .utils import OfflineSimulationMode, RequestWouldHangIndefinitelyError, offline, require_not_windows


@pytest.mark.integration
@require_not_windows  # fsspec get keeps a file handle on windows that raises PermissionError
def test_offline_with_timeout():
    with offline(OfflineSimulationMode.CONNECTION_TIMES_OUT):
        with pytest.raises(RequestWouldHangIndefinitelyError):
            requests.request("GET", "https://huggingface.co")
        with pytest.raises(requests.exceptions.Timeout):
            requests.request("GET", "https://huggingface.co", timeout=1.0)
        # old versions of `huggingface_hub` don't have timeouts by default and don't allow to set timeouts in HfFileSystem
        if version.parse(huggingface_hub.__version__) >= version.parse("0.23.0"):
            with pytest.raises(requests.exceptions.Timeout), NamedTemporaryFile() as temp_file:
                fsspec_get("hf://dummy", temp_file=temp_file)


@pytest.mark.integration
@require_not_windows  # fsspec get keeps a file handle on windows that raises PermissionError
def test_offline_with_connection_error():
    with offline(OfflineSimulationMode.CONNECTION_FAILS):
        with pytest.raises(requests.exceptions.ConnectionError):
            requests.request("GET", "https://huggingface.co")
        with pytest.raises(requests.exceptions.ConnectionError), NamedTemporaryFile() as temp_file:
            fsspec_get("hf://dummy", temp_file=temp_file)


def test_offline_with_datasets_offline_mode_enabled():
    with offline(OfflineSimulationMode.HF_HUB_OFFLINE_SET_TO_1):
        with pytest.raises(ConnectionError):
            fsspec_head("hf://dummy")
        with pytest.raises(ConnectionError), NamedTemporaryFile() as temp_file:
            fsspec_get("hf://dummy", temp_file=temp_file)
