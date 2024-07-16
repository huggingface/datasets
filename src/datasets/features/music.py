from __future__ import annotations

from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


if TYPE_CHECKING:
    from datasets.features.features import FeatureType

    try:
        from symusic import Score
    except ImportError:
        Score = None


@dataclass
class Music:
    """Music [`Feature`] to read symbolic music data from a MIDI or abc file.

    Input: The Music feature accepts as input:
    - A `pathlib.Path` or `str`: Absolute path to the music file (i.e. random access is allowed).
    - A `dict` with the keys:

        - `path`: String with relative path of the music file to the archive file.
        - `bytes`: Bytes of the music file.

      This is useful for archived files with sequential access.

    - A `symusic.Score`: symusic score object.

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the music data. If `False`,
            returns the underlying dictionary in the format `{"path": music_path, "bytes": music_bytes}`.

    Examples:

    ```py
    >>> from datasets import load_dataset, Music
    >>> ds = load_dataset("disco", split="train")
    >>> ds.features["music"]
    Music(decode=True, id=None)
    >>> ds[0]["music"]
    <Score(ttype=Tick, tpq=384, begin=0, end=19092, tracks=8, notes=610, time_sig=1, key_sig=1, markers=1, lyrics=0)>
    >>> ds = ds.cast_column('music', Music(decode=False))
    {'bytes': None,
     'path': '/root/.cache/huggingface/datasets/downloads/extracted/9fcfccf1c2245c74eb02fbd6ce70fbdf.mid'}
    ```
    """

    decode: bool = True
    id: str | None = None
    # Automatically constructed
    dtype: ClassVar[str] = "symusic.Score"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Music", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    @staticmethod
    def encode_example(value: Path | str | bytes | dict | "Score") -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `pathlib.Path` or `symusic.Score`):
                Data passed as input to Music feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        import symusic

        # cast pathlib.Path to str for pyArrow
        if isinstance(value, Path):
            value = str(value)
        if isinstance(value, str):
            return {"path": value, "bytes": None}
        if isinstance(value, bytes):
            return {"path": None, "bytes": value}
        if isinstance(value, symusic.Score):
            return {"path": None, "bytes": value.dumps_midi()}
        if value.get("path") is not None and Path(value["path"]).is_file():
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        if value.get("bytes") is not None or value.get("path") is not None:
            # store the image bytes, and path is used to infer the image format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        raise ValueError(
            f"A music sample should have one of 'path', 'bytes' or 'symusic.Score' but they are missing or None in {value}."
        )

    def decode_example(self, value: dict, token_per_repo_id: dict[str, str | bool | None] | None = None) -> "Score":
        """Decode example music file into music data.

        Args:
            value (`dict`):
                A dictionary with keys:

                - `path`: String with relative music file path.
                - `bytes`: Bytes of the music file.
            token_per_repo_id (`dict`, *optional*):
                To access and decode
                music files from private repositories on the Hub, you can pass
                a dictionary repo_id (`str`) -> token (`bool` or `str`)

        Returns:
            `dict`
        """
        if not self.decode:
            msg = "Decoding is disabled for this feature. Please use `Music(decode=True)` instead."
            raise RuntimeError(msg)

        try:
            from symusic import Score
        except ImportError as err:
            raise ImportError("To support decoding music files, please install 'symusic'.") from err

        if token_per_repo_id is None:
            token_per_repo_id = {}
        path, bytes_ = value["path"], value["bytes"]

        if bytes_ is None:
            if path is None:
                raise ValueError(f"An music should have one of 'path' or 'bytes' but both are None in {value}.")
            if is_local_path(path):
                score = Score(path)
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
                with xopen(path, "rb", download_config=download_config) as f:
                    bytes_ = BytesIO(f.read())
                if path.endswith(".abc"):
                    score = Score.from_abc(bytes_.read().decode("utf-8"))
                else:
                    score = Score.from_midi(bytes_)
        else:
            if bytes_[:4] == b"MThd":  # MIDI file header
                score = Score.from_midi(bytes_)
            else:  # assume it is an abc file
                score = Score.from_abc(str(bytes_, encoding="utf-8"))

        return score

    def flatten(self) -> "FeatureType" | dict[str, "FeatureType"]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from datasets.features import Value

        return (
            self
            if self.decode
            else {
                "bytes": Value("binary"),
                "path": Value("string"),
            }
        )

    def cast_storage(self, storage: pa.StringArray | pa.StructArray | pa.ListArray) -> pa.StructArray:
        """Cast an Arrow array to the Music arrow storage type.

        The Arrow types that can be converted to the Music pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the music (MIDI) bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter

        Args:
            storage (`pa.StringArray | pa.StructArray | pa.ListArray`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Music arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_binary(storage.type):
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

    def embed_storage(self, storage: pa.StructArray) -> pa.StructArray:
        """Embed music files into the Arrow array.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.

        Returns:
            `pa.StructArray`: Array in the Music arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """

        @no_op_if_value_is_null
        def path_to_bytes(path):
            with xopen(path, "rb") as f:
                bytes_ = f.read()
            return bytes_

        bytes_array = pa.array(
            [
                (path_to_bytes(x["path"]) if x["bytes"] is None else x["bytes"]) if x is not None else None
                for x in storage.to_pylist()
            ],
            type=pa.binary(),
        )
        path_array = pa.array(
            [Path(path).name if path is not None else None for path in storage.field("path").to_pylist()],
            type=pa.string(),
        )
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null())
        return array_cast(storage, self.pa_type)
