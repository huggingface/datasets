"""CoNLL format dataset builder.

Reads CoNLL-style files where each line carries one token plus its tag columns,
columns are whitespace-separated, and empty lines mark sentence boundaries.
Each example is one sentence, with each configured column produced as a list
aligned with the tokens list.

Supports CoNLL-2000 (chunking), CoNLL-2003 (NER), CoNLL-U (Universal
Dependencies), and any custom column schema by overriding ``column_names``.
"""

from dataclasses import dataclass, field
from typing import Optional

import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.features.features import require_storage_cast
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


DEFAULT_COLUMN_NAMES = ["tokens"]


@dataclass
class ConllConfig(datasets.BuilderConfig):
    """BuilderConfig for CoNLL-style files.

    Args:
        features: (`Features`, *optional*):
            Cast the data to `features`.
        column_names: (`list[str]`, defaults to `["tokens"]`):
            Names for each whitespace-separated column. The first name is the
            token column; subsequent names cover the tag columns. Common
            schemas:

            - CoNLL-2003 NER: `["tokens", "pos_tags", "chunk_tags", "ner_tags"]`
            - CoNLL-2000 chunking: `["tokens", "pos_tags", "chunk_tags"]`
            - CoNLL-U: `["id", "form", "lemma", "upos", "xpos", "feats",
              "head", "deprel", "deps", "misc"]`
        delimiter: (`str`, *optional*):
            Column delimiter inside each line. If `None` (default), any
            whitespace is used, matching the standard CoNLL convention.
        encoding: (`str`, defaults to `"utf-8"`):
            Encoding to decode the file.
        encoding_errors: (`str`, *optional*):
            Argument to define what to do in case of encoding error. Same as
            the `errors` argument in `open()`.
        skip_docstart: (`bool`, defaults to `True`):
            Skip CoNLL-2003 `-DOCSTART-` document-boundary marker lines.
        comment_prefix: (`str`, *optional*):
            If set, lines starting with this prefix are skipped. CoNLL-U
            comments start with `#`.
    """

    features: Optional[datasets.Features] = None
    column_names: list[str] = field(default_factory=lambda: list(DEFAULT_COLUMN_NAMES))
    delimiter: Optional[str] = None
    encoding: str = "utf-8"
    encoding_errors: Optional[str] = None
    skip_docstart: bool = True
    comment_prefix: Optional[str] = None


class Conll(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = ConllConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """The `data_files` kwarg in load_dataset() can be a str, List[str],
        Dict[str,str], or Dict[str,List[str]].

        If str or List[str], then the dataset returns only the 'train' split.
        If dict, then keys should be from the `datasets.Split` enum.
        """
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        base_data_files = dl_manager.download(self.config.data_files)
        extracted_data_files = dl_manager.extract(base_data_files)
        splits = []
        for split_name, files in extracted_data_files.items():
            files_iterables = [dl_manager.iter_files(file) for file in files]
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "files_iterables": files_iterables,
                        "base_files": base_data_files[split_name],
                    },
                )
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.config.features is not None:
            schema = self.config.features.arrow_schema
            if all(not require_storage_cast(feature) for feature in self.config.features.values()):
                pa_table = pa_table.cast(schema)
            else:
                pa_table = table_cast(pa_table, schema)
        return pa_table

    def _generate_shards(self, base_files, files_iterables):
        yield from base_files

    def _generate_tables(self, base_files, files_iterables):
        column_names = list(self.config.column_names)
        if not column_names:
            raise ValueError("ConllConfig.column_names must be a non-empty list")
        num_cols = len(column_names)
        delimiter = self.config.delimiter
        skip_docstart = self.config.skip_docstart
        comment_prefix = self.config.comment_prefix

        for shard_idx, files_iterable in enumerate(files_iterables):
            for file in files_iterable:
                sentences: list[list[list[str]]] = []
                current: list[list[str]] = [[] for _ in range(num_cols)]
                with open(file, encoding=self.config.encoding, errors=self.config.encoding_errors) as f:
                    for raw_line in f:
                        # Strip the trailing newline only — preserve embedded whitespace
                        line = raw_line.rstrip("\r\n")
                        if not line.strip():
                            # Sentence boundary
                            if current[0]:
                                sentences.append(current)
                                current = [[] for _ in range(num_cols)]
                            continue
                        if skip_docstart and line.startswith("-DOCSTART-"):
                            continue
                        if comment_prefix is not None and line.startswith(comment_prefix):
                            continue
                        parts = line.split(delimiter) if delimiter is not None else line.split()
                        # Pad or truncate to num_cols so column alignment is preserved
                        if len(parts) < num_cols:
                            parts = parts + [""] * (num_cols - len(parts))
                        elif len(parts) > num_cols:
                            parts = parts[:num_cols]
                        for i, val in enumerate(parts):
                            current[i].append(val)
                    # Tail sentence with no trailing blank line
                    if current[0]:
                        sentences.append(current)

                if sentences:
                    arrays = [pa.array([sentence[col_idx] for sentence in sentences]) for col_idx in range(num_cols)]
                    pa_table = pa.Table.from_arrays(arrays, names=column_names)
                    yield Key(shard_idx, 0), self._cast_table(pa_table)
