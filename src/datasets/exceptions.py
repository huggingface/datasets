# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The HuggingFace Authors.


class DatasetsError(Exception):
    """Base class for exceptions in this library."""

    pass


class DefunctDatasetError(DatasetsError):
    """The dataset has been defunct."""

    pass
