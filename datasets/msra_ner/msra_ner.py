# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""Introduction to MSRA NER Dataset"""

import logging

import datasets


_CITATION = """\
@inproceedings{levow2006third,
  author    = {Gina{-}Anne Levow},
  title     = {The Third International Chinese Language Processing Bakeoff: Word
               Segmentation and Named Entity Recognition},
  booktitle = {SIGHAN@COLING/ACL},
  pages     = {108--117},
  publisher = {Association for Computational Linguistics},
  year      = {2006}
}
"""

_DESCRIPTION = """\
The Third International Chinese Language
Processing Bakeoff was held in Spring
2006 to assess the state of the art in two
important tasks: word segmentation and
named entity recognition. Twenty-nine
groups submitted result sets in the two
tasks across two tracks and a total of five
corpora. We found strong results in both
tasks as well as continuing challenges.

MSRA NER is one of the provided dataset.
There are three types of NE, PER (person),
ORG (organization) and LOC (location).
The dataset is in the BIO scheme.

For more details see https://faculty.washington.edu/levow/papers/sighan06.pdf
"""

_URL = "https://raw.githubusercontent.com/OYE93/Chinese-NLP-Corpus/master/NER/MSRA/"
_TRAINING_FILE = "msra_train_bio.txt"
_TEST_FILE = "msra_test_bio.txt"


class MsraNerConfig(datasets.BuilderConfig):
    """BuilderConfig for MsraNer"""

    def __init__(self, **kwargs):
        """BuilderConfig for MSRA NER.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(MsraNerConfig, self).__init__(**kwargs)


class MsraNer(datasets.GeneratorBasedBuilder):
    """MSRA NER dataset."""

    BUILDER_CONFIGS = [
        MsraNerConfig(name="msra_ner", version=datasets.Version("1.0.0"), description="MSRA NER dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-PER",
                                "I-PER",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://www.microsoft.com/en-us/download/details.aspx?id=52531",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                line_stripped = line.strip()
                if line_stripped == "":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    splits = line_stripped.split("\t")
                    if len(splits) == 1:
                        splits.append("O")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1])
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
