# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import io
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


tsfile = pytest.importorskip("tsfile")

from datasets import load_dataset  # noqa: E402
from datasets.packaged_modules.tsfile import tsfile as tsfile_module  # noqa: E402
from tests.packaged_modules.test_tsfile import _write_multi_device  # noqa: E402


@pytest.fixture
def http_tsfile(tmp_path):
    path = tmp_path / "data.tsfile"
    _write_multi_device(str(path))
    payload = path.read_bytes()
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.respond(send_body=False)

        def do_GET(self):
            self.respond(send_body=True)

        def respond(self, send_body):
            start, end = 0, len(payload) - 1
            range_header = self.headers.get("Range")
            if range_header:
                interval = range_header.removeprefix("bytes=")
                first, last = interval.split("-", 1)
                start = int(first) if first else max(0, len(payload) - int(last))
                if first and last:
                    end = min(int(last), end)
            if start > end:
                self.send_error(416)
                return
            status = 206 if range_header else 200
            requests.append((self.command, range_header, status, end - start + 1))
            self.send_response(status)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(end - start + 1))
            if range_header:
                self.send_header("Content-Range", f"bytes {start}-{end}/{len(payload)}")
            self.end_headers()
            if send_body:
                self.wfile.write(payload[start : end + 1])

        def log_message(self, *args):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield path, f"http://127.0.0.1:{server.server_port}/data.tsfile", requests
        finally:
            server.shutdown()
            thread.join()


@pytest.mark.parametrize("stop_early", [False, True])
def test_http_streaming_matches_local_and_closes_sources(http_tsfile, monkeypatch, stop_early):
    path, url, requests = http_tsfile
    expected = list(load_dataset("tsfile", data_files=str(path), split="train", streaming=True))
    sources = []
    original_reader = tsfile.TsFileReader

    def open_reader(source):
        # A remote URL must never reach the native local-path reader.
        assert not isinstance(source, (str, bytes, os.PathLike))
        sources.append(source)
        return original_reader(source)

    monkeypatch.setattr(tsfile, "TsFileReader", open_reader)
    ds = load_dataset(
        "tsfile",
        data_files=url,
        split="train",
        streaming=True,
        storage_options={"http": {"block_size": 64}},
    )
    iterator = iter(ds)
    try:
        actual = [next(iterator)] if stop_early else list(iterator)
    finally:
        iterator.close()

    assert actual == (expected[:1] if stop_early else expected)
    assert sources and all(source.closed for source in sources)
    assert any(
        method == "GET" and range_header and status == 206 and size < path.stat().st_size
        for method, range_header, status, size in requests
    )


def test_remote_reader_closes_source_on_bad_magic(monkeypatch):
    source = io.BytesIO(b"not a TsFile")
    monkeypatch.setattr(tsfile_module, "open", lambda *args: source, raising=False)
    with pytest.raises(ValueError, match="bad magic header"):
        with tsfile_module.TsFile._open_reader("https://example.com/bad.tsfile"):
            pytest.fail("An invalid file must not be opened")
    assert source.closed


def test_remote_reader_closes_source_on_reader_error(monkeypatch):
    source = io.BytesIO(b"TsFile")
    monkeypatch.setattr(tsfile_module, "open", lambda *args: source, raising=False)

    def fail_reader(source):
        raise RuntimeError("Cannot construct reader")

    monkeypatch.setattr(tsfile, "TsFileReader", fail_reader)
    with pytest.raises(RuntimeError, match="Cannot construct reader"):
        with tsfile_module.TsFile._open_reader("https://example.com/bad.tsfile"):
            pytest.fail("Reader construction must fail")
    assert source.closed
