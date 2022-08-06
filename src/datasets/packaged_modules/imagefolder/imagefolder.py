from dataclasses import dataclass
from typing import ClassVar, List

import datasets
from datasets.tasks import ImageClassification

from ..base import autofolder


logger = datasets.utils.logging.get_logger(__name__)


IMAGE_FEATURE = datasets.Image()
IMAGE_FEATURE.__name__ = "image"  # set __name__ to enable documentation building


@dataclass
class ImageFolderConfig(autofolder.AutoFolderConfig):
    """BuilderConfig for ImageFolder."""

    base_feature: ClassVar = IMAGE_FEATURE
    drop_labels: bool = None
    drop_metadata: bool = None


class ImageFolder(autofolder.AutoFolder):
    BUILDER_CONFIG_CLASS = ImageFolderConfig
    EXTENSIONS: List[str] = []  # definition at the bottom of the script

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        # _prepare_split_generators() sets self.info.features,
        # infers labels, finds metadata files if needed and returns splits
        splits = self._prepare_split_generators(dl_manager)

        add_labels = splits[0].gen_kwargs["add_labels"]
        if self.config.features is None and add_labels:
            task_template = ImageClassification(
                image_column=self.config.base_feature_name, label_column=self.config.label_column
            )
            task_template = task_template.align_with_features(self.info.features)
            self.info.task_templates = [task_template]

        return splits

    def _generate_examples(self, files, metadata_files, split_name, add_metadata, add_labels):
        generator = self._prepare_generate_examples(files, metadata_files, split_name, add_metadata, add_labels)
        for _, example in generator:
            yield _, example


# Obtained with:
# ```
# import PIL.Image
# IMAGE_EXTENSIONS = []
# PIL.Image.init()
# for ext, format in PIL.Image.EXTENSION.items():
#     if format in PIL.Image.OPEN:
#         IMAGE_EXTENSIONS.append(ext[1:])
# ```
# We intentionally do not run this code on launch because:
# (1) Pillow is an optional dependency, so importing Pillow in global namespace is not allowed
# (2) To ensure the list of supported extensions is deterministic
IMAGE_EXTENSIONS = [
    ".blp",
    ".bmp",
    ".dib",
    ".bufr",
    ".cur",
    ".pcx",
    ".dcx",
    ".dds",
    ".ps",
    ".eps",
    ".fit",
    ".fits",
    ".fli",
    ".flc",
    ".ftc",
    ".ftu",
    ".gbr",
    ".gif",
    ".grib",
    ".h5",
    ".hdf",
    ".png",
    ".apng",
    ".jp2",
    ".j2k",
    ".jpc",
    ".jpf",
    ".jpx",
    ".j2c",
    ".icns",
    ".ico",
    ".im",
    ".iim",
    ".tif",
    ".tiff",
    ".jfif",
    ".jpe",
    ".jpg",
    ".jpeg",
    ".mpg",
    ".mpeg",
    ".msp",
    ".pcd",
    ".pxr",
    ".pbm",
    ".pgm",
    ".ppm",
    ".pnm",
    ".psd",
    ".bw",
    ".rgb",
    ".rgba",
    ".sgi",
    ".ras",
    ".tga",
    ".icb",
    ".vda",
    ".vst",
    ".webp",
    ".wmf",
    ".emf",
    ".xbm",
    ".xpm",
]
ImageFolder.EXTENSIONS = IMAGE_EXTENSIONS
