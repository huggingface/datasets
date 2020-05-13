"""TODO(break_data): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os
import textwrap

import six

import nlp


# TODO(break): BibTeX citation
_CITATION = """\
@article{Wolfson2020Break,
  title={Break It Down: A Question Understanding Benchmark},
  author={Wolfson, Tomer and Geva, Mor and Gupta, Ankit and Gardner, Matt and Goldberg, Yoav and Deutch, Daniel and Berant, Jonathan},
  journal={Transactions of the Association for Computational Linguistics},
  year={2020},
}
"""

# TODO(break):
_DESCRIPTION = """\
Break is a human annotated dataset of natural language questions and their Question Decomposition Meaning Representations
(QDMRs). Break consists of 83,978 examples sampled from 10 question answering datasets over text, images and databases. 
This repository contains the Break dataset along with information on the exact data format.
"""
_URL = "https://github.com/allenai/Break/raw/master/break_dataset/Break-dataset.zip"


class BreakDataConfig(nlp.BuilderConfig):

    """BuilderConfig for Break"""

    def __init__(self, text_features, lexicon_tokens, **kwargs):
        """

        Args:
            text_features: `dict[string, string]`, map from the name of the feature
        dict for each text field to the name of the column in the tsv file
            lexicon_tokens: to define if we want to load the lexicon_tokens files or not
            **kwargs: keyword arguments forwarded to super.
        """
        super(BreakDataConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )
        self.text_features = text_features
        self.lexicon_tokens = lexicon_tokens


class BreakData(nlp.GeneratorBasedBuilder):
    """TODO(break_data): Short description of my dataset."""

    # TODO(break_data): Set up version.
    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        BreakDataConfig(
            name="QDMR-high-level",
            description=textwrap.dedent(
                """
             Contains questions annotated with the high-level variant of QDMR. These decomposition are exclusive to Reading 
             Comprehension tasks (Section 2). lexicon_tokens files are also provided."""
            ),
            text_features={
                "question_id": "question_id",
                "question_text": "question_text",
                "decomposition": "decomposition",
                "operators": "operators",
                "split": "split",
            },
            lexicon_tokens=False,
        ),
        BreakDataConfig(
            name="QDMR-high-level-lexicon",
            description=textwrap.dedent(
                """
               Contains questions annotated with the high-level variant of QDMR. These decomposition are exclusive to Reading 
               Comprehension tasks (Section 2). lexicon_tokens files are also provided."""
            ),
            text_features={"source": "source", "allowed_tokens": "allowed_tokens",},
            lexicon_tokens=True,
        ),
        BreakDataConfig(
            name="QDMR",
            description=textwrap.dedent(
                """
               Contains questions over text, images and databases annotated with their Question Decomposition Meaning 
               Representation. In addition to the train, dev and (hidden) test sets we provide lexicon_tokens files. For 
               each question, the lexicon file contains the set of valid tokens that could potentially appear in its 
               decomposition """
            ),
            text_features={
                "question_id": "question_id",
                "question_text": "question_text",
                "decomposition": "decomposition",
                "operators": "operators",
                "split": "split",
            },
            lexicon_tokens=False,
        ),
        BreakDataConfig(
            name="QDMR-lexicon",
            description=textwrap.dedent(
                """
                 Contains questions over text, images and databases annotated with their Question Decomposition Meaning 
               Representation. In addition to the train, dev and (hidden) test sets we provide lexicon_tokens files. For 
               each question, the lexicon file contains the set of valid tokens that could potentially appear in its 
               decomposition """
            ),
            text_features={"source": "source", "allowed_tokens": "allowed_tokens",},
            lexicon_tokens=True,
        ),
        BreakDataConfig(
            name="logical-forms",
            description=textwrap.dedent(
                """
               Contains questions and QDMRs annotated with full logical-forms of QDMR operators + arguments. Full logical-forms 
               were inferred by the annotation-consistency algorithm described in """
            ),
            lexicon_tokens=False,
            text_features={
                "question_id": "question_id",
                "question_text": "question_text",
                "decomposition": "decomposition",
                "operators": "operators",
                "split": "split",
                "program": "program",
            },
        ),
    ]

    def _info(self):
        # TODO(break_data): Specifies the nlp.DatasetInfo object
        features = {text_feature: nlp.Value("string") for text_feature in six.iterkeys(self.config.text_features)}
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                features
                # These are the features of your dataset like images, labels ...
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/allenai/Break",
            citation=_CITATION,
        )
        # if

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(break_data): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "Break-dataset")
        qdmr_high_level = os.path.join(data_dir, "QDMR-high-level")
        qdmr = os.path.join(data_dir, "QDMR")
        logical = os.path.join(data_dir, "logical-forms")
        if self.config.name == "QDMR" or self.config.name == "QDMR-lexicon":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(qdmr, "train.csv")
                        if not self.config.lexicon_tokens
                        else os.path.join(qdmr, "train_lexicon_tokens.json")
                    },
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(qdmr, "dev.csv")
                        if not self.config.lexicon_tokens
                        else os.path.join(qdmr, "dev_lexicon_tokens.json")
                    },
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(qdmr, "test.csv")
                        if not self.config.lexicon_tokens
                        else os.path.join(qdmr, "test_lexicon_tokens.json")
                    },
                ),
            ]
        elif self.config.name == "QDMR-high-level" or self.config.name == "QDMR-high-level-lexicon":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(qdmr_high_level, "train.csv")
                        if not self.config.lexicon_tokens
                        else os.path.join(qdmr_high_level, "train_lexicon_tokens.json")
                    },
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(qdmr_high_level, "dev.csv")
                        if not self.config.lexicon_tokens
                        else os.path.join(qdmr_high_level, "dev_lexicon_tokens.json")
                    },
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(qdmr_high_level, "test.csv")
                        if not self.config.lexicon_tokens
                        else os.path.join(qdmr_high_level, "test_lexicon_tokens.json")
                    },
                ),
            ]
        elif self.config.name == "logical-forms":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(logical, "train.csv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(logical, "dev.csv")},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(logical, "test.csv")},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(break_data): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            if (
                self.config.name == "QDMR-high-level"
                or self.config.name == "QDMR"
                or self.config.name == "logical-forms"
            ):
                data = csv.DictReader(f)
                for id_, row in enumerate(data):
                    yield id_, row
            elif self.config.name == "QDMR-high-level-lexicon" or self.config.name == "QDMR-lexicon":
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    yield id_, data
