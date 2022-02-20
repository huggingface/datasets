import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pyarrow as pa

import datasets


logger = datasets.utils.logging.get_logger(__name__)

# Obtained with:
# ```
# import PIL.Image
# IMAGE_EXTENSIONS = []
# PIL.Image.init()
# for ext, format in PIL.Image.EXTENSION.items():
# if format in PIL.Image.OPEN:
#     IMAGE_EXTENSIONS.append(ext[1:])
# ```
# We intentionally do not run this code on launch because:
# (1) Pillow is an optional dependency, so importing Pillow in global namespace is not allowed
# (2) To ensure the list of supported extensions is deterministic
IMAGE_EXTENSIONS = [
    "blp",
    "bmp",
    "dib",
    "bufr",
    "cur",
    "pcx",
    "dcx",
    "dds",
    "ps",
    "eps",
    "fit",
    "fits",
    "fli",
    "flc",
    "ftc",
    "ftu",
    "gbr",
    "gif",
    "grib",
    "h5",
    "hdf",
    "png",
    "apng",
    "jp2",
    "j2k",
    "jpc",
    "jpf",
    "jpx",
    "j2c",
    "icns",
    "ico",
    "im",
    "iim",
    "tif",
    "tiff",
    "jfif",
    "jpe",
    "jpg",
    "jpeg",
    "mpg",
    "mpeg",
    "msp",
    "pcd",
    "pxr",
    "pbm",
    "pgm",
    "ppm",
    "pnm",
    "psd",
    "bw",
    "rgb",
    "rgba",
    "sgi",
    "ras",
    "tga",
    "icb",
    "vda",
    "vst",
    "webp",
    "wmf",
    "emf",
    "xbm",
    "xpm",
]


@dataclass
class ImageFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for ImageFolder."""

    features: Optional[datasets.Features] = None

    @property
    def schema(self):
        return pa.schema(self.features.type) if self.features is not None else None


class ImageFolder(datasets.GeneratorBasedBuilder):
    _CLASS_PATTERN = r"\w+"

    BUILDER_CONFIG_CLASS = ImageFolderConfig

    def __init__(self, *args, **kwargs):
        self.prefixes = {}
        super().__init__(*args, **kwargs)

    def _get_class_name(self, split: str, file: str) -> str:
        prefix = self.prefixes[split]
        sub_path = str(file)[len(prefix) :]
        for class_name_match in re.finditer(self._CLASS_PATTERN, sub_path):
            return class_name_match.group()
        raise ValueError(f"Couldn't find class name in {sub_path} at {prefix}")

    def _info(self):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        class_names = set()
        for split, files in self.config.data_files.items():
            prefix = os.path.commonprefix(files)
            self.prefixes[str(split)] = prefix
            for file in files:
                if Path(file).suffix in self._IMAGE_EXTENSIONS:
                    class_names.add(self._get_class_name(split, str(file)))
        return datasets.DatasetInfo(
            features=datasets.Features(
                {"image_file_path": datasets.Value("string"), "labels": datasets.ClassLabel(names=sorted(class_names))}
            ),
        )

    def _split_generators(self, dl_manager):
        data_files = self.config.data_files
        downloaded_data_files = dl_manager.download(data_files)
        if isinstance(data_files, (str, list, tuple)):
            files, downloaded_files = data_files, downloaded_data_files
            if isinstance(files, str):
                files, downloaded_files = [files], [downloaded_files]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN, gen_kwargs={"files": zip(downloaded_files, files), "split": "train"}
                )
            ]
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
        for i, (file, downloaded_file) in enumerate(files):
            if Path(file).suffix in IMAGE_EXTENSIONS:
                yield i, {"image_file_path": downloaded_file, "labels": self._get_class_name(split, str(file))}
