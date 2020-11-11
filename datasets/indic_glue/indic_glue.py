"""The IndicGLUE bencjmark."""

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
        REPLACE
        """
    ),
    "ncc": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "clsr": textwrap.dedent(
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
    "ncc": textwrap.dedent(
        """
        REPLACE
        """
    ),
    "clsr": textwrap.dedent(
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
    "ncc": {},
    "clsr": {},
}

_DATA_URLS = {
    "wnli": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wnli-translated.tar.gz",
    "copa": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/copa-translated.tar.gz",
    "sna": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/soham-articles.tar.gz",
    "csqa": "https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/evaluations/wiki-cloze.tar.gz",
    "ncc": "",
    "clsr": "",
}

_URLS = {
    "wnli": "https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference",
    "copa": "https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference",
    "sna": "https://indicnlp.ai4bharat.org/indic-glue/#news-category-classification",
    "csqa": "https://indicnlp.ai4bharat.org/indic-glue/#cloze-style-question-answering",
    "ncc": "",
    "clsr": "",
}

_INDIC_GLUE_URL = "https://indicnlp.ai4bharat.org/indic-glue/"

_WNLI_LANGS = ["en", "hi", "gu", "mr"]
_COPA_LANGS = ["en", "hi", "gu", "mr"]
_SNA_LANGS = ["bn"]
_CSQA_LANGS = ["as", "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "ta", "te"]
_CSMCQ_LANGS = []
_NCC_LANGS = []
_CLSR_LANGS = []

_NAMES = []

for lang in _WNLI_LANGS:
    _NAMES.append(f"wnli.{lang}")

for lang in _COPA_LANGS:
    _NAMES.append(f"copa.{lang}")

for lang in _SNA_LANGS:
    _NAMES.append(f"sna.{lang}")

for lang in _CSQA_LANGS:
    _NAMES.append(f"csqa.{lang}")

# for lang in _NCC_LANGS:
#     _NAMES.append(f'ncc.{lang}')

# for lang in _CLSR_LANGS:
#     _NAMES.append(f'clsr.{lang}')


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

        if self.config.name.startswith("wnli") or self.config.name.startswith("copa"):
            features["label"] = datasets.Value("int32")

        if self.config.name.startswith("csqa"):
            features["options"] = datasets.features.Sequence(datasets.Value("string"))
            features["out_of_context_options"] = datasets.features.Sequence(datasets.Value("string"))

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

    def _get_task_name_from_data_url(self, data_url):
        return data_url.split("/")[-1].split(".")[0]
