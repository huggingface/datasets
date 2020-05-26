# coding=utf-8

from dataclasses import dataclass

import pyarrow as pa
import pyarrow.json as paj

import nlp


@dataclass
class JsonConfig(nlp.BuilderConfig):
    """BuilderConfig for JSON."""

    read_options: paj.ReadOptions = paj.ReadOptions()
    parse_options: paj.ParseOptions = paj.ParseOptions()

    @property
    def pa_read_options(self):
        return self.read_options

    @property
    def pa_parse_options(self):
        return self.parse_options


class Json(nlp.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = JsonConfig

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
            pa_table = paj.read_json(
                file, read_options=self.config.pa_read_options, parse_options=self.config.pa_parse_options,
            )
            yield i, pa_table
