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

    sampling_rate: int = None
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

        with open(value, "rb") as f:
            array, sample_rate = librosa.load(f, sr=self.sampling_rate, mono=self.mono)
        return {"path": value, "array": array, "sampling_rate": sample_rate}
