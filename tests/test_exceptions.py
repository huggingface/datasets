import warnings

import pytest

import datasets.utils.deprecation_utils
from datasets.exceptions import (
    ChecksumVerificationError,
    DatasetGenerationCastError,
    ExpectedMoreDownloadedFilesError,
    ExpectedMoreSplitsError,
    NonMatchingChecksumError,
    NonMatchingSplitsSizesError,
    SplitsVerificationError,
    UnexpectedDownloadedFileError,
    UnexpectedSplitsError,
)
from datasets.table import CastError


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


def test_dataset_generation_cast_error_suggests_headerless_csv_options():
    cast_error = CastError(
        "columns do not match",
        table_column_names=["first row value", "another first row value"],
        requested_column_names=["text", "translation"],
    )

    error = DatasetGenerationCastError.from_cast_error(
        cast_error=cast_error, builder_name="csv", gen_kwargs={}, token=None
    )

    assert "All the data files must have the same columns" in str(error)
    assert "headerless CSV/TSV" in str(error)
    assert "`header=None`" in str(error)
    assert "`column_names`" in str(error)
