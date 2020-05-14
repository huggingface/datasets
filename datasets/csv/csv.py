# coding=utf-8

from dataclasses import dataclass

import pyarrow.csv as pac

import nlp


@dataclass
class CsvConfig(nlp.BuilderConfig):
    """BuilderConfig for CSV."""

    skip_rows: int = 0
    header_as_column_names: bool = True
    delimiter: str = ","
    quote_char: str = '"'
    read_options: pac.ReadOptions = None
    parse_options: pac.ParseOptions = None
    convert_options: pac.ConvertOptions = None

    @property
    def pa_read_options(self):
        read_options = self.read_options or pac.ReadOptions()
        read_options.skip_rows = self.skip_rows
        read_options.autogenerate_column_names = not self.header_as_column_names
        return read_options

    @property
    def pa_parse_options(self):
        parse_options = self.parse_options or pac.ParseOptions()
        parse_options.delimiter = self.delimiter
        parse_options.quote_char = self.quote_char
        return parse_options

    @property
    def pa_convert_options(self):
        convert_options = self.convert_options or pac.ConvertOptions()
        return convert_options


class Csv(nlp.ArrowBasedBuilder):
    BUILDER_CONFIGS = [
        CsvConfig(name="CSV", version=nlp.Version("1.0.0"), description="Csv dataloader",),
    ]

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
            pa_table = pac.read_csv(
                file,
                read_options=self.config.pa_read_options,
                parse_options=self.config.pa_parse_options,
                convert_options=self.config.convert_options,
            )
            yield i, pa_table
