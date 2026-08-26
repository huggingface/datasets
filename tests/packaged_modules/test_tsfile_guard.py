"""Tests for the TsFile optional-SDK guard (must run without the SDK)."""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest

from datasets.packaged_modules.tsfile.tsfile import _require_tsfile, _tsfile_install_message


def test_install_message_is_version_aware(monkeypatch):
    monkeypatch.setattr(sys, "version_info", (3, 12, 0, "final", 0))
    msg = _tsfile_install_message()
    assert "cannot be installed alongside" in msg
    assert "without installing anything" in msg

    monkeypatch.setattr(sys, "version_info", (3, 14, 0, "final", 0))
    msg = _tsfile_install_message()
    assert "datasets[tsfile]" in msg
    assert "cannot be installed" not in msg


def test_require_tsfile_missing_sdk_raises_actionable_import_error():
    real_import = __import__

    def blocked(name, *args, **kwargs):
        if name == "tsfile" or (isinstance(name, str) and name.startswith("tsfile.")):
            raise ImportError("No module named 'tsfile'")
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=blocked):
        with pytest.raises(ImportError) as ei:
            _require_tsfile()

    err = ei.value
    assert type(err) is ImportError
    assert "Apache TsFile" in str(err)
    assert err.__cause__ is not None
    assert "tsfile" in str(err.__cause__)
