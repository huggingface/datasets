# Copyright 2020 The HuggingFace Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
import sys
from collections.abc import Mapping
from typing import TYPE_CHECKING

import numpy as np
import pyarrow as pa

from .. import config
from .formatting import TensorFormatter


if TYPE_CHECKING:
    import torch

# Import torch once at module level once
try:
    import torch

    _torch_available = True
except ImportError:
    _torch_available = False
    torch = None


class TorchFormatter(TensorFormatter[Mapping, "torch.Tensor", Mapping]):
    def __init__(self, features=None, token_per_repo_id=None, **torch_tensor_kwargs):
        super().__init__(features=features, token_per_repo_id=token_per_repo_id)
        self.torch_tensor_kwargs = torch_tensor_kwargs

        if not _torch_available:
            raise ImportError("PyTorch is required but not available")

    def _consolidate(self, column):
        """Smarter consolidation that only stacks when safe and beneficial."""
        if not isinstance(column, list) or not column:
            return column

        # Check if all items are tensors with matching properties
        first = column[0]
        if not isinstance(first, torch.Tensor):
            return column

        # Fast check: if all tensors have same shape, dtype, and device, we can stack
        if all(
            isinstance(x, torch.Tensor)
            and x.shape == first.shape
            and x.dtype == first.dtype
            and x.device == first.device
            for x in column
        ):
            return torch.stack(column)

        return column

    def _tensorize(self, value):
        """Zero/low-copy tensor conversion with smart dtype handling."""
        # Fast path for strings, bytes, None
        if isinstance(value, (str, bytes, type(None))):
            return value

        # Handle string arrays
        if isinstance(value, (np.character, np.ndarray)) and np.issubdtype(value.dtype, np.character):
            return value.tolist()

        # PIL Image fast path - avoid extra copies
        if config.PIL_AVAILABLE and "PIL" in sys.modules:
            import PIL.Image

            if isinstance(value, PIL.Image.Image):
                # Single conversion path: PIL -> numpy -> torch
                arr = np.asarray(value)
                if arr.ndim == 2:
                    arr = arr[:, :, np.newaxis]
                # Use moveaxis instead of transpose
                arr = np.moveaxis(arr, -1, 0)  # HWC -> CHW
                # Ensure contiguous for zero-copy conversion
                if not arr.flags.c_contiguous:
                    arr = np.ascontiguousarray(arr)
                # Ensure array is writable for torch conversion
                if not arr.flags.writeable:
                    arr = arr.copy()
                return torch.from_numpy(arr)

        # Video/Audio decoder passthrough
        if config.TORCHVISION_AVAILABLE and "torchvision" in sys.modules:
            from torchvision.io import VideoReader

            if isinstance(value, VideoReader):
                return value

        if config.TORCHCODEC_AVAILABLE and "torchcodec" in sys.modules:
            from torchcodec.decoders import AudioDecoder, VideoDecoder

            if isinstance(value, (VideoDecoder, AudioDecoder)):
                return value

        # Support for other tensor libraries via __array__
        if hasattr(value, "__array__") and not isinstance(value, torch.Tensor):
            value = value.__array__()

        # Fast numpy conversion paths
        if isinstance(value, np.ndarray):
            # Handle integer types with smart casting
            if np.issubdtype(value.dtype, np.integer):
                # Check if user specified a dtype, otherwise default to int64
                kwargs = self.torch_tensor_kwargs.copy()
                target_dtype = kwargs.get("dtype", torch.int64)

                # Safe casting for unsigned types
                if value.dtype in (np.uint16, np.uint32):
                    # Cast to int64 in numpy (fast) then convert to torch
                    value = value.astype(np.int64)
                    if target_dtype == torch.int64:
                        if not value.flags.writeable:
                            value = value.copy()
                        return torch.from_numpy(value)
                    else:
                        if not value.flags.writeable:
                            value = value.copy()
                        kwargs.setdefault("dtype", target_dtype)
                        return torch.as_tensor(value, **kwargs)
                elif value.dtype == np.uint64:
                    # Check if values fit in int64 range
                    if np.all(value <= np.iinfo(np.int64).max):
                        value = value.astype(np.int64)
                        if target_dtype == torch.int64:
                            if not value.flags.writeable:
                                value = value.copy()
                            return torch.from_numpy(value)
                        else:
                            if not value.flags.writeable:
                                value = value.copy()
                            kwargs.setdefault("dtype", target_dtype)
                            return torch.as_tensor(value, **kwargs)
                    else:
                        # Fallback to safe conversion via Python ints
                        kwargs.setdefault("dtype", target_dtype)
                        return torch.tensor(value, **kwargs)
                else:
                    # Use zero-copy conversion for compatible integer types
                    if value.dtype == np.int64 and target_dtype == torch.int64:
                        # Perfect match, zero-copy conversion
                        if not value.flags.writeable:
                            value = value.copy()
                        return torch.from_numpy(value)
                    else:
                        # Need dtype conversion, use as_tensor for efficiency
                        if not value.flags.writeable:
                            value = value.copy()
                        kwargs.setdefault("dtype", target_dtype)
                        return torch.as_tensor(value, **kwargs)

            # Handle floating point types
            elif np.issubdtype(value.dtype, np.floating):
                # Check if user specified a dtype, otherwise default to float32
                kwargs = self.torch_tensor_kwargs.copy()
                target_dtype = kwargs.get("dtype", torch.float32)

                if value.dtype == np.float32 and target_dtype == torch.float32:
                    # Zero-copy conversion, but ensure array is writable
                    if not value.flags.writeable:
                        value = value.copy()
                    return torch.from_numpy(value)
                else:
                    # Need dtype conversion
                    if not value.flags.writeable:
                        value = value.copy()
                    kwargs.setdefault("dtype", target_dtype)
                    return torch.as_tensor(value, **kwargs)
            else:
                # Other numpy types, use zero-copy when possible
                if not value.flags.writeable:
                    value = value.copy()
                return torch.from_numpy(value)

        # Handle numpy scalars
        elif isinstance(value, np.number):
            kwargs = self.torch_tensor_kwargs.copy()
            if np.issubdtype(value.dtype, np.integer):
                # Use torch.as_tensor for scalar conversion with dtype control
                kwargs.setdefault("dtype", torch.int64)
                return torch.as_tensor(value, **kwargs)
            elif np.issubdtype(value.dtype, np.floating):
                kwargs.setdefault("dtype", torch.float32)
                return torch.as_tensor(value, **kwargs)
            else:
                return torch.as_tensor(value, **kwargs)

        # Handle Python lists/tuples of numbers efficiently
        elif isinstance(value, (list, tuple)):
            # Try to convert to numpy first for faster tensor creation
            try:
                arr = np.array(value)
                if arr.dtype.kind in "iuf":  # integer, unsigned, float
                    return self._tensorize(arr)  # Recursive call to handle numpy path
            except (ValueError, TypeError):
                pass  # Fall back to torch.tensor

        # Default fallback with dtype defaults
        default_dtype = {}
        if isinstance(value, (int, float)):
            if isinstance(value, int):
                default_dtype = {"dtype": torch.int64}
            else:
                default_dtype = {"dtype": torch.float32}

        return torch.tensor(value, **{**default_dtype, **self.torch_tensor_kwargs})

    def _recursive_tensorize(self, data_struct):
        """Optimized recursive walker with reduced Python overhead."""
        # Handle tensor-like objects with __array__ interface
        if hasattr(data_struct, "__array__") and not isinstance(data_struct, torch.Tensor):
            data_struct = data_struct.__array__()

        # Handle object arrays (nested structures)
        if isinstance(data_struct, np.ndarray):
            if data_struct.dtype == object:
                # Use list comprehension instead of map_nested
                result = [self._recursive_tensorize(item) for item in data_struct]
                return self._consolidate(result)
        # Handle lists and tuples
        elif isinstance(data_struct, (list, tuple)):
            result = [self._recursive_tensorize(item) for item in data_struct]
            return self._consolidate(result)
        # Handle dictionaries
        elif isinstance(data_struct, dict):
            return {key: self._recursive_tensorize(value) for key, value in data_struct.items()}

        # Base case: tensorize the leaf value
        return self._tensorize(data_struct)

    def recursive_tensorize(self, data_struct: dict):
        """Public interface maintaining compatibility."""
        return self._recursive_tensorize(data_struct)

    def format_row(self, pa_table: pa.Table) -> Mapping:
        row = self.numpy_arrow_extractor().extract_row(pa_table)
        row = self.python_features_decoder.decode_row(row)
        return self.recursive_tensorize(row)

    def format_column(self, pa_table: pa.Table) -> "torch.Tensor":
        column = self.numpy_arrow_extractor().extract_column(pa_table)
        column = self.python_features_decoder.decode_column(column, pa_table.column_names[0])
        column = self.recursive_tensorize(column)
        column = self._consolidate(column)
        return column

    def format_batch(self, pa_table: pa.Table) -> Mapping:
        batch = self.numpy_arrow_extractor().extract_batch(pa_table)
        batch = self.python_features_decoder.decode_batch(batch)
        batch = self.recursive_tensorize(batch)
        for column_name in batch:
            batch[column_name] = self._consolidate(batch[column_name])
        return batch
