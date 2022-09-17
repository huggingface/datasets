"""CoQA dataset."""


import json

import datasets


_HOMEPAGE = "https://stanfordnlp.github.io/coqa/"

_CITATION = """\
@article{reddy-etal-2019-coqa,
    title = "{C}o{QA}: A Conversational Question Answering Challenge",
    author = "Reddy, Siva  and
      Chen, Danqi  and
      Manning, Christopher D.",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "7",
    year = "2019",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/Q19-1016",
    doi = "10.1162/tacl_a_00266",
    pages = "249--266",
}
"""

_DESCRIPTION = """\
CoQA: A Conversational Question Answering Challenge
"""

_TRAIN_DATA_URL = "https://nlp.stanford.edu/data/coqa/coqa-train-v1.0.json"
_DEV_DATA_URL = "https://nlp.stanford.edu/data/coqa/coqa-dev-v1.0.json"


class Coqa(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "source": datasets.Value("string"),
                    "story": datasets.Value("string"),
                    "questions": datasets.features.Sequence(datasets.Value("string")),
                    "answers": datasets.features.Sequence(
                        {
                            "input_text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                            "answer_end": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {"train": _TRAIN_DATA_URL, "dev": _DEV_DATA_URL}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"], "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"], "split": "validation"}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for row in data["data"]:
                questions = [question["input_text"] for question in row["questions"]]
                story = row["story"]
                source = row["source"]
                answers_start = [answer["span_start"] for answer in row["answers"]]
                answers_end = [answer["span_end"] for answer in row["answers"]]
                answers = [answer["input_text"] for answer in row["answers"]]
                yield row["id"], {
                    "source": source,
                    "story": story,
                    "questions": questions,
                    "answers": {"input_text": answers, "answer_start": answers_start, "answer_end": answers_end},
                }
