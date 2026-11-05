import struct

import pytest

from datasets import config
from datasets.packaged_modules.harbor.harbor import Harbor
from datasets.packaged_modules.webdataset import _tenbin
from datasets.utils.file_utils import get_authentication_headers_for_url


def _chunk(nbytes):
    return _tenbin.magic_bytes + struct.pack("@q", nbytes)


def test_tenbin_decode_chunks_rejects_negative_size():
    # 4 chunks whose offsets cycle back to 0 used to loop forever
    buf = _chunk(0) * 3 + _chunk(-64)
    with pytest.raises(ValueError, match="invalid chunk size"):
        _tenbin.decode_chunks(buf)


def test_tenbin_decode_chunks_rejects_size_past_end():
    with pytest.raises(ValueError, match="invalid chunk size"):
        _tenbin.decode_chunks(_chunk(10**6))


def test_tenbin_decode_chunks_valid_roundtrip():
    payload = b"hello"
    buf = _chunk(len(payload)) + payload + b"\0" * (_tenbin.roundup(len(payload)) - len(payload))
    assert _tenbin.decode_chunks(buf) == [payload]


@pytest.mark.parametrize(
    "url",
    [
        "https://huggingface.co.attacker.example/x.csv",
        "https://huggingface.community/x.csv",
        "https://huggingface.com/x.csv",
        "https://example.org/x.csv",
    ],
)
def test_auth_headers_not_sent_to_lookalike_hosts(url):
    assert get_authentication_headers_for_url(url, token="hf_dummy_token") == {}


def test_auth_headers_sent_to_hf_endpoint():
    url = config.HF_ENDPOINT + "/datasets/user/repo/resolve/main/x.csv"
    headers = get_authentication_headers_for_url(url, token="hf_dummy_token")
    assert any(k.lower() == "authorization" for k in headers)


def test_harbor_generate_shards_accepts_gen_kwargs():
    builder = Harbor.__new__(Harbor)
    gen_kwargs = {
        "task_files": ["a/task.toml", "b/task.toml"],
        "instruction_files": [None, None],
        "task_dirs": ["a", "b"],
    }
    assert list(builder._generate_shards(**gen_kwargs)) == ["a/task.toml", "b/task.toml"]


def test_fsspec_http_extra_declared():
    import aiohttp  # noqa: F401  (needed by fsspec's HTTPFileSystem for http(s):// data files)
