import pyarrow.json as paj

from ..arrow_dataset import Dataset
from .abc import AbstractDatasetReader


class JsonlDatasetReader(AbstractDatasetReader):
    def read(self):
        table = self._read_table()
        return Dataset(table, info=self.info, split=self.split)

    def _read_table(self):
        # try:
        with open(self.path, "rb") as f:
            table = paj.read_json(f)
        return table
