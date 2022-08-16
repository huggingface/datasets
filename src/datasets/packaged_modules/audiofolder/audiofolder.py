from dataclasses import dataclass
from typing import List

import datasets

from ..folder_builder import folder_builder


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class AudioFolderConfig(folder_builder.FolderBuilderConfig):
    """Builder Config for AudioFolder."""

    drop_labels: bool = True  # usually we don't need labels as classification is not the main audio task
    drop_metadata: bool = None


class AudioFolder(folder_builder.FolderBuilder):
    BASE_FEATURE = datasets.Audio()
    BUILDER_CONFIG_CLASS = AudioFolderConfig
    EXTENSIONS: List[str]  # definition at the bottom of the script


# Obtained with:
# ```
# import soundfile as sf
#
# AUDIO_EXTENSIONS = [f".{format.lower()}" for format in sf.available_formats().keys()]
#
# # .mp3 is currently decoded via `torchaudio`, .opus decoding is supported if version of `libsndfile` >= 1.0.30:
# AUDIO_EXTENSIONS.extend([".mp3", ".opus"])
# ```
# We intentionally do not run this code on launch because:
# (1) Soundfile is an optional dependency, so importing it in global namespace is not allowed
# (2) To ensure the list of supported extensions is deterministic
AUDIO_EXTENSIONS = [
    ".aiff",
    ".au",
    ".avr",
    ".caf",
    ".flac",
    ".htk",
    ".svx",
    ".mat4",
    ".mat5",
    ".mpc2k",
    ".ogg",
    ".paf",
    ".pvf",
    ".raw",
    ".rf64",
    ".sd2",
    ".sds",
    ".ircam",
    ".voc",
    ".w64",
    ".wav",
    ".nist",
    ".wavex",
    ".wve",
    ".xi",
    ".mp3",
    ".opus",
]
AudioFolder.EXTENSIONS = AUDIO_EXTENSIONS
