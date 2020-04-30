# coding=utf-8

import nlp
import pyarrow.csv as pac

class Csv(nlp.GeneratorBasedBuilder):
    VERSION = nlp.Version("1.0.0")

    def __init__(self, name, dataset_files, **config):
        self.name = name
        self.files = {}
        self.files["validation"] = dataset_files.get(nlp.Split.VALIDATION, [])
        self.files["test"] = dataset_files.get(nlp.Split.TEST, [])
        self.files["train"] = dataset_files[nlp.Split.TRAIN]
        self.pa_read_options = pac.ReadOptions(
            skip_rows=config.pop("skip_rows", 0),
            autogenerate_column_names=not config.pop("header_as_column_names", True)
        )
        self.pa_parse_options = pac.ParseOptions(
            delimiter=config.pop("delimiter", ","),
            quote_char=config.pop("quote_char", "\"")
        )
        train_content = pac.read_csv(
            self.files["train"][0],
            read_options=self.pa_read_options,
            parse_options=self.pa_parse_options
        )
        self.features = {val.name: nlp.string for val in train_content.schema}
        
        if not self.files["validation"] and not self.files["test"]:
            raise ValueError("A Test or Validation dataset must be given.")

        super(Csv, self).__init__(**config)

    def _info(self):
        return nlp.DatasetInfo(
                builder=self,
                description="bla",
                features=nlp.features.FeaturesDict(
                    self.features
                ),
        )

    def _split_generators(self, dl_manager):
        return [
                nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        gen_kwargs={"split": "train"}),
                nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        gen_kwargs={"split": "validation"}),
                nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        gen_kwargs={"split": "test"})
        ]

    def _generate_examples(self, split):
        for file in self.files[split]:
            content = pac.read_csv(
                file,
                read_options=self.pa_read_options,
                parse_options=self.pa_parse_options
            ).to_pandas()

            for _, v in content.to_dict(orient='index').items():
                yield None, v
