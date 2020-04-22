import os
import csv

import nlp


class BbcConfig(nlp.BuilderConfig):
    def __init__(self, **kwargs):
        super(BbcConfig, self).__init__(**kwargs)


class Bbc(nlp.GeneratorBasedBuilder):
    _DIR = "./data"
    _DEV_FILE = "test.csv"
    _TRAINING_FILE = "train.csv"

    BUILDER_CONFIGS = [BbcConfig(name="bbc", version=nlp.Version("1.0.0"))]

    def _info(self):
        return nlp.DatasetInfo(builder=self,
                               features=nlp.features.FeaturesDict({"id": nlp.string, "text": nlp.string, "label": nlp.string}),
                               )

    def _split_generators(self, dl_manager):
        files = {"train": os.path.join(self._DIR, self._TRAINING_FILE), "dev": os.path.join(self._DIR, self._DEV_FILE)}

        return [nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": files["train"]}),
                nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": files["dev"]})]

    def _generate_examples(self, filepath):
        with open(filepath) as f:
            reader = csv.reader(f, delimiter=',', quotechar="\"")
            lines = list(reader)[1:]

            for idx, line in enumerate(lines):
                yield idx, {"idx": idx, "text": line[1], "label": line[0]}
