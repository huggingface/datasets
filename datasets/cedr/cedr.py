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

# Lint as: python3
"""CEDR dataset"""

import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{sboev2021data,
  title={Data-Driven Model for Emotion Detection in Russian Texts},
  author={Sboev, Alexander and Naumov, Aleksandr and Rybka, Roman},
  journal={Procedia Computer Science},
  volume={190},
  pages={637--642},
  year={2021},
  publisher={Elsevier}
}
"""

_LICENSE = """http://www.apache.org/licenses/LICENSE-2.0"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve emotion recognition task for text data in Russian. The Corpus for Emotions Detecting in
Russian-language text sentences of different social sources (CEDR) contains 9410 sentences in Russian labeled for 5 emotion
categories. The data collected from different sources: posts of the LiveJournal social network, texts of the online news
agency Lenta.ru, and Twitter microblog posts. There are two variants of the corpus: main and enriched. The enriched variant
is include tokenization and lemmatization. Dataset with predefined train/test splits.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/sag111/CEDR"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "main": "https://sagteam.ru/cedr/main.zip",
    "enriched": "https://sagteam.ru/cedr/enriched.zip",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Cedr(datasets.GeneratorBasedBuilder):
    """This dataset is designed to solve emotion recognition task for text data in Russian."""

    VERSION = datasets.Version("0.1.1")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="main", version=VERSION, description="This part of CEDR dataset covers a main version"
        ),
        datasets.BuilderConfig(
            name="enriched", version=VERSION, description="This part of CEDR dataset covers a enriched version"
        ),
    ]

    DEFAULT_CONFIG_NAME = "main"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "main":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "labels": datasets.features.Sequence(
                        datasets.ClassLabel(names=["joy", "sadness", "surprise", "fear", "anger"])
                    ),
                    "source": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "labels": datasets.features.Sequence(
                        datasets.ClassLabel(names=["joy", "sadness", "surprise", "fear", "anger"])
                    ),
                    "source": datasets.Value("string"),
                    "sentences": [
                        [
                            {
                                "forma": datasets.Value("string"),
                                "lemma": datasets.Value("string"),
                            }
                        ]
                    ]
                    # These are the features of your dataset like images, labels ...
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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, self.config.name, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, self.config.name, "test.jsonl"), "split": "test"},
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "main":
                    yield id_, {
                        "text": data["text"],
                        "source": data["source"],
                        "labels": data["labels"],
                    }
                else:
                    yield id_, {
                        "text": data["text"],
                        "source": data["source"],
                        "sentences": data["sentences"],
                        "labels": data["labels"],
                    }
