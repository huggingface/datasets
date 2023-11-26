# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The HuggingFace Authors.


class DatasetsError(Exception):
    """Base class for exceptions in this library."""


class DefunctDatasetError(DatasetsError):
    """The dataset has been defunct."""


class FileNotFoundDatasetsError(DatasetsError, FileNotFoundError):
    """FileNotFoundError raised by this library."""


class DataFilesNotFoundError(FileNotFoundDatasetsError):
    """No (supported) data files found."""


class DatasetNotFoundError(FileNotFoundDatasetsError):
    """Dataset not found.

    Raised when trying to access:
    - a missing dataset, or
    - a private/gated dataset and the user is not authenticated.
    """
