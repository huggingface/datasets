import pyarrow as pa
import pyarrow.json as paj

from ..arrow_dataset import Dataset
from .abc import AbstractDatasetReader


class JsonlDatasetReader(AbstractDatasetReader):
    def read(self):
        table = self._read_table()
        table = self._cast_table_to_info_features(table)
        return Dataset(table, info=self.info, split=self.split)

    def _read_table(self):
        # try:
        with open(self.path, "rb") as f:
            table = paj.read_json(f)
        return table

    def _cast_table_to_info_features(self, table):
        if self.info and self.info.features:
            type = self.info.features.type
            # try
            schema = pa.schema({col_name: type[col_name].type for col_name in table.column_names})
            # try
            table = table.cast(schema)
        return table
