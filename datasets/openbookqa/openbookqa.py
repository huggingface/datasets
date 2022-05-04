"""OpenBookQA dataset."""


import json
import os
import textwrap

import datasets


_HOMEPAGE = "https://allenai.org/data/open-book-qa"

_DESCRIPTION = """\
OpenBookQA aims to promote research in advanced question-answering, probing a deeper understanding of both the topic
(with salient facts summarized as an open book, also provided with the dataset) and the language it is expressed in. In
particular, it contains questions that require multi-step reasoning, use of additional common and commonsense knowledge,
and rich text comprehension.
OpenBookQA is a new kind of question-answering dataset modeled after open book exams for assessing human understanding
of a subject.
"""

_CITATION = """\
@inproceedings{OpenBookQA2018,
 title={Can a Suit of Armor Conduct Electricity? A New Dataset for Open Book Question Answering},
 author={Todor Mihaylov and Peter Clark and Tushar Khot and Ashish Sabharwal},
 booktitle={EMNLP},
 year={2018}
}
"""

_URL = "https://s3-us-west-2.amazonaws.com/ai2-website/data/OpenBookQA-V1-Sep2018.zip"


class OpenbookqaConfig(datasets.BuilderConfig):
    def __init__(self, data_dir=None, filenames=None, version=datasets.Version("1.0.1", ""), **kwargs):
        """BuilderConfig for openBookQA dataset

        Args:
          data_dir: directory for the given dataset name
          **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(version=version, **kwargs)
        self.data_dir = data_dir
        self.filenames = filenames


class Openbookqa(datasets.GeneratorBasedBuilder):
    """OpenBookQA dataset."""

    BUILDER_CONFIGS = [
        OpenbookqaConfig(
            name="main",
            description=textwrap.dedent(
                """\
                It consists of 5,957 multiple-choice elementary-level science questions (4,957 train, 500 dev, 500 test),
                which probe the understanding of a small “book” of 1,326 core science facts and the application of these facts to novel
                situations. For training, the dataset includes a mapping from each question to the core science fact it was designed to
                probe. Answering OpenBookQA questions requires additional broad common knowledge, not contained in the book. The questions,
                by design, are answered incorrectly by both a retrieval-based algorithm and a word co-occurrence algorithm. Strong neural
                baselines achieve around 50% on OpenBookQA, leaving a large gap to the 92% accuracy of crowd-workers.
                """
            ),
            data_dir="Main",
            filenames={
                "train": "train.jsonl",
                "validation": "dev.jsonl",
                "test": "test.jsonl",
            },
        ),
        OpenbookqaConfig(
            name="additional",
            description=textwrap.dedent(
                """\
                Additionally, we provide 5,167 crowd-sourced common knowledge facts, and an expanded version of the train/dev/test questions where
                each question is associated with its originating core fact, a human accuracy score, a clarity score, and an anonymized crowd-worker
                ID (in the 'Additional' folder).
                """
            ),
            data_dir="Additional",
            filenames={
                "train": "train_complete.jsonl",
                "validation": "dev_complete.jsonl",
                "test": "test_complete.jsonl",
            },
        ),
    ]
    DEFAULT_CONFIG_NAME = "main"

    def _info(self):
        if self.config.name == "main":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "question_stem": datasets.Value("string"),
                    "choices": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "label": datasets.Value("string"),
                        }
                    ),
                    "answerKey": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "question_stem": datasets.Value("string"),
                    "choices": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "label": datasets.Value("string"),
                        }
                    ),
                    "answerKey": datasets.Value("string"),
                    "fact1": datasets.Value("string"),
                    "humanScore": datasets.Value("float"),
                    "clarity": datasets.Value("float"),
                    "turkIdAnonymized": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "OpenBookQA-V1-Sep2018", "Data", self.config.data_dir)
        splits = [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={"filepath": os.path.join(data_dir, self.config.filenames[split])},
            )
            for split in splits
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for uid, row in enumerate(f):
                data = json.loads(row)
                example = {
                    "id": data["id"],
                    "question_stem": data["question"]["stem"],
                    "choices": {
                        "text": [choice["text"] for choice in data["question"]["choices"]],
                        "label": [choice["label"] for choice in data["question"]["choices"]],
                    },
                    "answerKey": data["answerKey"],
                }
                if self.config.name == "additional":
                    for key in ["fact1", "humanScore", "clarity", "turkIdAnonymized"]:
                        example[key] = data[key]
                yield uid, example
