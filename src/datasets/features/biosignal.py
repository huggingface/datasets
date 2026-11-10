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


_MULTIFILE_EXTENSIONS = {".vhdr", ".set", ".ds", ".mefd"}


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

    When decoding a local file located inside a BIDS dataset (a directory hierarchy containing
    `dataset_description.json`) and `mne-bids` is installed, `mne_bids.read_raw_bids` is used
    automatically so BIDS sidecars (`events.tsv`, `channels.tsv`, `electrodes.tsv`, `participants.tsv`,
    and JSON metadata) are attached to the returned `mne.io.BaseRaw` object.

    Args:
        preload (`bool`, defaults to `False`):
            Whether to preload the signal data into memory when reading local files.
        decode (`bool`, defaults to `True`):
            Whether to decode the biosignal data. If `False`,
            returns the underlying dictionary in the format `{"path": path, "bytes": bytes}`.

    Examples:

    ```py
    >>> from datasets import Dataset, Biosignal
    >>> ds = Dataset.from_dict({"biosignal": ["path/to/sub-01_task-rest_eeg.edf"]}).cast_column("biosignal", Biosignal())
    >>> ds.features["biosignal"]
    Biosignal(preload=False, decode=True)
    >>> raw = ds[0]["biosignal"]
    >>> raw.info["sfreq"]
    256.0
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
        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": bytes(value)}
        elif isinstance(value, dict):
            if value.get("path") is not None and os.path.exists(value["path"]):
                return {"bytes": None, "path": value.get("path")}
            elif value.get("bytes") is not None or value.get("path") is not None:
                return {"bytes": value.get("bytes"), "path": value.get("path")}
            raise ValueError(
                f"A biosignal sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )
        elif config.MNE_AVAILABLE:
            import mne

            if isinstance(value, mne.io.BaseRaw):
                filenames = getattr(value, "filenames", None)
                stem = Path(filenames[0]).stem if filenames and filenames[0] else "biosignal"
                if not stem.endswith(("raw", "_eeg", "_meg", "_ieeg")):
                    stem = f"{stem}_raw"
                fname = f"{stem}.fif"
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_path = os.path.join(tmpdir, fname)
                    value.save(tmp_path, overwrite=True, verbose="ERROR")
                    with open(tmp_path, "rb") as f:
                        return {"path": fname, "bytes": f.read()}
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

        if token_per_repo_id is None:
            token_per_repo_id = {}

        if isinstance(value, str):
            path, bytes_ = value, None
        else:
            path, bytes_ = value["path"], value["bytes"]

        if bytes_ is None:
            if path is None:
                raise ValueError(f"A biosignal should have one of 'path' or 'bytes' but both are None in {value}.")
            if is_local_path(path):
                if config.MNE_BIDS_AVAILABLE:
                    import mne_bids

                    try:
                        bids_path = mne_bids.get_bids_path_from_fname(path, check=False, verbose="ERROR")
                        if bids_path.subject is not None:
                            return mne_bids.read_raw_bids(
                                bids_path, extra_params={"preload": self.preload}, verbose="ERROR"
                            )
                    except Exception:
                        pass
                return mne.io.read_raw(path, preload=self.preload, verbose="ERROR")
            download_config = DownloadConfig(token=_resolve_token(path, token_per_repo_id))
            with xopen(path, "rb", download_config=download_config) as f:
                bytes_ = f.read()

        fname = os.path.basename(path) if path and os.path.splitext(path)[1] else "biosignal_raw.fif"
        if fname.lower().endswith((".fif", ".fif.gz")):
            return mne.io.read_raw_fif(io.BytesIO(bytes_), preload=True, verbose="ERROR")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = os.path.join(tmpdir, fname)
            with open(tmp_path, "wb") as f:
                f.write(bytes_)
            return mne.io.read_raw(tmp_path, preload=True, verbose="ERROR")

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
        """Embed biosignal files into the Arrow array.

        For multi-file formats (e.g. BrainVision `.vhdr`, EEGLAB `.set`) or local files inside a BIDS
        dataset when `mne` is installed, the recording (along with any BIDS sidecar metadata) is
        serialized into self-contained `.fif` bytes so that hub uploads preserve all channels,
        annotations, and montages. Single-file recordings outside BIDS are embedded directly as raw bytes.
        """
        if token_per_repo_id is None:
            token_per_repo_id = {}

        @no_op_if_value_is_null
        def path_to_embedded(path: str) -> tuple[bytes, str]:
            if is_local_path(path) and config.MNE_AVAILABLE:
                fpath = Path(path)
                if fpath.suffix.lower() in _MULTIFILE_EXTENSIONS or fpath.is_dir() or fpath.name.startswith("sub-"):
                    try:
                        encoded = self.encode_example(Biosignal(preload=True).decode_example(path))
                        return encoded["bytes"], encoded["path"]
                    except Exception:
                        pass
            download_config = DownloadConfig(token=_resolve_token(path, token_per_repo_id))
            with xopen(path, "rb", download_config=download_config) as f:
                return f.read(), os.path.basename(path)

        def should_embed(path: Optional[str]) -> bool:
            if path is None:
                return False
            return local_files if is_local_path(path) else remote_files

        new_bytes = []
        new_paths = []
        for bytes_, path in zip(storage.field("bytes").to_pylist(), storage.field("path").to_pylist()):
            if bytes_ is None and should_embed(path):
                embedded_bytes, embedded_path = path_to_embedded(path)
                new_bytes.append(embedded_bytes)
                new_paths.append(embedded_path)
            else:
                new_bytes.append(bytes_)
                new_paths.append(os.path.basename(path) if path is not None else None)

        bytes_array = pa.array(new_bytes, type=pa.binary())
        path_array = pa.array(new_paths, type=pa.string())
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=storage.is_null())
        return array_cast(storage, self.pa_type)
