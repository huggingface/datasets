import os
import warnings
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union

import numpy as np
import pyarrow as pa
from packaging import version

from .. import config
from ..download.streaming_download_manager import xopen
from ..table import array_cast
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


if TYPE_CHECKING:
    from .features import FeatureType


@dataclass
class Audio:
    """Audio Feature to extract audio data from an audio file.

    Input: The Audio feature accepts as input:
    - A :obj:`str`: Absolute path to the audio file (i.e. random access is allowed).
    - A :obj:`dict` with the keys:

        - path: String with relative path of the audio file to the archive file.
        - bytes: Bytes content of the audio file.

      This is useful for archived files with sequential access.

    - A :obj:`dict` with the keys:

        - path: String with relative path of the audio file to the archive file.
        - array: Array containing the audio sample
        - sampling_rate: Integer corresponding to the sampling rate of the audio sample.

      This is useful for archived files with sequential access.

    Args:
        sampling_rate (:obj:`int`, optional): Target sampling rate. If `None`, the native sampling rate is used.
        mono (:obj:`bool`, default ``True``): Whether to convert the audio signal to mono by averaging samples across
            channels.
        decode (:obj:`bool`, default ``True``): Whether to decode the audio data. If `False`,
            returns the underlying dictionary in the format {"path": audio_path, "bytes": audio_bytes}.

    Example:

    ```py
    >>> from datasets import load_dataset, Audio
    >>> ds = load_dataset("PolyAI/minds14", name="en-US", split="train")
    >>> ds = ds.cast_column("audio", Audio(sampling_rate=16000))
    >>> ds[0]["audio"]
    {'array': array([ 2.3443763e-05,  2.1729663e-04,  2.2145823e-04, ...,
         3.8356509e-05, -7.3497440e-06, -2.1754686e-05], dtype=float32),
     'path': '/root/.cache/huggingface/datasets/downloads/extracted/f14948e0e84be638dd7943ac36518a4cf3324e8b7aa331c5ab11541518e9368c/en-US~JOINT_ACCOUNT/602ba55abb1e6d0fbce92065.wav',
     'sampling_rate': 16000}
    ```
    """

    sampling_rate: Optional[int] = None
    mono: bool = True
    decode: bool = True
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Audio", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, dict]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (:obj:`str` or :obj:`dict`): Data passed as input to Audio feature.

        Returns:
            :obj:`dict`
        """
        try:
            import soundfile as sf  # soundfile is a dependency of librosa, needed to decode audio files.
        except ImportError as err:
            raise ImportError("To support encoding audio data, please install 'soundfile'.") from err
        if isinstance(value, str):
            return {"bytes": None, "path": value}
        elif "array" in value:
            # convert the audio array to wav bytes
            buffer = BytesIO()
            sf.write(buffer, value["array"], value["sampling_rate"], format="wav")
            return {"bytes": buffer.getvalue(), "path": None}
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            if value["path"].endswith("pcm"):
                # "PCM" only has raw audio bytes
                if value.get("sampling_rate") is None:
                    # At least, If you want to convert "PCM-byte" to "WAV-byte", you have to know sampling rate
                    raise KeyError("To use PCM files, please specify a 'sampling_rate' in Audio object")
                if value.get("bytes"):
                    # If we already had PCM-byte, we don`t have to make "read file, make bytes" (just use it!)
                    bytes_value = np.frombuffer(value["bytes"], dtype=np.int16).astype(np.float32) / 32767
                else:
                    bytes_value = np.memmap(value["path"], dtype="h", mode="r").astype(np.float32) / 32767

                buffer = BytesIO(bytes())
                sf.write(buffer, bytes_value, value["sampling_rate"], format="wav")
                return {"bytes": buffer.getvalue(), "path": None}
            else:
                return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            # store the audio bytes, and path is used to infer the audio format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"An audio sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(
        self, value: dict, token_per_repo_id: Optional[Dict[str, Union[str, bool, None]]] = None
    ) -> dict:
        """Decode example audio file into audio data.

        Args:
            value (:obj:`dict`): a dictionary with keys:

                - path: String with relative audio file path.
                - bytes: Bytes of the audio file.
            token_per_repo_id (:obj:`dict`, optional): To access and decode
                audio files from private repositories on the Hub, you can pass
                a dictionary repo_id (str) -> token (bool or str)

        Returns:
            dict
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Audio(decode=True) instead.")

        path, file = (value["path"], BytesIO(value["bytes"])) if value["bytes"] is not None else (value["path"], None)
        if path is None and file is None:
            raise ValueError(f"An audio sample should have one of 'path' or 'bytes' but both are None in {value}.")
        elif path is not None and path.endswith("mp3"):
            array, sampling_rate = self._decode_mp3(file if file else path)
        elif path is not None and path.endswith("opus"):
            if file:
                array, sampling_rate = self._decode_non_mp3_file_like(file, "opus")
            else:
                array, sampling_rate = self._decode_non_mp3_path_like(
                    path, "opus", token_per_repo_id=token_per_repo_id
                )
        else:
            if file:
                array, sampling_rate = self._decode_non_mp3_file_like(file)
            else:
                array, sampling_rate = self._decode_non_mp3_path_like(path, token_per_repo_id=token_per_repo_id)
        return {"path": path, "array": array, "sampling_rate": sampling_rate}

    def flatten(self) -> Union["FeatureType", Dict[str, "FeatureType"]]:
        """If in the decodable state, raise an error, otherwise flatten the feature into a dictionary."""
        from .features import Value

        if self.decode:
            raise ValueError("Cannot flatten a decoded Audio feature.")
        return {
            "bytes": Value("binary"),
            "path": Value("string"),
        }

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Audio arrow storage type.
        The Arrow types that can be converted to the Audio pyarrow storage type are:

        - pa.string() - it must contain the "path" data
        - pa.struct({"bytes": pa.binary()})
        - pa.struct({"path": pa.string()})
        - pa.struct({"bytes": pa.binary(), "path": pa.string()})  - order doesn't matter

        Args:
            storage (Union[pa.StringArray, pa.StructArray]): PyArrow array to cast.

        Returns:
            pa.StructArray: Array in the Audio arrow storage type, that is
                pa.struct({"bytes": pa.binary(), "path": pa.string()})
        """
        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_struct(storage.type) and storage.type.get_all_field_indices("array"):
            storage = pa.array([Audio().encode_example(x) if x is not None else None for x in storage.to_pylist()])
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

    def embed_storage(self, storage: pa.StructArray, drop_paths: bool = True) -> pa.StructArray:
        """Embed audio files into the Arrow array.

        Args:
            storage (pa.StructArray): PyArrow array to embed.
            drop_paths (bool, default ``True``): If True, the paths are set to None.

        Returns:
            pa.StructArray: Array in the Audio arrow storage type, that is
                pa.struct({"bytes": pa.binary(), "path": pa.string()})
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
        path_array = pa.array([None] * len(storage), type=pa.string()) if drop_paths else storage.field("path")
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null())
        return array_cast(storage, self.pa_type)

    def _decode_non_mp3_path_like(
        self, path, format=None, token_per_repo_id: Optional[Dict[str, Union[str, bool, None]]] = None
    ):
        try:
            import librosa
        except ImportError as err:
            raise ImportError("To support decoding audio files, please install 'librosa'.") from err

        token_per_repo_id = token_per_repo_id or {}
        if format == "opus":
            import soundfile

            if version.parse(soundfile.__libsndfile_version__) < version.parse("1.0.30"):
                raise RuntimeError(
                    "Decoding .opus files requires 'libsndfile'>=1.0.30, "
                    + "it can be installed via conda: `conda install -c conda-forge libsndfile>=1.0.30`"
                )
        source_url = path.split("::")[-1]
        try:
            repo_id = string_to_dict(source_url, config.HUB_DATASETS_URL)["repo_id"]
            use_auth_token = token_per_repo_id[repo_id]
        except (ValueError, KeyError):
            use_auth_token = None

        with xopen(path, "rb", use_auth_token=use_auth_token) as f:
            array, sampling_rate = librosa.load(f, sr=self.sampling_rate, mono=self.mono)
        return array, sampling_rate

    def _decode_non_mp3_file_like(self, file, format=None):
        try:
            import librosa
            import soundfile as sf
        except ImportError as err:
            raise ImportError("To support decoding audio files, please install 'librosa' and 'soundfile'.") from err

        if format == "opus":
            if version.parse(sf.__libsndfile_version__) < version.parse("1.0.30"):
                raise RuntimeError(
                    "Decoding .opus files requires 'libsndfile'>=1.0.30, "
                    + 'it can be installed via conda: `conda install -c conda-forge "libsndfile>=1.0.30"`'
                )
        array, sampling_rate = sf.read(file)
        array = array.T
        if self.mono:
            array = librosa.to_mono(array)
        if self.sampling_rate and self.sampling_rate != sampling_rate:
            array = librosa.resample(array, sampling_rate, self.sampling_rate, res_type="kaiser_best")
            sampling_rate = self.sampling_rate
        return array, sampling_rate

    def _decode_mp3(self, path_or_file):
        try:
            import torchaudio
        except ImportError as err:
            raise ImportError("To support decoding 'mp3' audio files, please install 'torchaudio'.") from err
        if version.parse(torchaudio.__version__) < version.parse("0.12.0"):
            try:
                torchaudio.set_audio_backend("sox_io")
            except RuntimeError as err:
                raise ImportError("To support decoding 'mp3' audio files, please install 'sox'.") from err
            array, sampling_rate = self._decode_mp3_torchaudio(path_or_file)
        else:
            try:  # try torchaudio anyway because sometimes it works (depending on the os and os packages installed)
                array, sampling_rate = self._decode_mp3_torchaudio(path_or_file)
            except RuntimeError:
                try:
                    # flake8: noqa
                    import librosa
                except ImportError as err:
                    raise ImportError(
                        "Your version of `torchaudio` (>=0.12.0) doesn't support decoding 'mp3' files on your machine. "
                        "To support 'mp3' decoding with `torchaudio>=0.12.0`, please install `ffmpeg>=4` system package "
                        'or downgrade `torchaudio` to <0.12: `pip install "torchaudio<0.12"`. '
                        "To support decoding 'mp3' audio files without `torchaudio`, please install `librosa`: "
                        "`pip install librosa`. Note that decoding will be extremely slow in that case."
                    ) from err
                # try to decode with librosa for torchaudio>=0.12.0 as a workaround
                warnings.warn("Decoding mp3 with `librosa` instead of `torchaudio`, decoding is slow.")
                try:
                    array, sampling_rate = self._decode_mp3_librosa(path_or_file)
                except RuntimeError as err:
                    raise RuntimeError(
                        "Decoding of 'mp3' failed, probably because of streaming mode "
                        "(`librosa` cannot decode 'mp3' file-like objects, only path-like)."
                    ) from err

        return array, sampling_rate

    def _decode_mp3_torchaudio(self, path_or_file):
        import torchaudio
        import torchaudio.transforms as T

        array, sampling_rate = torchaudio.load(path_or_file, format="mp3")
        if self.sampling_rate and self.sampling_rate != sampling_rate:
            if not hasattr(self, "_resampler") or self._resampler.orig_freq != sampling_rate:
                self._resampler = T.Resample(sampling_rate, self.sampling_rate)
            array = self._resampler(array)
            sampling_rate = self.sampling_rate
        array = array.numpy()
        if self.mono:
            array = array.mean(axis=0)
        return array, sampling_rate

    def _decode_mp3_librosa(self, path_or_file):
        import librosa

        array, sampling_rate = librosa.load(path_or_file, mono=self.mono, sr=self.sampling_rate)
        return array, sampling_rate
