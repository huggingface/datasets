import pandas as pd
import pyarrow as pa

from ..arrow_dataset import Dataset
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
