from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import pyarrow as pa


@dataclass
class Audio:
    """Audio Feature to extract audio data from an audio file.

    Args:
        coding_format (:obj:`str`, optional): Audio coding format. If `None`, this is inferred from file.
    """

    coding_format: str = None
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Audio", init=False, repr=False)

    def __post_init__(self):
        self.coding_format = self.coding_format.upper() if self.coding_format else None

    def __call__(self):
        return pa.string()

    def decode_example(self, value):
        """Decode example audio file into audio data.

        Args:
            value: Audio file path.

        Returns:
            dict
        """
        import soundfile as sf

        if self.coding_format and self.coding_format not in self._supported_coding_formats:
            raise ValueError(
                f"Audio coding format {self.coding_format} is not supported. Audio coding format must be "
                f"one of: {self._supported_coding_formats}"
            )

        with open(value, "rb") as f:
            array, sample_rate = sf.read(f, format=self.coding_format)
        return {"array": array.reshape(-1), "sample_rate": sample_rate}

    @property
    def _supported_coding_formats(self):
        import soundfile as sf

        return list(sf.available_formats().keys())
