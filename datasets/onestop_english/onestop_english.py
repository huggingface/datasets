# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""OneStopEnglish Corpus: Dataset of texts classified into reading levels/text complexities."""


import os

import datasets
from datasets.tasks import TextClassification


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{vajjala-lucic-2018-onestopenglish,
    title = {OneStopEnglish corpus: A new corpus for automatic readability assessment and text simplification},
    author = {Sowmya Vajjala and Ivana Lučić},
    booktitle = {Proceedings of the Thirteenth Workshop on Innovative Use of NLP for Building Educational Applications},
    year = {2018}
}
"""

_DESCRIPTION = """\
This dataset is a compilation of the OneStopEnglish corpus of texts written at three reading levels into one file.
Text documents are classified into three reading levels - ele, int, adv (Elementary, Intermediate and Advance).
This dataset demonstrates its usefulness for through two applica-tions - automatic  readability  assessment  and automatic text simplification.
The corpus consists of 189 texts, each in three versions/reading levels (567 in total).
"""

_HOMEPAGE = "https://github.com/nishkalavallabhi/OneStopEnglishCorpus"

_LICENSE = "Creative Commons Attribution-ShareAlike 4.0 International License"

_URL = "https://github.com/purvimisal/OneStopCorpus-Compiled/raw/main/Texts-SeparatedByReadingLevel.zip"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class OnestopEnglish(datasets.GeneratorBasedBuilder):
    """OneStopEnglish Corpus: Dataset of texts classified into reading levels"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"text": datasets.Value("string"), "label": datasets.features.ClassLabel(names=["ele", "int", "adv"])}
            ),
            supervised_keys=[""],
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _vocab_text_gen(self, train_file):
        for _, ex in self._generate_examples(train_file):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        """Downloads OneStopEnglish corpus"""
        extracted_folder_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"split_key": "train", "data_dir": extracted_folder_path},
            )
        ]

    def _get_examples_from_split(self, split_key, data_dir):
        """Reads the downloaded and extracted files and combines the individual text files to one dataset."""

        data_dir = os.path.join(data_dir, "Texts-SeparatedByReadingLevel")

        ele_samples = []
        dir_path = os.path.join(data_dir, "Ele-Txt")
        files = os.listdir(dir_path)
        for f in sorted(files):
            try:
                with open(os.path.join(dir_path, f), encoding="utf-8-sig") as myfile:
                    text = myfile.read().strip()
                    ele_samples.append(text)
            except Exception as e:
                logger.info("Error with:", os.path.join(dir_path, f), e)

        int_samples = []
        dir_path = os.path.join(data_dir, "Int-Txt")
        files = os.listdir(dir_path)
        for f in sorted(files):
            try:
                with open(os.path.join(dir_path, f), encoding="utf-8-sig") as myfile:
                    text = myfile.read().strip()
                    int_samples.append(text)
            except Exception as e:
                logger.info("Error with:", os.path.join(dir_path, f), e)

        adv_samples = []
        dir_path = os.path.join(data_dir, "Adv-Txt")
        files = os.listdir(dir_path)
        for f in sorted(files):
            try:
                with open(os.path.join(dir_path, f), encoding="utf-8-sig") as myfile:
                    text = myfile.read().strip()
                    adv_samples.append(text)
            except Exception as e:
                logger.info("Error with:", os.path.join(dir_path, f), e)

        train_samples = ele_samples + int_samples + adv_samples
        train_labels = (["ele"] * len(ele_samples)) + (["int"] * len(int_samples)) + (["adv"] * len(adv_samples))

        if split_key == "train":
            return (train_samples, train_labels)
        else:
            raise ValueError(f"Invalid split key {split_key}")

    def _generate_examples(self, split_key, data_dir):
        """Yields examples for a given split of dataset."""
        split_text, split_labels = self._get_examples_from_split(split_key, data_dir)
        for id_, (text, label) in enumerate(zip(split_text, split_labels)):
            feature_dict = {"text": text, "label": label}
            yield id_, feature_dict
