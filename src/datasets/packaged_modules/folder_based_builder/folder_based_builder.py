import collections
import io
import itertools
import os
from dataclasses import dataclass
from typing import Any, Callable, Iterator, Optional, Union

import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.json as paj
import pyarrow.parquet as pq

import datasets
from datasets import config
from datasets.builder import Key
from datasets.features.features import FeatureType, _visit, _visit_with_path, _VisitPath, require_storage_cast
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
    metadata_filenames: list[str] = None
    filters: Optional[Union[ds.Expression, list[tuple], list[list[tuple]]]] = None

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

    BASE_FEATURE: type[FeatureType]
    BASE_COLUMN_NAME: str
    BUILDER_CONFIG_CLASS: FolderBasedBuilderConfig
    EXTENSIONS: list[str]

    METADATA_FILENAMES: list[str] = ["metadata.csv", "metadata.jsonl", "metadata.parquet"]

    def _info(self):
        if not self.config.data_dir and not self.config.data_files:
            raise ValueError(
                "Folder-based datasets require either `data_dir` or `data_files` to be specified. "
                "Neither was provided."
            )

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
        all_metadata_files = collections.defaultdict(set)
        metadata_filenames = self.config.metadata_filenames or self.METADATA_FILENAMES

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
                    elif os.path.basename(original_file) in metadata_filenames:
                        all_metadata_files[split].add((original_file, None, downloaded_file))
                    else:
                        original_file_name = os.path.basename(original_file)
                        logger.debug(
                            f"The file '{original_file_name}' was ignored: it is not a {self.BASE_COLUMN_NAME}, and is not {metadata_filenames} either."
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
                        elif os.path.basename(downloaded_dir_file) in metadata_filenames:
                            all_metadata_files[split].add((None, downloaded_dir, downloaded_dir_file))
                        else:
                            archive_file_name = os.path.basename(archive)
                            original_file_name = os.path.basename(downloaded_dir_file)
                            logger.debug(
                                f"The file '{original_file_name}' from the archive '{archive_file_name}' was ignored: it is not a {self.BASE_COLUMN_NAME}, and is not {metadata_filenames} either."
                            )

        data_files = self.config.data_files
        splits = []
        for split_name, files in data_files.items():
            files, metadata_files, archives = self._split_files_and_metadata_and_archives(files)
            downloaded_files = dl_manager.download(files)
            downloaded_metadata_files = dl_manager.download(metadata_files)
            downloaded_dirs = dl_manager.download_and_extract(archives)
            if do_analyze:  # drop_metadata is None or False, drop_labels is None or False
                logger.info(f"Searching for labels and/or metadata files in {split_name} data files...")
                analyze(files, downloaded_files, split_name)
                analyze(metadata_files, downloaded_metadata_files, split_name)
                analyze(archives, downloaded_dirs, split_name)

                if all_metadata_files:
                    # add metadata if `all_metadata_files` are found and `drop_metadata` is None (default) or False
                    add_metadata = not self.config.drop_metadata
                    # if `all_metadata_files` are found, don't add labels
                    add_labels = False
                else:
                    # if `all_metadata_files` are not found, don't add metadata
                    add_metadata = False
                    # if `all_metadata_files` are not found and `drop_labels` is None (default) -
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
                add_labels, add_metadata, all_metadata_files = False, False, {}

            # files info (original_file, None, downloaded_file)
            files = tuple(zip(files, [None] * len(files), downloaded_files))
            # archives info (original_archive_file, downloaded_dir, downloaded_files)
            files += tuple(
                (archive, downloaded_dir, dl_manager.iter_files(downloaded_dir))
                for archive, downloaded_dir in zip(archives, downloaded_dirs)
            )
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "files": files,
                        "metadata_files": all_metadata_files.get(split_name, []),
                        "add_labels": add_labels,
                        "add_metadata": add_metadata,
                    },
                )
            )

        if add_metadata:
            # Verify that:
            # * all metadata files have the same set of features in each split
            # * the `file_name` key is one of the metadata keys and is of type string
            features_per_metadata_file: list[tuple[str, datasets.Features]] = []

            # Check that all metadata files share the same format
            metadata_ext = {
                os.path.splitext(original_metadata_file or downloaded_metadata_file)[-1]
                for original_metadata_file, _, downloaded_metadata_file in itertools.chain.from_iterable(
                    all_metadata_files.values()
                )
            }
            if len(metadata_ext) > 1:
                raise ValueError(f"Found metadata files with different extensions: {list(metadata_ext)}")
            metadata_ext = metadata_ext.pop()

            for split_metadata_files in all_metadata_files.values():
                pa_metadata_table = None
                for _, _, downloaded_metadata_file in split_metadata_files:
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
            feature_not_found = True

            def _set_feature(feature):
                nonlocal feature_not_found
                if isinstance(feature, dict):
                    out = type(feature)()
                    for key in feature:
                        if (key == "file_name" or key.endswith("_file_name")) and feature[key] == datasets.Value(
                            "string"
                        ):
                            key = key[: -len("_file_name")] or self.BASE_COLUMN_NAME
                            out[key] = self.BASE_FEATURE()
                            feature_not_found = False
                        elif (key == "file_names" or key.endswith("_file_names")) and feature[key] == datasets.List(
                            datasets.Value("string")
                        ):
                            key = key[: -len("_file_names")] or (self.BASE_COLUMN_NAME + "s")
                            out[key] = datasets.List(self.BASE_FEATURE())
                            feature_not_found = False
                        elif (key == "file_names" or key.endswith("_file_names")) and feature[key] == [
                            datasets.Value("string")
                        ]:
                            key = key[: -len("_file_names")] or (self.BASE_COLUMN_NAME + "s")
                            out[key] = [self.BASE_FEATURE()]
                            feature_not_found = False
                        else:
                            out[key] = feature[key]
                    return out
                return feature

            metadata_features = _visit(metadata_features, _set_feature)

            if feature_not_found:
                raise ValueError(
                    "`file_name` or `*_file_name` must be present as dictionary key (with type string) in metadata files"
                )
        else:
            metadata_features = None

        # Normally, we would do this in _info, but we need to know the labels and/or metadata
        # before building the features
        if self.config.features is None:
            if add_metadata:
                self.info.features = metadata_features
            elif add_labels:
                self.info.features = datasets.Features(
                    {
                        self.BASE_COLUMN_NAME: self.BASE_FEATURE(),
                        "label": datasets.ClassLabel(names=sorted(labels)),
                    }
                )
            else:
                self.info.features = datasets.Features({self.BASE_COLUMN_NAME: self.BASE_FEATURE()})

        return splits

    def _split_files_and_metadata_and_archives(self, data_files):
        files, metadata_files, archives = [], [], []
        metadata_filenames = self.config.metadata_filenames or self.METADATA_FILENAMES
        for data_file in data_files:
            data_file_root, data_file_ext = os.path.splitext(data_file)
            _, second_data_file_ext = os.path.splitext(data_file_root)
            if data_file_ext.lower() in self.EXTENSIONS or second_data_file_ext.lower() in self.EXTENSIONS:
                files.append(data_file)
            elif os.path.basename(data_file) in metadata_filenames:
                metadata_files.append(data_file)
            elif data_file_ext.lower() == ".zip":
                archives.append(data_file)
        return files, metadata_files, archives

    def _read_metadata(self, metadata_file: str, metadata_ext: str = "") -> Iterator[pa.Table]:
        """using the same logic as the Csv, Json and Parquet dataset builders to stream the data"""
        if self.config.filters is not None:
            filter_expr = (
                pq.filters_to_expression(self.config.filters)
                if isinstance(self.config.filters, list)
                else self.config.filters
            )
        else:
            filter_expr = None
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
                    batch_size = parquet_fragment.row_groups[0].num_rows
                else:
                    batch_size = config.DEFAULT_MAX_BATCH_SIZE
                for record_batch in parquet_fragment.to_batches(
                    batch_size=batch_size,
                    filter=filter_expr,
                    batch_readahead=0,
                    fragment_readahead=0,
                ):
                    yield pa.Table.from_batches([record_batch])

    def _generate_shards(self, files, metadata_files, add_metadata, add_labels):
        if add_metadata:
            for _, _, downloaded_metadata_file in metadata_files:
                yield downloaded_metadata_file
        else:
            for _, downloaded_dir, downloaded_file in files:
                yield downloaded_dir or downloaded_file

    def _generate_examples(self, files, metadata_files, add_metadata, add_labels):
        if add_metadata:
            feature_paths = []

            def find_feature_path(feature, feature_path):
                nonlocal feature_paths
                if feature_path and isinstance(feature, self.BASE_FEATURE):
                    feature_paths.append(feature_path)

            _visit_with_path(self.info.features, find_feature_path)

            for shard_idx, metadata_file_info in enumerate(metadata_files):
                if len(metadata_file_info) == 2:
                    original_metadata_file, downloaded_metadata_file = metadata_file_info
                else:
                    original_metadata_file, downloaded_metadata_dir, downloaded_metadata_file = metadata_file_info
                metadata_ext = os.path.splitext(original_metadata_file or downloaded_metadata_file)[-1]
                downloaded_metadata_dir = os.path.dirname(downloaded_metadata_file)

                def set_feature(item, feature_path: _VisitPath):
                    if len(feature_path) == 2 and isinstance(feature_path[0], str) and feature_path[1] == 0:
                        item[feature_path[0]] = item.pop("file_names", None) or item.pop(
                            feature_path[0] + "_file_names", None
                        )
                    elif len(feature_path) == 1 and isinstance(feature_path[0], str):
                        item[feature_path[0]] = item.pop("file_name", None) or item.pop(
                            feature_path[0] + "_file_name", None
                        )
                    elif len(feature_path) == 0:
                        file_relpath = os.path.normpath(item).replace("\\", "/")
                        item = os.path.join(downloaded_metadata_dir, file_relpath)
                    return item

                for pa_metadata_table in self._read_metadata(downloaded_metadata_file, metadata_ext=metadata_ext):
                    for sample_idx, sample in enumerate(pa_metadata_table.to_pylist()):
                        for feature_path in feature_paths:
                            _nested_apply(sample, feature_path, set_feature)
                        yield Key(shard_idx, sample_idx), sample
        else:
            if self.config.filters is not None:
                filter_expr = (
                    pq.filters_to_expression(self.config.filters)
                    if isinstance(self.config.filters, list)
                    else self.config.filters
                )
            for shard_idx, (original_file, _, downloaded_files) in enumerate(files):
                if isinstance(downloaded_files, str):
                    downloaded_files = [downloaded_files]
                for sample_idx, downloaded_file in enumerate(downloaded_files):
                    sample = {self.BASE_COLUMN_NAME: downloaded_file}
                    if add_labels:
                        sample["label"] = os.path.basename(os.path.dirname(original_file or downloaded_file))
                    if self.config.filters is not None:
                        pa_table = pa.Table.from_pylist([sample]).filter(filter_expr)
                        if len(pa_table) == 0:
                            continue
                    yield Key(shard_idx, sample_idx), sample


def _nested_apply(item: Any, feature_path: _VisitPath, func: Callable[[Any, _VisitPath], Any]):
    # see _visit_with_path() to see how feature paths are constructed
    item = func(item, feature_path)
    if feature_path:
        key = feature_path[0]
        if key == 0:
            for i in range(len(item)):
                item[i] = _nested_apply(item[i], feature_path[1:], func)
        else:
            item[key] = _nested_apply(item[key], feature_path[1:], func)
    return item
