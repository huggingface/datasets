import io
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import no_op_if_value_is_null
from .bio_sequence import _cast_to_bytes_path_struct, _resolve_token


if TYPE_CHECKING:
    import mne

    from .features import FeatureType


@dataclass
class Biosignal:
    """
    **Experimental.**
    Biosignal [`Feature`] to read electrophysiology and biosignal files (EEG, MEG, iEEG, EMG, fNIRS)
    using MNE-Python and MNE-BIDS.

    Input: The Biosignal feature accepts as input:
    - A `str`: Absolute path to the biosignal file.
    - A `pathlib.Path`: Path to the biosignal file.
    - A `dict` with the keys:
        - `path`: String with relative or absolute path of the biosignal file.
        - `bytes`: Bytes of the biosignal file.
    - An `mne.io.BaseRaw`: MNE raw recording object.

    When decoding a local file located inside a BIDS dataset and `mne-bids` is installed,
    `mne_bids.read_raw_bids` is used automatically so BIDS sidecars (`events.tsv`, `channels.tsv`,
    `electrodes.tsv`, `participants.tsv`, and JSON metadata) are attached to the returned
    `mne.io.BaseRaw` object.

    Args:
        preload (`bool`, defaults to `False`):
            Whether to preload the signal data into memory when reading local files.
        decode (`bool`, defaults to `True`):
            Whether to decode the biosignal data. If `False`,
            returns the underlying dictionary in the format `{"path": path, "bytes": bytes}`.

    Example:

    ```py
    >>> from datasets import load_dataset, Biosignal
    >>> ds = load_dataset("bids", data_dir="path/to/bids", split="train")
    >>> ds[0]["biosignal"]
    <RawBrainVision | sub-01_task-rest_eeg.vhdr, 64 x 10000 (40.0 s), ~35 kB, data not loaded>
    >>> ds = ds.cast_column("biosignal", Biosignal(decode=False))
    >>> ds[0]["biosignal"]
    {'bytes': None, 'path': 'path/to/bids/sub-01/eeg/sub-01_task-rest_eeg.vhdr'}
    ```
    """

    preload: bool = False
    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)

    # Automatically constructed
    dtype: ClassVar[str] = "mne.io.BaseRaw"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Biosignal", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, Path, bytes, bytearray, dict, "mne.io.BaseRaw"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `Path`, `bytes`, `mne.io.BaseRaw` or `dict`):
                Data passed as input to Biosignal feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if config.MNE_AVAILABLE:
            import mne

            if isinstance(value, mne.io.BaseRaw):
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_path = os.path.join(tmpdir, "raw.fif")
                    value.save(tmp_path, overwrite=True, verbose="ERROR")
                    return {"path": None, "bytes": Path(tmp_path).read_bytes()}

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": bytes(value)}
        elif isinstance(value, dict) and (value.get("bytes") is not None or value.get("path") is not None):
            return {
                "bytes": None
                if value.get("path") is not None and os.path.exists(value["path"])
                else value.get("bytes"),
                "path": value.get("path"),
            }
        raise ValueError(
            f"A biosignal sample should have one of 'path' or 'bytes' or be an mne.io.BaseRaw, but got {value}."
        )

    def decode_example(self, value: Union[str, dict], token_per_repo_id=None) -> "mne.io.BaseRaw":
        """Decode example biosignal file into an `mne.io.BaseRaw` object."""
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Biosignal(decode=True) instead.")

        if not isinstance(value, (dict, str)):
            return value

        if not config.MNE_AVAILABLE:
            raise ImportError("To support decoding biosignal files, please install 'mne'.")

        import mne

        path, bytes_ = (value, None) if isinstance(value, str) else (value["path"], value["bytes"])
        if bytes_ is None:
            if path is None:
                raise ValueError(f"A biosignal should have one of 'path' or 'bytes' but both are None in {value}.")
            if is_local_path(path):
                if config.MNE_BIDS_AVAILABLE:
                    import mne_bids

                    try:
                        return mne_bids.read_raw_bids(
                            mne_bids.get_bids_path_from_fname(path, check=False, verbose="ERROR"),
                            extra_params={"preload": self.preload},
                            verbose="ERROR",
                        )
                    except Exception:
                        pass
                return mne.io.read_raw(path, preload=self.preload, verbose="ERROR")
            download_config = DownloadConfig(token=_resolve_token(path, token_per_repo_id or {}))
            with xopen(path, "rb", download_config=download_config) as f:
                bytes_ = f.read()

        return mne.io.read_raw_fif(io.BytesIO(bytes_), preload=True, verbose="ERROR")

    def flatten(self) -> Union["FeatureType", dict[str, "FeatureType"]]:
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

    def cast_storage(self, storage: Union[pa.StringArray, pa.BinaryArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Biosignal arrow storage type."""
        return _cast_to_bytes_path_struct(storage, self.pa_type)

    def embed_storage(
        self, storage: pa.StructArray, token_per_repo_id=None, local_files: bool = True, remote_files: bool = True
    ) -> pa.StructArray:
        """Embed biosignal files into the Arrow array."""

        @no_op_if_value_is_null
        def path_to_bytes(path: str) -> bytes:
            return self.encode_example(
                Biosignal(preload=True).decode_example(path, token_per_repo_id=token_per_repo_id)
            )["bytes"]

        bytes_array = pa.array(
            [
                path_to_bytes(path)
                if bytes_ is None and path is not None and (local_files if is_local_path(path) else remote_files)
                else bytes_
                for bytes_, path in zip(storage.field("bytes").to_pylist(), storage.field("path").to_pylist())
            ],
            type=pa.binary(),
        )
        path_array = pa.array(
            [os.path.basename(path) if path is not None else None for path in storage.field("path").to_pylist()],
            type=pa.string(),
        )
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=storage.is_null())
        return array_cast(storage, self.pa_type)
