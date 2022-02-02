from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, ClassVar, Optional, Union

import pyarrow as pa

from ..table import array_cast
from ..utils.streaming_download_manager import xopen


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
        - sampling_rate: Integer corresponding to the samping rate of the audio sample.

      This is useful for archived files with sequential access.

    Args:
        sampling_rate (:obj:`int`, optional): Target sampling rate. If `None`, the native sampling rate is used.
        mono (:obj:`bool`, default ``True``): Whether to convert the audio signal to mono by averaging samples across
            channels.
        decode (:obj:`bool`, default ``True``): Whether to decode the audio data. If `False`,
            returns the underlying dictionary in the format {"path": audio_path, "bytes": audio_bytes}.
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
        elif isinstance(value, dict) and "array" in value:
            buffer = BytesIO()
            sf.write(buffer, value["array"], value["sampling_rate"])
            return {"bytes": buffer.getvalue(), "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"An audio sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict) -> dict:
        """Decode example audio file into audio data.

        Args:
            value (:obj:`dict`): a dictionary with keys:

                - path: String with relative audio file path.
                - bytes: Bytes of the audio file.

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
        else:
            if file:
                array, sampling_rate = self._decode_non_mp3_file_like(file)
            else:
                array, sampling_rate = self._decode_non_mp3_path_like(path)
        return {"path": path, "array": array, "sampling_rate": sampling_rate}

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Audio arrow storage type.
        The Arrow types that can be converted to the Audio pyarrow storage type are:

        - pa.string() - it must contain the "path" data
        - pa.struct({"bytes": pa.binary()})
        - pa.struct({"path": pa.string()})
        - pa.struct({"bytes": pa.binary(), "path": pa.string()})  - order doesn't matter

        Args:
            storage (Union[pa.StringArray, pa.StructArray]): [description]

        Returns:
            pa.StructArray: Array in the Audio arrow storage type, that is
                pa.struct({"bytes": pa.binary(), "path": pa.string()})
        """
        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"])
        elif pa.types.is_struct(storage.type) and storage.type.get_all_field_indices("array"):
            storage = pa.array([Audio().encode_example(x) for x in storage.to_pylist()])
        elif pa.types.is_struct(storage.type):
            if storage.type.get_field_index("bytes") >= 0:
                bytes_array = storage.field("bytes")
            else:
                bytes_array = pa.array([None] * len(storage), type=pa.binary())
            if storage.type.get_field_index("path") >= 0:
                path_array = storage.field("path")
            else:
                path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"])
        return array_cast(storage, self.pa_type)

    def _decode_non_mp3_path_like(self, path):
        try:
            import librosa
        except ImportError as err:
            raise ImportError("To support decoding audio files, please install 'librosa'.") from err

        with xopen(path, "rb") as f:
            array, sampling_rate = librosa.load(f, sr=self.sampling_rate, mono=self.mono)
        return array, sampling_rate

    def _decode_non_mp3_file_like(self, file):
        try:
            import librosa
            import soundfile as sf
        except ImportError as err:
            raise ImportError("To support decoding audio files, please install 'librosa' and 'soundfile'.") from err

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
            import torchaudio.transforms as T
        except ImportError as err:
            raise ImportError("To support decoding 'mp3' audio files, please install 'torchaudio'.") from err
        try:
            torchaudio.set_audio_backend("sox_io")
        except RuntimeError as err:
            raise ImportError("To support decoding 'mp3' audio files, please install 'sox'.") from err

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
