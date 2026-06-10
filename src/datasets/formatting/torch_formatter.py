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
from typing import TYPE_CHECKING, Optional, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..features import Features
from ..features.features import decode_nested_example
from ..utils.file_utils import is_local_path
from ..utils.py_utils import map_nested
from .formatting import TensorFormatter


if TYPE_CHECKING:
    import torch

    from ..features.image import Image


_PIL_MODE_TO_TORCHVISION_MODE = {
    "L": "GRAY",
    "LA": "GRAY_ALPHA",
    "RGB": "RGB",
    "RGBA": "RGB_ALPHA",
}


def _decode_image_for_torch(value: dict, image_feature: "Image") -> "torch.Tensor":
    """Decode an image dict {"bytes": ..., "path": ...} to a CHW torch.Tensor using torchvision.

    Uses torchvision.io.decode_image for efficient decoding. Falls back to PIL
    decoding + torchvision.transforms.v2.functional.pil_to_tensor on failure
    (e.g. unsupported format).

    Args:
        value: dict with "bytes" and "path" keys from Arrow extraction
        image_feature: the Image feature instance (carries mode/decode info)

    Returns:
        torch.Tensor in CHW format
    """
    import torch
    from torchvision.io import decode_image

    path, bytes_ = value["path"], value["bytes"]

    tv_mode = _PIL_MODE_TO_TORCHVISION_MODE.get(image_feature.mode) if image_feature.mode else None

    try:
        if bytes_ is not None:
            input_tensor = torch.frombuffer(bytearray(bytes_), dtype=torch.uint8)
            return decode_image(input_tensor, mode=tv_mode or "UNCHANGED", apply_exif_orientation=True)
        elif path is not None and is_local_path(path):
            return decode_image(path, mode=tv_mode or "UNCHANGED", apply_exif_orientation=True)
    except Exception:
        pass

    # Fallback: PIL decode + pil_to_tensor
    from torchvision.transforms.v2.functional import pil_to_tensor

    pil_image = image_feature.decode_example(value)
    return pil_to_tensor(pil_image)


class TorchFeaturesDecoder:
    """Features decoder that uses torchvision for Image columns when available.

    For Image features, decodes directly to torch.Tensor via torchvision.io.decode_image,
    bypassing PIL entirely. This works for both top-level and nested Image features
    (e.g. List(Image())). For all other decodable features (Audio, Video, etc.),
    delegates to the standard decode_nested_example path.
    """

    def __init__(
        self,
        features: Optional[Features],
        token_per_repo_id: Optional[dict[str, Union[str, bool, None]]] = None,
    ):
        self.features = features
        self.token_per_repo_id = token_per_repo_id

        self._decoder_overrides = None
        if self.features and config.TORCHVISION_AVAILABLE:
            from ..features.image import Image

            self._decoder_overrides = {Image: _decode_image_for_torch}

    def decode_row(self, row: dict) -> dict:
        if not self.features:
            return row
        return {
            column_name: (
                decode_nested_example(
                    self.features[column_name],
                    value,
                    token_per_repo_id=self.token_per_repo_id,
                    decoder_overrides=self._decoder_overrides,
                )
                if self.features._column_requires_decoding[column_name]
                else value
            )
            for column_name, value in row.items()
        }

    def decode_column(self, column: list, column_name: str) -> list:
        if not self.features:
            return column
        if not self.features._column_requires_decoding[column_name]:
            return column
        return [
            decode_nested_example(
                self.features[column_name],
                value,
                token_per_repo_id=self.token_per_repo_id,
                decoder_overrides=self._decoder_overrides,
            )
            if value is not None
            else None
            for value in column
        ]

    def decode_batch(self, batch: dict) -> dict:
        if not self.features:
            return batch
        return {column_name: self.decode_column(column, column_name) for column_name, column in batch.items()}


class TorchFormatter(TensorFormatter[Mapping, "torch.Tensor", Mapping]):
    def __init__(self, features=None, token_per_repo_id=None, **torch_tensor_kwargs):
        super().__init__(features=features, token_per_repo_id=token_per_repo_id)
        self.torch_tensor_kwargs = torch_tensor_kwargs
        self.torch_features_decoder = TorchFeaturesDecoder(self.features, self.token_per_repo_id)
        import torch  # noqa import torch at initialization

    def _consolidate(self, column):
        import torch

        if isinstance(column, list) and column:
            if all(
                isinstance(x, torch.Tensor) and x.shape == column[0].shape and x.dtype == column[0].dtype
                for x in column
            ):
                return torch.stack(column)
        return column

    def _tensorize(self, value):
        import torch

        if isinstance(value, torch.Tensor):
            return value

        if isinstance(value, (str, bytes, type(None))):
            return value
        elif isinstance(value, (np.character, np.ndarray)) and np.issubdtype(value.dtype, np.character):
            return value.tolist()

        default_dtype = {}

        if isinstance(value, (np.number, np.ndarray)) and np.issubdtype(value.dtype, np.integer):
            default_dtype = {"dtype": torch.int64}

            # Convert dtype to np.int64 if it's either np.uint16 or np.uint32 to ensure compatibility.
            # np.uint64 is excluded from this conversion as there is no compatible PyTorch dtype that can handle it without loss.
            if value.dtype in [np.uint16, np.uint32]:
                value = value.astype(np.int64)

        elif isinstance(value, (np.number, np.ndarray)) and np.issubdtype(value.dtype, np.floating):
            default_dtype = {"dtype": torch.float32}

        if config.PIL_AVAILABLE and "PIL" in sys.modules:
            import PIL.Image

            if isinstance(value, PIL.Image.Image):
                value = np.asarray(value)
                if value.ndim == 2:
                    value = value[:, :, np.newaxis]

                value = value.transpose((2, 0, 1))
        if config.TORCHVISION_AVAILABLE and "torchvision" in sys.modules:
            try:
                from torchvision.io import VideoReader

                if isinstance(value, VideoReader):
                    return value  # TODO(QL): set output to torch tensors ?
            except ImportError:
                pass
        if config.TORCHCODEC_AVAILABLE and "torchcodec" in sys.modules:
            from torchcodec.decoders import AudioDecoder, VideoDecoder

            if isinstance(value, (VideoDecoder, AudioDecoder)):
                return value  # TODO(QL): set output to jax arrays ?

        return torch.tensor(value, **{**default_dtype, **self.torch_tensor_kwargs})

    def _recursive_tensorize(self, data_struct):
        import torch

        # support for torch, tf, jax etc.
        if hasattr(data_struct, "__array__") and not isinstance(data_struct, torch.Tensor):
            data_struct = data_struct.__array__()
        # support for nested types like struct of list of struct
        if isinstance(data_struct, np.ndarray):
            if data_struct.dtype == object:  # torch tensors cannot be instantied from an array of objects
                return self._consolidate([self.recursive_tensorize(substruct) for substruct in data_struct])
        elif isinstance(data_struct, (list, tuple)):
            return self._consolidate([self.recursive_tensorize(substruct) for substruct in data_struct])
        return self._tensorize(data_struct)

    def recursive_tensorize(self, data_struct: dict):
        return map_nested(self._recursive_tensorize, data_struct, map_list=False)

    def format_row(self, pa_table: pa.Table) -> Mapping:
        row = self.numpy_arrow_extractor().extract_row(pa_table)
        row = self.torch_features_decoder.decode_row(row)
        return self.recursive_tensorize(row)

    def format_column(self, pa_table: pa.Table) -> "torch.Tensor":
        column = self.numpy_arrow_extractor().extract_column(pa_table)
        column = self.torch_features_decoder.decode_column(column, pa_table.column_names[0])
        column = self.recursive_tensorize(column)
        column = self._consolidate(column)
        return column

    def format_batch(self, pa_table: pa.Table) -> Mapping:
        batch = self.numpy_arrow_extractor().extract_batch(pa_table)
        batch = self.torch_features_decoder.decode_batch(batch)
        batch = self.recursive_tensorize(batch)
        for column_name in batch:
            batch[column_name] = self._consolidate(batch[column_name])
        return batch
