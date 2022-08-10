"""CommonsenseQA dataset."""


import json

import datasets


_HOMEPAGE = "https://www.tau-nlp.org/commonsenseqa"

_DESCRIPTION = """\
CommonsenseQA is a new multiple-choice question answering dataset that requires different types of commonsense knowledge
to predict the correct answers . It contains 12,102 questions with one correct answer and four distractor answers.
The dataset is provided in two major training/validation/testing set splits: "Random split" which is the main evaluation
split, and "Question token split", see paper for details.
"""

_CITATION = """\
@inproceedings{talmor-etal-2019-commonsenseqa,
    title = "{C}ommonsense{QA}: A Question Answering Challenge Targeting Commonsense Knowledge",
    author = "Talmor, Alon  and
      Herzig, Jonathan  and
      Lourie, Nicholas  and
      Berant, Jonathan",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/N19-1421",
    doi = "10.18653/v1/N19-1421",
    pages = "4149--4158",
    archivePrefix = "arXiv",
    eprint        = "1811.00937",
    primaryClass  = "cs",
}
"""

_URL = "https://s3.amazonaws.com/commensenseqa"
_URLS = {
    "train": f"{_URL}/train_rand_split.jsonl",
    "validation": f"{_URL}/dev_rand_split.jsonl",
    "test": f"{_URL}/test_rand_split_no_answers.jsonl",
}


class CommonsenseQa(datasets.GeneratorBasedBuilder):
    """CommonsenseQA dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "question": datasets.Value("string"),
                "question_concept": datasets.Value("string"),
                "choices": datasets.features.Sequence(
                    {
                        "label": datasets.Value("string"),
                        "text": datasets.Value("string"),
                    }
                ),
                "answerKey": datasets.Value("string"),
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
        filepaths = dl_manager.download_and_extract(_URLS)
        splits = [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "filepath": filepaths[split],
                },
            )
            for split in splits
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for uid, row in enumerate(f):
                data = json.loads(row)
                choices = data["question"]["choices"]
                labels = [label["label"] for label in choices]
                texts = [text["text"] for text in choices]
                yield uid, {
                    "id": data["id"],
                    "question": data["question"]["stem"],
                    "question_concept": data["question"]["question_concept"],
                    "choices": {"label": labels, "text": texts},
                    "answerKey": data.get("answerKey", ""),
                }
