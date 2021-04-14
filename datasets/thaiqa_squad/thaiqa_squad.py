"""TODO(squad_v2): Add a description here."""


import json
import os

import datasets


_CITATION = """\
No clear citation guidelines from source:
https://aiforthai.in.th/corpus.php
SQuAD version:
https://github.com/PyThaiNLP/thaiqa_squad
"""

_DESCRIPTION = """\
`thaiqa_squad` is an open-domain, extractive question answering dataset (4,000 questions in `train` and 74 questions in `dev`) in
[SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) format, originally created by [NECTEC](https://www.nectec.or.th/en/) from
Wikipedia articles and adapted to [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) format by [PyThaiNLP](https://github.com/PyThaiNLP/).
"""


class ThaiQaSquadConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        """BuilderConfig

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ThaiQaSquadConfig, self).__init__(**kwargs)


class ThaiqaSquad(datasets.GeneratorBasedBuilder):
    _DOWNLOAD_URL = "https://github.com/PyThaiNLP/thaiqa_squad/raw/main/data.zip"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "dev.jsonl"

    BUILDER_CONFIGS = [
        ThaiQaSquadConfig(
            name="thaiqa_squad",
            version=datasets.Version("1.0.0"),
            description="`thaiqa_squad` is an open-domain, extractive question answering dataset (4,000 questions in `train` and 74 questions in `dev`) in [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) format",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "question_id": datasets.Value("int32"),
                    "article_id": datasets.Value("int32"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "answer": datasets.Value("string"),
                            "answer_begin_position": datasets.Value("int32"),
                            "answer_end_position": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/PyThaiNLP/thaiqa_squad",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "data")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TRAIN_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(data_dir, self._VAL_FILE)},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if not isinstance(data["answer"], list):
                    answer = [data["answer"]]
                    answer_begin_position = [data["answer_begin_position"]]
                    answer_end_position = [data["answer_end_position"]]
                yield id_, {
                    "question_id": data["question_id"],
                    "article_id": data["article_id"],
                    "context": data["context"],
                    "question": data["question"],
                    "answers": {
                        "answer": answer,
                        "answer_begin_position": answer_begin_position,
                        "answer_end_position": answer_end_position,
                    },
                }
