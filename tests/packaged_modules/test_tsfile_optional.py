"""Tests for the TsFile builder that must run without the optional SDK."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from datasets.packaged_modules.tsfile.tsfile import _TSFILE_INSTALL_ERROR, _require_tsfile


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
    assert "datasets[tsfile]" in str(err)
    assert _TSFILE_INSTALL_ERROR in str(err)
    assert err.__cause__ is not None
    assert "tsfile" in str(err.__cause__)
