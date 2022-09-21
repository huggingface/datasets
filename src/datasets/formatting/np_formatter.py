from .formatting import Formatter
import numpy as np
import pyarrow as pa
from .. import config
import sys
from ..utils.py_utils import map_nested


class NumpyFormatter(Formatter[dict, np.ndarray, dict]):
    def __init__(self, features=None, decoded=True, **np_array_kwargs):
        super().__init__(features=features, decoded=decoded)
        self.np_array_kwargs = np_array_kwargs

    def _tensorize(self, value):
        if config.PIL_AVAILABLE and "PIL" in sys.modules:
            import PIL.Image

            if isinstance(value, PIL.Image.Image):
                return np.asarray(value)
        return value

    def _recursive_tensorize(self, data_struct: dict):
        # support for nested types like struct of list of struct
        if isinstance(data_struct, (list, np.ndarray)):
            data_struct = np.array(data_struct, copy=False)
            if data_struct.dtype == object:  # pytorch tensors cannot be instantied from an array of objects
                return [self.recursive_tensorize(substruct) for substruct in data_struct]
        return self._tensorize(data_struct)

    def recursive_tensorize(self, data_struct: dict):
        return map_nested(self._recursive_tensorize, data_struct, map_list=False)

    def format_row(self, pa_table: pa.Table) -> dict:
        row = self.numpy_arrow_extractor(**self.np_array_kwargs).extract_row(pa_table)
        if self.decoded:
            row = self.python_features_decoder.decode_row(row)
        return self.recursive_tensorize(row)

    def format_column(self, pa_table: pa.Table) -> np.ndarray:
        column = self.numpy_arrow_extractor(**self.np_array_kwargs).extract_column(pa_table)
        if self.decoded:
            column = self.python_features_decoder.decode_column(column, pa_table.column_names[0])
        return self.recursive_tensorize(column)

    def format_batch(self, pa_table: pa.Table) -> dict:
        batch = self.numpy_arrow_extractor(**self.np_array_kwargs).extract_batch(pa_table)
        if self.decoded:
            batch = self.python_features_decoder.decode_batch(batch)
        return self.recursive_tensorize(batch)
