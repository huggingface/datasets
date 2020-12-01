"""TODO(xtreme): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import glob
import json
import os
import textwrap

import six

import datasets


# TODO(xtreme): BibTeX citation
_CITATION = """\
@article{hu2020xtreme,
      author    = {Junjie Hu and Sebastian Ruder and Aditya Siddhant and Graham Neubig and Orhan Firat and Melvin Johnson},
      title     = {XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization},
      journal   = {CoRR},
      volume    = {abs/2003.11080},
      year      = {2020},
      archivePrefix = {arXiv},
      eprint    = {2003.11080}
}
"""

# TODO(xtrem):
_DESCRIPTION = """\
The Cross-lingual TRansfer Evaluation of Multilingual Encoders (XTREME) benchmark is a benchmark for the evaluation of
the cross-lingual generalization ability of pre-trained multilingual models. It covers 40 typologically diverse languages
(spanning 12 language families) and includes nine tasks that collectively require reasoning about different levels of
syntax and semantics. The languages in XTREME are selected to maximize language diversity, coverage in existing tasks,
and availability of training data. Among these are many under-studied languages, such as the Dravidian languages Tamil
(spoken in southern India, Sri Lanka, and Singapore), Telugu and Malayalam (spoken mainly in southern India), and the
Niger-Congo languages Swahili and Yoruba, spoken in Africa.
"""
_PREFIX = "https://raw.githubusercontent.com/UniversalDependencies/"
_UD_DATASETS = {
    "af_afribooms": {
        "train": "UD_Afrikaans-AfriBooms/master/af_afribooms-ud-train.conllu",
        "dev": "UD_Afrikaans-AfriBooms/master/af_afribooms-ud-dev.conllu",
        "test": "UD_Afrikaans-AfriBooms/master/af_afribooms-ud-test.conllu",
    },
    "akk_pisandub": {
        "test": "UD_Akkadian-PISANDUB/master/akk_pisandub-ud-test.conllu"
    },
    "akk_riao": {
        "test": "UD_Akkadian-RIAO/master/akk_riao-ud-test.conllu"
    },

}

class UniversaldependenciesConfig(datasets.BuilderConfig):
    """BuilderConfig for Universal dependencies"""

    def __init__(self, data_url, citation, url, text_features, **kwargs):
        """

        Args:
            text_features: `dict[string, string]`, map from the name of the feature
        dict for each text field to the name of the column in the tsv file
            label_column:
            label_classes
            **kwargs: keyword arguments forwarded to super.
        """
        super(UniversaldependenciesConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.data_url = data_url
        self.citation = citation
        self.url = url


class Universaldependencies(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.1.0")
    BUILDER_CONFIGS = [
        UniversaldependenciesConfig(
            name=name,
            description=_DESCRIPTIONS[name.split(".")[0]],
            citation=_CITATIONS[name.split(".")[0]],
            text_features=_TEXT_FEATURES[name.split(".")[0]],
            data_url=_DATA_URLS[name.split(".")[0]],
            url=_URLS[name.split(".")[0]],
        )
        for name in _NAMES
    ]

    def _info(self):
        # info

    def _generate_examples(self, filepath):
        # parsing
