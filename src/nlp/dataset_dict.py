from typing import Dict, List, Optional

import numpy as np

from .arrow_dataset import Dataset
from .features import Features


class DatasetDict(dict):

    def _check_values_type(self):
        for dataset in self.values():
            if not isinstance(dataset, Dataset):
                raise TypeError(
                    "Values in `DatasetDict` should of type `Dataset` but got type '{}'".format(type(dataset))
                )

    def map(
        self,
        function,
        with_indices: bool = False,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_names: Optional[Dict[str, str]] = None,
        writer_batch_size: Optional[int] = 1000,
        features: Optional[Features] = None,
        disable_nullable: bool = True,
        verbose: bool = True,
    ) -> "DatasetDict":
        """ Apply a function to all the elements in the table (individually or in batches)
            and update the table (if function does updated examples).
            The transformation is applied to all the datasets of the dataset dictionary.

            Args:
                `function` (`callable`): with one of the following signature:
                    - `function(example: Dict) -> Union[Dict, Any]` if `batched=False` and `with_indices=False`
                    - `function(example: Dict, indices: int) -> Union[Dict, Any]` if `batched=False` and `with_indices=True`
                    - `function(batch: Dict[List]) -> Union[Dict, Any]` if `batched=True` and `with_indices=False`
                    - `function(batch: Dict[List], indices: List[int]) -> Union[Dict, Any]` if `batched=True` and `with_indices=True`
                `with_indices` (`bool`, default: `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
                `batched` (`bool`, default: `False`): Provide batch of examples to `function`
                `batch_size` (`Optional[int]`, default: `1000`): Number of examples per batch provided to `function` if `batched=True`
                    `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
                `remove_columns` (`Optional[List[str]]`, default: `None`): Remove a selection of columns while doing the mapping.
                    Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                    columns with names in `remove_columns`, these columns will be kept.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_names` (`Optional[Dict[str, str]]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                    You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
                `features` (`Optional[nlp.Features]`, default: `None`): Use a specific Features to store the cache file
                    instead of the automatically generated one.
                `disable_nullable` (`bool`, default: `True`): Allow null values in the table.
                `verbose` (`bool`, default: `True`): Set to `False` to deactivate the tqdm progress bar and informations.
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.map(
                    function=function,
                    with_indices=with_indices,
                    batched=batched,
                    batch_size=batch_size,
                    remove_columns=remove_columns,
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    cache_file_name=cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                    features=features,
                    disable_nullable=disable_nullable,
                    verbose=verbose,
                )
                for k, dataset in self.items()
            }
        )

    def filter(
        self,
        function,
        with_indices=False,
        batch_size: Optional[int] = 1000,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_names: Optional[Dict[str, str]] = None,
        writer_batch_size: Optional[int] = 1000,
        verbose: bool = True,
    ) -> "DatasetDict":
        """ Apply a filter function to all the elements in the table in batches
            and update the table so that the dataset only includes examples according to the filter function.
            The transformation is applied to all the datasets of the dataset dictionary.

            Args:
                `function` (`callable`): with one of the following signature:
                    - `function(example: Dict) -> bool` if `with_indices=False`
                    - `function(example: Dict, indices: int) -> bool` if `with_indices=True`
                `with_indices` (`bool`, default: `False`): Provide example indices to `function`. Note that in this case the signature of `function` should be `def function(example, idx): ...`.
                `batch_size` (`Optional[int]`, default: `1000`): Number of examples per batch provided to `function` if `batched=True`
                    `batch_size <= 0` or `batch_size == None`: Provide the full dataset as a single batch to `function`
                `remove_columns` (`Optional[List[str]]`, default: `None`): Remove a selection of columns while doing the mapping.
                    Columns will be removed before updating the examples with the output of `function`, i.e. if `function` is adding
                    columns with names in `remove_columns`, these columns will be kept.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_names` (`Optional[Dict[str, str]]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                    You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
                `verbose` (`bool`, default: `True`): Set to `False` to deactivate the tqdm progress bar and informations.
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.filter(
                    function=function,
                    with_indices=with_indices,
                    batch_size=batch_size,
                    remove_columns=remove_columns,
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    cache_file_name=cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                    verbose=verbose,
                )
                for k, dataset in self.items()
            }
        )

    def sort(
        self,
        column: str,
        reverse: bool = False,
        kind: str = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_names: Optional[Dict[str, str]] = None,
        writer_batch_size: Optional[int] = 1000,
        verbose: bool = True,
    ) -> "DatasetDict":
        """ Create a new dataset sorted according to a column.
            The transformation is applied to all the datasets of the dataset dictionary.

            Currently sorting according to a column name uses numpy sorting algorithm under the hood.
            The column should thus be a numpy compatible type (in particular not a nested type).
            This also means that the column used for sorting is fully loaded in memory (which should be fine in most cases).

            Args:
                `column` (`str`): column name to sort by.
                `reverse`: (`bool`, default: `False`): If True, sort by descending order rather then ascending.
                `kind` (Optional `str`): Numpy algorithm for sorting selected in {‘quicksort’, ‘mergesort’, ‘heapsort’, ‘stable’},
                    The default is ‘quicksort’. Note that both ‘stable’ and ‘mergesort’ use timsort under the covers and, in general,
                    the actual implementation will vary with data type. The ‘mergesort’ option is retained for backwards compatibility.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_names` (`Optional[Dict[str, str]]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                    You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
                `verbose` (`bool`, default: `True`): Set to `False` to deactivate the tqdm progress bar and informations.
        """
        self._check_values_type()
        if cache_file_names is None:
            cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.sort(
                    column=column,
                    reverse=reverse,
                    kind=kind,
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    cache_file_name=cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                    verbose=verbose,
                )
                for k, dataset in self.items()
            }
        )

    def shuffle(
        self,
        seeds: Optional[Dict[str, int]] = None,
        generators: Optional[Dict[str, np.random.Generator]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_names: Optional[Dict[str, str]] = None,
        writer_batch_size: Optional[int] = 1000,
        verbose: bool = True,
    ):
        """ Create a new Dataset where the rows are shuffled.
            The transformation is applied to all the datasets of the dataset dictionary.

            Currently shuffling uses numpy random generators.
            You can either supply a NumPy BitGenerator to use, or a seed to initiate NumPy's default random generator (PCG64).

            Args:
                `seeds` (Optional `Dict[str, int]`): A seed to initialize the default BitGenerator if ``generator=None``.
                    If None, then fresh, unpredictable entropy will be pulled from the OS.
                    If an int or array_like[ints] is passed, then it will be passed to SeedSequence to derive the initial BitGenerator state.
                    You have to provide one :obj:`seed` per dataset in the dataset dictionary.
                `generators` (Optional `Dict[str, np.random.Generator]`): Numpy random Generator to use to compute the permutation of the dataset rows.
                    If ``generator=None`` (default), uses np.random.default_rng (the default BitGenerator (PCG64) of NumPy).
                    You have to provide one :obj:`generator` per dataset in the dataset dictionary.
                `keep_in_memory` (`bool`, default: `False`): Keep the dataset in memory instead of writing it to a cache file.
                `load_from_cache_file` (`bool`, default: `True`): If a cache file storing the current computation from `function`
                    can be identified, use it instead of recomputing.
                `cache_file_names` (`Optional[Dict[str, str]]`, default: `None`): Provide the name of a cache file to use to store the
                    results of the computation instead of the automatically generated cache file name.
                    You have to provide one :obj:`cache_file_name` per dataset in the dataset dictionary.
                `writer_batch_size` (`int`, default: `1000`): Number of rows per write operation for the cache file writer.
                    Higher value gives smaller cache files, lower value consume less temporary memory while running `.map()`.
                `verbose` (`bool`, default: `True`): Set to `False` to deactivate the tqdm progress bar and informations.
        """
        self._check_values_type()
        if seeds is None:
            seeds = {k: None for k in self}
        if generators is None:
            generators = {k: None for k in self}
        if cache_file_names is None:
            cache_file_names = {k: None for k in self}
        return DatasetDict(
            {
                k: dataset.shuffle(
                    seed=seeds[k],
                    generator=generators[k],
                    keep_in_memory=keep_in_memory,
                    load_from_cache_file=load_from_cache_file,
                    cache_file_name=cache_file_names[k],
                    writer_batch_size=writer_batch_size,
                    verbose=verbose,
                )
                for k, dataset in self.items()
            }
        )
