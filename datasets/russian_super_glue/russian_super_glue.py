# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""The Russian SuperGLUE Benchmark"""

import json
import os
from typing import List, Union

import datasets


_RUSSIAN_SUPER_GLUE_CITATION = """\
@article{shavrina2020russiansuperglue,
                  title={RussianSuperGLUE: A Russian Language Understanding Evaluation Benchmark},
                  author={Shavrina, Tatiana and Fenogenova, Alena and Emelyanov, Anton and Shevelev, Denis and Artemova,
                  Ekaterina and Malykh, Valentin and Mikhailov, Vladislav and Tikhonova, Maria and Chertok, Andrey and
                  Evlampiev, Andrey},
                  journal={arXiv preprint arXiv:2010.15925},
                  year={2020}
                  }
"""

_MUSERC_CITATION = """\
@inproceedings{fenogenova-etal-2020-read,
    title = "Read and Reason with {M}u{S}e{RC} and {R}u{C}o{S}: Datasets for Machine Reading Comprehension for {R}ussian",
    author = "Fenogenova, Alena  and
      Mikhailov, Vladislav  and
      Shevelev, Denis",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://aclanthology.org/2020.coling-main.570",
    doi = "10.18653/v1/2020.coling-main.570",
    pages = "6481--6497",
    abstract = "The paper introduces two Russian machine reading comprehension (MRC) datasets, called MuSeRC and RuCoS,
    which require reasoning over multiple sentences and commonsense knowledge to infer the answer. The former follows
    the design of MultiRC, while the latter is a counterpart of the ReCoRD dataset. The datasets are included
    in RussianSuperGLUE, the Russian general language understanding benchmark. We provide a comparative analysis
    and demonstrate that the proposed tasks are relatively more complex as compared to the original ones for English.
    Besides, performance results of human solvers and BERT-based models show that MuSeRC and RuCoS represent a challenge
    for recent advanced neural models. We thus hope to facilitate research in the field of MRC for Russian and prompt
    the study of multi-hop reasoning in a cross-lingual scenario.",
}
"""

_RUSSE_CITATION = """\
@inproceedings{RUSSE2018,
  author    = {Panchenko, Alexander and Lopukhina, Anastasia and Ustalov, Dmitry and Lopukhin, Konstantin and Arefyev,
               Nikolay and Leontyev, Alexey and Loukachevitch, Natalia},
  title     = {{RUSSE'2018: A Shared Task on Word Sense Induction for the Russian Language}},
  booktitle = {Computational Linguistics and Intellectual Technologies:
               Papers from the Annual International Conference ``Dialogue''},
  year      = {2018},
  pages     = {547--564},
  url       = {http://www.dialog-21.ru/media/4539/panchenkoaplusetal.pdf},
  address   = {Moscow, Russia},
  publisher = {RSUH},
  issn      = {2221-7932},
  language  = {english},
}
"""

_DANETQA_CITATION = """\
@InProceedings{10.1007/978-3-030-72610-2_4,
author="Glushkova, Taisia
and Machnev, Alexey
and Fenogenova, Alena
and Shavrina, Tatiana
and Artemova, Ekaterina
and Ignatov, Dmitry I.",
editor="van der Aalst, Wil M. P.
and Batagelj, Vladimir
and Ignatov, Dmitry I.
and Khachay, Michael
and Koltsova, Olessia
and Kutuzov, Andrey
and Kuznetsov, Sergei O.
and Lomazova, Irina A.
and Loukachevitch, Natalia
and Napoli, Amedeo
and Panchenko, Alexander
and Pardalos, Panos M.
and Pelillo, Marcello
and Savchenko, Andrey V.
and Tutubalina, Elena",
title="DaNetQA: A Yes/No Question Answering Dataset for the Russian Language",
booktitle="Analysis of Images, Social Networks and Texts",
year="2021",
publisher="Springer International Publishing",
address="Cham",
pages="57--68",
abstract="DaNetQA, a new question-answering corpus, follows BoolQ [2] design: it comprises natural yes/no questions.
Each question is paired with a paragraph from Wikipedia and an answer, derived from the paragraph. The task is to take
both the question and a paragraph as input and come up with a yes/no answer, i.e. to produce a binary output. In this
paper, we present a reproducible approach to DaNetQA creation and investigate transfer learning methods for task and
language transferring. For task transferring we leverage three similar sentence modelling tasks: 1) a corpus of
paraphrases, Paraphraser, 2) an NLI task, for which we use the Russian part of XNLI, 3) another question answering task,
SberQUAD. For language transferring we use English to Russian translation together
with multilingual language fine-tuning.",
isbn="978-3-030-72610-2"
}
"""

_RUCOS_CITATION = _MUSERC_CITATION

_RUSSIAN_SUPER_GLUE_DESCRIPTION = """\
Recent advances in the field of universal language models and transformers require the development of a methodology for
their broad diagnostics and testing for general intellectual skills - detection of natural language inference,
commonsense reasoning, ability to perform simple logical operations regardless of text subject or lexicon. For the first
time, a benchmark of nine tasks, collected and organized analogically to the SuperGLUE methodology, was developed from
scratch for the Russian language. We provide baselines, human level evaluation, an open-source framework for evaluating
models and an overall leaderboard of transformer models for the Russian language.
"""

_HOMEPAGE = "https://russiansuperglue.com/"

_LICENSE = "MIT License"

_LIDIRUS_DESCRIPTION = """"\
LiDiRus (Linguistic Diagnostic for Russian) is a diagnostic dataset that covers a large volume of linguistic phenomena,
while allowing you to evaluate information systems on a simple test of textual entailment recognition.
See more details diagnostics.
"""

_RCB_DESCRIPTION = """\
The Russian Commitment Bank is a corpus of naturally occurring discourses whose final sentence contains
a clause-embedding predicate under an entailment canceling operator (question, modal, negation, antecedent
of conditional).
"""

_PARUS_DESCRIPTION = """\
Choice of Plausible Alternatives for Russian language
Choice of Plausible Alternatives for Russian language (PARus) evaluation provides researchers with a tool for assessing
progress in open-domain commonsense causal reasoning. Each question in PARus is composed of a premise and two
alternatives, where the task is to select the alternative that more plausibly has a causal relation with the premise.
The correct alternative is randomized so that the expected performance of randomly guessing is 50%.
"""

_MUSERC_DESCRIPTION = """\
We present a reading comprehension challenge in which questions can only be answered by taking into account information
from multiple sentences. The dataset is the first to study multi-sentence inference at scale, with an open-ended set of
question types that requires reasoning skills.
"""

_TERRA_DESCRIPTION = """\
Textual Entailment Recognition has been proposed recently as a generic task that captures major semantic inference
needs across many NLP applications, such as Question Answering, Information Retrieval, Information Extraction,
and Text Summarization. This task requires to recognize, given two text fragments, whether the meaning of one text is
entailed (can be inferred) from the other text.
"""

_RUSSE_DESCRIPTION = """\
WiC: The Word-in-Context Dataset A reliable benchmark for the evaluation of context-sensitive word embeddings.
Depending on its context, an ambiguous word can refer to multiple, potentially unrelated, meanings. Mainstream static
word embeddings, such as Word2vec and GloVe, are unable to reflect this dynamic semantic nature. Contextualised word
embeddings are an attempt at addressing this limitation by computing dynamic representations for words which can adapt
based on context.
Russian SuperGLUE task borrows original data from the Russe project, Word Sense Induction and Disambiguation
shared task (2018)
"""

_RWSD_DESCRIPTION = """\
A Winograd schema is a pair of sentences that differ in only one or two words and that contain an ambiguity that is
resolved in opposite ways in the two sentences and requires the use of world knowledge and reasoning for its resolution.
The schema takes its name from a well-known example by Terry Winograd.
The set would then be presented as a challenge for AI programs, along the lines of the Turing test. The strengths of
the challenge are that it is clear-cut, in that the answer to each schema is a binary choice; vivid, in that it is
obvious to non-experts that a program that fails to get the right answers clearly has serious gaps in its understanding;
and difficult, in that it is far beyond the current state of the art.
"""

_DANETQA_DESCRIPTION = """\
DaNetQA is a question answering dataset for yes/no questions. These questions are naturally occurring -- they are
generated in unprompted and unconstrained settings.

Each example is a triplet of (question, passage, answer), with the title of the page as optional additional context.
The text-pair classification setup is similar to existing natural language inference tasks.

By sampling questions from a distribution of information-seeking queries (rather than prompting annotators for
text pairs), we observe significantly more challenging examples compared to existing NLI datasets.
"""

_RUCOS_DESCRIPTION = """\
Russian reading comprehension with Commonsense reasoning (RuCoS) is a large-scale reading comprehension dataset which
requires commonsense reasoning. RuCoS consists of queries automatically generated from CNN/Daily Mail news articles;
the answer to each query is a text span from a summarizing passage of the corresponding news. The goal of RuCoS is to
evaluate a machine`s ability of commonsense reasoning in reading comprehension.
"""


class RussianSuperGlueConfig(datasets.BuilderConfig):
    """BuilderConfig for the Russian SuperGLUE."""

    VERSION = datasets.Version("0.0.1")

    def __init__(
        self,
        features: List[str],
        data_url: str,
        citation: str,
        url: str,
        label_classes: List[str] = ("False", "True"),
        **kwargs,
    ):
        """BuilderConfig for the Russian SuperGLUE.

        Args:
          features: `list[string]`, list of the features that will appear in the
            feature dict. Should not include "label".
          data_url: `string`, url to download the zip file from.
          citation: `string`, citation for the data set.
          url: `string`, url for information about the data set.
          label_classes: `list[string]`, the list of classes for the label if the
            label is present as a string. Non-string labels will be cast to either
            'False' or 'True'.
          **kwargs: keyword arguments forwarded to super.
        """
        # 0.0.1: Initial version.
        super(RussianSuperGlueConfig, self).__init__(version=self.VERSION, **kwargs)
        self.features = features
        self.label_classes = label_classes
        self.data_url = data_url
        self.citation = citation
        self.url = url


class RussianSuperGlue(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        RussianSuperGlueConfig(
            name="lidirus",
            description=_LIDIRUS_DESCRIPTION,
            features=[
                "sentence1",
                "sentence2",
                "knowledge",
                "lexical-semantics",
                "logic",
                "predicate-argument-structure",
            ],
            label_classes=["entailment", "not_entailment"],
            data_url="https://russiansuperglue.com/tasks/download/LiDiRus",
            citation="",
            url="https://russiansuperglue.com/tasks/task_info/LiDiRus",
        ),
        RussianSuperGlueConfig(
            name="rcb",
            description=_RCB_DESCRIPTION,
            features=["premise", "hypothesis", "verb", "negation"],
            label_classes=["entailment", "contradiction", "neutral"],
            data_url="https://russiansuperglue.com/tasks/download/RCB",
            citation="",
            url="https://russiansuperglue.com/tasks/task_info/RCB",
        ),
        RussianSuperGlueConfig(
            name="parus",
            description=_PARUS_DESCRIPTION,
            label_classes=["choice1", "choice2"],
            features=["premise", "choice1", "choice2", "question"],
            data_url="https://russiansuperglue.com/tasks/download/PARus",
            citation="",
            url="https://russiansuperglue.com/tasks/task_info/PARus",
        ),
        RussianSuperGlueConfig(
            name="muserc",
            description=_MUSERC_DESCRIPTION,
            features=["paragraph", "question", "answer"],
            data_url="https://russiansuperglue.com/tasks/download/MuSeRC",
            citation=_MUSERC_CITATION,
            label_classes=["False", "True"],
            url="https://russiansuperglue.com/tasks/task_info/MuSeRC",
        ),
        RussianSuperGlueConfig(
            name="terra",
            description=_TERRA_DESCRIPTION,
            features=["premise", "hypothesis"],
            label_classes=["entailment", "not_entailment"],
            data_url="https://russiansuperglue.com/tasks/download/TERRa",
            citation="",
            url="https://russiansuperglue.com/tasks/task_info/TERRa",
        ),
        RussianSuperGlueConfig(
            name="russe",
            description=_RUSSE_DESCRIPTION,
            features=[
                "word",
                "sentence1",
                "sentence2",
                "start1",
                "start2",
                "end1",
                "end2",
                "gold_sense1",
                "gold_sense2",
            ],
            data_url="https://russiansuperglue.com/tasks/download/RUSSE",
            citation=_RUSSE_CITATION,
            label_classes=["False", "True"],
            url="https://russiansuperglue.com/tasks/task_info/RUSSE",
        ),
        RussianSuperGlueConfig(
            name="rwsd",
            description=_RWSD_DESCRIPTION,
            features=["text", "span1_index", "span2_index", "span1_text", "span2_text"],
            data_url="https://russiansuperglue.com/tasks/download/RWSD",
            citation="",
            label_classes=["False", "True"],
            url="https://russiansuperglue.com/tasks/task_info/RWSD",
        ),
        RussianSuperGlueConfig(
            name="danetqa",
            description=_DANETQA_DESCRIPTION,
            features=["question", "passage"],
            data_url="https://russiansuperglue.com/tasks/download/DaNetQA",
            citation=_DANETQA_CITATION,
            label_classes=["False", "True"],
            url="https://russiansuperglue.com/tasks/task_info/DaNetQA",
        ),
        RussianSuperGlueConfig(
            name="rucos",
            description=_RUCOS_DESCRIPTION,
            features=["passage", "query", "entities", "answers"],
            data_url="https://russiansuperglue.com/tasks/download/RuCoS",
            citation=_RUCOS_CITATION,
            url="https://russiansuperglue.com/tasks/task_info/RuCoS",
        ),
    ]

    def _info(self):

        if self.config.name == "russe":
            features = {feature: datasets.Value("string") for feature in ("word", "sentence1", "sentence2")}
            features["start1"] = datasets.Value("int32")
            features["start2"] = datasets.Value("int32")
            features["end1"] = datasets.Value("int32")
            features["end2"] = datasets.Value("int32")
            features["gold_sense1"] = datasets.Value("int32")
            features["gold_sense2"] = datasets.Value("int32")

        else:
            features = {feature: datasets.Value("string") for feature in self.config.features}

        if self.config.name == "rwsd":
            features["span1_index"] = datasets.Value("int32")
            features["span2_index"] = datasets.Value("int32")

        if self.config.name == "muserc":
            features["idx"] = dict(
                {
                    "paragraph": datasets.Value("int32"),
                    "question": datasets.Value("int32"),
                    "answer": datasets.Value("int32"),
                }
            )
        elif self.config.name == "rucos":
            features["idx"] = dict(
                {
                    "passage": datasets.Value("int32"),
                    "query": datasets.Value("int32"),
                }
            )
        else:
            features["idx"] = datasets.Value("int32")

        if self.config.name == "rucos":
            # Entities are the set of possible choices for the placeholder.
            features["entities"] = datasets.features.Sequence(datasets.Value("string"))
            # Answers are the subset of entities that are correct.
            features["answers"] = datasets.features.Sequence(datasets.Value("string"))
        else:
            features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)

        return datasets.DatasetInfo(
            description=_RUSSIAN_SUPER_GLUE_DESCRIPTION + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _RUSSIAN_SUPER_GLUE_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url) or ""
        task_name = _get_task_name_from_data_url(self.config.data_url)
        dl_dir = os.path.join(dl_dir, task_name)
        if self.config.name == "lidirus":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, f"{task_name}.jsonl"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, "train.jsonl"),
                        "split": datasets.Split.TRAIN,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, "val.jsonl"),
                        "split": datasets.Split.VALIDATION,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, "test.jsonl"),
                        "split": datasets.Split.TEST,
                    },
                ),
            ]

    def _generate_examples(self, data_file: str, split: datasets.Split):
        with open(data_file, encoding="utf-8") as file:
            for line in file:
                row = json.loads(line)

                if self.config.name == "muserc":

                    paragraph = row["passage"]
                    for question in paragraph["questions"]:
                        for answer in question["answers"]:
                            label = answer.get("label")
                            key = "%s_%s_%s" % (row["idx"], question["idx"], answer["idx"])
                            yield key, {
                                "paragraph": paragraph["text"],
                                "question": question["question"],
                                "answer": answer["text"],
                                "label": -1 if label is None else _cast_label(bool(label)),
                                "idx": {"paragraph": row["idx"], "question": question["idx"], "answer": answer["idx"]},
                            }

                elif self.config.name == "rucos":
                    passage = row["passage"]
                    for qa in row["qas"]:
                        yield qa["idx"], {
                            "passage": passage["text"],
                            "query": qa["query"],
                            "entities": _get_rucos_entities(passage),
                            "answers": _get_rucos_answers(qa),
                            "idx": {"passage": row["idx"], "query": qa["idx"]},
                        }
                else:
                    if self.config.name in ("lidirus", "rcb"):
                        # features may be missing
                        example = {feature: row.get(feature, "") for feature in self.config.features}
                    elif self.config.name == "russe" and split == datasets.Split.TEST:
                        # gold senses are not available in `test` split
                        example = {
                            feature: row[feature]
                            for feature in self.config.features
                            if feature not in ("gold_sense1", "gold_sense2")
                        }
                        example["gold_sense1"] = -1
                        example["gold_sense2"] = -1
                    else:
                        if self.config.name == "rwsd":
                            row.update(row["target"])

                        example = {feature: row[feature] for feature in self.config.features}

                    example["idx"] = row["idx"]

                    if "label" in row:
                        if self.config.name == "parus":
                            example["label"] = "choice2" if row["label"] else "choice1"
                        else:
                            example["label"] = _cast_label(row["label"])
                    else:
                        assert split == datasets.Split.TEST, row
                        example["label"] = -1

                    yield example["idx"], example


def _get_task_name_from_data_url(data_url: str) -> str:
    return data_url.split("/")[-1]


def _cast_label(label: Union[str, bool, int]) -> str:
    """Converts the label into the appropriate string version."""
    if isinstance(label, str):
        return label
    elif isinstance(label, bool):
        return "True" if label else "False"
    elif isinstance(label, int):
        assert label in (0, 1)
        return str(label)
    else:
        raise ValueError("Invalid label format.")


def _get_rucos_entities(passage: dict) -> List[str]:
    """Returns the unique set of entities."""
    text = passage["text"]
    entities = set()
    for entity in passage["entities"]:
        entities.add(text[entity["start"] : entity["end"] + 1])
    return sorted(entities)


def _get_rucos_answers(qa: dict) -> List[str]:
    """Returns the unique set of answers."""
    if "answers" not in qa:
        return []
    answers = set()
    for answer in qa["answers"]:
        answers.add(answer["text"])
    return sorted(answers)
