from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import pyarrow as pa


@dataclass(frozen=True)
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

    def __call__(self):
        return pa.string()

    def decode_example(self, value):
        """Decode example audio file into audio data.

        Args:
            value: Audio file path.

        Returns:
            dict
        """
        try:
            import librosa
        except ImportError:
            return value

        try:
            array, sample_rate = self._decode_example_with_librosa(value)
        except RuntimeError:
            if value.endswith(".mp3"):
                array, sample_rate = self._decode_example_with_torchaudio(value)
            else:
                raise
        return {"path": value, "array": array, "sampling_rate": sample_rate}

    def _decode_example_with_librosa(self, value):
        import librosa

        with open(value, "rb") as f:
            array, sample_rate = librosa.load(f, sr=self.sampling_rate, mono=self.mono)
        return array, sample_rate

    def _decode_example_with_torchaudio(self, value):
        try:
            import torchaudio
            import torchaudio.functional as F
        except ImportError:
            raise RuntimeError("To support decoding 'mp3' audio files, please install 'torchaudio'.")

        array, sample_rate = torchaudio.load(value)
        if self.sampling_rate and self.sampling_rate != sample_rate:
            # kaiser_best (as librosa)
            array = F.resample(
                array,
                sample_rate,
                self.sampling_rate,
                lowpass_filter_width=64,
                rolloff=0.9475937167399596,
                resampling_method="kaiser_window",
                beta=14.769656459379492
            )
        return array, self.sampling_rate
