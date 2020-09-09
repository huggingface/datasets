import logging
from dataclasses import dataclass
from typing import List

import pyarrow.csv as pac

import nlp


logger = logging.getLogger(__name__)

FEATURES = nlp.Features(
    {
        "text": nlp.Value("string"),
    }
)


@dataclass
class TextConfig(nlp.BuilderConfig):
    """BuilderConfig for text files."""

    encoding: str = None
    block_size: int = None
    use_threads: bool = None
    read_options: pac.ReadOptions = None
    parse_options: pac.ParseOptions = None
    convert_options: pac.ConvertOptions = None

    @property
    def pa_read_options(self):
        if self.read_options is not None:
            read_options = self.read_options
        else:
            read_options = pac.ReadOptions(column_names=["text"])
        if self.encoding is not None:
            read_options.encoding = self.encoding
        if self.block_size is not None:
            read_options.block_size = self.block_size
        if self.use_threads is not None:
            read_options.use_threads = self.use_threads
        return read_options

    @property
    def pa_parse_options(self):
        if self.parse_options is not None:
            parse_options = self.parse_options
        else:
            parse_options = pac.ParseOptions(
                delimiter="\r",
                quote_char=False,
                double_quote=False,
                escape_char=False,
                newlines_in_values=False,
                ignore_empty_lines=False,
            )
        return parse_options

    @property
    def pa_convert_options(self):
        if self.convert_options is not None:
            convert_options = self.convert_options
        else:
            convert_options = pac.ConvertOptions(
                column_types=FEATURES.type,
            )
        return convert_options


class Text(nlp.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = TextConfig

    def _info(self):
        return nlp.DatasetInfo(features=FEATURES)

    def _split_generators(self, dl_manager):
        """The `datafiles` kwarg in load_dataset() can be a str, List[str], Dict[str,str], or Dict[str,List[str]].

        If str or List[str], then the dataset returns only the 'train' split.
        If dict, then keys should be from the `nlp.Split` enum.
        """
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download_and_extract(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            return [nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name in [nlp.Split.TRAIN, nlp.Split.VALIDATION, nlp.Split.TEST]:
            if split_name in data_files:
                files = data_files[split_name]
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
            # Uncomment for debugging (will print the Arrow table size and elements)
            # logger.warning(f"pa_table: {pa_table} num rows: {pa_table.num_rows}")
            # logger.warning('\n'.join(str(pa_table.slice(i, 1).to_pydict()) for i in range(pa_table.num_rows)))
            yield i, pa_table
