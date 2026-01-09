import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


if TYPE_CHECKING:
    from .features import FeatureType


@dataclass
class ProteinStructure:
    """
    **Experimental.**
    ProteinStructure [`Feature`] to read protein 3D structure files (PDB/mmCIF).

    This feature stores raw file content for lazy loading. The viewer or downstream
    code handles parsing. Supports both PDB (.pdb, .ent) and mmCIF (.cif, .mmcif) formats.

    Input: The ProteinStructure feature accepts as input:
    - A `str`: Absolute path to the structure file (i.e. random access is allowed).
    - A `pathlib.Path`: path to the structure file (i.e. random access is allowed).
    - A `dict` with the keys:
        - `path`: String with relative path of the structure file in a dataset repository.
        - `bytes`: Bytes of the structure file.
      This is useful for archived files with sequential access.
    - A `bytes` object: Raw bytes of the structure file content.

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the structure data to a string. If `False`,
            returns the underlying dictionary in the format `{"path": structure_path, "bytes": structure_bytes}`.

    Examples:

    ```py
    >>> from datasets import Dataset, ProteinStructure
    >>> ds = Dataset.from_dict({"structure": ["path/to/structure.pdb"]}).cast_column("structure", ProteinStructure())
    >>> ds.features["structure"]
    ProteinStructure(decode=True, id=None)
    >>> ds[0]["structure"]
    'HEADER    PLANT PROTEIN...\\nATOM      1  N   THR A   1...'
    >>> ds = ds.cast_column("structure", ProteinStructure(decode=False))
    >>> ds[0]["structure"]
    {'bytes': None,
    'path': 'path/to/structure.pdb'}
    ```
    """

    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)

    # Automatically constructed
    dtype: ClassVar[str] = "str"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="ProteinStructure", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, dict, Path]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `bytes`, `pathlib.Path` or `dict`):
                Data passed as input to ProteinStructure feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": value}
        elif isinstance(value, dict):
            if value.get("path") is not None and os.path.isfile(value["path"]):
                # we set "bytes": None to not duplicate the data if they're already available locally
                return {"bytes": None, "path": value.get("path")}
            elif value.get("bytes") is not None or value.get("path") is not None:
                # store the structure bytes, and path is used to infer the format using the file extension
                return {"bytes": value.get("bytes"), "path": value.get("path")}
            else:
                raise ValueError(
                    f"A protein structure sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
                )
        else:
            raise ValueError(
                f"Unsupported input type for ProteinStructure: {type(value)}. "
                f"Expected str, bytes, pathlib.Path, or dict."
            )

    def decode_example(self, value: dict, token_per_repo_id=None) -> str:
        """Decode example structure file into structure data.

        Args:
            value (`dict`):
                A dictionary with keys:
                - `path`: String with absolute or relative structure file path.
                - `bytes`: The bytes of the structure file.

            token_per_repo_id (`dict`, *optional*):
                To access and decode structure files from private repositories on
                the Hub, you can pass a dictionary repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            `str`: The structure file content as a string (PDB/mmCIF are text formats).
        """
        if not self.decode:
            raise RuntimeError(
                "Decoding is disabled for this feature. Please use ProteinStructure(decode=True) instead."
            )

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(
                    f"A protein structure should have one of 'path' or 'bytes' but both are None in {value}."
                )
            else:
                if is_local_path(path):
                    with open(path, "r", encoding="utf-8") as f:
                        return f.read()
                else:
                    source_url = path.split("::")[-1]
                    pattern = (
                        config.HUB_DATASETS_URL
                        if source_url.startswith(config.HF_ENDPOINT)
                        else config.HUB_DATASETS_HFFS_URL
                    )
                    try:
                        repo_id = string_to_dict(source_url, pattern)["repo_id"]
                        token = token_per_repo_id.get(repo_id)
                    except ValueError:
                        token = None
                    download_config = DownloadConfig(token=token)
                    with xopen(path, "r", download_config=download_config) as f:
                        return f.read()
        else:
            # PDB/mmCIF are text formats, decode bytes to string
            if isinstance(bytes_, (bytes, bytearray)):
                return bytes_.decode("utf-8")
            # If it's already a string, return as-is
            return str(bytes_)

    def flatten(self) -> Union["FeatureType", Dict[str, "FeatureType"]]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from .features import Value

        return (
            self
            if self.decode
            else {
                "bytes": Value("binary"),
                "path": Value("string"),
            }
        )

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray, pa.ListArray]) -> pa.StructArray:
        """Cast an Arrow array to the ProteinStructure arrow storage type.
        The Arrow types that can be converted to the ProteinStructure pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the structure bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter
        - `pa.list(*)` - it must contain the structure array data

        Args:
            storage (`Union[pa.StringArray, pa.StructArray, pa.ListArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the ProteinStructure arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if pa.types.is_string(storage.type) or pa.types.is_large_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_binary(storage.type) or pa.types.is_large_binary(storage.type):
            path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([storage, path_array], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_struct(storage.type):
            if storage.type.get_field_index("bytes") >= 0:
                bytes_array = storage.field("bytes")
            else:
                bytes_array = pa.array([None] * len(storage), type=pa.binary())
            if storage.type.get_field_index("path") >= 0:
                path_array = storage.field("path")
            else:
                path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=storage.is_null())
        return array_cast(storage, self.pa_type)

    def embed_storage(self, storage: pa.StructArray, token_per_repo_id=None) -> pa.StructArray:
        """Embed protein structure files into the Arrow array.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.
            token_per_repo_id (`dict`, *optional*):
                To access structure files from private repositories on the Hub.

        Returns:
            `pa.StructArray`: Array in the ProteinStructure arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if token_per_repo_id is None:
            token_per_repo_id = {}

        @no_op_if_value_is_null
        def path_to_bytes(path):
            source_url = path.split("::")[-1]
            pattern = (
                config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
            )
            source_url_fields = string_to_dict(source_url, pattern)
            token = token_per_repo_id.get(source_url_fields["repo_id"]) if source_url_fields is not None else None
            download_config = DownloadConfig(token=token)
            with xopen(path, "rb", download_config=download_config) as f:
                return f.read()

        bytes_array = pa.array(
            [
                (path_to_bytes(x["path"]) if x["bytes"] is None else x["bytes"]) if x is not None else None
                for x in storage.to_pylist()
            ],
            type=pa.binary(),
        )
        path_array = pa.array(
            [os.path.basename(path) if path is not None else None for path in storage.field("path").to_pylist()],
            type=pa.string(),
        )
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null())
        return array_cast(storage, self.pa_type)
