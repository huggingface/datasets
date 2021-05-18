import importlib
from typing import Dict, List, Optional, Union

from .builder import DatasetBuilder
from .dataset_dict import IterableDatasetDict
from .features import Features
from .iterable_dataset import IterableDataset
from .load import import_main_class, prepare_module, url_or_path_parent
from .splits import Split
from .utils import DownloadConfig
from .utils.download_manager import GenerateMode
from .utils.logging import get_logger
from .utils.streaming_download_manager import xjoin, xopen
from .utils.version import Version


logger = get_logger(__name__)


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
) -> Union[IterableDataset, IterableDatasetDict]:
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
    ds = builder_instance.as_streaming_dataset(
        split=split,
        base_path=base_path,
        use_auth_token=use_auth_token,
    )

    return ds


class _PatchedModuleObj:
    """Set all the modules components as attributes of the _PatchedModuleObj object"""

    def __init__(self, module):
        if module is not None:
            for key in getattr(module, "__all__", module.__dict__):
                if not key.startswith("__"):
                    setattr(self, key, getattr(module, key))


class patch_submodule:
    """
    Patch a submodule attribute of an object, by keeping all other submodules intact at all levels.

    Example::

        >>> import importlib
        >>> from datasets.load import prepare_module
        >>> from datasets.streaming import patch_submodule, xjoin
        >>>
        >>> snli_module_path, _ = prepare_module("snli")
        >>> snli_module = importlib.import_module(snli_module_path)
        >>> patcher = patch_submodule(snli_module, "os.path.join", xjoin)
        >>> patcher.start()
        >>> assert snli_module.os.path.join is xjoin
    """

    _active_patches = []

    def __init__(self, obj, target: str, new):
        self.obj = obj
        self.target = target
        self.new = new
        self.key = target.split(".")[0]
        self.original = getattr(obj, self.key, None)

    def __enter__(self):
        *submodules, attr = self.target.split(".")
        current = self.obj
        for key in submodules:
            setattr(current, key, _PatchedModuleObj(getattr(current, key, None)))
            current = getattr(current, key)
        setattr(current, attr, self.new)

    def __exit__(self, *exc_info):
        setattr(self.obj, self.key, self.original)

    def start(self):
        """Activate a patch."""
        self.__enter__()
        self._active_patches.append(self)

    def stop(self):
        """Stop an active patch."""
        try:
            self._active_patches.remove(self)
        except ValueError:
            # If the patch hasn't been started this will fail
            return None

        return self.__exit__()


def extend_module_for_streaming(module_path):
    """
    Extend the `open` and `os.path.join` functions of the module to support data streaming.
    They rare replaced by `xopen` and `xjoin` defined to work with the StreamingDownloadManager.

    We use fsspec to extend `open` to be able to read remote files.
    To join paths and naviguate in remote compressed archives, we use the "::" separator.
    """

    module = importlib.import_module(module_path)
    # open files in a streaming fashion
    patch_submodule(module, "open", xopen).start()
    # allow to navigate in remote zip files
    patch_submodule(module, "os.path.join", xjoin).start()
