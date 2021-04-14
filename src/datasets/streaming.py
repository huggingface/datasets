import importlib
import os
from functools import partial
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import fsspec
import pyarrow as pa

from .arrow_dataset import DatasetInfoMixin
from .builder import DatasetBuilder, GeneratorBasedBuilder
from .features import Features
from .info import DatasetInfo
from .load import import_main_class, prepare_module, url_or_path_parent
from .splits import NamedSplit, Split
from .utils import DownloadConfig, map_nested
from .utils.download_manager import GenerateMode
from .utils.logging import get_logger
from .utils.version import Version


logger = get_logger(__name__)


def _infer_features_from_batch(batch: Dict[str, list]) -> Features:
    pa_table = pa.Table.from_pydict(batch)
    return Features.from_arrow_schema(pa_table.schema)


def _examples_to_batch(examples: List[Dict[str, Any]]) -> Dict[str, list]:
    cols = sorted(examples[0].keys())
    arrays = []
    for col in cols:
        arrays.append([example[col] for example in examples])
    return dict(zip(cols, arrays))


class ExamplesIterable:
    def __init__(self, generate_examples_fn, kwargs):
        self.generate_examples_fn = generate_examples_fn
        self.kwargs = kwargs

    def __iter__(self):
        for key, example in self.generate_examples_fn(**self.kwargs):
            yield example


class IterableDataset(DatasetInfoMixin):
    """A Dataset backed by an iterable."""

    def __init__(
        self,
        iterable: Iterable,
        info: Optional[DatasetInfo] = None,
        split: Optional[NamedSplit] = None,
        format: Optional[dict] = None,
    ):
        info = info.copy() if info is not None else DatasetInfo()
        format = format if format is not None else {}
        DatasetInfoMixin.__init__(self, info=info, split=split)

        self._iterable = iterable
        self._format_type = format.get("format_type")
        self._transform = format.get("transform")

        # Infer features if None

        inferred_features = _infer_features_from_batch(self._head())
        if self.info.features is None:
            self.info.features = inferred_features

        # Sanity checks

        assert self.features is not None, "Features can't be None in a Dataset object"
        if self.info.features.type != inferred_features.type:
            raise ValueError(
                "External features info don't match the dataset:\nGot\n{}\nwith type\n{}\n\nbut expected something like\n{}\nwith type\n{}".format(
                    self.info.features, self.info.features.type, inferred_features, inferred_features.type
                )
            )

    def _head(self, n=5):
        return _examples_to_batch([x for x, _ in zip(self, range(n))])

    def __iter__(self):
        for example in self._iterable:
            if self._transform is not None:
                yield self._transform(example)
            else:
                yield example

    def with_format(
        self,
        type: Optional[str] = None,
        transform: Optional[Callable] = None,
    ):
        if type == "torch":
            import torch

            class TorchIterableDataset(IterableDataset, torch.utils.data.IterableDataset):
                pass

            cls = TorchIterableDataset
        else:
            cls = IterableDataset
        dataset = cls(
            iterable=self._iterable,
            info=self._info,
            split=self._split,
            format={"format_type": self._format_type, "transform": self._transform},
        )
        return dataset


class IterableDatasetDict(dict):
    pass


def load_dataset(
    path: str,
    name: Optional[str] = None,
    data_dir: Optional[str] = None,
    data_files: Union[Dict, List] = None,
    split: Optional[Union[str, Split]] = None,
    cache_dir: Optional[str] = None,
    features: Optional[Features] = None,
    download_config: Optional[DownloadConfig] = None,
    download_mode: Optional[GenerateMode] = None,
    script_version: Optional[Union[str, Version]] = None,
    use_auth_token: Optional[Union[bool, str]] = None,
    **config_kwargs,
):
    r"""Load a dataset in a streaming fashion to get iterable datasets.
    The data are loaded on-the-fly while iterating the dataset.

    This method does the following under the hood:

        1. Download and import in the library the dataset loading script from ``path`` if it's not already cached inside the library.

            Processing scripts are small python scripts that define the citation, info and format of the dataset,
            contain the URL to the original data files and the code to load examples from the original data files.

            You can find some of the scripts here: https://github.com/huggingface/datasets/datasets
            and easily upload yours to share them using the CLI ``huggingface-cli``.
            You can find the complete list of datasets in the Datasets Hub at https://huggingface.co/datasets

        2. Run the dataset loading script which will:

            * Prefetch the dataset file from the original URL (see the script) if it's not already downloaded and cached.
            * Iterate through the dataset file to generate examples.

                Usually data are loaded line by line from the dataset file in order to stream the data instead of downloading everything.
                However in some cases (for json data or compressed archives for example), the whole file needs to be loaded in memory.
                In this case, the dataset file is entirely downloaded before the examples are generated.

        3. Return a dataset built from the requested splits in ``split`` (default: all).

    Args:

        path (:obj:`str`): Path to the dataset processing script with the dataset builder. Can be either:

            - a local path to processing script or the directory containing the script (if the script has the same name as the directory),
              e.g. ``'./dataset/squad'`` or ``'./dataset/squad/squad.py'``.
            - a dataset identifier in the HuggingFace Datasets Hub (list all available datasets and ids with ``datasets.list_datasets()``)
              e.g. ``'squad'``, ``'glue'`` or ``'openai/webtext'``.
        name (:obj:`str`, optional): Defining the name of the dataset configuration.
        data_files (:obj:`str`, optional): Defining the data_files of the dataset configuration.
        data_dir (:obj:`str`, optional): Defining the data_dir of the dataset configuration.
        split (:class:`Split` or :obj:`str`): Which split of the data to load.
            If None, will return a `dict` with all splits (typically `datasets.Split.TRAIN` and `datasets.Split.TEST`).
            If given, will return a single Dataset.
            Splits can be combined and specified like in tensorflow-datasets.
        cache_dir (:obj:`str`, optional): Directory to read/write data. Defaults to "~/datasets".
        features (:class:`Features`, optional): Set the features type to use for this dataset.
        download_config (:class:`~utils.DownloadConfig`, optional): Specific download configuration parameters.
        download_mode (:class:`GenerateMode`, optional): Select the download/generate mode - Default to REUSE_DATASET_IF_EXISTS
        script_version (:class:`~utils.Version` or :obj:`str`, optional): Version of the dataset script to load:

            - For canonical datasets in the `huggingface/datasets` library like "squad", the default version of the module is the local version fo the lib.
              You can specify a different version from your local version of the lib (e.g. "master" or "1.2.0") but it might cause compatibility issues.
            - For community provided datasets like "lhoestq/squad" that have their own git repository on the Datasets Hub, the default version "main" corresponds to the "main" branch.
              You can specify a different version that the default "main" by using a commit sha or a git tag of the dataset repository.
        use_auth_token (Optional ``Union[str, bool]``): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
            If True, will get token from `~/.huggingface`.
        **config_kwargs: Keyword arguments to be passed to the :class:`BuilderConfig` and used in the :class:`DatasetBuilder`.

    Returns:
        :class:`IterableDataset` or :class:`IterableDatasetDict`:
            if `split` is not None: the dataset requested,
            if `split` is None, a ``datasets.streaming.IterableDatasetDict`` with each split.

    """
    # Download/copy dataset processing script
    module_path, hash, resolved_file_path = prepare_module(
        path,
        script_version=script_version,
        download_config=download_config,
        download_mode=download_mode,
        dataset=True,
        return_resolved_file_path=True,
        use_auth_token=use_auth_token,
    )
    extend_module_for_streaming(module_path)

    # Set the base path for downloads as the parent of the script location
    if resolved_file_path is not None:
        base_path = url_or_path_parent(resolved_file_path)
    else:
        base_path = None

    # Get dataset builder class from the processing script
    builder_cls = import_main_class(module_path, dataset=True)

    # Instantiate the dataset builder
    builder_instance: DatasetBuilder = builder_cls(
        cache_dir=cache_dir,
        name=name,
        data_dir=data_dir,
        data_files=data_files,
        hash=hash,
        features=features,
        **config_kwargs,
    )

    # Build dataset for splits
    ds = as_streaming_dataset(
        builder_instance,
        split=split,
        base_path=base_path,
        use_auth_token=use_auth_token,
    )

    return ds


def extend_module_for_streaming(module_path):
    def xopen(file, mode="r", *args, **kwargs):
        return fsspec.open(file, mode=mode, *args, **kwargs).open()

    module = importlib.import_module(module_path)
    module.open = xopen


class StreamingDownloadManager(object):
    def __init__(
        self,
        dataset_name: Optional[str] = None,
        data_dir: Optional[str] = None,
        download_config: Optional[DownloadConfig] = None,
        base_path: Optional[str] = None,
    ):
        self._dataset_name = dataset_name
        self._data_dir = data_dir
        self._download_config = download_config or DownloadConfig()
        self._base_path = base_path or os.path.abspath(".")

    @property
    def manual_dir(self):
        return self._data_dir

    def download(self, url_or_urls):
        return url_or_urls

    def extract(self, path_or_paths):
        return path_or_paths

    def download_and_extract(self, url_or_urls):
        return self.extract(self.download(url_or_urls))


def as_streaming_dataset(
    builder_instance: GeneratorBasedBuilder,
    split: Optional[str] = None,
    base_path: Optional[str] = None,
    use_auth_token: Optional[str] = None,
) -> Union[Dict[str, IterableDataset], IterableDataset]:
    if not isinstance(builder_instance, GeneratorBasedBuilder):
        raise ValueError(f"Builder {builder_instance.name} is not streamable.")
    # By default, return all splits
    if split is None:
        split = {s: s for s in builder_instance.info.splits}

    # Create a dataset for each of the given splits
    datasets = map_nested(
        partial(
            _as_streaming_dataset_single,
            builder_instance=builder_instance,
            base_path=base_path,
            use_auth_token=use_auth_token,
        ),
        split,
        map_tuple=True,
    )
    if isinstance(datasets, dict):
        datasets = IterableDatasetDict(datasets)
    return datasets


def _as_streaming_dataset_single(
    split: str,
    builder_instance: GeneratorBasedBuilder,
    base_path: Optional[str] = None,
    use_auth_token: Optional[str] = None,
) -> IterableDataset:
    dl_manager = StreamingDownloadManager(
        base_path=base_path,
        download_config=DownloadConfig(use_auth_token=use_auth_token),
        dataset_name=builder_instance.name,
        data_dir=builder_instance.config.data_dir,
    )
    splits_generators = {sg.name: sg for sg in builder_instance._split_generators(dl_manager)}
    if split not in splits_generators:
        raise ValueError(f"Bad split: {split}. Available splits: {list(splits_generators)}")
    gen_kwargs = splits_generators[split].gen_kwargs
    iterable = ExamplesIterable(builder_instance._generate_examples, kwargs=gen_kwargs)
    return IterableDataset(iterable, info=builder_instance.info, split=split)
