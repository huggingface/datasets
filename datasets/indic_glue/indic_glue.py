"""The IndicGLUE benchmark."""

from __future__ import absolute_import, division, print_function

import csv
import json
import math
import os
import textwrap

import pandas as pd
import six

import datasets


_INDIC_GLUE_CITATION = """\
    @inproceedings{kakwani2020indicnlpsuite,
    title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
    author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
    year={2020},
    booktitle={Findings of EMNLP},
}
"""

_INDIC_GLUE_DECSRIPTION = """\
    To thoroughly evaluate language models on Indian languages, 
    we need a robust NLU benchmark consisting of a wide variety of tasks and covering all the Indian languages. 
    IndicGLUE is a natural language understanding benchmark that we propose.
"""
_DESCRIPTIONS = {
    "wnli": textwrap.dedent(
        """
        The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task
        in which a system must read a sentence with a pronoun and select the referent of that pronoun from
        a list of choices. The examples are manually constructed to foil simple statistical methods: Each
        one is contingent on contextual information provided by a single word or phrase in the sentence.
        To convert the problem into sentence pair classification, we construct sentence pairs by replacing
        the ambiguous pronoun with each possible referent. The task is to predict if the sentence with the
        pronoun substituted is entailed by the original sentence. We use a small evaluation set consisting of
        new examples derived from fiction books that was shared privately by the authors of the original
        corpus. While the included training set is balanced between two classes, the test set is imbalanced
        between them (65% not entailment). Also, due to a data quirk, the development set is adversarial:
        hypotheses are sometimes shared between training and development examples, so if a model memorizes the
        training examples, they will predict the wrong label on corresponding development set
        example. As with QNLI, each example is evaluated separately, so there is not a systematic correspondence
        between a model's score on this task and its score on the unconverted original task. We
        call converted dataset WNLI (Winograd NLI). The dataset is available in 3 languages.
        """
    ),
    "copa": textwrap.dedent(
        """
        The Choice Of Plausible Alternatives (COPA) evaluation provides researchers with a tool for assessing 
        progress in open-domain commonsense causal reasoning. COPA consists of 1000 questions, split equally 
        into development and test sets of 500 questions each. Each question is composed of a premise and two 
        alternatives, where the task is to select the alternative that more plausibly has a causal relation 
        with the premise. The correct alternative is randomized so that the expected performance of randomly 
        guessing is 50%. The dataset is available is 3 languages.
        """
    ),
    "sna": textwrap.dedent(
        """
        This dataset is a collection of Bengali News articles. The dataset is used for classifying articles into
        5 different classes namely international, state, kolkata, entertainment and sports.
        """
    ),
    "csqa": textwrap.dedent(
        """
        Given a text with an entity randomly masked, the task is to predict that masked entity from a list of 4 
        candidate entities. The dataset contains around 239k examples across 11 languages.
        """
    ),
    "wstp": textwrap.dedent(
        """
        Predict the correct title for a Wikipedia section from a given list of four candidate titles. 
        The dataset has 400k examples across 11 Indian languages.
        """
    ),
    "inltkh": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "bbca": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "cvit-mkb-clsr": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "iitp-mr": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "iitp-pr": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "actsa-sc": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "md": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "wiki-ner": textwrap.dedent(
        """
        REPLACE
        """
    ),
}

_CITATIONS = {
    "wnli": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "copa": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "sna": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "csqa": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "wstp": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "inltkh": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "bbca": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "cvit-mkb-clsr": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "iitp-mr": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "iitp-pr": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "actsa-sc": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "md": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "wiki-ner": textwrap.dedent(
        """
        REPLACE
        """
    ),
}

_TEXT_FEATURES = {
    "wnli": {"sentence1": "sentence1", "sentence2": "sentence2"},
    "copa": {"premise": "premise", "choice1": "choice1", "choice2": "choice2", "question": "question"},
    "sna": {"text": "text", "label": "label"},
    "csqa": {"question": "question", "answer": "answer", "category": "category", "title": "title"},
    "wstp": {
        "sectionText": "sectionText",
        "correctTitle": "correctTitle",
        "titleA": "titleA",
        "titleB": "titleB",
        "titleC": "titleC",
        "titleD": "titleD",
        "url": "url",
    },
    "inltkh": {"label": "label", "text": "text"},
    "bbca": {"label": "label", "text": "text"},
    "cvit-mkb-clsr": {"sentence1": "sentence1", "sentence2": "sentence2"},
    "iitp-mr": {"label": "label", "text": "text"},
    "iitp-pr": {"label": "label", "text": "text"},
    "actsa-sc": {"text": "text"},
    "md": {"sentence": "sentence", "discourse_mode": "discourse_mode"},
    "wiki-ner": {},
}

_DATA_URLS = {
    "wnli": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wnli-translated.tar.gz",
    "copa": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/copa-translated.tar.gz",
    "sna": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/soham-articles.tar.gz",
    "csqa": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wiki-cloze.tar.gz",
    "wstp": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wiki-section-titles.tar.gz",
    "inltkh": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/inltk-headlines.tar.gz",
    "bbca": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/bbc-articles.tar.gz",
    "cvit-mkb-clsr": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/cvit-mkb.tar.gz",
    "iitp-mr": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/iitp-movie-reviews.tar.gz",
    "iitp-pr": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/iitp-product-reviews.tar.gz",
    "actsa-sc": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/actsa.tar.gz",
    "md": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/midas-discourse.tar.gz",
    "wiki-ner": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wikiann-ner.tar.gz",
}

_URLS = {
    "wnli": "https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference",
    "copa": "https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference",
    "sna": "https://indicnlp.ai4bharat.org/indic-glue/#news-category-classification",
    "csqa": "https://indicnlp.ai4bharat.org/indic-glue/#cloze-style-question-answering",
    "wstp": "https://indicnlp.ai4bharat.org/indic-glue/#wikipedia-section-title-prediction",
    "inltkh": "https://indicnlp.ai4bharat.org/indic-glue/#news-category-classification",
    "bbca": "https://indicnlp.ai4bharat.org/indic-glue/#news-category-classification",
    "cvit-mkb-clsr": "https://indicnlp.ai4bharat.org/indic-glue/#cross-lingual-sentence-retrieval",
    "iitp-mr": "https://indicnlp.ai4bharat.org/indic-glue/#sentiment-analysis",
    "iitp-pr": "https://indicnlp.ai4bharat.org/indic-glue/#sentiment-analysis",
    "actsa-sc": "https://indicnlp.ai4bharat.org/indic-glue/#sentiment-analysis",
    "md": "https://indicnlp.ai4bharat.org/indic-glue/#discourse-analysis",
    "wiki-ner": "https://indicnlp.ai4bharat.org/indic-glue/#named-entity-recognition",
}

_INDIC_GLUE_URL = "https://indicnlp.ai4bharat.org/indic-glue/"

_WNLI_LANGS = ["en", "hi", "gu", "mr"]
_COPA_LANGS = ["en", "hi", "gu", "mr"]
_SNA_LANGS = ["bn"]
_CSQA_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
_WSTP_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
_iNLTKH_LANGS = ["gu", "ml", "mr", "ta", "te"]
_BBCA_LANGS = ["hi"]
_CVIT_MKB_CLSR = ["en-bn", "en-gu", "en-hi", "en-ml", "en-mr", "en-or", "en-ta", "en-te", "en-ur"]
_IITP_MR_LANGS = ["hi"]
_IITP_PR_LANGS = ["hi"]
_ACTSA_LANGS = ["te"]
_MD_LANGS = ["hi"]
_WIKI_NER_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]

_NAMES = []

for lang in _WNLI_LANGS:
    _NAMES.append(f"wnli.{lang}")

for lang in _COPA_LANGS:
    _NAMES.append(f"copa.{lang}")

for lang in _SNA_LANGS:
    _NAMES.append(f"sna.{lang}")

for lang in _CSQA_LANGS:
    _NAMES.append(f"csqa.{lang}")

for lang in _WSTP_LANGS:
    _NAMES.append(f"wstp.{lang}")

for lang in _iNLTKH_LANGS:
    _NAMES.append(f"inltkh.{lang}")

for lang in _BBCA_LANGS:
    _NAMES.append(f"bbca.{lang}")

for lang in _CVIT_MKB_CLSR:
    _NAMES.append(f"cvit-mkb-clsr.{lang}")

for lang in _IITP_MR_LANGS:
    _NAMES.append(f"iitp-mr.{lang}")

for lang in _IITP_PR_LANGS:
    _NAMES.append(f"iitp-pr.{lang}")

for lang in _ACTSA_LANGS:
    _NAMES.append(f"actsa-sc.{lang}")

for lang in _MD_LANGS:
    _NAMES.append(f"md.{lang}")

for lang in _WIKI_NER_LANGS:
    _NAMES.append(f"wiki-ner.{lang}")


class IndicGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for IndicGLUE."""

    def __init__(self, data_url, citation, url, text_features, **kwargs):
        """
        Args:

          data_url: `string`, url to download the zip file from.
          citation: `string`, citation for the data set.
          url: `string`, url for information about the data set.
          text_features: `dict[string, string]`, map from the name of the feature
        dict for each text field to the name of the column in the csv/json file
          **kwargs: keyword arguments forwarded to super.
        """
        super(IndicGlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.data_url = data_url
        self.citation = citation
        self.url = url
        self.text_features = text_features


class IndicGlue(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        IndicGlueConfig(
            name=name,
            description=_DESCRIPTIONS[name.split(".")[0]],
            text_features=_TEXT_FEATURES[name.split(".")[0]],
            data_url=_DATA_URLS[name.split(".")[0]],
            citation=_CITATIONS[name.split(".")[0]],
            url=_URLS[name.split(".")[0]],
        )
        for name in _NAMES
    ]

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in six.iterkeys(self.config.text_features)}

        if (
            self.config.name.startswith("wnli")
            or self.config.name.startswith("copa")
            or self.config.name.startswith("actsa")
        ):
            features["label"] = datasets.Value("int32")

        if self.config.name.startswith("csqa"):
            features["options"] = datasets.features.Sequence(datasets.Value("string"))
            features["out_of_context_options"] = datasets.features.Sequence(datasets.Value("string"))

        if self.config.name.startswith("md"):
            features["story_number"] = datasets.Value("int32")
            features["id"] = datasets.Value("int32")

        if self.config.name.startswith("wiki-ner"):
            features["tokens"] = datasets.features.Sequence(datasets.Value("string"))
            features["labels"] = datasets.features.Sequence(datasets.Value("string"))
            features["additional_info"] = datasets.features.Sequence(
                datasets.features.Sequence(datasets.Value("string"))
            )

        return datasets.DatasetInfo(
            description=_INDIC_GLUE_DECSRIPTION + "\n" + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=_INDIC_GLUE_CITATION + "\n" + self.config.citation,
        )

    def _split_generators(self, dl_manager):

        if self.config.name.startswith("wnli"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "dev.csv"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                # datasets.SplitGenerator(
                #     name=datasets.Split.TEST,
                #     gen_kwargs={
                #         "datafile": os.path.join(dl_dir, "test.csv"),
                #         "split": datasets.Split.TEST,
                #     },
                # )
            ]

        if self.config.name.startswith("copa"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "train.jsonl"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "val.jsonl"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                # datasets.SplitGenerator(
                #     name=datasets.Split.TEST,
                #     gen_kwargs={
                #         "datafile": os.path.join(dl_dir, "test.csv"),
                #         "split": datasets.Split.TEST,
                #     },
                # )
            ]

        if self.config.name.startswith("sna"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "bn-train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "bn-valid.csv"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "bn-test.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("csqa"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name)

            return [
                # datasets.SplitGenerator(
                #     name=datasets.Split.TRAIN,
                #     gen_kwargs={
                #         "datafile": os.path.join(dl_dir, "bn-train.csv"),
                #         "split": datasets.Split.TRAIN,
                #     },
                # ),
                # datasets.SplitGenerator(
                #     name=datasets.Split.VALIDATION,
                #     gen_kwargs={
                #         "datafile": os.path.join(dl_dir, "bn-valid.csv"),
                #         "split": datasets.Split.VALIDATION,
                #     },
                # ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}.json"),
                        "split": datasets.Split.TEST,
                    },
                )
            ]

        if self.config.name.startswith("wstp"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            if self.config.name.split(".")[1] == "te":
                return [
                    datasets.SplitGenerator(
                        name=datasets.Split.TRAIN,
                        gen_kwargs={
                            "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.json"),
                            "split": datasets.Split.TRAIN,
                        },
                    ),
                    datasets.SplitGenerator(
                        name=datasets.Split.VALIDATION,
                        gen_kwargs={
                            "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-valid.json"),
                            "split": datasets.Split.VALIDATION,
                        },
                    ),
                    datasets.SplitGenerator(
                        name=datasets.Split.TEST,
                        gen_kwargs={
                            "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.json"),
                            "split": datasets.Split.TEST,
                        },
                    ),
                ]

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-valid.csv"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if (
            self.config.name.startswith("inltkh")
            or self.config.name.startswith("iitp")
            or self.config.name.startswith("actsa")
        ):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-valid.csv"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("bbca"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.csv"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.csv"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("cvit"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": None,
                        "src": os.path.join(dl_dir, f"mkb.{self.config.name.split('.')[1].split('-')[0]}"),
                        "tgt": os.path.join(dl_dir, f"mkb.{self.config.name.split('.')[1].split('-')[1]}"),
                        "split": datasets.Split.TEST,
                    },
                )
            ]

        if self.config.name.startswith("md"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "train.json"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "val.json"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, "test.json"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

        if self.config.name.startswith("wiki-ner"):
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            task_name = self._get_task_name_from_data_url(self.config.data_url)
            dl_dir = os.path.join(dl_dir, task_name + "/" + self.config.name.split(".")[1])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-train.txt"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-valid.txt"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "datafile": os.path.join(dl_dir, f"{self.config.name.split('.')[1]}-test.txt"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

    def _generate_examples(self, **args):
        """Yields examples."""
        filepath = args["datafile"]

        if self.config.name.startswith("wnli"):
            with open(filepath, encoding="utf-8") as f:
                data = csv.DictReader(f)
                for id_, row in enumerate(data):
                    yield id_, {"sentence1": row["sentence1"], "sentence2": row["sentence2"], "label": row["label"]}

        if self.config.name.startswith("copa"):
            with open(filepath, "r") as f:
                lines = f.readlines()
                data = map(lambda l: json.loads(l), lines)
                data = list(data)
                for id_, row in enumerate(data):
                    yield id_, {
                        "premise": row["premise"],
                        "choice1": row["choice1"],
                        "choice2": row["choice2"],
                        "question": row["question"],
                        "label": row["label"],
                    }

        if self.config.name.startswith("sna"):
            df = pd.read_csv(filepath, names=["label", "text"])
            for id_, row in df.iterrows():
                yield id_, {"text": row["text"], "label": row["label"]}

        if self.config.name.startswith("csqa"):
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                df = pd.DataFrame(data["cloze_data"])
                df["out_of_context_options"].loc[df["out_of_context_options"].isnull()] = (
                    df["out_of_context_options"].loc[df["out_of_context_options"].isnull()].apply(lambda x: [])
                )
                for id_, row in df.iterrows():
                    yield id_, {
                        "question": row["question"],
                        "answer": row["answer"],
                        "category": row["category"],
                        "title": row["title"],
                        "out_of_context_options": row["out_of_context_options"],
                        "options": row["options"],
                    }

        if self.config.name.startswith("wstp"):
            df = pd.read_json(filepath)
            for id_, row in df.iterrows():
                yield id_, {
                    "sectionText": row["sectionText"],
                    "correctTitle": row["correctTitle"],
                    "titleA": row["titleA"],
                    "titleB": row["titleB"],
                    "titleC": row["titleC"],
                    "titleD": row["titleD"],
                    "url": row["url"],
                }

        if (
            self.config.name.startswith("inltkh")
            or self.config.name.startswith("bbca")
            or self.config.name.startswith("iitp")
            or self.config.name.startswith("actsa")
        ):
            df = pd.read_csv(filepath, names=["label", "text"])
            for id_, row in df.iterrows():
                yield id_, {"text": row["text"], "label": row["label"]}

        if self.config.name.startswith("cvit"):
            source = args["src"]
            target = args["tgt"]

            src, tgt = open(source, "r"), open(target, "r")
            src, tgt = src.readlines(), tgt.readlines()

            for id_, row in enumerate(zip(src, tgt)):
                yield id_, {"sentence1": row[0], "sentence2": row[1]}

        if self.config.name.startswith("md"):
            df = pd.read_json(filepath)
            for id_, row in df.iterrows():
                yield id_, {
                    "story_number": row["Story_no"],
                    "sentence": row["Sentence"],
                    "discourse_mode": row["Discourse Mode"],
                    "id": row["id"],
                }

        if self.config.name.startswith("wiki-ner"):
            with open(filepath, "r") as f:
                data = f.readlines()
                for id_, row in enumerate(data):
                    tokens = []
                    labels = []
                    infos = []

                    row = row.split()

                    if len(row) == 0:
                        yield id_, {"tokens": tokens, "labels": labels, "additional_info": infos}
                        continue

                    tokens.append(row[0])
                    labels.append(row[-1])
                    infos.append(row[1:-1])

    def _get_task_name_from_data_url(self, data_url):
        return data_url.split("/")[-1].split(".")[0]
