from typing import List

import datasets
from datasets.tasks import VideoClassification

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class VideoFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """Builder Config for VideoFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None


class VideoFolder(folder_based_builder.FolderBasedBuilder):
    BASE_FEATURE = datasets.Video()
    BASE_COLUMN_NAME = "video"
    BUILDER_CONFIG_CLASS = VideoFolderConfig
    EXTENSIONS: List[str]  # definition at the bottom of the script
    CLASSIFICATION_TASK = VideoClassification(video_column="video", label_column="label")


# Obtained with:
# ```
# How to get this reliably with av without including audio-only extensions too???
# Here is an attempt...
# import av
# from pprint import pprint
# extensions = set()
# for format in av.video.format.names:
#     extensions.update(av.ContainerFormat(format).extensions)
# pprint(sorted(extensions))
# ```
# We intentionally do not run this code on launch because:
# (1) PyAV is an optional dependency, so importing it in global namespace is not allowed
# (2) To ensure the list of supported extensions is deterministic
VIDEO_EXTENSIONS = [
    ".mp4",
    ".avi",
]
VideoFolder.EXTENSIONS = VIDEO_EXTENSIONS
