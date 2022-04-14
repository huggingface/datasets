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
"""roman_urdu_hate_speech dataset"""


import csv

import datasets
from datasets.tasks import TextClassification


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{rizwan2020hate,
  title={Hate-speech and offensive language detection in roman Urdu},
  author={Rizwan, Hammad and Shakeel, Muhammad Haroon and Karim, Asim},
  booktitle={Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  pages={2512--2522},
  year={2020}
}
"""

# You can copy an official description
_DESCRIPTION = """\
 The Roman Urdu Hate-Speech and Offensive Language Detection (RUHSOLD) dataset is a \
 Roman Urdu dataset of tweets annotated by experts in the relevant language. \
 The authors develop the gold-standard for two sub-tasks. \
 First sub-task is based on binary labels of Hate-Offensive content and Normal content (i.e., inoffensive language). \
 These labels are self-explanatory. \
 The authors refer to this sub-task as coarse-grained classification. \
 Second sub-task defines Hate-Offensive content with \
 four labels at a granular level. \
 These labels are the most relevant for the demographic of users who converse in RU and \
 are defined in related literature. The authors refer to this sub-task as fine-grained classification. \
 The objective behind creating two gold-standards is to enable the researchers to evaluate the hate speech detection \
 approaches on both easier (coarse-grained) and challenging (fine-grained) scenarios. \
"""

_HOMEPAGE = "https://github.com/haroonshakeel/roman_urdu_hate_speech"

_LICENSE = "MIT License"

_Download_URL = "https://raw.githubusercontent.com/haroonshakeel/roman_urdu_hate_speech/main/"

# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {
    "Coarse_Grained_train": _Download_URL + "task_1_train.tsv",
    "Coarse_Grained_validation": _Download_URL + "task_1_validation.tsv",
    "Coarse_Grained_test": _Download_URL + "task_1_test.tsv",
    "Fine_Grained_train": _Download_URL + "task_2_train.tsv",
    "Fine_Grained_validation": _Download_URL + "task_2_validation.tsv",
    "Fine_Grained_test": _Download_URL + "task_2_test.tsv",
}


class RomanUrduHateSpeechConfig(datasets.BuilderConfig):
    """BuilderConfig for RomanUrduHateSpeech Config"""

    def __init__(self, **kwargs):
        """BuilderConfig for RomanUrduHateSpeech Config.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(RomanUrduHateSpeechConfig, self).__init__(**kwargs)


class RomanUrduHateSpeech(datasets.GeneratorBasedBuilder):
    """Roman Urdu Hate Speech dataset"""

    VERSION = datasets.Version("1.1.0")

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
        RomanUrduHateSpeechConfig(
            name="Coarse_Grained",
            version=VERSION,
            description="This part of my dataset covers the Coarse Grained dataset",
        ),
        RomanUrduHateSpeechConfig(
            name="Fine_Grained", version=VERSION, description="This part of my dataset covers the Fine Grained dataset"
        ),
    ]

    DEFAULT_CONFIG_NAME = "Coarse_Grained"
    # It's not mandatory to have a default configuration. Just use one if it makes sense.

    def _info(self):

        if self.config.name == "Coarse_Grained":
            features = datasets.Features(
                {
                    "tweet": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["Abusive/Offensive", "Normal"]),
                    # These are the features of your dataset like images, labels ...
                }
            )
        if self.config.name == "Fine_Grained":
            features = datasets.Features(
                {
                    "tweet": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=["Abusive/Offensive", "Normal", "Religious Hate", "Sexism", "Profane/Untargeted"]
                    ),
                    # These are the features of your dataset like images, labels ...
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
            task_templates=[TextClassification(text_column="tweet", label_column="label")],
        )

    def _split_generators(self, dl_manager):

        urls_train = _URLS[self.config.name + "_train"]

        urls_validate = _URLS[self.config.name + "_validation"]

        urls_test = _URLS[self.config.name + "_test"]

        data_dir_train = dl_manager.download_and_extract(urls_train)

        data_dir_validate = dl_manager.download_and_extract(urls_validate)

        data_dir_test = dl_manager.download_and_extract(urls_test)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir_train,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir_test,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir_validate,
                    "split": "dev",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):

        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(filepath, encoding="utf-8") as tsv_file:
            tsv_reader = csv.reader(tsv_file, quotechar="|", delimiter="\t", quoting=csv.QUOTE_ALL)
            for key, row in enumerate(tsv_reader):
                if key == 0:
                    continue
                if self.config.name == "Coarse_Grained":
                    tweet, label = row
                    label = int(label)
                    yield key, {
                        "tweet": tweet,
                        "label": None if split == "test" else label,
                    }
                if self.config.name == "Fine_Grained":
                    tweet, label = row
                    label = int(label)
                    yield key, {
                        "tweet": tweet,
                        "label": None if split == "test" else label,
                    }
                # Yields examples as (key, example) tuples
