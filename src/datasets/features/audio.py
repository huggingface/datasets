from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional


@dataclass
class Audio:
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Audio", init=False, repr=False)

    def encode_example(self, value):
        import soundfile as sf

        with open(value, "rb") as f:
            array, sample_rate = sf.read(f)
        return {"array": array, "sample_rate": sample_rate}
