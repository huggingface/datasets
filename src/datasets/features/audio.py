from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import pyarrow as pa


@dataclass(unsafe_hash=True)
class Audio:
    """Audio Feature to extract audio data from an audio file.

    Args:
        sampling_rate (:obj:`int`, optional): Target sampling rate. If `None`, the native sampling rate is used.
        mono (:obj:`bool`, default ```True``): Whether to convert the audio signal to mono by averaging samples across channels.
    """

    sampling_rate: Optional[int] = None
    mono: bool = True
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Audio", init=False, repr=False)
    _resampler: Any = field(default=None, init=False, repr=False, compare=False)

    def __call__(self):
        return pa.string()

    def decode_example(self, value):
        """Decode example audio file into audio data.

        Args:
            value: Audio file path.

        Returns:
            dict
        """
        # TODO: backard compatibility for users without audio dependencies
        array, sampling_rate = (
            self._decode_example_with_torchaudio(value)
            if value.endswith(".mp3")
            else self._decode_example_with_librosa(value)
        )
        return {"path": value, "array": array, "sampling_rate": sampling_rate}

    def _decode_example_with_librosa(self, value):
        try:
            import librosa
        except ImportError as err:
            raise ImportError("To support decoding audio files, please install 'librosa'.") from err

        with open(value, "rb") as f:
            array, sampling_rate = librosa.load(f, sr=self.sampling_rate, mono=self.mono)
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
        array = array.numpy()
        if self.mono:
            array = array.mean(axis=0)
        if self.sampling_rate and self.sampling_rate != sampling_rate:
            if not self._resampler:
                self._resampler = T.Resample(sampling_rate, self.sampling_rate)
            array = self._resampler(array, sampling_rate, self.sampling_rate)
            sampling_rate = self.sampling_rate
        return array, sampling_rate

    def decode_batch(self, values):
        decoded_batch = defaultdict(list)
        for value in values:
            decoded_example = self.decode_example(value)
            for k, v in decoded_example.items():
                decoded_batch[k].append(v)
        return dict(decoded_batch)
