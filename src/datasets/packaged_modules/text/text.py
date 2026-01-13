from dataclasses import dataclass
from io import StringIO
from typing import Optional

import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.features.features import require_storage_cast
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class TextConfig(datasets.BuilderConfig):
    """BuilderConfig for text files."""

    features: Optional[datasets.Features] = None
    encoding: str = "utf-8"
    encoding_errors: Optional[str] = None
    chunksize: int = 10 << 20  # 10MB
    keep_linebreaks: bool = False
    sample_by: str = "line"


class Text(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = TextConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """The `data_files` kwarg in load_dataset() can be a str, List[str], Dict[str,str], or Dict[str,List[str]].

        If str or List[str], then the dataset returns only the 'train' split.
        If dict, then keys should be from the `datasets.Split` enum.
        """
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        base_data_files = dl_manager.download(self.config.data_files)
        extracted_data_files = dl_manager.extract(base_data_files)
        splits = []
        for split_name, files in extracted_data_files.items():
            files_iterables = [dl_manager.iter_files(file) for file in files]
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={"files_iterables": files_iterables, "base_files": base_data_files[split_name]},
                )
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.config.features is not None:
            schema = self.config.features.arrow_schema
            if all(not require_storage_cast(feature) for feature in self.config.features.values()):
                # cheaper cast
                pa_table = pa_table.cast(schema)
            else:
                # more expensive cast; allows str <-> int/float or str to Audio for example
                pa_table = table_cast(pa_table, schema)
            return pa_table
        else:
            return pa_table.cast(pa.schema({"text": pa.string()}))

    def _generate_shards(self, base_files, files_iterables):
        yield from base_files

    def _generate_tables(self, base_files, files_iterables):
        pa_table_names = list(self.config.features) if self.config.features is not None else ["text"]
        for shard_idx, files_iterable in enumerate(files_iterables):
            for file in files_iterable:
                # open in text mode, by default translates universal newlines ("\n", "\r\n" and "\r") into "\n"
                with open(file, encoding=self.config.encoding, errors=self.config.encoding_errors) as f:
                    if self.config.sample_by == "line":
                        batch_idx = 0
                        while True:
                            batch = f.read(self.config.chunksize)
                            if not batch:
                                break
                            batch += f.readline()  # finish current line
                            # StringIO.readlines, by default splits only on "\n" (and keeps line breaks)
                            batch = StringIO(batch).readlines()
                            if not self.config.keep_linebreaks:
                                batch = [line.rstrip("\n") for line in batch]
                            pa_table = pa.Table.from_arrays([pa.array(batch)], names=pa_table_names)
                            # Uncomment for debugging (will print the Arrow table size and elements)
                            # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                            # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                            yield Key(shard_idx, batch_idx), self._cast_table(pa_table)
                            batch_idx += 1
                    elif self.config.sample_by == "paragraph":
                        batch_idx = 0
                        batch = ""
                        while True:
                            new_batch = f.read(self.config.chunksize)
                            if not new_batch:
                                break
                            batch += new_batch
                            batch += f.readline()  # finish current line
                            batch = batch.split("\n\n")
                            pa_table = pa.Table.from_arrays(
                                [pa.array([example for example in batch[:-1] if example])], names=pa_table_names
                            )
                            # Uncomment for debugging (will print the Arrow table size and elements)
                            # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                            # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                            yield Key(shard_idx, batch_idx), self._cast_table(pa_table)
                            batch_idx += 1
                            batch = batch[-1]
                        if batch:
                            pa_table = pa.Table.from_arrays([pa.array([batch])], names=pa_table_names)
                            yield (shard_idx, batch_idx), self._cast_table(pa_table)
                    elif self.config.sample_by == "document":
                        text = f.read()
                        pa_table = pa.Table.from_arrays([pa.array([text])], names=pa_table_names)
                        yield Key(shard_idx, 0), self._cast_table(pa_table)
