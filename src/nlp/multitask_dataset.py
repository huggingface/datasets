from typing import List, Optional, Union

import numpy as np
import pyarrow as pa

from .arrow_reader import Dataset


class MultiDataset:
    def __init__(self, tasks, seed=None):
        self.tasks = tasks
        self.seed = seed

        # Check matching columns
        for task in self.tasks[1:]:
            if task.column_names != self.tasks[0].column_names:
                raise Exception("Tasks must have matching columns")

        # Create random order of tasks
        # Using size-proportional sampling
        task_choice_list = []
        for i, task in enumerate(self.tasks):
            task_choice_list += [i] * len(task)
        task_choice_list = np.array(task_choice_list)
        np.random.seed(self.seed)
        np.random.shuffle(task_choice_list)

        # Add index into each dataset
        # - We don't want to shuffle within each task
        counters = {}
        self.task_choice_list = []
        for i in range(len(task_choice_list)):
            idx = counters.get(task_choice_list[i], 0)
            self.task_choice_list.append((task_choice_list[i], idx))
            counters[task_choice_list[i]] = idx + 1

    @property
    def data(self):
        raise NotImplementedError()

    @property
    def cache_files(self):
        return [j for t in self.tasks for j in t.cache_files]

    def columns(self):
        return np.concatenate([d.columns for d in self.tasks], axis=1)

    @property
    def nbytes(self):
        return np.sum([t.nbytes for t in self.tasks])

    @property
    def num_columns(self):
        return self.tasks[0].num_columns

    @property
    def num_rows(self):
        return len(self)

    @property
    def column_names(self):
        return self.tasks[0].column_names

    @property
    def schema(self) -> pa.Schema:
        return self.tasks[0].schema

    @property
    def shape(self):
        return (self.num_rows, self.num_columns)

    def drop(self, columns: Union[str, List[str]]):
        """ Drop one or more columns.

        Args:
            columns: list of str
        """
        for task in self.tasks:
            task.drop(columns)

    def unique(self, column: str):
        """ Return a list of the unique elements in a column.

        Args:
        columns: str
        """
        raise NotImplementedError()

    def dictionary_encode_column(self, column: str):
        raise NotImplementedError()

    def flatten(self):
        raise NotImplementedError()

    def __len__(self):
        return np.sum([len(t) for t in self.tasks])

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __repr__(self):
        task_str = ", ".join([str(t) for t in self.tasks])
        return f"MultiDataset(tasks: {task_str})"

    def format(self):
        raise NotImplementedError()

    def formated_as(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        raise NotImplementedError()

    def set_format(
        self,
        type: Optional[str] = None,
        columns: Optional[List] = None,
        output_all_columns: bool = False,
        **format_kwargs,
    ):
        raise NotImplementedError()

    def reset_format(self):
        raise NotImplementedError()

    def __getitem__(self, key):
        if isinstance(key, int):
            task_idx, example_idx = self.task_choice_list[key]
            task = self.tasks[task_idx]
            example = task[example_idx]
            example["task_name"] = task.info.builder_name
            return example
        elif isinstance(key, slice):
            raise NotImplementedError()

    def cleanup_cache_files(self):
        len_files_to_remove = 0
        for task in self.tasks:
            len_files_to_remove += task.cleanup_cache_files()
        return len_files_to_remove

    def map(
        self,
        function,
        with_indices: bool = False,
        batched: bool = False,
        batch_size: Optional[int] = 1000,
        remove_columns: Optional[List[str]] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
        arrow_schema: Optional[pa.Schema] = None,
        disable_nullable: bool = True,
    ):
        raise NotImplementedError()

    def filter(self, function, with_indices=False, **kwargs):
        raise NotImplementedError()

    def select(
        self,
        indices: Union[List[int], np.ndarray],
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        raise NotImplementedError()

    def sort(
        self,
        column: str,
        reverse: bool = False,
        kind: str = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        raise NotImplementedError()

    def shuffle(
        self,
        seed: Optional[int] = None,
        generator: Optional[np.random.Generator] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        raise NotImplementedError()

    def train_test_split(
        self,
        test_size: Union[float, int, None] = None,
        train_size: Union[float, int, None] = None,
        shuffle: bool = True,
        seed: Optional[int] = None,
        generator: Optional[np.random.Generator] = None,
        keep_in_memory: bool = False,
        load_from_cache_file: bool = True,
        train_cache_file_name: Optional[str] = None,
        test_cache_file_name: Optional[str] = None,
        writer_batch_size: Optional[int] = 1000,
    ):
        raise NotImplementedError()


def build_multitask(*tasks):
    r"""Create a multitask dataset

        This method creates a ``MultiDataset`` wrapper when given a ``Dataset`` object or a dictionary of splits
    """

    if isinstance(tasks[0], Dataset):
        for task in tasks:
            if not isinstance(task, Dataset):
                raise Exception("Mismatched dataset types")

            return MultiDataset(tasks)

    elif isinstance(tasks[0], dict):
        for task in tasks:
            if not isinstance(task, dict):
                raise Exception("Mismatched dataset types")

        def _get_common_splits(tasks):
            """Finds the common splits present in all self.datasets"""
            min_set = None
            for task in tasks:
                if min_set is not None:
                    min_set.intersection(set(task.keys()))
                else:
                    min_set = set(task.keys())
            return min_set

        common_splits = _get_common_splits(tasks)
        out = {}
        for split in common_splits:
            out[split] = MultiDataset([t[split] for t in tasks])
        return out
