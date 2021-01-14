# coding=utf-8

import json
from dataclasses import dataclass
from io import BytesIO

import pyarrow as pa
import pyarrow.json as paj

import datasets


@dataclass
class JsonConfig(datasets.BuilderConfig):
    """BuilderConfig for JSON."""

    features: datasets.Features = None
    field: str = None
    use_threads: bool = True
    block_size: int = None
    newlines_in_values: bool = None

    @property
    def pa_read_options(self):
        return paj.ReadOptions(use_threads=self.use_threads, block_size=self.block_size)

    @property
    def pa_parse_options(self):
        return paj.ParseOptions(explicit_schema=self.schema, newlines_in_values=self.newlines_in_values)

    @property
    def schema(self):
        return pa.schema(self.features.type) if self.features is not None else None


class Json(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = JsonConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download_and_extract(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _generate_tables(self, files):
        for i, file in enumerate(files):
            if self.config.field is not None:
                with open(file, encoding="utf-8") as f:
                    dataset = json.load(f)

                # We keep only the field we are interested in
                dataset = dataset[self.config.field]

                # We accept two format: a list of dicts or a dict of lists
                if isinstance(dataset, (list, tuple)):
                    pa_table = paj.read_json(
                        BytesIO("\n".join(json.dumps(row) for row in dataset).encode("utf-8")),
                        read_options=self.config.pa_read_options,
                        parse_options=self.config.pa_parse_options,
                    )
                else:
                    pa_table = pa.Table.from_pydict(mapping=dataset, schema=self.config.schema)
            else:
                try:
                    pa_table = paj.read_json(
                        file,
                        read_options=self.config.pa_read_options,
                        parse_options=self.config.pa_parse_options,
                    )
                except pa.ArrowInvalid:
                    with open(file, encoding="utf-8") as f:
                        dataset = json.load(f)
                    raise ValueError(
                        f"Not able to read records in the JSON file at {file}. "
                        f"You should probably indicate the field of the JSON file containing your records. "
                        f"This JSON file contain the following fields: {str(list(dataset.keys()))}. "
                        f"Select the correct one and provide it as `field='XXX'` to the `load_dataset` method. "
                    )
            yield i, pa_table
