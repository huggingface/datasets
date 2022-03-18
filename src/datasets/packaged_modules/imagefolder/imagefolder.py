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
    drop_labels: bool = False


class ImageFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = ImageFolderConfig

    IMAGE_EXTENSIONS: List[str] = []  # definition at the bottom of the script

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        capture_labels = not self.config.drop_labels and self.config.features is None
        if capture_labels:
            labels = set()

            def capture_labels_for_split(files_or_archives, downloaded_files_or_dirs):
                if len(downloaded_files_or_dirs) == 0:
                    return
                # The files are separated from the archives at this point, so check the first sample
                # to see if it's a file or a directory and iterate accordingly
                if os.path.isfile(downloaded_files_or_dirs[0]):
                    files, downloaded_files = files_or_archives, downloaded_files_or_dirs
                    for file, downloaded_file in zip(files, downloaded_files):
                        file, downloaded_file = str(file), str(downloaded_file)
                        _, file_ext = os.path.splitext(file)
                        if file_ext.lower() in self.IMAGE_EXTENSIONS:
                            labels.add(os.path.basename(os.path.dirname(file)))
                else:
                    archives, downloaded_dirs = files_or_archives, downloaded_files_or_dirs
                    for archive, downloaded_dir in zip(archives, downloaded_dirs):
                        archive, downloaded_file = str(archive), str(downloaded_dir)
                        for downloaded_dir_file in dl_manager.iter_files(downloaded_dir):
                            _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                            if downloaded_dir_file_ext in self.IMAGE_EXTENSIONS:
                                labels.add(os.path.basename(os.path.dirname(downloaded_dir_file)))

            logger.info("Inferring labels from data files...")

        data_files = self.config.data_files
        splits = []
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            files, archives = self._split_files_and_archives(files)
            downloaded_files = dl_manager.download(files)
            downloaded_dirs = dl_manager.download_and_extract(archives)
            if capture_labels:
                capture_labels_for_split(files, downloaded_files)
                capture_labels_for_split(archives, downloaded_dirs)
            splits.append(
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "files": [(file, downloaded_file) for file, downloaded_file in zip(files, downloaded_files)]
                        + [(None, dl_manager.iter_files(downloaded_dir)) for downloaded_dir in downloaded_dirs]
                    },
                )
            )
        else:
            for split_name, files in data_files.items():
                if isinstance(files, str):
                    files = [files]
                files, archives = self._split_files_and_archives(files)
                downloaded_files = dl_manager.download(files)
                downloaded_dirs = dl_manager.download_and_extract(archives)
                if capture_labels:
                    capture_labels_for_split(files, downloaded_files)
                    capture_labels_for_split(archives, downloaded_dirs)
                splits.append(
                    datasets.SplitGenerator(
                        name=split_name,
                        gen_kwargs={
                            "files": [
                                (file, downloaded_file) for file, downloaded_file in zip(files, downloaded_files)
                            ]
                            + [(None, dl_manager.iter_files(downloaded_dir)) for downloaded_dir in downloaded_dirs]
                        },
                    )
                )

        # Normally we would do this in _info, but we need to know the labels before building the features
        if capture_labels:
            if not self.config.drop_labels:
                self.info.features = datasets.Features(
                    {"image": datasets.Image(), "label": datasets.ClassLabel(names=sorted(labels))}
                )
                task_template = ImageClassification(image_column="image", label_column="label")
                task_template = task_template.align_with_features(self.info.features)
                self.info.task_templates = [task_template]
            else:
                self.info.features = datasets.Features({"image": datasets.Image()})

        return splits

    def _split_files_and_archives(self, data_files):
        files, archives = [], []
        for data_file in data_files:
            _, data_file_ext = os.path.splitext(data_file)
            if data_file_ext.lower() in self.IMAGE_EXTENSIONS:
                files.append(data_file)
            else:
                archives.append(data_file)
        return files, archives

    def _generate_examples(self, files):
        if not self.config.drop_labels:
            file_idx = 0
            for file, downloaded_file_or_dir in files:
                if file is not None:
                    _, file_ext = os.path.splitext(file)
                    if file_ext.lower() in self.IMAGE_EXTENSIONS:
                        yield file_idx, {
                            "image": downloaded_file_or_dir,
                            "label": os.path.basename(os.path.dirname(file)),
                        }
                        file_idx += 1
                else:
                    for downloaded_dir_file in downloaded_file_or_dir:
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext.lower() in self.IMAGE_EXTENSIONS:
                            yield file_idx, {
                                "image": downloaded_dir_file,
                                "label": os.path.basename(os.path.dirname(downloaded_dir_file)),
                            }
                            file_idx += 1
        else:
            file_idx = 0
            for file, downloaded_file_or_dir in files:
                if file is not None:
                    _, file_ext = os.path.splitext(file)
                    if file_ext.lower() in self.IMAGE_EXTENSIONS:
                        yield file_idx, {"image": downloaded_file_or_dir}
                        file_idx += 1
                else:
                    for downloaded_dir_file in downloaded_file_or_dir:
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext.lower() in self.IMAGE_EXTENSIONS:
                            yield file_idx, {"image": downloaded_dir_file}
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
