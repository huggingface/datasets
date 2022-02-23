import os
from dataclasses import dataclass
from typing import List, Optional

import datasets
from datasets.tasks import ImageClassification


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class ImageFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for ImageFolder."""

    features: Optional[datasets.Features] = None


class ImageFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = ImageFolderConfig

    IMAGE_EXTENSIONS: List[str] = []  # definition at the bottom of the script

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        labels = set()

        def capture_labels_for_split(files, downloaded_files):
            for file, downloaded_file in zip(files, downloaded_files):
                file, downloaded_file = str(file), str(downloaded_file)
                if os.path.isfile(downloaded_file):
                    _, file_ext = os.path.splitext(file)
                    if file_ext in self.IMAGE_EXTENSIONS:
                        labels.add(os.path.basename(os.path.dirname(file)))
                else:
                    for downloaded_dir_file in dl_manager.iter_files([downloaded_file]):
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext in self.IMAGE_EXTENSIONS:
                            labels.add(os.path.basename(os.path.dirname(downloaded_dir_file)))

        data_files = self.config.data_files
        downloaded_data_files = dl_manager.download_and_extract(data_files)
        logger.info("Inferring labels from data files...")
        splits = []
        if isinstance(downloaded_data_files, (str, list, tuple)):
            files, downloaded_files = data_files, downloaded_data_files
            if isinstance(files, str):
                files, downloaded_files = [files], [downloaded_files]
            capture_labels_for_split(files, downloaded_files)
            splits.append(
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "files": [
                            (file, downloaded_file)
                            if os.path.isfile(downloaded_file)
                            else (None, dl_manager.iter_files([downloaded_file]))
                            for file, downloaded_file in zip(files, downloaded_files)
                        ]
                    },
                )
            )
        else:
            for split_name, files in data_files.items():
                downloaded_files = downloaded_data_files[split_name]
                if isinstance(files, str):
                    files, downloaded_files = [files], [downloaded_files]
                capture_labels_for_split(files, downloaded_files)
                splits.append(
                    datasets.SplitGenerator(
                        name=split_name,
                        gen_kwargs={
                            "files": [
                                (file, downloaded_file)
                                if os.path.isfile(downloaded_file)
                                else (None, dl_manager.iter_files([downloaded_file]))
                                for file, downloaded_file in zip(files, downloaded_files)
                            ]
                        },
                    )
                )

        if self.config.features is None:
            self.info.features = datasets.Features(
                {"image": datasets.Image(), "label": datasets.ClassLabel(names=sorted(labels))}
            )
            self.info.task_templates = [ImageClassification(image_column="image", label_column="label")]

        return splits

    def _generate_examples(self, files):
        file_idx = 0
        for file, downloaded_file_or_dir in files:
            if file is not None:
                _, file_ext = os.path.splitext(file)
                if file_ext in self.IMAGE_EXTENSIONS:
                    yield file_idx, {"image": downloaded_file_or_dir, "label": os.path.basename(os.path.dirname(file))}
                    file_idx += 1
            else:
                for downloaded_dir_file in downloaded_file_or_dir:
                    _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                    if downloaded_dir_file_ext in self.IMAGE_EXTENSIONS:
                        yield file_idx, {
                            "image": downloaded_dir_file,
                            "label": os.path.basename(os.path.dirname(downloaded_dir_file)),
                        }
                        file_idx += 1


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
