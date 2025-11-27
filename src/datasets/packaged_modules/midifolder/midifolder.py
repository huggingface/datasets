import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class MidiFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """Builder Config for MidiFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class MidiFolder(folder_based_builder.FolderBasedBuilder):
    BASE_FEATURE = datasets.Midi
    BASE_COLUMN_NAME = "midi"
    BUILDER_CONFIG_CLASS = MidiFolderConfig
    EXTENSIONS: list[str]  # definition at the bottom of the script


# Common MIDI file extensions
MIDI_EXTENSIONS = [
    ".mid",
    ".midi",
    ".kar",  # Karaoke MIDI files
    ".rmi",  # RIFF MIDI files
]
MidiFolder.EXTENSIONS = MIDI_EXTENSIONS
