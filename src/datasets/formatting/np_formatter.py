import sys

import numpy as np
import pyarrow as pa

from .. import config
from ..utils.py_utils import map_nested
from .formatting import Formatter


class NumpyFormatter(Formatter[dict, np.ndarray, dict]):
    def __init__(self, features=None, decoded=True, **np_array_kwargs):
        super().__init__(features=features, decoded=decoded)
        self.np_array_kwargs = np_array_kwargs

    def _consolidate(self, column):
        if isinstance(column, list):
            if column and all(
                isinstance(x, np.ndarray) and x.shape == column[0].shape and x.dtype == column[0].dtype for x in column
            ):
                return np.stack(column)
            else:
                # don't use np.array(column, dtype=object)
                # since it fails in certain cases
                # see https://stackoverflow.com/q/51005699
                out = np.empty(len(column), dtype=object)
                out[:] = column
                return out
        return column

    def _tensorize(self, value):

        if isinstance(value, (str, bytes, type(None))):
            return value
        elif isinstance(value, (np.character, np.ndarray)) and np.issubdtype(value.dtype, np.character):
            return value
        elif isinstance(value, np.number):
            return value

        default_dtype = {}

        if isinstance(value, np.ndarray) and np.issubdtype(value.dtype, np.integer):
            default_dtype = {"dtype": np.int64}
        elif isinstance(value, np.ndarray) and np.issubdtype(value.dtype, np.floating):
            default_dtype = {"dtype": np.float32}
        elif config.PIL_AVAILABLE and "PIL" in sys.modules:
            import PIL.Image

            if isinstance(value, PIL.Image.Image):
                return np.asarray(value, **self.np_array_kwargs)

        return np.array(value, **{**default_dtype, **self.np_array_kwargs})

    def _recursive_tensorize(self, data_struct: dict):
        # support for nested types like struct of list of struct
        if isinstance(data_struct, np.ndarray):
            if data_struct.dtype == object:  # torch tensors cannot be instantied from an array of objects
                return self._consolidate([self.recursive_tensorize(substruct) for substruct in data_struct])
        return self._tensorize(data_struct)

    def recursive_tensorize(self, data_struct: dict):
        return map_nested(self._recursive_tensorize, data_struct)

    def format_row(self, pa_table: pa.Table) -> dict:
        row = self.numpy_arrow_extractor().extract_row(pa_table)
        if self.decoded:
            row = self.python_features_decoder.decode_row(row)
        return self.recursive_tensorize(row)

    def format_column(self, pa_table: pa.Table) -> np.ndarray:
        column = self.numpy_arrow_extractor().extract_column(pa_table)
        if self.decoded:
            column = self.python_features_decoder.decode_column(column, pa_table.column_names[0])
        column = self.recursive_tensorize(column)
        column = self._consolidate(column)
        return column

    def format_batch(self, pa_table: pa.Table) -> dict:
        batch = self.numpy_arrow_extractor().extract_batch(pa_table)
        if self.decoded:
            batch = self.python_features_decoder.decode_batch(batch)
        batch = self.recursive_tensorize(batch)
        for column_name in batch:
            batch[column_name] = self._consolidate(batch[column_name])
        return batch
