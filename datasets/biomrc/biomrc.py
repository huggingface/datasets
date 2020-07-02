# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""BioMRC Dataset"""

from __future__ import absolute_import, division, print_function

import json
import logging
import os

import nlp


_CITATION = """\
@inproceedings{pappas-etal-2020-biomrc,
    title = "{B}io{MRC}: A Dataset for Biomedical Machine Reading Comprehension",
    author = "Pappas, Dimitris  and
      Stavropoulos, Petros  and
      Androutsopoulos, Ion  and
      McDonald, Ryan",
    booktitle = "Proceedings of the 19th SIGBioMed Workshop on Biomedical Language Processing",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.bionlp-1.15",
    pages = "140--149",
    abstract = "We introduce BIOMRC, a large-scale cloze-style biomedical MRC dataset. Care was taken to reduce noise, compared to the previous BIOREAD dataset of Pappas et al. (2018). Experiments show that simple heuristics do not perform well on the new dataset and that two neural MRC models that had been tested on BIOREAD perform much better on BIOMRC, indicating that the new dataset is indeed less noisy or at least that its task is more feasible. Non-expert human performance is also higher on the new dataset compared to BIOREAD, and biomedical experts perform even better. We also introduce a new BERT-based MRC model, the best version of which substantially outperforms all other methods tested, reaching or surpassing the accuracy of biomedical experts in some experiments. We make the new dataset available in three different sizes, also releasing our code, and providing a leaderboard.",
}
"""

_DESCRIPTION = """\
We introduce BIOMRC, a large-scale cloze-style biomedical MRC dataset. Care was taken to reduce noise, compared to the previous BIOREAD dataset of Pappas et al. (2018). Experiments show that simple heuristics do not perform well on the new dataset and that two neural MRC models that had been tested on BIOREAD perform much better on BIOMRC, indicating that the new dataset is indeed less noisy or at least that its task is more feasible. Non-expert human performance is also higher on the new dataset compared to BIOREAD, and biomedical experts perform even better. We also introduce a new BERT-based MRC model, the best version of which substantially outperforms all other methods tested, reaching or surpassing the accuracy of biomedical experts in some experiments. We make the new dataset available in three different sizes, also releasing our code, and providing a leaderboard.
"""

_SETTING = "A"
_VERSION = "large"


class BiomrcConfig(nlp.BuilderConfig):
    """BuilderConfig for BioMRC."""

    global _SETTING, _VERSION

    def __init__(self, **kwargs):
        """BuilderConfig for BioMRC.
    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        if "biomrc_setting" in kwargs:
            if kwargs["biomrc_setting"] in ["B", "b"]:
                _SETTING = "B"
            else:
                if kwargs["biomrc_setting"] not in ["A", "a"]:
                    print("Wrong Setting for BioMRC, using Setting A instead.")

        if "biomrc_version" in kwargs:
            if kwargs["biomrc_version"] in ["small", "SMALL", "Small"]:
                _VERSION = "small"
            elif kwargs["biomrc_version"] in ["tiny", "TINY", "Tiny"]:
                _VERSION = "tiny"
            else:
                if kwargs["biomrc_version"] not in ["large", "LARGE", "Large"]:
                    print("Wrong version for BioMRC, using BioMRC Large instead.")

        super(BiomrcConfig, self).__init__(**kwargs)


class Biomrc(nlp.GeneratorBasedBuilder):
    """BioMRC Dataset"""

    BUILDER_CONFIGS = [
        BiomrcConfig(
            name="plain_text",
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"),
            description="Plain text",
        ),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "abstract": nlp.Value("string"),
                    "title": nlp.Value("string"),
                    "entities_list": nlp.features.Sequence(nlp.Value("string")),
                    "answer": nlp.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="http://nlp.cs.aueb.gr/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        setting = "" if _SETTING == "A" else "_B"
        if _VERSION == "large":
            urls_to_download = {
                "train": "https://archive.org/download/biomrc_dataset/biomrc_large/dataset_train{}.json.gz".format(
                    setting
                ),
                "val": "https://archive.org/download/biomrc_dataset/biomrc_large/dataset_val{}.json.gz".format(
                    setting
                ),
                "test": "https://archive.org/download/biomrc_dataset/biomrc_large/dataset_test{}.json.gz".format(
                    setting
                ),
            }
        elif _VERSION == "small":
            urls_to_download = {
                "train": "https://archive.org/download/biomrc_dataset/biomrc_small/dataset_small_train{}.json.gz".format(
                    setting
                ),
                "val": "https://archive.org/download/biomrc_dataset/biomrc_small/dataset_small_val{}.json.gz".format(
                    setting
                ),
                "test": "https://archive.org/download/biomrc_dataset/biomrc_small/dataset_small_test{}.json.gz".format(
                    setting
                ),
            }
        else:
            urls_to_download = {
                "test": "https://archive.org/download/biomrc_dataset/biomrc_tiny/dataset_tiny_test{}.json.gz".format(
                    setting
                )
            }

        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        if _VERSION == "tiny":
            return [
                nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
            ]
        else:
            if _SETTING == "A":
                return [
                    nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
                    nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["val"]}),
                    nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
                ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        # Id for the biomrc dataset
        with open(filepath) as fp:
            biomrc = json.load(fp)
            for _id, (ab, ti, el, an) in enumerate(
                zip(biomrc["abstracts"], biomrc["titles"], biomrc["entities_list"], biomrc["answers"])
            ):
                yield _id, {"abstract": ab, "title": ti, "entities_list": el, "answer": an}
