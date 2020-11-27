"""ARCD: Arabic Reading Comprehension Dataset."""

from __future__ import absolute_import, division, print_function

import json
import logging

import datasets


_CITATION = """\
@inproceedings{mozannar-etal-2019-neural,
    title = {Neural {A}rabic Question Answering},
    author = {Mozannar, Hussein  and Maamary, Elie  and El Hajal, Karl  and Hajj, Hazem},
    booktitle = {Proceedings of the Fourth Arabic Natural Language Processing Workshop},
    month = {aug},
    year = {2019},
    address = {Florence, Italy},
    publisher = {Association for Computational Linguistics},
    url = {https://www.aclweb.org/anthology/W19-4612},
    doi = {10.18653/v1/W19-4612},
    pages = {108--118},
    abstract = {This paper tackles the problem of open domain factual Arabic question answering (QA) using Wikipedia as our knowledge source. This constrains the answer of any question to be a span of text in Wikipedia. Open domain QA for Arabic entails three challenges: annotated QA datasets in Arabic, large scale efficient information retrieval and machine reading comprehension. To deal with the lack of Arabic QA datasets we present the Arabic Reading Comprehension Dataset (ARCD) composed of 1,395 questions posed by crowdworkers on Wikipedia articles, and a machine translation of the Stanford Question Answering Dataset (Arabic-SQuAD). Our system for open domain question answering in Arabic (SOQAL) is based on two components: (1) a document retriever using a hierarchical TF-IDF approach and (2) a neural reading comprehension model using the pre-trained bi-directional transformer BERT. Our experiments on ARCD indicate the effectiveness of our approach with our BERT-based reader achieving a 61.3 F1 score, and our open domain system SOQAL achieving a 27.6 F1 score.}
}
"""

_DESCRIPTION = """\
 Arabic Reading Comprehension Dataset (ARCD) composed of 1,395 questions\
      posed by crowdworkers on Wikipedia articles.
"""

_URL = "https://raw.githubusercontent.com/husseinmozannar/SOQAL/master/data/"
_URLs = {
    "train": _URL + "arcd-train.json",
    "dev": _URL + "arcd-test.json",
}


class ArcdConfig(datasets.BuilderConfig):
    """BuilderConfig for ARCD."""

    def __init__(self, **kwargs):
        """BuilderConfig for ARCD.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ArcdConfig, self).__init__(**kwargs)


class Arcd(datasets.GeneratorBasedBuilder):
    """ARCD: Arabic Reading Comprehension Dataset."""

    BUILDER_CONFIGS = [
        ArcdConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {"text": datasets.Value("string"), "answer_start": datasets.Value("int32")}
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://github.com/husseinmozannar/SOQAL/tree/master/data",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls_to_download = _URLs
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            arcd = json.load(f)
            for article in arcd["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"answer_start": answer_starts, "text": answers},
                        }
