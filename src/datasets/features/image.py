from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import pyarrow as pa


@dataclass
class Image:
    """Image Feature to extract image data from an image file.
    """

    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Image", init=False, repr=False)

    def __call__(self):
        return pa.string()

    def decode_example(self, value):
        """Decode example image file into image data.

        Args:
            value: Image file path.

        Returns:
            dict
        """
        array, sampling_rate = (
            self._decode_example_with_torchaudio(value)
            if value.endswith(".mp3")
            else self._decode_example_with_librosa(value)
        )
        return {"path": value, "array": array, "sampling_rate": sampling_rate}

    def decode_batch(self, values):
        decoded_batch = defaultdict(list)
        for value in values:
            decoded_example = self.decode_example(value)
            for k, v in decoded_example.items():
                decoded_batch[k].append(v)
        return dict(decoded_batch)
