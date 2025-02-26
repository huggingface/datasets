import collections
import io
import itertools
import os
from dataclasses import dataclass
from typing import Iterator, List, Optional, Tuple, Type, Union

import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.json as paj
import pyarrow.parquet as pq

import datasets
from datasets import config
from datasets.features.features import FeatureType, require_storage_cast
from datasets.utils.file_utils import readline


logger = datasets.utils.logging.get_logger(__name__)


def count_path_segments(path):
    return path.replace("\\", "/").count("/")


@dataclass
class FolderBasedBuilderConfig(datasets.BuilderConfig):
    """BuilderConfig for AutoFolder."""

    features: Optional[datasets.Features] = None
    drop_labels: bool = None
    drop_metadata: bool = None
    filters: Optional[Union[ds.Expression, List[tuple], List[List[tuple]]]] = None

    def __post_init__(self):
        super().__post_init__()


class FolderBasedBuilder(datasets.GeneratorBasedBuilder):
    """
    Base class for generic data loaders for vision and image data.


    Abstract class attributes to be overridden by a child class:
        BASE_FEATURE: feature object to decode data (i.e. datasets.Image, datasets.Audio, ...)
        BASE_COLUMN_NAME: string key name of a base feature (i.e. "image", "audio", ...)
        BUILDER_CONFIG_CLASS: builder config inherited from `folder_based_builder.FolderBasedBuilderConfig`
        EXTENSIONS: list of allowed extensions (only files with these extensions and METADATA_FILENAME files
            will be included in a dataset)
    """

    BASE_FEATURE: Type[FeatureType]
    BASE_COLUMN_NAME: str
    BUILDER_CONFIG_CLASS: FolderBasedBuilderConfig
    EXTENSIONS: List[str]

    METADATA_FILENAMES: List[str] = ["metadata.csv", "metadata.jsonl", "metadata.parquet"]

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        # Do an early pass if:
        # * `drop_labels` is None (default) or False, to infer the class labels
        # * `drop_metadata` is None (default) or False, to find the metadata files
        do_analyze = not self.config.drop_labels or not self.config.drop_metadata
        labels, path_depths = set(), set()
        metadata_files = collections.defaultdict(set)

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
                    if original_file_ext.lower() in self.EXTENSIONS:
                        if not self.config.drop_labels:
                            labels.add(os.path.basename(os.path.dirname(original_file)))
                            path_depths.add(count_path_segments(original_file))
                    elif os.path.basename(original_file) in self.METADATA_FILENAMES:
                        metadata_files[split].add((original_file, downloaded_file))
                    else:
                        original_file_name = os.path.basename(original_file)
                        logger.debug(
                            f"The file '{original_file_name}' was ignored: it is not a {self.BASE_COLUMN_NAME}, and is not {self.METADATA_FILENAMES} either."
                        )
            else:
                archives, downloaded_dirs = files_or_archives, downloaded_files_or_dirs
                for archive, downloaded_dir in zip(archives, downloaded_dirs):
                    archive, downloaded_dir = str(archive), str(downloaded_dir)
                    for downloaded_dir_file in dl_manager.iter_files(downloaded_dir):
                        _, downloaded_dir_file_ext = os.path.splitext(downloaded_dir_file)
                        if downloaded_dir_file_ext in self.EXTENSIONS:
                            if not self.config.drop_labels:
                                labels.add(os.path.basename(os.path.dirname(downloaded_dir_file)))
                                path_depths.add(count_path_segments(downloaded_dir_file))
                        elif os.path.basename(downloaded_dir_file) in self.METADATA_FILENAMES:
                            metadata_files[split].add((None, downloaded_dir_file))
                        else:
                            archive_file_name = os.path.basename(archive)
                            original_file_name = os.path.basename(downloaded_dir_file)
                            logger.debug(
                                f"The file '{original_file_name}' from the archive '{archive_file_name}' was ignored: it is not a {self.BASE_COLUMN_NAME}, and is not {self.METADATA_FILENAMES} either."
                            )

        data_files = self.config.data_files
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files, archives = self._split_files_and_archives(files)
            downloaded_files = dl_manager.download(files)
            downloaded_dirs = dl_manager.download_and_extract(archives)
            if do_analyze:  # drop_metadata is None or False, drop_labels is None or False
                logger.info(f"Searching for labels and/or metadata files in {split_name} data files...")
                analyze(files, downloaded_files, split_name)
                analyze(archives, downloaded_dirs, split_name)

                if metadata_files:
                    # add metadata if `metadata_files` are found and `drop_metadata` is None (default) or False
                    add_metadata = not self.config.drop_metadata
                    # if `metadata_files` are found, don't add labels
                    add_labels = False
                else:
                    # if `metadata_files` are not found, don't add metadata
                    add_metadata = False
                    # if `metadata_files` are not found and `drop_labels` is None (default) -
                    # add labels if files are on the same level in directory hierarchy and there is more than one label
                    add_labels = (
                        (len(labels) > 1 and len(path_depths) == 1)
                        if self.config.drop_labels is None
                        else not self.config.drop_labels
                    )

                if add_labels:
                    logger.info("Adding the labels inferred from data directories to the dataset's features...")
                if add_metadata:
                    logger.info("Adding metadata to the dataset...")
            else:
                add_labels, add_metadata, metadata_files = False, False, {}

            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "files": tuple(zip(files, downloaded_files))
                        + tuple((None, dl_manager.iter_files(downloaded_dir)) for downloaded_dir in downloaded_dirs),
                        "metadata_files": metadata_files.get(split_name, []),
                        "add_labels": add_labels,
                        "add_metadata": add_metadata,
                    },
                )
            )

        if add_metadata:
            # Verify that:
            # * all metadata files have the same set of features in each split
            # * the `file_name` key is one of the metadata keys and is of type string
            features_per_metadata_file: List[Tuple[str, datasets.Features]] = []

            # Check that all metadata files share the same format
            metadata_ext = {
                os.path.splitext(original_metadata_file)[-1]
                for original_metadata_file, _ in itertools.chain.from_iterable(metadata_files.values())
            }
            if len(metadata_ext) > 1:
                raise ValueError(f"Found metadata files with different extensions: {list(metadata_ext)}")
            metadata_ext = metadata_ext.pop()

            for split_metadata_files in metadata_files.values():
                pa_metadata_table = None
                for _, downloaded_metadata_file in split_metadata_files:
                    for pa_metadata_table in self._read_metadata(downloaded_metadata_file, metadata_ext=metadata_ext):
                        break  # just fetch the first rows
                    if pa_metadata_table is not None:
                        features_per_metadata_file.append(
                            (downloaded_metadata_file, datasets.Features.from_arrow_schema(pa_metadata_table.schema))
                        )
                        break  # no need to fetch all the files
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
            if add_labels:
                self.info.features = datasets.Features(
                    {
                        self.BASE_COLUMN_NAME: self.BASE_FEATURE(),
                        "label": datasets.ClassLabel(names=sorted(labels)),
                    }
                )
            else:
                self.info.features = datasets.Features({self.BASE_COLUMN_NAME: self.BASE_FEATURE()})

            if add_metadata:
                # Warn if there are duplicated keys in metadata compared to the existing features
                # (`BASE_COLUMN_NAME`, optionally "label")
                duplicated_keys = set(self.info.features) & set(metadata_features)
                if duplicated_keys:
                    logger.warning(
                        f"Ignoring metadata columns {list(duplicated_keys)} as they are already present in "
                        f"the features dictionary."
                    )
                # skip metadata duplicated keys
                self.info.features.update(
                    {
                        feature: metadata_features[feature]
                        for feature in metadata_features
                        if feature not in duplicated_keys
                    }
                )

        return splits

    def _split_files_and_archives(self, data_files):
        files, archives = [], []
        for data_file in data_files:
            _, data_file_ext = os.path.splitext(data_file)
            if data_file_ext.lower() in self.EXTENSIONS:
                files.append(data_file)
            elif os.path.basename(data_file) in self.METADATA_FILENAMES:
                files.append(data_file)
            else:
                archives.append(data_file)
        return files, archives

    def _read_metadata(self, metadata_file: str, metadata_ext: str = "") -> Iterator[pa.Table]:
        """using the same logic as the Csv, Json and Parquet dataset builders to stream the data"""
        if self.config.filters is not None:
            filter_expr = (
                pq.filters_to_expression(self.config.filters)
                if isinstance(self.config.filters, list)
                else self.config.filters
            )
        if metadata_ext == ".csv":
            chunksize = 10_000  # 10k lines
            schema = self.config.features.arrow_schema if self.config.features else None
            # dtype allows reading an int column as str
            dtype = (
                {
                    name: dtype.to_pandas_dtype() if not require_storage_cast(feature) else object
                    for name, dtype, feature in zip(schema.names, schema.types, self.config.features.values())
                }
                if schema is not None
                else None
            )
            csv_file_reader = pd.read_csv(metadata_file, iterator=True, dtype=dtype, chunksize=chunksize)
            for df in csv_file_reader:
                pa_table = pa.Table.from_pandas(df)
                if self.config.filters is not None:
                    pa_table = pa_table.filter(filter_expr)
                if len(pa_table) > 0:
                    yield pa_table
        elif metadata_ext == ".jsonl":
            with open(metadata_file, "rb") as f:
                chunksize: int = 10 << 20  # 10MB
                # Use block_size equal to the chunk size divided by 32 to leverage multithreading
                # Set a default minimum value of 16kB if the chunk size is really small
                block_size = max(chunksize // 32, 16 << 10)
                while True:
                    batch = f.read(chunksize)
                    if not batch:
                        break
                    # Finish current line
                    try:
                        batch += f.readline()
                    except (AttributeError, io.UnsupportedOperation):
                        batch += readline(f)
                    while True:
                        try:
                            pa_table = paj.read_json(
                                io.BytesIO(batch), read_options=paj.ReadOptions(block_size=block_size)
                            )
                            break
                        except (pa.ArrowInvalid, pa.ArrowNotImplementedError) as e:
                            if (
                                isinstance(e, pa.ArrowInvalid)
                                and "straddling" not in str(e)
                                or block_size > len(batch)
                            ):
                                raise
                            else:
                                # Increase the block size in case it was too small.
                                # The block size will be reset for the next file.
                                logger.debug(
                                    f"Batch of {len(batch)} bytes couldn't be parsed with block_size={block_size}. Retrying with block_size={block_size * 2}."
                                )
                                block_size *= 2
                    if self.config.filters is not None:
                        pa_table = pa_table.filter(filter_expr)
                    if len(pa_table) > 0:
                        yield pa_table
        else:
            with open(metadata_file, "rb") as f:
                parquet_fragment = ds.ParquetFileFormat().make_fragment(f)
                if parquet_fragment.row_groups:
                    batch_size = self.config.batch_size or parquet_fragment.row_groups[0].num_rows
                else:
                    batch_size = self.config.batch_size or config.DEFAULT_MAX_BATCH_SIZE
                for record_batch in parquet_fragment.to_batches(
                    batch_size=batch_size,
                    filter=filter_expr,
                    batch_readahead=0,
                    fragment_readahead=0,
                ):
                    yield pa.Table.from_batches([record_batch])

    def _generate_examples(self, files, metadata_files, add_metadata, add_labels):
        sample_empty_metadata = (
            {k: None for k in self.info.features if k != self.BASE_COLUMN_NAME} if self.info.features else {}
        )

        file_idx = 0
        if add_metadata:
            for original_metadata_file, downloaded_metadata_file in metadata_files:
                metadata_ext = os.path.splitext(original_metadata_file)[-1]
                for pa_metadata_table in self._read_metadata(downloaded_metadata_file, metadata_ext=metadata_ext):
                    pa_file_name_array = pa_metadata_table["file_name"]
                    pa_metadata_table = pa_metadata_table.drop(["file_name"])
                    downloaded_metadata_dir = os.path.dirname(downloaded_metadata_file)
                    for file_name, sample_metadata in zip(
                        pa_file_name_array.to_pylist(), pa_metadata_table.to_pylist()
                    ):
                        file_relpath = os.path.normpath(file_name).replace("\\", "/")
                        downloaded_file = os.path.join(downloaded_metadata_dir, file_relpath)
                        sample = dict(sample_empty_metadata)
                        sample[self.BASE_COLUMN_NAME] = downloaded_file
                        sample.update(sample_metadata)
                        yield file_idx, sample
                        file_idx += 1
        else:
            for original_file, downloaded_file_or_dir in files:
                downloaded_files = [downloaded_file_or_dir] if original_file else downloaded_file_or_dir
                for downloaded_file in downloaded_files:
                    original_file_ext = os.path.splitext(original_file or downloaded_file)[-1]
                    if original_file_ext.lower() not in self.EXTENSIONS:
                        continue
                    sample = {self.BASE_COLUMN_NAME: downloaded_file}
                    if add_labels:
                        sample["label"] = os.path.basename(os.path.dirname(original_file or downloaded_file))
                    yield file_idx, sample
                    file_idx += 1
