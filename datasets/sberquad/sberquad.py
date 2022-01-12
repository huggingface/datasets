# coding=utf-8
"""SberQUAD: Sber Question Answering Dataset."""

import json

import datasets
from datasets.tasks import QuestionAnsweringExtractive


logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@article{Efimov_2020,
   title={SberQuAD – Russian Reading Comprehension Dataset: Description and Analysis},
   ISBN={9783030582197},
   ISSN={1611-3349},
   url={http://dx.doi.org/10.1007/978-3-030-58219-7_1},
   DOI={10.1007/978-3-030-58219-7_1},
   journal={Experimental IR Meets Multilinguality, Multimodality, and Interaction},
   publisher={Springer International Publishing},
   author={Efimov, Pavel and Chertok, Andrey and Boytsov, Leonid and Braslavski, Pavel},
   year={2020},
   pages={3–15}
}
 """


_DESCRIPTION = """\
Sber Question Answering Dataset (SberQuAD) is a reading comprehension \
dataset, consisting of questions posed by crowdworkers on a set of Wikipedia \
articles, where the answer to every question is a segment of text, or span, \
from the corresponding reading passage, or the question might be unanswerable. \
Russian original analogue presented in Sberbank Data Science Journey 2017.
"""

_URLS = {"train": "https://sc.link/PNWl", "dev": "https://sc.link/W6oX", "test": "https://sc.link/VOn9"}


class Sberquad(datasets.GeneratorBasedBuilder):
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
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        key = 0
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
