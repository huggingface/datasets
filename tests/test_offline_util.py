from tempfile import NamedTemporaryFile

import httpx
import pytest
import requests
from huggingface_hub import get_session
from huggingface_hub.errors import OfflineModeIsEnabled

from datasets.utils.file_utils import fsspec_get, fsspec_head

from .utils import (

    IS_HF_HUB_1_x,

    OfflineSimulationMode,
    RequestWouldHangIndefinitelyError,
    offline,
    require_not_windows,
)


@pytest.mark.integration
@require_not_windows  # fsspec get keeps a file handle on windows that raises PermissionError
def test_offline_with_timeout():
    expected_exception = httpx.ReadTimeout if IS_HF_HUB_1_x else requests.ConnectTimeout
    with offline(OfflineSimulationMode.CONNECTION_TIMES_OUT):
        with pytest.raises(RequestWouldHangIndefinitelyError):

            get_session().request("GET", "https://huggingface.co")

        with pytest.raises(expected_exception):
            get_session().request("GET", "https://huggingface.co", timeout=1.0)

        with pytest.raises(expected_exception), NamedTemporaryFile() as temp_file:

            fsspec_get("hf://dummy", temp_file=temp_file)


@pytest.mark.integration
@require_not_windows  # fsspec get keeps a file handle on windows that raises PermissionError
def test_offline_with_connection_error():
    expected_exception = httpx.ConnectError if IS_HF_HUB_1_x else requests.ConnectionError
    with offline(OfflineSimulationMode.CONNECTION_FAILS):

        with pytest.raises(expected_exception):
            get_session().request("GET", "https://huggingface.co")

        with pytest.raises(expected_exception), NamedTemporaryFile() as temp_file:

            fsspec_get("hf://dummy", temp_file=temp_file)


def test_offline_with_datasets_offline_mode_enabled():
    with offline(OfflineSimulationMode.HF_HUB_OFFLINE_SET_TO_1):
        with pytest.raises(OfflineModeIsEnabled):
            fsspec_head("hf://dummy")
        with pytest.raises(OfflineModeIsEnabled), NamedTemporaryFile() as temp_file:
            fsspec_get("hf://dummy", temp_file=temp_file)
