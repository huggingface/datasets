# coding=utf-8

import nlp

class Csv(nlp.GeneratorBasedBuilder):
    VERSION = nlp.Version("1.0.0")

    def __init__(self, **config):
        print(config)
        self.n = "ytiuytut"
        super(Csv, self).__init__(**config)

    def _info(self):
        print(self.n)
        return nlp.DatasetInfo(
                builder=self,
                description="bla",
                features=nlp.features.FeaturesDict({
                        "id":
                                nlp.string,
                        "title":
                                nlp.string,
                        "context":
                                nlp.string,
                        "question":
                                nlp.string,
                }),
        )

    def _split_generators(self, dl_manager):
        return [
                nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        gen_kwargs={"filepath": "train"}),
                nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        gen_kwargs={"filepath": "dev"}),
        ]

    def _generate_examples(self, filepath):
        yield 1, {
            "title": "title",
            "context": "context",
            "question": "question",
            "id": "id_",
        }
