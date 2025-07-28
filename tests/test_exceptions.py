import warnings

import pytest

import datasets.utils.deprecation_utils
from datasets.exceptions import (
    ChecksumVerificationError,
    ExpectedMoreDownloadedFilesError,
    ExpectedMoreSplitsError,
    NonMatchingChecksumError,
    NonMatchingSplitsSizesError,
    SplitsVerificationError,
    UnexpectedDownloadedFileError,
    UnexpectedSplitsError,
)


@pytest.mark.parametrize(
    "error",
    [
        ChecksumVerificationError,
        UnexpectedDownloadedFileError,
        ExpectedMoreDownloadedFilesError,
        NonMatchingChecksumError,
        SplitsVerificationError,
        UnexpectedSplitsError,
        ExpectedMoreSplitsError,
        NonMatchingSplitsSizesError,
    ],
)
def test_error_not_deprecated(error, monkeypatch):
    monkeypatch.setattr(datasets.utils.deprecation_utils, "_emitted_deprecation_warnings", set())
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        error()
