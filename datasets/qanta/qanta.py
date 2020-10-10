"""qanta dataset."""

from __future__ import absolute_import, division, print_function

import json
from typing import List, Tuple

import datasets


_CITATION = """
@article{Rodriguez2019QuizbowlTC,
  title={Quizbowl: The Case for Incremental Question Answering},
  author={Pedro Rodriguez and Shi Feng and Mohit Iyyer and He He and Jordan L. Boyd-Graber},
  journal={ArXiv},
  year={2019},
  volume={abs/1904.04792}
}
"""

_DESCRIPTION = """
The Qanta dataset is a question answering dataset based on the academic trivia game Quizbowl.
"""


_QANTA_URL = "https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.mapped.2018.04.18.json"
_TRICK_URL = "https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/trick-tacl-datasets/qanta.tacl-trick.json"
_VERSION = datasets.Version("2018.04.18")
_FIRST = "first"
_FULL = "full"
_SENTENCES = "sentences"
_RUNS = "runs"
# Order matters, the first one is default
_MODES = [_FULL, _FIRST, _SENTENCES, _RUNS]
_DEFAULT_CHAR_SKIP = 25


class QantaConfig(datasets.BuilderConfig):
    """BuilderConfig for Qanta."""

    def __init__(self, mode: str, char_skip: int, **kwargs):
        super(QantaConfig, self).__init__(version=_VERSION, **kwargs)
        self.mode = mode
        self.char_skip = char_skip


def create_char_runs(text: str, char_skip: int) -> List[Tuple[str, int]]:
    """
    Returns runs of the question based on skipping char_skip characters at a time. Also returns the indices used
    q: name this first united states president.
    runs with char_skip=10:
    ['name this ',
        'name this first unit',
        'name this first united state p',
        'name this first united state president.']
    :param char_skip: Number of characters to skip each time
    """
    char_indices = list(range(char_skip, len(text) + char_skip, char_skip))
    return [(text[:idx], idx) for idx in char_indices]


def with_default(key, lookup, default):
    if key in lookup:
        value = lookup[key]
        if value is None:
            return default
        else:
            return value
    else:
        return default


def question_to_examples(question, mode: str, char_skip: int):
    features = {
        "qanta_id": question["qanta_id"],
        "proto_id": with_default("proto_id", question, ""),
        "qdb_id": with_default("qdb_id", question, -1),
        # We refer to the actual answer as page, but this
        # may be misleading externally, so rename here to
        # be clearer
        "page": question["page"],
        "answer": question["page"],
        "raw_answer": question["answer"],
        "dataset": with_default("dataset", question, ""),
        "full_question": question["text"],
        "first_sentence": question["first_sentence"],
        "tokenizations": question["tokenizations"],
        "fold": question["fold"],
        "gameplay": question["gameplay"],
        "category": with_default("category", question, ""),
        "subcategory": with_default("subcategory", question, ""),
        "tournament": question["tournament"],
        "difficulty": with_default("difficulty", question, ""),
        "year": question["year"],
        "char_idx": -1,
        "sentence_idx": -1,
    }
    if mode == _FULL:
        yield {
            "text": question["text"],
            "id": str(question["qanta_id"]) + "-full",
            **features,
        }
    elif mode == _FIRST:
        yield {
            "text": question["first_sentence"],
            "id": str(question["qanta_id"]) + "-first",
            **features,
        }
    elif mode == _RUNS:
        text = question["text"]
        for text_run, char_idx in create_char_runs(text, char_skip):
            yield {
                "text": text_run,
                "char_idx": char_idx,
                "id": str(question["qanta_id"]) + "-char-" + str(char_idx),
                **features,
            }
    elif mode == _SENTENCES:
        for sentence_idx, (start, end) in enumerate(question["tokenizations"]):
            sentence = question["text"][start:end]
            yield {
                "text": sentence,
                "sentence_idx": sentence_idx,
                "id": str(question["qanta_id"]) + "-sentence-" + str(sentence_idx),
                **features,
            }
    else:
        raise ValueError(f"Invalid mode: {mode}")


_FEATURES = {
    # Generated ID based modes set, unique
    "id": datasets.Value("string"),
    # Dataset defined IDs
    "qanta_id": datasets.Value("int32"),
    "proto_id": datasets.Value("string"),
    "qdb_id": datasets.Value("int32"),
    "dataset": datasets.Value("string"),
    # Inputs
    "text": datasets.Value("string"),
    "full_question": datasets.Value("string"),
    "first_sentence": datasets.Value("string"),
    "char_idx": datasets.Value("int32"),
    "sentence_idx": datasets.Value("int32"),
    # Character indices of sentences: List[Tuple[int, int]]
    "tokenizations": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("int32"), length=2)),
    # Labels: Number is equal to number of unique pages across all folds
    "answer": datasets.Value("string"),
    "page": datasets.Value("string"),
    "raw_answer": datasets.Value("string"),
    # Meta Information
    "fold": datasets.Value("string"),
    "gameplay": datasets.Value("bool"),
    "category": datasets.Value("string"),
    "subcategory": datasets.Value("string"),
    "tournament": datasets.Value("string"),
    "difficulty": datasets.Value("string"),
    "year": datasets.Value("int32"),
}


class Qanta(datasets.GeneratorBasedBuilder):
    """The Qanta dataset is a question answering dataset based on the academic trivia game Quizbowl."""

    VERSION = _VERSION
    BUILDER_CONFIGS = [
        QantaConfig(
            name=f"mode={mode},char_skip={_DEFAULT_CHAR_SKIP}",
            description=f"Question format: {mode}, char_skip: {_DEFAULT_CHAR_SKIP}",
            mode=mode,
            char_skip=_DEFAULT_CHAR_SKIP,
        )
        for mode in _MODES
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(_FEATURES),
            # Number of classes is a function of the dataset, ClassLabel doesn't support dynamic
            # definition, so have to defer conversion to classes to later, so can't define
            # supervied keys
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://www.qanta.org/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        qanta_path = dl_manager.download_and_extract(_QANTA_URL)
        trick_path = dl_manager.download_and_extract(_TRICK_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split("guesstrain"),
                gen_kwargs={
                    "qanta_filepath": qanta_path,
                    "trick_filepath": trick_path,
                    "fold": "guesstrain",
                    "mode": self.config.mode,
                    "char_skip": self.config.char_skip,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("buzztrain"),
                gen_kwargs={
                    "qanta_filepath": qanta_path,
                    "trick_filepath": trick_path,
                    "fold": "buzztrain",
                    "mode": self.config.mode,
                    "char_skip": self.config.char_skip,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("guessdev"),
                gen_kwargs={
                    "qanta_filepath": qanta_path,
                    "trick_filepath": trick_path,
                    "fold": "guessdev",
                    "mode": self.config.mode,
                    "char_skip": self.config.char_skip,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("buzzdev"),
                gen_kwargs={
                    "qanta_filepath": qanta_path,
                    "trick_filepath": trick_path,
                    "fold": "buzzdev",
                    "mode": self.config.mode,
                    "char_skip": self.config.char_skip,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("guesstest"),
                gen_kwargs={
                    "qanta_filepath": qanta_path,
                    "trick_filepath": trick_path,
                    "fold": "guesstest",
                    "mode": self.config.mode,
                    "char_skip": self.config.char_skip,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("buzztest"),
                gen_kwargs={
                    "qanta_filepath": qanta_path,
                    "trick_filepath": trick_path,
                    "fold": "buzztest",
                    "mode": self.config.mode,
                    "char_skip": self.config.char_skip,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("adversarial"),
                gen_kwargs={
                    "qanta_filepath": qanta_path,
                    "trick_filepath": trick_path,
                    "fold": "adversarial",
                    "mode": self.config.mode,
                    "char_skip": self.config.char_skip,
                },
            ),
        ]

    def _generate_examples(
        self,
        qanta_filepath: str,
        trick_filepath: str,
        fold: str,
        mode: str,
        char_skip: int,
    ):
        """Yields examples."""
        if mode not in _MODES:
            raise ValueError(f"Invalid mode: {mode}")

        if fold == "adversarial":
            path = trick_filepath
        else:
            path = qanta_filepath
        with open(path, encoding="utf-8") as f:
            questions = json.load(f)["questions"]
            for q in questions:
                if q["page"] is not None and q["fold"] == fold:
                    for example in question_to_examples(q, mode, char_skip):
                        yield example["id"], example
