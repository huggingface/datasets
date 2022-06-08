import collections
import itertools
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pyarrow.compute as pc
import pyarrow.json as paj

import datasets
from datasets.tasks import ImageClassification


logger = datasets.utils.logging.get_logger(__name__)


if datasets.config.PYARROW_VERSION.major >= 7:

    def pa_table_to_pylist(table):
        return table.to_pylist()

else:

    def pa_table_to_pylist(table):
        keys = table.column_names
        values = table.to_pydict().values()
        return [{k: v for k, v in zip(keys, row_values)} for row_values in zip(*values)]


def count_path_segments(path):
    cnt = 0
    while True:
        parts = os.path.split(path)
        if parts[0] == path:
            break
        elif parts[1] == path:
            break
        else:
            path = parts[0]
            cnt += 1
    return cnt


@dataclass
class ImageFolderConfig(datasets.BuilderConfig):
    """BuilderConfig for ImageFolder."""

    features: Optional[datasets.Features] = None
    drop_labels: bool = False
    drop_metadata: bool = False


class ImageFolder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = ImageFolderConfig

    IMAGE_EXTENSIONS: List[str] = []  # definition at the bottom of the script
    SKIP_CHECKSUM_COMPUTATION_BY_DEFAULT = True
    METADATA_FILENAME: str = "metadata.jsonl"

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        # Do an early pass if:
        # * `features` are not specified, to infer the class labels
        # * `drop_metadata` is False, to find the metadata files
        do_analyze = (self.config.features is None and not self.config.drop_labels) or not self.config.drop_metadata
        if do_analyze:
            labels = set()
            metadata_files = collections.defaultdict(list)

            def analyze(files_or_archives, downloaded_files_or_dirs, split):
                if len(downloaded_files_or_dirs) == 0:
                    return
                # The files are separated from the archives at this point, so check the first sample
                # to see if it's a file or a directory and iterate accordingly
                if os.path.isfile(downloaded_files_or_dirs[0]):
                    original_files, downloaded_files = files_or_archives, downloaded_files_or_dirs
                    for original_file, downloaded_file in zip(original_files, downloaded_files):
                        original_file, downloaded_file = str(original_file), str(downloaded_file)
                        _, original_file_ext = os.path.splitext(original_file)
                        if original_file_ext.lower() in self.IMAGE_EXTENSIONS:
                            labels.add(os.path.basename(os.path.dirname(original_file)))
                        elif os.path.basename(original_file) == self.METADATA_FILENAME:
                            metadata_files[split].append((original_file, downloaded_file))
                        else:
                            original_file_name = os.path.basename(original_file)
                            logger.debug(
                                f"The file '{original_file_name}' was ignored: it is not an image, and is not {self.METADATA_FILENAME} either."
                            )
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
                            else:
                                archive_file_name = os.path.basename(archive)
                                original_file_name = os.path.basename(downloaded_dir_file)
                                logger.debug(
                                    f"The file '{original_file_name}' from the archive '{archive_file_name}' was ignored: it is not an image, and is not {self.METADATA_FILENAME} either."
                                )

            if not self.config.drop_labels:
                logger.info("Inferring labels from data files...")
            if not self.config.drop_metadata:
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
                        "metadata_files": metadata_files if not self.config.drop_metadata else None,
                        "split_name": split_name,
                    },
                )
            )

        if not self.config.drop_metadata and metadata_files:
            # Verify that:
            # * all metadata files have the same set of features
            # * the `file_name` key is one of the metadata keys and is of type string
            features_per_metadata_file: List[Tuple[str, datasets.Features]] = []
            for _, downloaded_metadata_file in itertools.chain.from_iterable(metadata_files.values()):
                with open(downloaded_metadata_file, "rb") as f:
                    pa_metadata_table = paj.read_json(f)
                features_per_metadata_file.append(
                    (downloaded_metadata_file, datasets.Features.from_arrow_schema(pa_metadata_table.schema))
                )
            for downloaded_metadata_file, metadata_features in features_per_metadata_file:
                if metadata_features != features_per_metadata_file[0][1]:
                    raise ValueError(
                        f"Metadata files {downloaded_metadata_file} and {features_per_metadata_file[0][0]} have different features: {features_per_metadata_file[0]} != {metadata_features}"
                    )
            metadata_features = features_per_metadata_file[0][1]
            if "file_name" not in metadata_features:
                raise ValueError("`file_name` must be present as dictionary key in metadata files")
            if metadata_features["file_name"] != datasets.Value("string"):
                raise ValueError("`file_name` key must be a string")
            del metadata_features["file_name"]
        else:
            metadata_features = None

        # Normally, we would do this in _info, but we need to know the labels and/or metadata
        # before building the features
        if self.config.features is None:
            if not self.config.drop_labels and not metadata_files:
                self.info.features = datasets.Features(
                    {"image": datasets.Image(), "label": datasets.ClassLabel(names=sorted(labels))}
                )
                task_template = ImageClassification(image_column="image", label_column="label")
                task_template = task_template.align_with_features(self.info.features)
                self.info.task_templates = [task_template]
            else:
                self.info.features = datasets.Features({"image": datasets.Image()})

            if not self.config.drop_metadata and metadata_files:
                # Verify that there are no duplicated keys when compared to the existing features ("image", optionally "label")
                duplicated_keys = set(self.info.features) & set(metadata_features)
                if duplicated_keys:
                    raise ValueError(
                        f"Metadata feature keys {list(duplicated_keys)} are already present as the image features"
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

    def _generate_examples(self, files, metadata_files, split_name):
        if not self.config.drop_metadata and metadata_files:
            split_metadata_files = metadata_files.get(split_name, [])
            image_empty_metadata = {k: None for k in self.info.features if k != "image"}

            last_checked_dir = None
            metadata_dir = None
            metadata_dict = None
            downloaded_metadata_file = None

            file_idx = 0
            for original_file, downloaded_file_or_dir in files:
                if original_file is not None:
                    _, original_file_ext = os.path.splitext(original_file)
                    if original_file_ext.lower() in self.IMAGE_EXTENSIONS:
                        # If the file is an image, and we've just entered a new directory,
                        # find the nereast metadata file (by counting path segments) for the directory
                        current_dir = os.path.dirname(original_file)
                        if last_checked_dir is None or last_checked_dir != current_dir:
                            last_checked_dir = current_dir
                            metadata_file_candidates = [
                                (
                                    os.path.relpath(original_file, os.path.dirname(metadata_file_candidate)),
                                    metadata_file_candidate,
                                    downloaded_metadata_file,
                                )
                                for metadata_file_candidate, downloaded_metadata_file in split_metadata_files
                                if metadata_file_candidate
                                is not None  # ignore metadata_files that are inside archives
                                and not os.path.relpath(
                                    original_file, os.path.dirname(metadata_file_candidate)
                                ).startswith("..")
                            ]
                            if metadata_file_candidates:
                                _, metadata_file, downloaded_metadata_file = min(
                                    metadata_file_candidates, key=lambda x: count_path_segments(x[0])
                                )
                                with open(downloaded_metadata_file, "rb") as f:
                                    pa_metadata_table = paj.read_json(f)
                                pa_file_name_array = pa_metadata_table["file_name"]
                                pa_file_name_array = pc.replace_substring(
                                    pa_file_name_array, pattern="\\", replacement="/"
                                )
                                pa_metadata_table = pa_metadata_table.drop(["file_name"])
                                metadata_dir = os.path.dirname(metadata_file)
                                metadata_dict = {
                                    file_name: image_metadata
                                    for file_name, image_metadata in zip(
                                        pa_file_name_array.to_pylist(), pa_table_to_pylist(pa_metadata_table)
                                    )
                                }
                            else:
                                raise ValueError(
                                    f"One or several metadata.jsonl were found, but not in the same directory or in a parent directory of {downloaded_file_or_dir}."
                                )
                        if metadata_dir is not None and downloaded_metadata_file is not None:
                            file_relpath = os.path.relpath(original_file, metadata_dir)
                            file_relpath = file_relpath.replace("\\", "/")
                            if file_relpath not in metadata_dict:
                                raise ValueError(
                                    f"Image at {file_relpath} doesn't have metadata in {downloaded_metadata_file}."
                                )
                            image_metadata = metadata_dict[file_relpath]
                        else:
                            raise ValueError(
                                f"One or several metadata.jsonl were found, but not in the same directory or in a parent directory of {downloaded_file_or_dir}."
                            )
                        yield file_idx, {
                            **image_empty_metadata,
                            "image": downloaded_file_or_dir,
                            **image_metadata,
                        }
                        file_idx += 1
                else:
                    for downloaded_dir_file in downloaded_file_or_dir:
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext.lower() in self.IMAGE_EXTENSIONS:
                            current_dir = os.path.dirname(downloaded_dir_file)
                            if last_checked_dir is None or last_checked_dir != current_dir:
                                last_checked_dir = current_dir
                                metadata_file_candidates = [
                                    (
                                        os.path.relpath(
                                            downloaded_dir_file, os.path.dirname(downloaded_metadata_file)
                                        ),
                                        metadata_file_candidate,
                                        downloaded_metadata_file,
                                    )
                                    for metadata_file_candidate, downloaded_metadata_file in split_metadata_files
                                    if metadata_file_candidate
                                    is None  # ignore metadata_files that are not inside archives
                                    and not os.path.relpath(
                                        downloaded_dir_file, os.path.dirname(downloaded_metadata_file)
                                    ).startswith("..")
                                ]
                                if metadata_file_candidates:
                                    _, metadata_file, downloaded_metadata_file = min(
                                        metadata_file_candidates, key=lambda x: count_path_segments(x[0])
                                    )
                                    with open(downloaded_metadata_file, "rb") as f:
                                        pa_metadata_table = paj.read_json(f)
                                    pa_file_name_array = pa_metadata_table["file_name"]
                                    pa_file_name_array = pc.replace_substring(
                                        pa_file_name_array, pattern="\\", replacement="/"
                                    )
                                    pa_metadata_table = pa_metadata_table.drop(["file_name"])
                                    metadata_dir = os.path.dirname(downloaded_metadata_file)
                                    metadata_dict = {
                                        file_name: image_metadata
                                        for file_name, image_metadata in zip(
                                            pa_file_name_array.to_pylist(), pa_table_to_pylist(pa_metadata_table)
                                        )
                                    }
                                else:
                                    raise ValueError(
                                        f"One or several metadata.jsonl were found, but not in the same directory or in a parent directory of {downloaded_dir_file}."
                                    )
                            if metadata_dir is not None and downloaded_metadata_file is not None:
                                downloaded_dir_file_relpath = os.path.relpath(downloaded_dir_file, metadata_dir)
                                downloaded_dir_file_relpath = downloaded_dir_file_relpath.replace("\\", "/")
                                if downloaded_dir_file_relpath not in metadata_dict:
                                    raise ValueError(
                                        f"Image at {downloaded_dir_file_relpath} doesn't have metadata in {downloaded_metadata_file}."
                                    )
                                image_metadata = metadata_dict[downloaded_dir_file_relpath]
                            else:
                                raise ValueError(
                                    f"One or several metadata.jsonl were found, but not in the same directory or in a parent directory of {downloaded_dir_file}."
                                )
                            yield file_idx, {
                                **image_empty_metadata,
                                "image": downloaded_dir_file,
                                **image_metadata,
                            }
                            file_idx += 1
        else:
            file_idx = 0
            for original_file, downloaded_file_or_dir in files:
                if original_file is not None:
                    _, original_file_ext = os.path.splitext(original_file)
                    if original_file_ext.lower() in self.IMAGE_EXTENSIONS:
                        if self.config.drop_labels or metadata_files:
                            yield file_idx, {
                                "image": downloaded_file_or_dir,
                            }
                        else:
                            yield file_idx, {
                                "image": downloaded_file_or_dir,
                                "label": os.path.basename(os.path.dirname(original_file)),
                            }
                        file_idx += 1
                else:
                    for downloaded_dir_file in downloaded_file_or_dir:
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext.lower() in self.IMAGE_EXTENSIONS:
                            if self.config.drop_labels or metadata_files:
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
