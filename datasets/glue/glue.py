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
"""The General Language Understanding Evaluation (GLUE) benchmark."""


import csv
import os
import textwrap

import numpy as np

import datasets


_GLUE_CITATION = """\
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}
"""

_GLUE_DESCRIPTION = """\
GLUE, the General Language Understanding Evaluation benchmark
(https://gluebenchmark.com/) is a collection of resources for training,
evaluating, and analyzing natural language understanding systems.

"""

_MRPC_DEV_IDS = "https://dl.fbaipublicfiles.com/glue/data/mrpc_dev_ids.tsv"
_MRPC_TRAIN = "https://dl.fbaipublicfiles.com/senteval/senteval_data/msr_paraphrase_train.txt"
_MRPC_TEST = "https://dl.fbaipublicfiles.com/senteval/senteval_data/msr_paraphrase_test.txt"

_MNLI_BASE_KWARGS = dict(
    text_features={
        "premise": "sentence1",
        "hypothesis": "sentence2",
    },
    label_classes=["entailment", "neutral", "contradiction"],
    label_column="gold_label",
    data_url="https://dl.fbaipublicfiles.com/glue/data/MNLI.zip",
    data_dir="MNLI",
    citation=textwrap.dedent(
        """\
      @InProceedings{N18-1101,
        author = "Williams, Adina
                  and Nangia, Nikita
                  and Bowman, Samuel",
        title = "A Broad-Coverage Challenge Corpus for
                 Sentence Understanding through Inference",
        booktitle = "Proceedings of the 2018 Conference of
                     the North American Chapter of the
                     Association for Computational Linguistics:
                     Human Language Technologies, Volume 1 (Long
                     Papers)",
        year = "2018",
        publisher = "Association for Computational Linguistics",
        pages = "1112--1122",
        location = "New Orleans, Louisiana",
        url = "http://aclweb.org/anthology/N18-1101"
      }
      @article{bowman2015large,
        title={A large annotated corpus for learning natural language inference},
        author={Bowman, Samuel R and Angeli, Gabor and Potts, Christopher and Manning, Christopher D},
        journal={arXiv preprint arXiv:1508.05326},
        year={2015}
      }"""
    ),
    url="http://www.nyu.edu/projects/bowman/multinli/",
)


class GlueConfig(datasets.BuilderConfig):
    """BuilderConfig for GLUE."""

    def __init__(
        self,
        text_features,
        label_column,
        data_url,
        data_dir,
        citation,
        url,
        label_classes=None,
        process_label=lambda x: x,
        **kwargs,
    ):
        """BuilderConfig for GLUE.

        Args:
          text_features: `dict[string, string]`, map from the name of the feature
            dict for each text field to the name of the column in the tsv file
          label_column: `string`, name of the column in the tsv file corresponding
            to the label
          data_url: `string`, url to download the zip file from
          data_dir: `string`, the path to the folder containing the tsv files in the
            downloaded zip
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          label_classes: `list[string]`, the list of classes if the label is
            categorical. If not provided, then the label will be of type
            `datasets.Value('float32')`.
          process_label: `Function[string, any]`, function  taking in the raw value
            of the label and processing it to the form required by the label feature
          **kwargs: keyword arguments forwarded to super.
        """
        super(GlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.label_column = label_column
        self.label_classes = label_classes
        self.data_url = data_url
        self.data_dir = data_dir
        self.citation = citation
        self.url = url
        self.process_label = process_label


class Glue(datasets.GeneratorBasedBuilder):
    """The General Language Understanding Evaluation (GLUE) benchmark."""

    BUILDER_CONFIGS = [
        GlueConfig(
            name="cola",
            description=textwrap.dedent(
                """\
            The Corpus of Linguistic Acceptability consists of English
            acceptability judgments drawn from books and journal articles on
            linguistic theory. Each example is a sequence of words annotated
            with whether it is a grammatical English sentence."""
            ),
            text_features={"sentence": "sentence"},
            label_classes=["unacceptable", "acceptable"],
            label_column="is_acceptable",
            data_url="https://dl.fbaipublicfiles.com/glue/data/CoLA.zip",
            data_dir="CoLA",
            citation=textwrap.dedent(
                """\
            @article{warstadt2018neural,
              title={Neural Network Acceptability Judgments},
              author={Warstadt, Alex and Singh, Amanpreet and Bowman, Samuel R},
              journal={arXiv preprint arXiv:1805.12471},
              year={2018}
            }"""
            ),
            url="https://nyu-mll.github.io/CoLA/",
        ),
        GlueConfig(
            name="sst2",
            description=textwrap.dedent(
                """\
            The Stanford Sentiment Treebank consists of sentences from movie reviews and
            human annotations of their sentiment. The task is to predict the sentiment of a
            given sentence. We use the two-way (positive/negative) class split, and use only
            sentence-level labels."""
            ),
            text_features={"sentence": "sentence"},
            label_classes=["negative", "positive"],
            label_column="label",
            data_url="https://dl.fbaipublicfiles.com/glue/data/SST-2.zip",
            data_dir="SST-2",
            citation=textwrap.dedent(
                """\
            @inproceedings{socher2013recursive,
              title={Recursive deep models for semantic compositionality over a sentiment treebank},
              author={Socher, Richard and Perelygin, Alex and Wu, Jean and Chuang, Jason and Manning, Christopher D and Ng, Andrew and Potts, Christopher},
              booktitle={Proceedings of the 2013 conference on empirical methods in natural language processing},
              pages={1631--1642},
              year={2013}
            }"""
            ),
            url="https://datasets.stanford.edu/sentiment/index.html",
        ),
        GlueConfig(
            name="mrpc",
            description=textwrap.dedent(
                """\
            The Microsoft Research Paraphrase Corpus (Dolan & Brockett, 2005) is a corpus of
            sentence pairs automatically extracted from online news sources, with human annotations
            for whether the sentences in the pair are semantically equivalent."""
            ),  # pylint: disable=line-too-long
            text_features={"sentence1": "", "sentence2": ""},
            label_classes=["not_equivalent", "equivalent"],
            label_column="Quality",
            data_url="",  # MRPC isn't hosted by GLUE.
            data_dir="MRPC",
            citation=textwrap.dedent(
                """\
            @inproceedings{dolan2005automatically,
              title={Automatically constructing a corpus of sentential paraphrases},
              author={Dolan, William B and Brockett, Chris},
              booktitle={Proceedings of the Third International Workshop on Paraphrasing (IWP2005)},
              year={2005}
            }"""
            ),
            url="https://www.microsoft.com/en-us/download/details.aspx?id=52398",
        ),
        GlueConfig(
            name="qqp",
            description=textwrap.dedent(
                """\
            The Quora Question Pairs2 dataset is a collection of question pairs from the
            community question-answering website Quora. The task is to determine whether a
            pair of questions are semantically equivalent."""
            ),
            text_features={
                "question1": "question1",
                "question2": "question2",
            },
            label_classes=["not_duplicate", "duplicate"],
            label_column="is_duplicate",
            data_url="https://dl.fbaipublicfiles.com/glue/data/QQP-clean.zip",
            data_dir="QQP",
            citation=textwrap.dedent(
                """\
          @online{WinNT,
            author = {Iyer, Shankar and Dandekar, Nikhil and Csernai, Kornel},
            title = {First Quora Dataset Release: Question Pairs},
            year = {2017},
            url = {https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs},
            urldate = {2019-04-03}
          }"""
            ),
            url="https://data.quora.com/First-Quora-Dataset-Release-Question-Pairs",
        ),
        GlueConfig(
            name="stsb",
            description=textwrap.dedent(
                """\
            The Semantic Textual Similarity Benchmark (Cer et al., 2017) is a collection of
            sentence pairs drawn from news headlines, video and image captions, and natural
            language inference data. Each pair is human-annotated with a similarity score
            from 1 to 5."""
            ),
            text_features={
                "sentence1": "sentence1",
                "sentence2": "sentence2",
            },
            label_column="score",
            data_url="https://dl.fbaipublicfiles.com/glue/data/STS-B.zip",
            data_dir="STS-B",
            citation=textwrap.dedent(
                """\
            @article{cer2017semeval,
              title={Semeval-2017 task 1: Semantic textual similarity-multilingual and cross-lingual focused evaluation},
              author={Cer, Daniel and Diab, Mona and Agirre, Eneko and Lopez-Gazpio, Inigo and Specia, Lucia},
              journal={arXiv preprint arXiv:1708.00055},
              year={2017}
            }"""
            ),
            url="http://ixa2.si.ehu.es/stswiki/index.php/STSbenchmark",
            process_label=np.float32,
        ),
        GlueConfig(
            name="mnli",
            description=textwrap.dedent(
                """\
            The Multi-Genre Natural Language Inference Corpus is a crowdsourced
            collection of sentence pairs with textual entailment annotations. Given a premise sentence
            and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis
            (entailment), contradicts the hypothesis (contradiction), or neither (neutral). The premise sentences are
            gathered from ten different sources, including transcribed speech, fiction, and government reports.
            We use the standard test set, for which we obtained private labels from the authors, and evaluate
            on both the matched (in-domain) and mismatched (cross-domain) section. We also use and recommend
            the SNLI corpus as 550k examples of auxiliary training data."""
            ),
            **_MNLI_BASE_KWARGS,
        ),
        GlueConfig(
            name="mnli_mismatched",
            description=textwrap.dedent(
                """\
          The mismatched validation and test splits from MNLI.
          See the "mnli" BuilderConfig for additional information."""
            ),
            **_MNLI_BASE_KWARGS,
        ),
        GlueConfig(
            name="mnli_matched",
            description=textwrap.dedent(
                """\
          The matched validation and test splits from MNLI.
          See the "mnli" BuilderConfig for additional information."""
            ),
            **_MNLI_BASE_KWARGS,
        ),
        GlueConfig(
            name="qnli",
            description=textwrap.dedent(
                """\
            The Stanford Question Answering Dataset is a question-answering
            dataset consisting of question-paragraph pairs, where one of the sentences in the paragraph (drawn
            from Wikipedia) contains the answer to the corresponding question (written by an annotator). We
            convert the task into sentence pair classification by forming a pair between each question and each
            sentence in the corresponding context, and filtering out pairs with low lexical overlap between the
            question and the context sentence. The task is to determine whether the context sentence contains
            the answer to the question. This modified version of the original task removes the requirement that
            the model select the exact answer, but also removes the simplifying assumptions that the answer
            is always present in the input and that lexical overlap is a reliable cue."""
            ),  # pylint: disable=line-too-long
            text_features={
                "question": "question",
                "sentence": "sentence",
            },
            label_classes=["entailment", "not_entailment"],
            label_column="label",
            data_url="https://dl.fbaipublicfiles.com/glue/data/QNLIv2.zip",
            data_dir="QNLI",
            citation=textwrap.dedent(
                """\
            @article{rajpurkar2016squad,
              title={Squad: 100,000+ questions for machine comprehension of text},
              author={Rajpurkar, Pranav and Zhang, Jian and Lopyrev, Konstantin and Liang, Percy},
              journal={arXiv preprint arXiv:1606.05250},
              year={2016}
            }"""
            ),
            url="https://rajpurkar.github.io/SQuAD-explorer/",
        ),
        GlueConfig(
            name="rte",
            description=textwrap.dedent(
                """\
            The Recognizing Textual Entailment (RTE) datasets come from a series of annual textual
            entailment challenges. We combine the data from RTE1 (Dagan et al., 2006), RTE2 (Bar Haim
            et al., 2006), RTE3 (Giampiccolo et al., 2007), and RTE5 (Bentivogli et al., 2009).4 Examples are
            constructed based on news and Wikipedia text. We convert all datasets to a two-class split, where
            for three-class datasets we collapse neutral and contradiction into not entailment, for consistency."""
            ),  # pylint: disable=line-too-long
            text_features={
                "sentence1": "sentence1",
                "sentence2": "sentence2",
            },
            label_classes=["entailment", "not_entailment"],
            label_column="label",
            data_url="https://dl.fbaipublicfiles.com/glue/data/RTE.zip",
            data_dir="RTE",
            citation=textwrap.dedent(
                """\
            @inproceedings{dagan2005pascal,
              title={The PASCAL recognising textual entailment challenge},
              author={Dagan, Ido and Glickman, Oren and Magnini, Bernardo},
              booktitle={Machine Learning Challenges Workshop},
              pages={177--190},
              year={2005},
              organization={Springer}
            }
            @inproceedings{bar2006second,
              title={The second pascal recognising textual entailment challenge},
              author={Bar-Haim, Roy and Dagan, Ido and Dolan, Bill and Ferro, Lisa and Giampiccolo, Danilo and Magnini, Bernardo and Szpektor, Idan},
              booktitle={Proceedings of the second PASCAL challenges workshop on recognising textual entailment},
              volume={6},
              number={1},
              pages={6--4},
              year={2006},
              organization={Venice}
            }
            @inproceedings{giampiccolo2007third,
              title={The third pascal recognizing textual entailment challenge},
              author={Giampiccolo, Danilo and Magnini, Bernardo and Dagan, Ido and Dolan, Bill},
              booktitle={Proceedings of the ACL-PASCAL workshop on textual entailment and paraphrasing},
              pages={1--9},
              year={2007},
              organization={Association for Computational Linguistics}
            }
            @inproceedings{bentivogli2009fifth,
              title={The Fifth PASCAL Recognizing Textual Entailment Challenge.},
              author={Bentivogli, Luisa and Clark, Peter and Dagan, Ido and Giampiccolo, Danilo},
              booktitle={TAC},
              year={2009}
            }"""
            ),
            url="https://aclweb.org/aclwiki/Recognizing_Textual_Entailment",
        ),
        GlueConfig(
            name="wnli",
            description=textwrap.dedent(
                """\
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
            call converted dataset WNLI (Winograd NLI)."""
            ),
            text_features={
                "sentence1": "sentence1",
                "sentence2": "sentence2",
            },
            label_classes=["not_entailment", "entailment"],
            label_column="label",
            data_url="https://dl.fbaipublicfiles.com/glue/data/WNLI.zip",
            data_dir="WNLI",
            citation=textwrap.dedent(
                """\
            @inproceedings{levesque2012winograd,
              title={The winograd schema challenge},
              author={Levesque, Hector and Davis, Ernest and Morgenstern, Leora},
              booktitle={Thirteenth International Conference on the Principles of Knowledge Representation and Reasoning},
              year={2012}
            }"""
            ),
            url="https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html",
        ),
        GlueConfig(
            name="ax",
            description=textwrap.dedent(
                """\
            A manually-curated evaluation dataset for fine-grained analysis of
            system performance on a broad range of linguistic phenomena. This
            dataset evaluates sentence understanding through Natural Language
            Inference (NLI) problems. Use a model trained on MulitNLI to produce
            predictions for this dataset."""
            ),
            text_features={
                "premise": "sentence1",
                "hypothesis": "sentence2",
            },
            label_classes=["entailment", "neutral", "contradiction"],
            label_column="",  # No label since we only have test set.
            # We must use a URL shortener since the URL from GLUE is very long and
            # causes issues in TFDS.
            data_url="https://dl.fbaipublicfiles.com/glue/data/AX.tsv",
            data_dir="",  # We are downloading a tsv.
            citation="",  # The GLUE citation is sufficient.
            url="https://gluebenchmark.com/diagnostics",
        ),
    ]

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features.keys()}
        if self.config.label_classes:
            features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        else:
            features["label"] = datasets.Value("float32")
        features["idx"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_GLUE_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _GLUE_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "ax":
            data_file = dl_manager.download(self.config.data_url)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": data_file,
                        "split": "test",
                    },
                )
            ]

        if self.config.name == "mrpc":
            data_dir = None
            mrpc_files = dl_manager.download(
                {
                    "dev_ids": _MRPC_DEV_IDS,
                    "train": _MRPC_TRAIN,
                    "test": _MRPC_TEST,
                }
            )
        else:
            dl_dir = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(dl_dir, self.config.data_dir)
            mrpc_files = None
        train_split = datasets.SplitGenerator(
            name=datasets.Split.TRAIN,
            gen_kwargs={
                "data_file": os.path.join(data_dir or "", "train.tsv"),
                "split": "train",
                "mrpc_files": mrpc_files,
            },
        )
        if self.config.name == "mnli":
            return [
                train_split,
                _mnli_split_generator("validation_matched", data_dir, "dev", matched=True),
                _mnli_split_generator("validation_mismatched", data_dir, "dev", matched=False),
                _mnli_split_generator("test_matched", data_dir, "test", matched=True),
                _mnli_split_generator("test_mismatched", data_dir, "test", matched=False),
            ]
        elif self.config.name == "mnli_matched":
            return [
                _mnli_split_generator("validation", data_dir, "dev", matched=True),
                _mnli_split_generator("test", data_dir, "test", matched=True),
            ]
        elif self.config.name == "mnli_mismatched":
            return [
                _mnli_split_generator("validation", data_dir, "dev", matched=False),
                _mnli_split_generator("test", data_dir, "test", matched=False),
            ]
        else:
            return [
                train_split,
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "data_file": os.path.join(data_dir or "", "dev.tsv"),
                        "split": "dev",
                        "mrpc_files": mrpc_files,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(data_dir or "", "test.tsv"),
                        "split": "test",
                        "mrpc_files": mrpc_files,
                    },
                ),
            ]

    def _generate_examples(self, data_file, split, mrpc_files=None):
        if self.config.name == "mrpc":
            # We have to prepare the MRPC dataset from the original sources ourselves.
            examples = self._generate_example_mrpc_files(mrpc_files=mrpc_files, split=split)
            for example in examples:
                yield example["idx"], example
        else:
            process_label = self.config.process_label
            label_classes = self.config.label_classes

            # The train and dev files for CoLA are the only tsv files without a
            # header.
            is_cola_non_test = self.config.name == "cola" and split != "test"

            with open(data_file, encoding="utf8") as f:
                reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                if is_cola_non_test:
                    reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)

                for n, row in enumerate(reader):
                    if is_cola_non_test:
                        row = {
                            "sentence": row[3],
                            "is_acceptable": row[1],
                        }

                    example = {feat: row[col] for feat, col in self.config.text_features.items()}
                    example["idx"] = n

                    if self.config.label_column in row:
                        label = row[self.config.label_column]
                        # For some tasks, the label is represented as 0 and 1 in the tsv
                        # files and needs to be cast to integer to work with the feature.
                        if label_classes and label not in label_classes:
                            label = int(label) if label else None
                        example["label"] = process_label(label)
                    else:
                        example["label"] = process_label(-1)

                    # Filter out corrupted rows.
                    for value in example.values():
                        if value is None:
                            break
                    else:
                        yield example["idx"], example

    def _generate_example_mrpc_files(self, mrpc_files, split):
        if split == "test":
            with open(mrpc_files["test"], encoding="utf8") as f:
                # The first 3 bytes are the utf-8 BOM \xef\xbb\xbf, which messes with
                # the Quality key.
                f.seek(3)
                reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                for n, row in enumerate(reader):
                    yield {
                        "sentence1": row["#1 String"],
                        "sentence2": row["#2 String"],
                        "label": int(row["Quality"]),
                        "idx": n,
                    }
        else:
            with open(mrpc_files["dev_ids"], encoding="utf8") as f:
                reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                dev_ids = [[row[0], row[1]] for row in reader]
            with open(mrpc_files["train"], encoding="utf8") as f:
                # The first 3 bytes are the utf-8 BOM \xef\xbb\xbf, which messes with
                # the Quality key.
                f.seek(3)
                reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                for n, row in enumerate(reader):
                    is_row_in_dev = [row["#1 ID"], row["#2 ID"]] in dev_ids
                    if is_row_in_dev == (split == "dev"):
                        yield {
                            "sentence1": row["#1 String"],
                            "sentence2": row["#2 String"],
                            "label": int(row["Quality"]),
                            "idx": n,
                        }


def _mnli_split_generator(name, data_dir, split, matched):
    return datasets.SplitGenerator(
        name=name,
        gen_kwargs={
            "data_file": os.path.join(data_dir, "%s_%s.tsv" % (split, "matched" if matched else "mismatched")),
            "split": split,
            "mrpc_files": None,
        },
    )
