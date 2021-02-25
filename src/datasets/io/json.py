import json

import pyarrow as pa
import pyarrow.json as paj

from ..arrow_dataset import Dataset
from .abc import AbstractDatasetReader


class JsonlDatasetReader(AbstractDatasetReader):
    def read(self):
        table = self._read_table()
        # table = self._cast_table_to_info_features(table)
        return Dataset(table, info=self.info, split=self.split)

    def _read_table(self):
        schema = pa.schema(self.info.features.type) if self.info and self.info.features else None
        with open(self.path, "rb") as f:
            try:
                table = paj.read_json(f, parse_options=paj.ParseOptions(explicit_schema=schema))
            except pa.ArrowInvalid:
                with open(self.path, encoding="utf-8") as f:
                    dataset = json.load(f)
                raise ValueError(
                    f"Not able to read records in the JSON file at {self.path}. "
                    f"You should probably indicate the field of the JSON file containing your records. "
                    f"This JSON file contain the following fields: {str(list(dataset.keys()))}. "
                    f"Select the correct one and provide it as `field='XXX'` to the `load_dataset` method. "
                )
        return table

    # def _cast_table_to_info_features(self, table):
    #     if self.info and self.info.features:
    #         type = self.info.features.type
    #         # try
    #         schema = pa.schema({col_name: type[col_name].type for col_name in table.column_names})
    #         # try
    #         table = table.cast(schema)
    #     return table
