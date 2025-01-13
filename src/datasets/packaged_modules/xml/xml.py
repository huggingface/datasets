import itertools
from dataclasses import dataclass
from typing import Optional

import pyarrow as pa

import datasets
from datasets.features.features import require_storage_cast
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class XmlConfig(datasets.BuilderConfig):
    """BuilderConfig for xml files."""

    features: Optional[datasets.Features] = None
    encoding: str = "utf-8"
    encoding_errors: Optional[str] = None


class Xml(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = XmlConfig

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
        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files = [dl_manager.iter_files(file) for file in files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
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
            return pa_table.cast(pa.schema({"xml": pa.string()}))

    def _generate_tables(self, files):
        pa_table_names = list(self.config.features) if self.config.features is not None else ["xml"]
        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            # open in text mode, by default translates universal newlines ("\n", "\r\n" and "\r") into "\n"
            with open(file, encoding=self.config.encoding, errors=self.config.encoding_errors) as f:
                xml = f.read()
                pa_table = pa.Table.from_arrays([pa.array([xml])], names=pa_table_names)
                yield file_idx, self._cast_table(pa_table)
