from collections import defaultdict
from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, ClassVar, Optional

import pyarrow as pa


@dataclass(unsafe_hash=True)
class Audio:
    """Audio Feature to extract audio data from an audio file.

    Input: The Audio feature accepts as input:
    - A :obj:`str`: Absolute path to the audio file (i.e. random access is allowed).
    - A :obj:`dict` with the keys:

        - path: String with relative path of the audio file to the archive file.
        - bytes: Bytes of the audio file.
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
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Audio", init=False, repr=False)

    def __call__(self):
        return pa.struct({"path": pa.string(), "bytes": pa.binary()})

    def encode_example(self, value):
        """Encode example into a format for Arrow.

        Args:
            value (:obj:`str` or :obj:`dict`): Data passed as input to Audio feature.

        Returns:
            :obj:`dict`
        """
        if isinstance(value, str):
            return {"path": value}
        return value

    def decode_example(self, value):
        """Decode example audio file into audio data.

        Args:
            value (:obj:`dict`): Dictionary with keys:

                - path: String with absolute or relative audio file path.
                - bytes: Optionally, the bytes of the audio file.

        Returns:
            dict
        """
        if value["bytes"]:
            path, file = value["path"], BytesIO(value["bytes"])
            array, sampling_rate = (
                self._decode_example_with_torchaudio(file)
                if path.endswith(".mp3")
                else self._decode_example_with_soundfile(file)
            )
        else:
            path = value["path"]
            array, sampling_rate = (
                self._decode_example_with_torchaudio(path)
                if path.endswith(".mp3")
                else self._decode_example_with_librosa(path)
            )
        return {"path": path, "array": array, "sampling_rate": sampling_rate}

    def _decode_example_with_librosa(self, value):
        try:
            import librosa
        except ImportError as err:
            raise ImportError("To support decoding audio files, please install 'librosa'.") from err

        with open(value, "rb") as f:
            array, sampling_rate = librosa.load(f, sr=self.sampling_rate, mono=self.mono)
        return array, sampling_rate

    def _decode_example_with_soundfile(self, file):
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

    def _decode_example_with_torchaudio(self, value):
        try:
            import torchaudio
            import torchaudio.transforms as T
        except ImportError as err:
            raise ImportError("To support decoding 'mp3' audio files, please install 'torchaudio'.") from err
        try:
            torchaudio.set_audio_backend("sox_io")
        except RuntimeError as err:
            raise ImportError("To support decoding 'mp3' audio files, please install 'sox'.") from err

        array, sampling_rate = torchaudio.load(value)
        if self.sampling_rate and self.sampling_rate != sampling_rate:
            if not hasattr(self, "_resampler"):
                self._resampler = T.Resample(sampling_rate, self.sampling_rate)
            array = self._resampler(array)
            sampling_rate = self.sampling_rate
        array = array.numpy()
        if self.mono:
            array = array.mean(axis=0)
        return array, sampling_rate

    def decode_batch(self, values):
        decoded_batch = defaultdict(list)
        for value in values:
            decoded_example = self.decode_example(value)
            for k, v in decoded_example.items():
                decoded_batch[k].append(v)
        return dict(decoded_batch)
