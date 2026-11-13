import io
import os
import sys
import tempfile
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..utils import logging
from ..utils.file_utils import is_local_path, xbasename, xopen
from .bio_sequence import _cast_to_bytes_path_struct, _resolve_token


if TYPE_CHECKING:
    import mne

    from .features import FeatureType


logger = logging.get_logger(__name__)


@dataclass
class Biosignal:
    """
    **Experimental.**
    Biosignal [`Feature`] to read electrophysiology and biosignal files (EEG, MEG, iEEG, EMG, fNIRS)
    using MNE-Python and MNE-BIDS.

    Input: The Biosignal feature accepts as input:
    - A `str`: Absolute path or URL to the biosignal file.
    - A `pathlib.Path`: Path to the biosignal file.
    - A `dict` with the keys:
        - `path`: String with relative or absolute path of the biosignal file.
        - `bytes`: Bytes of the biosignal file.
    - An `mne.io.BaseRaw`: MNE raw recording object.

    When decoding a local file located inside a BIDS dataset and `mne-bids` is installed,
    `mne_bids.read_raw_bids` is used automatically so BIDS sidecars (`events.tsv`, `channels.tsv`,
    `electrodes.tsv`, `participants.tsv`, and JSON metadata) are attached to the returned
    `mne.io.BaseRaw` object.

    Recordings are read lazily (`preload=False`); operations such as `load_data()`, `pick()` or `resample()` are
    applied on the returned object, for example in [`Dataset.map`].

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the biosignal data. If `False`,
            returns the underlying dictionary in the format `{"path": path, "bytes": bytes}`.

    Example:

    ```py
    >>> from datasets import load_dataset, Biosignal
    >>> ds = load_dataset("bids", data_dir="path/to/bids", split="train")
    >>> ds[0]["biosignal"]
    <RawBrainVision | sub-01_task-rest_eeg.vhdr, 64 x 10000 (40.0 s), ~35 kB, data not loaded>
    >>> ds = ds.map(lambda x: {"biosignal": x["biosignal"].load_data().pick("eeg").resample(250)})
    ```
    """

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
            `dict` with `"path"` and `"bytes"` fields.
        """
        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": bytes(value)}
        elif isinstance(value, dict) and (value.get("path") is not None or value.get("bytes") is not None):
            path, raw_bytes = value.get("path"), value.get("bytes")
            return {
                "path": path,
                "bytes": None
                if (path is not None and os.path.exists(path)) or raw_bytes is None
                else bytes(raw_bytes),
            }
        elif config.MNE_AVAILABLE and "mne" in sys.modules:
            import mne

            if isinstance(value, mne.io.BaseRaw):
                # tempfile until mne>=1.14 supports raw.save(BytesIO()) (mne-tools/mne-python#14516)
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_path = Path(tmpdir) / "raw.fif"
                    value.save(tmp_path, overwrite=True, verbose="ERROR")
                    return {"path": None, "bytes": tmp_path.read_bytes()}

        raise ValueError(
            f"A biosignal sample should have one of 'path' or 'bytes' or be an mne.io.BaseRaw, but got {value}."
        )

    def decode_example(self, value: Union[str, dict], token_per_repo_id=None) -> "mne.io.BaseRaw":
        """Decode example biosignal file into an `mne.io.BaseRaw` object.

        Args:
            value (`str` or `dict`):
                A string with the absolute file path or URL, or a dictionary with keys:

                - `path`: String with absolute or relative file path.
                - `bytes`: The bytes of the biosignal file.
            token_per_repo_id (`dict`, *optional*):
                To access and decode files from private repositories on the Hub, pass
                a dictionary `repo_id` (`str`) -> `token` (`bool` or `str`).

        Returns:
            `mne.io.BaseRaw`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Biosignal(decode=True) instead.")

        if not isinstance(value, (dict, str)):
            return value

        if not config.MNE_AVAILABLE:
            raise ImportError("To support decoding biosignal files, please install 'mne'.")

        import mne

        path, bytes_ = (value, None) if isinstance(value, str) else (value["path"], value["bytes"])
        if path is None and bytes_ is None:
            raise ValueError(f"A biosignal should have one of 'path' or 'bytes' but both are None in {value}.")
        if bytes_ is None and not is_local_path(path):
            download_config = DownloadConfig(token=_resolve_token(path, token_per_repo_id or {}))
            with xopen(path, "rb", download_config=download_config) as f:
                bytes_ = f.read()

        fname = xbasename(path) if path else "raw.fif"
        if bytes_ is not None and fname.lower().endswith(".fif"):
            raw = mne.io.read_raw_fif(io.BytesIO(bytes_), preload=True, verbose="ERROR")
        elif bytes_ is not None:
            # tempfile until mne>=1.14 supports BytesIO across readers (mne-tools/mne-python#14516, #14517)
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir) / fname
                tmp_path.write_bytes(bytes_)
                raw = mne.io.read_raw(tmp_path, preload=True, verbose="ERROR")
        elif config.MNE_BIDS_AVAILABLE and fname.startswith("sub-"):
            import mne_bids

            try:
                # get_bids_path_from_fname until mne-bids>=0.21 accepts path-like directly (mne-tools/mne-bids#1696)
                bids_path = mne_bids.get_bids_path_from_fname(path, check=False, verbose="ERROR")
                raw = mne_bids.read_raw_bids(bids_path, verbose="ERROR")
            except Exception as err:
                logger.warning(f"Reading {path} without its BIDS sidecars: mne_bids.read_raw_bids failed ({err}).")
                raw = mne.io.read_raw(path, verbose="ERROR")
        else:
            raw = mne.io.read_raw(path, verbose="ERROR")
        return raw

    def flatten(self) -> Union["FeatureType", dict[str, "FeatureType"]]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from .features import Value

        return self if self.decode else {"bytes": Value("binary"), "path": Value("string")}

    def cast_storage(self, storage: Union[pa.StringArray, pa.BinaryArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Biosignal arrow storage type.

        Args:
            storage (`Union[pa.StringArray, pa.BinaryArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Biosignal arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        return _cast_to_bytes_path_struct(storage, self.pa_type)

    def embed_storage(
        self, storage: pa.StructArray, token_per_repo_id=None, local_files: bool = True, remote_files: bool = True
    ) -> pa.StructArray:
        """Embed biosignal files into the Arrow array.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.
            token_per_repo_id (`dict`, *optional*):
                Dictionary `repo_id` -> `token` to fetch remote file bytes.
            local_files (`bool`, defaults to `True`):
                Whether to embed local files data in the array.
            remote_files (`bool`, defaults to `True`):
                Whether to embed remote files data in the array.

        Returns:
            `pa.StructArray`: Array in the Biosignal arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """

        decoder = replace(self, decode=True)
        embedded = []
        for x in storage.to_pylist():
            if x is None or x["path"] is None or not (local_files if is_local_path(x["path"]) else remote_files):
                embedded.append(x)
                continue
            name = xbasename(x["path"])
            if x["bytes"] is not None:
                embedded.append({"bytes": x["bytes"], "path": name})
                continue
            # recordings are embedded as self-contained FIF, so multi-file formats need no companion files
            raw = decoder.decode_example(x["path"], token_per_repo_id=token_per_repo_id)
            fif_name = name if name.lower().endswith(".fif") else f"{os.path.splitext(name)[0]}_raw.fif"
            embedded.append({"bytes": self.encode_example(raw)["bytes"], "path": fif_name})
        return pa.array(embedded, type=self.pa_type)
