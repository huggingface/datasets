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
"""BioMRC Dataset"""

from __future__ import absolute_import, division, print_function

import json
import logging

import datasets


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


class BiomrcConfig(datasets.BuilderConfig):
    """BuilderConfig for BioMRC."""

    def __init__(self, biomrc_setting="A", biomrc_version="large", **kwargs):
        """BuilderConfig for BioMRC.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        if biomrc_setting.lower() == "b":
            self.biomrc_setting = "B"
        else:
            if biomrc_setting.lower() != "a":
                logging.warning("Wrong Setting for BioMRC, using Setting A instead.")
            self.biomrc_setting = "A"

        if biomrc_version.lower() == "small":
            self.biomrc_version = "small"
        elif biomrc_version.lower() == "tiny":
            self.biomrc_version = "tiny"
        else:
            if biomrc_version.lower() != "large":
                logging.warning("Wrong version for BioMRC, using BioMRC Large instead.")
            self.biomrc_version = "large"

        super(BiomrcConfig, self).__init__(**kwargs)


class Biomrc(datasets.GeneratorBasedBuilder):
    """BioMRC Dataset"""

    BUILDER_CONFIG_CLASS = BiomrcConfig

    BUILDER_CONFIGS = [
        BiomrcConfig(
            name="biomrc_large_A",
            version=datasets.Version("1.0.0", ""),
            description="Biomrc Version Large Setting A",
            biomrc_setting="A",
            biomrc_version="large",
        ),
        BiomrcConfig(
            name="biomrc_large_B",
            version=datasets.Version("1.0.0", ""),
            description="Biomrc Version Large Setting B",
            biomrc_setting="B",
            biomrc_version="large",
        ),
        BiomrcConfig(
            name="biomrc_small_A",
            version=datasets.Version("1.0.0", ""),
            description="Biomrc Version Small Setting A",
            biomrc_setting="A",
            biomrc_version="small",
        ),
        BiomrcConfig(
            name="biomrc_small_B",
            version=datasets.Version("1.0.0", ""),
            description="Biomrc Version Small Setting B",
            biomrc_setting="B",
            biomrc_version="small",
        ),
        BiomrcConfig(
            name="biomrc_tiny_A",
            version=datasets.Version("1.0.0", ""),
            description="Biomrc Version Tiny Setting A",
            biomrc_setting="A",
            biomrc_version="tiny",
        ),
        BiomrcConfig(
            name="biomrc_tiny_B",
            version=datasets.Version("1.0.0", ""),
            description="Biomrc Version Tiny Setting B",
            biomrc_setting="B",
            biomrc_version="tiny",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "abstract": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "entities_list": datasets.features.Sequence(datasets.Value("string")),
                    "answer": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="http://datasets.cs.aueb.gr/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        setting = "" if self.config.biomrc_setting == "A" else "_B"
        if self.config.biomrc_version == "large":
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
        elif self.config.biomrc_version == "small":
            urls_to_download = {
                "train": "https://archive.org/download/biomrc_dataset/biomrc_small/dataset_train_small{}.json.gz".format(
                    setting
                ),
                "val": "https://archive.org/download/biomrc_dataset/biomrc_small/dataset_val_small{}.json.gz".format(
                    setting
                ),
                "test": "https://archive.org/download/biomrc_dataset/biomrc_small/dataset_test_small{}.json.gz".format(
                    setting
                ),
            }
        else:
            urls_to_download = {
                "test": "https://archive.org/download/biomrc_dataset/biomrc_tiny/dataset_tiny{}.json.gz".format(
                    setting
                )
            }

        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        if self.config.biomrc_version == "tiny":
            return [
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
            ]
        else:
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["val"]}
                ),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
            ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        # Id for the biomrc dataset
        with open(filepath, encoding="utf-8") as fp:
            biomrc = json.load(fp)
            for _id, (ab, ti, el, an) in enumerate(
                zip(biomrc["abstracts"], biomrc["titles"], biomrc["entities_list"], biomrc["answers"])
            ):
                yield _id, {"abstract": ab, "title": ti, "entities_list": el, "answer": an}
