from dataclasses import dataclass, field
from typing import Optional

import soundfile as sf


@dataclass
class Audio:
    id: Optional[str] = None
    _type: str = field(default="Audio", init=False, repr=False)

    def encode_example(self, value):
        with open(value, "rb") as f:
            array, sample_rate = sf.read(f)
        return {"array": array, "sample_rate": sample_rate}
