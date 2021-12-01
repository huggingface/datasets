from dataclasses import dataclass
from typing import ClassVar, Dict

from ..features import Audio, Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class AutomaticSpeechRecognition(TaskTemplate):
    task: str = "automatic-speech-recognition"
    input_schema: ClassVar[Features] = Features({"audio": Audio(_storage_dtype="string")})
    label_schema: ClassVar[Features] = Features({"transcription": Value("string")})
    audio_column: str = "audio"
    transcription_column: str = "transcription"
    # set the `streaming` flag when casting streamable datasets that have `Audio` stored as `struct{path, bytes}`
    streaming: bool = False

    def __post_init__(self):
        if self.streaming:
            self.__dict__["input_schema"] = Features({"audio": Audio(_storage_dtype="struct")})

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {self.audio_column: "audio", self.transcription_column: "transcription"}
