from dataclasses import dataclass
from typing import ClassVar


class Feature:
    """
    Base class for feature types like Audio, Image, ClassLabel, etc that require special treatment (encoding/decoding).
    """

    requires_encoding: ClassVar[bool] = False
    requires_decoding: ClassVar[bool] = False

    def encode_example(self, example):
        if self.requires_encoding:
            return self._encode_example(example)
        return example

    def decode_example(self, example):
        if self.requires_decoding:
            return self._decode_example(example)
        return example
