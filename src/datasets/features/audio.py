from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, ClassVar, Optional, Union

import pyarrow as pa

from ..utils.streaming_download_manager import xopen
from .base_extension import BasePyarrowExtensionType


class AudioExtensionType(BasePyarrowExtensionType):
    pa_storage_type = pa.struct({"bytes": pa.binary(), "path": pa.string()})

    def cast_storage(self, array: Union[pa.StringArray, pa.StructArray]) -> pa.StructArray:
        if array.type == AudioExtensionType():
            return array
        elif array.type == pa.struct({"bytes": pa.binary(), "paths": pa.string()}):
            return self.wrap_array(array)
        elif isinstance(array.type, pa.StructType):
            subarrays = {array.type[i].name: array.field(i) for i in range(array.type.num_fields)}
            bytes_array = (
                subarrays["bytes"].cast(pa.binary())
                if "bytes" in subarrays
                else pa.array([None] * len(array), type=pa.binary())
            )
            path_array = (
                subarrays["path"].cast(pa.string())
                if "path" in subarrays
                else pa.array([None] * len(array), type=pa.string())
            )
            return self.wrap_array(pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"]))
        elif array.type == pa.string():
            bytes_array = pa.array([None] * len(array), type=pa.binary())
            return self.wrap_array(pa.StructArray.from_arrays([bytes_array, array], ["bytes", "path"]))
        else:
            raise TypeError(f"Can't convert array of type {array.type} to audio type {type(self)}.")


@dataclass(unsafe_hash=True)
class Audio:
    """Audio Feature to extract audio data from an audio file.

    Input: The Audio feature accepts as input:
    - A :obj:`str`: Absolute path to the audio file (i.e. random access is allowed).
    - A :obj:`dict` with the keys:

        - path: String with relative path of the audio file to the archive file.
        - bytes: Bytes content of the audio file.

      This is useful for archived files with sequential access.

    Args:
        sampling_rate (:obj:`int`, optional): Target sampling rate. If `None`, the native sampling rate is used.
        mono (:obj:`bool`, default ``True``): Whether to convert the audio signal to mono by averaging samples across
            channels.
    """

    sampling_rate: Optional[int] = None
    mono: bool = True
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = AudioExtensionType
    _type: str = field(default="Audio", init=False, repr=False)

    def __call__(self):
        return self.pa_type()

    def encode_example(self, value):
        """Encode example into a format for Arrow.

        Args:
            value (:obj:`str` or :obj:`dict`): Data passed as input to Audio feature.

        Returns:
            :obj:`dict`
        """
        return {"bytes": None, "path": value} if isinstance(value, str) else value

    def decode_example(self, value):
        """Decode example audio file into audio data.

        Args:
            value (:obj:`dict`): a dictionary with keys:

                - path: String with relative audio file path.
                - bytes: Bytes of the audio file.

        Returns:
            dict
        """
        path, file = (value["path"], BytesIO(value["bytes"])) if value["bytes"] is not None else (value["path"], None)
        if path.endswith("mp3"):
            array, sampling_rate = self._decode_mp3(file if file else path)
        else:
            if file:
                array, sampling_rate = self._decode_non_mp3_file_like(file)
            else:
                array, sampling_rate = self._decode_non_mp3_path_like(path)
        return {"path": path, "array": array, "sampling_rate": sampling_rate}

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
            raise ImportError("To support decoding audio files, please install 'librosa'.") from err

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
            if not hasattr(self, "_resampler"):
                self._resampler = T.Resample(sampling_rate, self.sampling_rate)
            array = self._resampler(array)
            sampling_rate = self.sampling_rate
        array = array.numpy()
        if self.mono:
            array = array.mean(axis=0)
        return array, sampling_rate
