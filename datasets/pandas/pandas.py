# coding=utf-8

import pandas as pd
import pyarrow as pa

import nlp


class Pandas(nlp.ArrowBasedBuilder):
    def _info(self):
        return nlp.DatasetInfo()

    def _split_generators(self, dl_manager):
        """ We handle string, list and dicts in datafiles
        """
        if isinstance(self.config.data_files, (str, list, tuple)):
            files = self.config.data_files
            if isinstance(files, str):
                files = [files]
            return [nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name in [nlp.Split.TRAIN, nlp.Split.VALIDATION, nlp.Split.TEST]:
            if split_name in self.config.data_files:
                files = self.config.data_files[split_name]
                if isinstance(files, str):
                    files = [files]
                splits.append(nlp.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _generate_tables(self, files):
        for i, file in enumerate(files):
            pa_table = pa.Table.from_pandas(pd.read_pickle(file))
            yield i, pa_table
