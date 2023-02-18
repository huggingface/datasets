# Copyright 2021 The HuggingFace Authors.
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
from ..utils.py_utils import map_nested
from .formatting import Formatter


if TYPE_CHECKING:
    from typing import Dict

    import jax
    import jaxlib


class JaxFormatter(Formatter[Mapping, "jax.Array", Mapping]):
    def __init__(self, features=None, device=None, **jnp_array_kwargs):
        super().__init__(features=features)
        import jax
        from jaxlib.xla_client import Device

        self.device_mapping = self._map_devices_to_str()
        self.device = (
            device if isinstance(device, str) else str(device) if isinstance(device, Device) else str(jax.devices()[0])
        )
        self.jnp_array_kwargs = jnp_array_kwargs

    def _map_devices_to_str() -> Dict[str, "jaxlib.xla_extension.Device"]:
        import jax

        return {str(device): device for device in jax.devices()}

    def _consolidate(self, column):
        import jax
        import jax.numpy as jnp

        if isinstance(column, list) and column:
            if all(
                isinstance(x, jax.Array) and x.shape == column[0].shape and x.dtype == column[0].dtype for x in column
            ):
                return jnp.stack(column, axis=0)
        return column

    def _tensorize(self, value):
        import jax
        import jax.numpy as jnp

        if isinstance(value, (str, bytes, type(None))):
            return value
        elif isinstance(value, (np.character, np.ndarray)) and np.issubdtype(value.dtype, np.character):
            return value.tolist()

        default_dtype = {}

        if isinstance(value, (np.number, np.ndarray)) and np.issubdtype(value.dtype, np.integer):
            # the default int precision depends on the jax config
            # see https://jax.readthedocs.io/en/latest/notebooks/Common_Gotchas_in_JAX.html#double-64bit-precision
            if jax.config.jax_enable_x64:
                default_dtype = {"dtype": jnp.int64}
            else:
                default_dtype = {"dtype": jnp.int32}
        elif isinstance(value, (np.number, np.ndarray)) and np.issubdtype(value.dtype, np.floating):
            default_dtype = {"dtype": jnp.float32}
        elif config.PIL_AVAILABLE and "PIL" in sys.modules:
            import PIL.Image

            if isinstance(value, PIL.Image.Image):
                value = np.asarray(value)

        with jax.default_device(self.device_mapping[self.device]):
            # calling jnp.array on a np.ndarray does copy the data
            # see https://github.com/google/jax/issues/4486
            return jnp.array(value, **{**default_dtype, **self.jnp_array_kwargs})

    def _recursive_tensorize(self, data_struct: dict):
        # support for nested types like struct of list of struct
        if isinstance(data_struct, np.ndarray):
            if data_struct.dtype == object:  # jax arrays cannot be instantied from an array of objects
                return self._consolidate([self.recursive_tensorize(substruct) for substruct in data_struct])
        return self._tensorize(data_struct)

    def recursive_tensorize(self, data_struct: dict):
        return map_nested(self._recursive_tensorize, data_struct)

    def format_row(self, pa_table: pa.Table) -> Mapping:
        row = self.numpy_arrow_extractor().extract_row(pa_table)
        row = self.python_features_decoder.decode_row(row)
        return self.recursive_tensorize(row)

    def format_column(self, pa_table: pa.Table) -> "jax.Array":
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
