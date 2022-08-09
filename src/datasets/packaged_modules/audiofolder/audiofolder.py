from dataclasses import dataclass
from typing import ClassVar, List

import datasets

from ..base import autofolder


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class AudioFolderConfig(autofolder.AutoFolderConfig):
    """Builder Config for AudioFolder."""

    _base_feature: ClassVar = datasets.Audio()
    drop_labels: bool = True  # usually we don't need labels as classification is not the main audio task
    drop_metadata: bool = None


class AudioFolder(autofolder.AutoFolder):
    BUILDER_CONFIG_CLASS = AudioFolderConfig
    EXTENSIONS: List[str] = []  # definition at the bottom of the script

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        # _prepare_split_generators() sets self.info.features,
        # infers labels, finds metadata files if needed and returns splits
        return self._prepare_split_generators(dl_manager)

    def _generate_examples(self, files, metadata_files, split_name, add_metadata, add_labels):
        generator = self._prepare_generate_examples(files, metadata_files, split_name, add_metadata, add_labels)
        for _, example in generator:
            yield _, example


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
