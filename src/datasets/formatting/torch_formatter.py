from typing import TYPE_CHECKING

import numpy as np
import pyarrow as pa

from ..utils.py_utils import map_nested
from .formatting import Formatter


if TYPE_CHECKING:
    import torch


class TorchFormatter(Formatter[dict, "torch.Tensor", dict]):
    def __init__(self, **torch_tensor_kwargs):
        self.torch_tensor_kwargs = torch_tensor_kwargs
        import torch  # noqa import torch at initialization

    def _tensorize(self, value):
        import torch

        return torch.tensor(value, **self.torch_tensor_kwargs)

    def _recursive_tensorize(self, data_struct: dict):
        # support for nested types like struct of list of struct
        if isinstance(data_struct, (list, np.ndarray)):
            data_struct = np.array(data_struct, copy=False)
            if data_struct.dtype == np.object:  # pytorch tensors cannot be instantied from an array of objects
                return [self.recursive_tensorize(substruct) for substruct in data_struct]
        return self._tensorize(data_struct)

    def recursive_tensorize(self, data_struct: dict):
        return map_nested(self._recursive_tensorize, data_struct, map_list=False)

    def format_row(self, pa_table: pa.Table) -> dict:
        row = self.numpy_arrow_extractor().extract_row(pa_table)
        return self.recursive_tensorize(row)

    def format_column(self, pa_table: pa.Table) -> "torch.Tensor":
        col = self.numpy_arrow_extractor().extract_column(pa_table)
        return self.recursive_tensorize(col)

    def format_batch(self, pa_table: pa.Table) -> dict:
        batch = self.numpy_arrow_extractor().extract_batch(pa_table)
        return self.recursive_tensorize(batch)
