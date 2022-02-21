import os
import re
from dataclasses import dataclass
from typing import Optional

import datasets
from datasets.tasks.image_classification import ImageClassification


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class ImageFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for ImageFolder."""

    features: Optional[datasets.Features] = None


class ImageFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = ImageFolderConfig

    IMAGE_EXTENSIONS = []  # defined at the bottom of the script
    CLASS_PATTERN_RE = re.compile(r"\w+")

    def __init__(self, *args, **kwargs):
        self.prefixes = {}
        self.class_names = set()
        super().__init__(*args, **kwargs)

    @classmethod
    def _get_class_name(cls, prefix: str, file: str) -> str:
        file_name = os.path.basename(file)
        sub_path = file[len(prefix) : -len(file_name)]
        for class_name_match in cls.CLASS_PATTERN_RE.finditer(sub_path):
            return class_name_match.group()

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        # ignore non-image files to not "pollute" the prefix computation 
        image_data_files = {}
        for split, files in self.config.data_files.items():
            image_files = []
            for file in files:
                file = str(file)
                _, file_ext = os.path.splitext(file)
                if file_ext in self.IMAGE_EXTENSIONS:
                    image_files.append(file)
            image_data_files[str(split)] = image_files

        if self.config.features is None:
            for split, files in image_data_files.items():
                prefix = os.path.commonprefix(files)
                self.prefixes[split] = prefix
                for file in files:
                    self.class_names.add(self._get_class_name(prefix, file))
            if self.class_names:
                self.info.features = datasets.Features(
                    {"image": datasets.Image(), "label": datasets.ClassLabel(names=sorted(self.class_names))}
                )
                self.info.task_templates = [ImageClassification(image_column="image", label_column="label")]

        data_files = image_data_files
        downloaded_data_files = dl_manager.download(data_files)
        splits = []
        for split_name, files in data_files.items():
            downloaded_files = downloaded_data_files[split_name]
            if isinstance(files, str):
                files, downloaded_files = [files], [downloaded_files]
            splits.append(
                datasets.SplitGenerator(
                    name=split_name, gen_kwargs={"files": zip(downloaded_files, files), "split": split_name}
                )
            )
        return splits

    def _generate_examples(self, files, split):
        prefix = self.prefixes[split]
        for i, (file, downloaded_file) in enumerate(files):
            if self.class_names:
                ex = {"image": downloaded_file, "label": self._get_class_name(prefix, file)}
            else:
                ex = {"image": downloaded_file}
            yield i, ex


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
ImageFolder.IMAGE_EXTENSIONS = [
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
