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

import json

import datasets


logger = datasets.logging.get_logger(__name__)

# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{dumitrescu2019introducing,
  title={Introducing RONEC--the Romanian Named Entity Corpus},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei-Marius},
  journal={arXiv preprint arXiv:1909.01247},
  year={2019}
}
"""

# You can copy an official description
_DESCRIPTION = """\
RONEC - the Romanian Named Entity Corpus, at version 2.0, holds 12330 sentences with over 0.5M tokens, annotated with 15 classes, to a total of 80.283 distinctly annotated entities. It is used for named entity recognition and represents the largest Romanian NER corpus to date.
"""

_HOMEPAGE = "https://github.com/dumitrescustefan/ronec"

_LICENSE = "MIT License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/dumitrescustefan/ronec/master/data/"
_TRAINING_FILE = "train.json"
_DEV_FILE = "valid.json"
_TEST_FILE = "test.json"


class RONECConfig(datasets.BuilderConfig):
    """BuilderConfig for RONEC dataset"""

    def __init__(self, **kwargs):
        super(RONECConfig, self).__init__(**kwargs)


class RONEC(datasets.GeneratorBasedBuilder):
    """RONEC dataset"""

    VERSION = datasets.Version("2.0.0")
    BUILDER_CONFIGS = [
        RONECConfig(name="ronec", version=VERSION, description="RONEC dataset"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_ids": datasets.Sequence(datasets.Value("int32")),
                "space_after": datasets.Sequence(datasets.Value("bool")),
                "ner_tags": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "B-PERSON",
                            "I-PERSON",
                            "B-ORG",
                            "I-ORG",
                            "B-GPE",
                            "I-GPE",
                            "B-LOC",
                            "I-LOC",
                            "B-NAT_REL_POL",
                            "I-NAT_REL_POL",
                            "B-EVENT",
                            "I-EVENT",
                            "B-LANGUAGE",
                            "I-LANGUAGE",
                            "B-WORK_OF_ART",
                            "I-WORK_OF_ART",
                            "B-DATETIME",
                            "I-DATETIME",
                            "B-PERIOD",
                            "I-PERIOD",
                            "B-MONEY",
                            "I-MONEY",
                            "B-QUANTITY",
                            "I-QUANTITY",
                            "B-NUMERIC",
                            "I-NUMERIC",
                            "B-ORDINAL",
                            "I-ORDINAL",
                            "B-FACILITY",
                            "I-FACILITY",
                        ]
                    )
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        urls_to_download = {"train": _URL + _TRAINING_FILE, "dev": _URL + _DEV_FILE, "test": _URL + _TEST_FILE}

        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["dev"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["test"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for instance in data:
                yield instance["id"], instance
