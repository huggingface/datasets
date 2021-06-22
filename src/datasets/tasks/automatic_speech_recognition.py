from dataclasses import dataclass
from typing import ClassVar, Dict

from ..features import Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class AutomaticSpeechRecognition(TaskTemplate):
    task: str = "automatic-speech-recognition"
    input_schema: ClassVar[Features] = Features({"audio_file": Value("string")})
    label_schema: ClassVar[Features] = Features({"transcription": Value("string")})
    audio_file_column: str = "audio_file"
    transcription_column: str = "transcription"

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {self.audio_file_column: "audio_file", self.transcription_column: "transcription"}
