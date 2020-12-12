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
"""XED: A multilingual fine-grained emotion dataset. The dataset consists of humanannotated Finnish (25k) and English sentences (30k)."""

from __future__ import absolute_import, division, print_function

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{ohman2020xed,
  title={XED: A Multilingual Dataset for Sentiment Analysis and Emotion Detection},
  author={{\"O}hman, Emily and P{\"a}mies, Marc and Kajava, Kaisla and Tiedemann, J{\"o}rg},
  booktitle={The 28th International Conference on Computational Linguistics (COLING 2020)},
  year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
A multilingual fine-grained emotion dataset. The dataset consists of humanannotated Finnish (25k) and English sentences (30k). Plutchik’s
core emotions are used to annotate the dataset with the addition of neutral to create a multilabel multiclass
dataset. The dataset is carefully evaluated using language-specific BERT models and SVMs to
show that XED performs on par with other similar datasets and is therefore a useful tool for
sentiment analysis and emotion detection.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "License: Creative Commons Attribution 4.0 International License (CC-BY)"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "en_annotated": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/en-annotated.tsv",
    "fi_annotated": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/fi-annotated.tsv",
    "en_neutral": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/neu_en.txt",
    "fi_neutral": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/neu_fi.txt",
}


class XedEnFi(datasets.GeneratorBasedBuilder):
    """XED: A multilingual fine-grained emotion dataset. The dataset consists of humanannotated Finnish (25k) and English sentences (30k)."""

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
        datasets.BuilderConfig(
            name="en_annotated", version=VERSION, description="English, Covers 8 classes without neutral"
        ),
        datasets.BuilderConfig(name="en_neutral", version=VERSION, description="English, Covers neutral"),
        datasets.BuilderConfig(
            name="fi_annotated", version=VERSION, description="Finnish, Covers 8 classes without neutral"
        ),
        datasets.BuilderConfig(name="fi_neutral", version=VERSION, description="Finnish, Covers neutral"),
    ]

    DEFAULT_CONFIG_NAME = (
        "en_annotated"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "en_annotated" or self.config.name == "fi_annotated":
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "labels": datasets.Sequence(datasets.features.ClassLabel(names=[0, 1, 2, 3, 4, 5, 6, 7]))
                    # the number indicates the emotion in ascending alphabetical order: anger:1, anticipation:2, disgust:3, fear:4, joy:5, #sadness:6, surprise:7, trust:8 in the text. Subtract 1 from proper indexing in ClassLabel.
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {"sentence": datasets.Value("string"), "labels": datasets.features.ClassLabel(names=["neutral"])}
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
        my_urls = _URLs
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir[self.config.name]},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                if self.config.name == "en_neutral":
                    sentence = line[1:].strip()
                    labels = "neutral"
                elif self.config.name == "fi_neutral":
                    sentence = line.split("\t")[1].strip()
                    labels = "neutral"
                else:
                    sentence = line.split("\t")[0]
                    labels = list(map(int, line.split("\t")[1].split(",")))
                    # Original labels are [1, 2, 3, 4, 5, 6, 7, 8] ->
                    #                   [anger, anticipation, disgust, fear, joy, sadness, surprise, trust]
                    # Re-map to [0, 1, 2, 3, 4, 5, 6, 7].
                    labels = [label - 1 for label in labels]

                yield id_, {"sentence": sentence, "labels": labels}
