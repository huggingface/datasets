import logging
from dataclasses import dataclass

import pandas as pd
import pyarrow as pa

import datasets


logger = logging.getLogger(__name__)

FEATURES = datasets.Features(
    {
        "text": datasets.Value("string"),
    }
)


@dataclass
class TextConfig(datasets.BuilderConfig):
    """BuilderConfig for text files."""

    encoding: str = None
    chunksize: int = 10_000


class Text(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = TextConfig

    def _info(self):
        return datasets.DatasetInfo(features=FEATURES)

    def _split_generators(self, dl_manager):
        """The `datafiles` kwarg in load_dataset() can be a str, List[str], Dict[str,str], or Dict[str,List[str]].

        If str or List[str], then the dataset returns only the 'train' split.
        If dict, then keys should be from the `datasets.Split` enum.
        """
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download_and_extract(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]:
            if split_name in data_files:
                files = data_files[split_name]
                if isinstance(files, str):
                    files = [files]
                splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _generate_tables(self, files):
        for i, file in enumerate(files):
            text_file_reader = pd.read_csv(
                file,
                dtype={"text": str},
                names=["text"],
                header=None,
                iterator=True,
                chunksize=self.config.chunksize,
                encoding=self.config.encoding,
                sep="\n",
            )
            for j, df in enumerate(text_file_reader):
                pa_table = pa.Table.from_pandas(df)
                # Uncomment for debugging (will print the Arrow table size and elements)
                # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
                # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
                yield (i, j), pa_table
