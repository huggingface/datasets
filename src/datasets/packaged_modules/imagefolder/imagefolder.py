import collections
import itertools
import os
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
import pyarrow as pa

import datasets
from datasets.tasks import ImageClassification


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class ImageFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for ImageFolder."""

    features: Optional[datasets.Features] = None
    drop_labels: bool = False
    with_metadata: bool = False


class ImageFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = ImageFolderConfig

    IMAGE_EXTENSIONS: List[str] = []  # definition at the bottom of the script
    METADATA_FILENAME: str = "info.csv"

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        do_analyze = self.config.features is None and (not self.config.drop_labels or self.config.with_metadata)
        if do_analyze:
            labels = set()
            metadata_files = collections.defaultdict(list)

            def analyze(files_or_archives, downloaded_files_or_dirs, split):
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
                        elif os.path.basename(file) == self.METADATA_FILENAME:
                            metadata_files[split].append((file, downloaded_file))
                else:
                    archives, downloaded_dirs = files_or_archives, downloaded_files_or_dirs
                    for archive, downloaded_dir in zip(archives, downloaded_dirs):
                        archive, downloaded_dir = str(archive), str(downloaded_dir)
                        for downloaded_dir_file in dl_manager.iter_files(downloaded_dir):
                            _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                            if downloaded_dir_file_ext in self.IMAGE_EXTENSIONS:
                                labels.add(os.path.basename(os.path.dirname(downloaded_dir_file)))
                            elif os.path.basename(downloaded_dir_file) == self.METADATA_FILENAME:
                                metadata_files[split].append((None, downloaded_dir_file))

            if not self.config.drop_labels:
                logger.info("Inferring labels from data files...")
            if self.config.with_metadata:
                logger.info("Analyzing metadata files...")

        data_files = self.config.data_files
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files, archives = self._split_files_and_archives(files)
            downloaded_files = dl_manager.download(files)
            downloaded_dirs = dl_manager.download_and_extract(archives)
            if do_analyze:
                analyze(files, downloaded_files, split_name)
                analyze(archives, downloaded_dirs, split_name)
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "files": [(file, downloaded_file) for file, downloaded_file in zip(files, downloaded_files)]
                        + [(None, dl_manager.iter_files(downloaded_dir)) for downloaded_dir in downloaded_dirs],
                        "metadata_files": metadata_files[split_name] if self.config.with_metadata else None,
                    },
                )
            )

        # Normally, we would do this in _info, but we need to know the labels and/or metadata
        # before building the features
        if self.config.features is None:
            if not self.config.drop_labels:
                self.info.features = datasets.Features(
                    {"image": datasets.Image(), "label": datasets.ClassLabel(names=sorted(labels))}
                )
                task_template = ImageClassification(image_column="image", label_column="label")
                task_template = task_template.align_with_features(self.info.features)
                self.info.task_templates = [task_template]
            else:
                self.info.features = datasets.Features({"image": datasets.Image()})

            if self.config.with_metadata:
                # TODO: maybe read a smaller chunk?
                metadata_features_all = [
                    datasets.Features.from_arrow_schema(
                        pa.Table.from_pandas(pd.read_csv(downloaded_metadata_file)).schema
                    )
                    for _, downloaded_metadata_file in itertools.chain.from_iterable(metadata_files.values())
                ]
                for metadata_features in metadata_features_all:
                    if metadata_features != metadata_features_all[0]:
                        raise ValueError(
                            f"Metadata files have different features: {metadata_features_all[0]} != {metadata_features}"
                        )
                metadata_features = metadata_features_all[0]
                if "image_id" not in metadata_features:
                    raise ValueError("`image_id` column must be present in metadata files")
                del metadata_features["image_id"]
                duplicated_keys = set(self.info.features) & set(metadata_features)
                if duplicated_keys:
                    raise ValueError(
                        f"Metadata feature keys {list(duplicated_keys)} are already present in the image features"
                    )
                self.info.features.update(metadata_features)

        return splits

    def _split_files_and_archives(self, data_files):
        files, archives = [], []
        for data_file in data_files:
            _, data_file_ext = os.path.splitext(data_file)
            if data_file_ext.lower() in self.IMAGE_EXTENSIONS:
                files.append(data_file)
            elif os.path.basename(data_file) == self.METADATA_FILENAME:
                files.append(data_file)
            else:
                archives.append(data_file)
        return files, archives

    def _generate_examples(self, files, metadata_files):
        if self.config.with_metadata:
            non_metadata_keys = ["image", "label"] if not self.config.drop_labels else ["image"]
            image_empty_metadata = {k: None for k in self.info.features if k not in non_metadata_keys}

            last_dir_checked = None
            metadata_dir = None
            metadata_df = None

            file_idx = 0
            for file, downloaded_file_or_dir in files:
                if file is not None:
                    _, file_ext = os.path.splitext(file)
                    if file_ext.lower() in self.IMAGE_EXTENSIONS:
                        if last_dir_checked is None or os.path.dirname(file) != last_dir_checked:
                            last_dir_checked = os.path.dirname(file)
                            metadata_dir = None
                            metadata_df = None
                            for metadata_file, downloaded_metadata_file in metadata_files:
                                if metadata_file is not None and not os.path.relpath(
                                    file, os.path.dirname(metadata_file)
                                ).startswith(".."):
                                    metadata_dir = os.path.dirname(metadata_file)
                                    metadata_df = pd.read_csv(downloaded_metadata_file)
                                    metadata_df["image_id"] = metadata_df["image_id"].apply(
                                        lambda x: x.replace("\\", "/")
                                    )
                                    metadata_df = metadata_df.set_index("image_id")
                                    break
                        if metadata_dir is not None:
                            file_relpath = os.path.relpath(file, metadata_dir)
                            file_relpath = file_relpath.replace("\\", "/")
                            if not file_relpath.startswith("..") and file_relpath in metadata_df.index:
                                image_metadata = metadata_df.loc[file_relpath].to_dict()
                            else:
                                image_metadata = image_empty_metadata
                        else:
                            image_metadata = image_empty_metadata
                        if self.config.drop_labels:
                            yield file_idx, {
                                "image": downloaded_file_or_dir,
                                **image_metadata,
                            }
                        else:
                            yield file_idx, {
                                "image": downloaded_file_or_dir,
                                "label": os.path.basename(os.path.dirname(file)),
                                **image_metadata,
                            }
                        file_idx += 1
                else:
                    for downloaded_dir_file in downloaded_file_or_dir:
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext.lower() in self.IMAGE_EXTENSIONS:
                            if last_dir_checked is None or os.path.dirname(downloaded_dir_file) != last_dir_checked:
                                last_dir_checked = os.path.dirname(downloaded_dir_file)
                                metadata_dir = None
                                metadata_file = None
                                for metadata_file, downloaded_metadata_file in metadata_files:
                                    if metadata_file is None and not os.path.relpath(
                                        downloaded_dir_file, os.path.dirname(downloaded_metadata_file)
                                    ).startswith(".."):
                                        metadata_dir = os.path.dirname(downloaded_metadata_file)
                                        metadata_df = pd.read_csv(downloaded_metadata_file)
                                        metadata_df["image_id"] = metadata_df["image_id"].apply(
                                            lambda x: x.replace("\\", "/")
                                        )
                                        metadata_df = metadata_df.set_index("image_id")
                                        break
                            if metadata_dir is not None:
                                downloaded_dir_file_relpath = os.path.relpath(downloaded_dir_file, metadata_dir)
                                downloaded_dir_file_relpath = downloaded_dir_file_relpath.replace("\\", "/")
                                if (
                                    not downloaded_dir_file_relpath.startswith("..")
                                    and downloaded_dir_file_relpath in metadata_df.index
                                ):
                                    image_metadata = metadata_df.loc[downloaded_dir_file_relpath].to_dict()
                                else:
                                    image_metadata = image_empty_metadata
                            else:
                                image_metadata = image_empty_metadata
                            if self.config.drop_labels:
                                yield file_idx, {
                                    "image": downloaded_dir_file,
                                    **image_metadata,
                                }
                            else:
                                yield file_idx, {
                                    "image": downloaded_dir_file,
                                    "label": os.path.basename(os.path.dirname(downloaded_dir_file)),
                                    **image_metadata,
                                }
                            file_idx += 1
        else:
            file_idx = 0
            for file, downloaded_file_or_dir in files:
                if file is not None:
                    _, file_ext = os.path.splitext(file)
                    if file_ext.lower() in self.IMAGE_EXTENSIONS:
                        if self.config.drop_labels:
                            yield file_idx, {
                                "image": downloaded_file_or_dir,
                            }
                        else:
                            yield file_idx, {
                                "image": downloaded_file_or_dir,
                                "label": os.path.basename(os.path.dirname(file)),
                            }
                        file_idx += 1
                else:
                    for downloaded_dir_file in downloaded_file_or_dir:
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext.lower() in self.IMAGE_EXTENSIONS:
                            if self.config.drop_labels:
                                yield file_idx, {
                                    "image": downloaded_dir_file,
                                }
                            else:
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
