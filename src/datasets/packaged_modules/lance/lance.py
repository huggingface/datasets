from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pyarrow as pa

import datasets
from datasets.builder import Key


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class LanceConfig(datasets.BuilderConfig):
    """
    BuilderConfig for Lance format.

    Args:
        dataset_dirs: (`List[dict[str, str]]`):
            List of dataset directories with their split names.
            Example: [{"path": ["path/to/dataset1.lance", "path/to/dataset2.lance"], "split": "train"},
                      {"path": ["path/to/dataset3.lance"], "split": "test"}]
        features: (`Features`, *optional*):
            Cast the data to `features`.
        columns: (`List[str]`, *optional*):
            List of columns to load, the other ones are ignored.
        batch_size: (`int`, *optional*):
            Size of the RecordBatches to iterate on.
    """

    dataset_dirs: list[dict[str, str]] = None

    features: Optional[datasets.Features] = None
    columns: Optional[List[str]] = None
    batch_size: Optional[int] = None

    def __post_init__(self):
        return super().__post_init__()


class Lance(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = LanceConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        print("GENERATING: ", self.config, self)
        splits = []
        if self.config.dataset_dirs is None:
            # if not speficied, treat whole data_files as a single split
            for split, files in self.config.data_files.items():
                dataset_paths = set()
                for data_file in files:
                    print(data_file)
                    dataset_paths.add(str(Path(data_file).parent.parent))
                print(list(dataset_paths))
                splits.append(
                    datasets.SplitGenerator(name=split, gen_kwargs={"paths": dl_manager.download(list(dataset_paths))})
                )
            return splits

        for split_dataset in self.config.dataset_dirs:
            split = split_dataset.get("split", "train")
            dataset_paths = split_dataset["path"]
            files = []
            for dataset_path in dataset_paths:
                files.append(dl_manager.download(dataset_path))

            splits.append(datasets.SplitGenerator(name=split, gen_kwargs={"paths": files}))

        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, paths: List[str]):
        import lance

        for dataset_path in paths:
            dataset = lance.dataset(dataset_path)
            for idx, batch in enumerate(
                dataset.to_batches(columns=self.config.columns, batch_size=self.config.batch_size)
            ):
                table = pa.Table.from_batches([batch])
                table = self._cast_table(table)
                yield Key(0, idx), table
