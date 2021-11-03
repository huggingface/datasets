from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import numpy as np
import pyarrow as pa


@dataclass(unsafe_hash=True)
class Image:
    """Image Feature to extract image data from an image file.

    Args:
        mode (:obj:`str`, optional): Target image mode. If `None`, the mode is infered from the underlying image data.
            The list of supported modes is available `here <https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes>`_.
    """

    mode: Optional[str] = None
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Image", init=False, repr=False)

    def __post_init__(self):
        if self.mode is not None:
            try:
                from PIL import ImageMode
            except ImportError as err:
                raise ImportError("To use the Image feature, please install 'Pillow'.") from err

            try:
                ImageMode.getmode(self.mode)
            except KeyError as err:
                raise ValueError(
                    f"Mode {err} is not supported. For the list of available modes, "
                    f"see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes."
                ) from None

    def __call__(self):
        return pa.string()

    def decode_example(self, value):
        """Decode example image file into image data.

        Args:
            value: Image file path.

        Returns:
            dict
        """
        try:
            from PIL import Image
        except ImportError as err:
            raise ImportError("To support decoding image files, please install 'Pillow'.") from err

        image = Image.open(value)

        if self.mode is not None and self.mode != image.mode:
            image = image.convert(self.mode)

        mode = image.mode

        array = np.array(image)
        # Add a third axis to a single-channel image
        if array.ndim == 2:
            array = array[..., np.newaxis]
        assert array.ndim == 3
        # Reorder channels: (H, W, C) -> (C, H, W)
        array = array.transpose(2, 0, 1)

        return {"path": value, "array": array, "mode": mode}

    def decode_batch(self, values):
        decoded_batch = defaultdict(list)
        for value in values:
            decoded_example = self.decode_example(value)
            for k, v in decoded_example.items():
                decoded_batch[k].append(v)
        return dict(decoded_batch)
