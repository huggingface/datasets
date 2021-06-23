from dataclasses import dataclass
from typing import ClassVar, Dict

from ..features import Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class AutomaticSpeechRecognition(TaskTemplate):
    task: str = "automatic-speech-recognition"
    # TODO(lewtun): Replace input path feature with dedicated `Audio` features
    # when https://github.com/huggingface/datasets/pull/2324 is implemented
    input_schema: ClassVar[Features] = Features({"audio_file_path": Value("string")})
    label_schema: ClassVar[Features] = Features({"transcription": Value("string")})
    audio_file_path_column: str = "audio_file_path"
    transcription_column: str = "transcription"

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {self.audio_file_path_column: "audio_file_path", self.transcription_column: "transcription"}
