import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class VideoFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for ImageFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class VideoFolder(folder_based_builder.FolderBasedBuilder):
    BASE_FEATURE = datasets.Video
    BASE_COLUMN_NAME = "video"
    BUILDER_CONFIG_CLASS = VideoFolderConfig
    EXTENSIONS: list[str]  # definition at the bottom of the script


# TODO: initial list, we should check the compatibility of other formats
VIDEO_EXTENSIONS = [
    ".mkv",
    ".mp4",
    ".avi",
    ".mpeg",
    ".mov",
]
VideoFolder.EXTENSIONS = VIDEO_EXTENSIONS
