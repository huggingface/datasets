import io
import json
from dataclasses import dataclass
from typing import Optional

import pyarrow as pa
import pyarrow.json as paj

import datasets
from datasets.table import table_cast
from datasets.utils.file_utils import readline


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class JsonConfig(datasets.BuilderConfig):
    """BuilderConfig for JSON."""

    features: Optional[datasets.Features] = None
    field: Optional[str] = None
    use_threads: bool = True  # deprecated
    block_size: Optional[int] = None  # deprecated
    chunksize: int = 10 << 20  # 10MB
    newlines_in_values: Optional[bool] = None

    @property
    def schema(self):
        return self.features.arrow_schema if self.features is not None else None


class Json(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = JsonConfig

    def _info(self):
        if self.config.block_size is not None:
            logger.warning("The JSON loader parameter `block_size` is deprecated. Please use `chunksize` instead")
            self.config.chunksize = self.config.block_size
        if self.config.use_threads is not True:
            logger.warning(
                "The JSON loader parameter `use_threads` is deprecated and doesn't have any effect anymore."
            )
        if self.config.newlines_in_values is not None:
            raise ValueError("The JSON loader parameter `newlines_in_values` is no longer supported")
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
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": dl_manager.iter_files(files)})
            ]
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": dl_manager.iter_files(files)}))
        return splits

    def _cast_classlabels(self, pa_table: pa.Table) -> pa.Table:
        if self.config.features:
            # Encode column if ClassLabel
            for i, col in enumerate(self.config.features.keys()):
                if isinstance(self.config.features[col], datasets.ClassLabel):
                    if pa_table[col].type == pa.string():
                        pa_table = pa_table.set_column(
                            i, self.config.schema.field(col), [self.config.features[col].str2int(pa_table[col])]
                        )
                    elif pa_table[col].type != self.config.schema.field(col).type:
                        raise ValueError(
                            f"Field '{col}' from the JSON data of type {pa_table[col].type} is not compatible with ClassLabel. Compatible types are int64 and string."
                        )
            # Cast allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.config.schema)
        return pa_table

    def _generate_tables(self, files):
        for file_idx, file in enumerate(files):

            # If the file is one json object and if we need to look at the list of items in one specific field
            if self.config.field is not None:
                with open(file, encoding="utf-8") as f:
                    dataset = json.load(f)

                # We keep only the field we are interested in
                dataset = dataset[self.config.field]

                # We accept two format: a list of dicts or a dict of lists
                if isinstance(dataset, (list, tuple)):
                    mapping = {col: [dataset[i][col] for i in range(len(dataset))] for col in dataset[0].keys()}
                else:
                    mapping = dataset
                pa_table = pa.Table.from_pydict(mapping=mapping)
                yield file_idx, self._cast_classlabels(pa_table)

            # If the file has one json object per line
            else:
                with open(file, "rb") as f:
                    batch_idx = 0
                    # Use block_size equal to the chunk size divided by 32 to leverage multithreading
                    # Set a default minimum value of 16kB if the chunk size is really small
                    block_size = max(self.config.chunksize // 32, 16 << 10)
                    while True:
                        batch = f.read(self.config.chunksize)
                        if not batch:
                            break
                        # Finish current line
                        try:
                            batch += f.readline()
                        except (AttributeError, io.UnsupportedOperation):
                            batch += readline(f)
                        try:
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
                        except pa.ArrowInvalid as e:
                            logger.error(f"Failed to read file '{file}' with error {type(e)}: {e}")
                            try:
                                with open(file, encoding="utf-8") as f:
                                    dataset = json.load(f)
                            except json.JSONDecodeError:
                                raise e
                            raise ValueError(
                                f"Not able to read records in the JSON file at {file}. "
                                f"You should probably indicate the field of the JSON file containing your records. "
                                f"This JSON file contain the following fields: {str(list(dataset.keys()))}. "
                                f"Select the correct one and provide it as `field='XXX'` to the dataset loading method. "
                            ) from None
                        # Uncomment for debugging (will print the Arrow table size and elements)
                        # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                        # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                        yield (file_idx, batch_idx), self._cast_classlabels(pa_table)
                        batch_idx += 1
