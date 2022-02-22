import os
import re
from dataclasses import dataclass
from typing import List, Optional, Pattern, Tuple

import datasets
from datasets.tasks.image_classification import ImageClassification


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class ImageFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for ImageFolder."""

    features: Optional[datasets.Features] = None


class ImageFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = ImageFolderConfig

    IMAGE_EXTENSIONS: List[str] = []  # defined at the bottom of the script
    CLASS_PATTERN_RE: Pattern = re.compile(r"\w+")

    @classmethod
    def _get_class_name(cls, prefix: str, file: str) -> str:
        file_name = os.path.basename(file)
        sub_path = file[len(prefix) : -len(file_name)]
        for class_name_match in cls.CLASS_PATTERN_RE.finditer(sub_path):
            return class_name_match.group()

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        data_files = self.config.data_files
        if not data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={data_files}")

        def process_split_files(data_files, downloaded_data_files, find_class_names=False):
            image_files: List[Tuple[Optional[str], str]] = []
            for file, downloaded_file in zip(data_files, downloaded_data_files):
                file, downloaded_file = str(file), str(downloaded_file)
                if os.path.isfile(downloaded_file):
                    _, file_ext = os.path.splitext(file)
                    if file_ext in self.IMAGE_EXTENSIONS:
                        image_files.append(
                            (file if find_class_names and file != downloaded_file else None, downloaded_file)
                        )
                else:
                    for downloaded_dir_file in dl_manager.iter_files([downloaded_file]):
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext in self.IMAGE_EXTENSIONS:
                            image_files.append((None, downloaded_dir_file))
            if find_class_names:
                image_file_names = [
                    file if file is not None else downloaded_file for file, downloaded_file in image_files
                ]
                prefix = os.path.commonprefix(image_file_names)
                class_names = {self._get_class_name(prefix, file) for file in image_file_names}
            else:
                prefix = None
                class_names = None
            return image_files, prefix, class_names

        find_class_names = self.config.features is None
        downloaded_data_files = dl_manager.download_and_extract(data_files)

        split_args = []
        if isinstance(downloaded_data_files, (str, list, tuple)):
            files, downloaded_files = data_files, downloaded_data_files
            if isinstance(files, str):
                files, downloaded_files = [files], [downloaded_files]
            split_image_files, split_prefix, split_class_names = process_split_files(
                files, downloaded_files, find_class_names=find_class_names
            )
            split_args.append((str(datasets.Split.TRAIN), split_image_files, split_prefix, split_class_names))
        else:
            for split_name, files in data_files.items():
                downloaded_files = downloaded_data_files[split_name]
                if isinstance(files, str):
                    files, downloaded_files = [files], [downloaded_files]
                split_image_files, split_prefix, split_class_names = process_split_files(
                    files, downloaded_files, find_class_names=find_class_names
                )
                split_args.append((split_name, split_image_files, split_prefix, split_class_names))

        class_names = set()
        if find_class_names:
            for *_, split_class_names in split_args:
                class_names |= split_class_names
            if class_names:
                self.info.features = datasets.Features(
                    {"image": datasets.Image(), "label": datasets.ClassLabel(names=sorted(class_names))}
                )
                self.info.task_templates = [ImageClassification(image_column="image", label_column="label")]
            else:
                self.info.features = datasets.Features({"image": datasets.Image()})
        else:
            self.info.features = datasets.Features({"image": datasets.Image()})

        add_label = find_class_names and class_names
        return [
            datasets.SplitGenerator(
                name=split_name,
                gen_kwargs={"files": split_image_files, "prefix": split_prefix, "add_label": add_label},
            )
            for split_name, split_image_files, split_prefix, _ in split_args
        ]

    def _generate_examples(self, files, prefix, add_label):
        for i, (file, downloaded_file) in enumerate(files):
            file = downloaded_file if file is None else file
            if add_label:
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
