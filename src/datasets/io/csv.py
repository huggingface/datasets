import pandas as pd
import pyarrow as pa

from ..arrow_dataset import Dataset
from ..packaged_modules.csv.csv import Csv
from .abc import AbstractDatasetReader


class CsvDatasetReader(AbstractDatasetReader):
    def read(self):
        table = self._read_table()
        return Dataset(table, info=self.info, split=self.split)

    def _read_table(self):
        schema = pa.schema(self.info.features.type) if self.info and self.info.features else None
        dtype = {name: dtype.to_pandas_dtype() for name, dtype in zip(schema.names, schema.types)} if schema else None
        df = pd.read_csv(self.path, dtype=dtype, **self.kwargs)  # dtype allows reading an int column as str
        table = pa.Table.from_pandas(df, schema=schema)
        return table


class CsvDatasetBuilder:
    def __init__(
        self,
        path,
        name=None,
        data_dir=None,
        data_files=None,
        split=None,
        cache_dir=None,
        features=None,
        **config_kwargs,
    ):
        self.split = split
        self.builder = Csv(
            cache_dir=cache_dir,
            name=name,
            data_dir=data_dir,
            data_files=path or data_files,
            hash=hash,
            features=features,
            **config_kwargs,
        )

    def build(self):
        # split = "train"  # None  # if None: num_rows = {'train': 4} instead of 4

        download_config = None
        download_mode = None
        ignore_verifications = False

        use_auth_token = None

        keep_in_memory = False
        save_infos = False

        base_path = None

        # import pdb;pdb.set_trace()

        self.builder.download_and_prepare(
            download_config=download_config,
            download_mode=download_mode,
            ignore_verifications=ignore_verifications,
            # try_from_hf_gcs=try_from_hf_gcs,
            base_path=base_path,
            use_auth_token=use_auth_token,
        )

        # Build dataset for splits
        ds = self.builder.as_dataset(
            split=self.split, ignore_verifications=ignore_verifications, in_memory=keep_in_memory
        )
        if save_infos:
            self.builder._save_infos()

        return ds
