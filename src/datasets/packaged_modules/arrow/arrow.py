import itertools
from dataclasses import dataclass
from typing import List, Optional

import pyarrow as pa

import datasets
from datasets.table import _memory_mapped_record_batch_reader_from_file, read_schema_from_file, table_cast


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class ArrowConfig(datasets.BuilderConfig):
    """BuilderConfig for Arrow."""

    batch_size: int = 10_000
    columns: Optional[List[str]] = None
    features: Optional[datasets.Features] = None


class Arrow(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = ArrowConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download_and_extract(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            # Use `dl_manager.iter_files` to skip hidden files in an extracted archive
            files = [dl_manager.iter_files(file) for file in files]
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            # Use `dl_manager.iter_files` to skip hidden files in an extracted archive
            files = [dl_manager.iter_files(file) for file in files]
            # Infer features is they are stoed in the arrow schema
            if self.info.features is None:
                for file in itertools.chain.from_iterable(files):
                    self.info.features = datasets.Features.from_arrow_schema(read_schema_from_file(file))
                    # with open(file, "rb") as f:
                    break
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, files):
        schema = self.info.features.arrow_schema if self.info.features is not None else None
        if self.info.features is not None and self.config.columns is not None:
            if sorted(field.name for field in schema) != sorted(self.config.columns):
                raise ValueError(
                    f"Tried to load parquet data with columns '{self.config.columns}' with mismatching features '{self.info.features}'"
                )
        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            for batch_idx, record_batch in enumerate(_memory_mapped_record_batch_reader_from_file(file)):
                pa_table = pa.Table.from_batches([record_batch])
                yield f"{file_idx}_{batch_idx}", self._cast_table(pa_table)
