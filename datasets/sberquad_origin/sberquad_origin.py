# coding=utf-8
"""SberQUAD: Sber Question Answering Dataset."""

import json

import datasets
from datasets.tasks import QuestionAnsweringExtractive


logger = datasets.logging.get_logger(__name__)

_CITATION = """ https://arxiv.org/pdf/1912.09723.pdf """


_DESCRIPTION = """\
Sber Question Answering Dataset (SberQuAD) Origin is a reading comprehension \
dataset, consisting of questions posed by crowdworkers on a set of Wikipedia \
articles, where the answer to every question is a segment of text, or span, \
from the corresponding reading passage, or the question might be unanswerable.
Russian original analogue presented in Sberbank Data Science Journey 2017 https://github.com/sberbank-ai/data-science-journey-2017
"""

_URLS = {"train": "https://sc.link/PNWl", "dev": "https://sc.link/W6oX", "test": "https://sc.link/VOn9"}


class SberQuadConfig(datasets.BuilderConfig):
    """BuilderConfig for SQUAD."""

    def __init__(self, **kwargs):
        """BuilderConfig for SQUAD.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SberQuadConfig, self).__init__(**kwargs)
        print("INITIAL CONFIG: ", self.config)


class SberQuad(datasets.GeneratorBasedBuilder):
    """SberQUAD: Sber Question Answering Dataset. Version 1.0."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [datasets.BuilderConfig(name="sberquad", version=VERSION, description=_DESCRIPTION)]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage="",
            citation=_CITATION,
            task_templates=[
                QuestionAnsweringExtractive(
                    question_column="question", context_column="context", answers_column="answers"
                )
            ],
        )

    def _split_generators(self, dl_manager):
        downloaded_files = dl_manager.download_and_extract(_URLS)
        print("DONWLOADED: ", downloaded_files.keys())
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        key = 0
        print("GENERATION OF EXAMPLES from: ", filepath)
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
            for article in squad["data"]:
                title = article.get("title", "")
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"]
                    for qa in paragraph["qas"]:
                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"] for answer in qa["answers"]]
                        yield key, {
                            "title": title,
                            "context": context,
                            "question": qa["question"],
                            "id": qa["id"],
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
                        key += 1
