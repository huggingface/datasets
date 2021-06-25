from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

import pyarrow as pa


@dataclass
class Audio:
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Audio", init=False, repr=False)

    def __call__(self):
        return pa.struct({"array": pa.array(), "sample_rate": pa.int32()})

    def encode_example(self, value):
        import soundfile as sf

        with open(value, "rb") as f:
            array, sample_rate = sf.read(f)
        return {"array": array, "sample_rate": sample_rate}
