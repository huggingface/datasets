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
"""SentiWS: German-language resource for sentiment analysis, pos-tagging"""


import os

import datasets


_CITATION = """\
@INPROCEEDINGS{remquahey2010,
title = {SentiWS -- a Publicly Available German-language Resource for Sentiment Analysis},
booktitle = {Proceedings of the 7th International Language Resources and Evaluation (LREC'10)},
author = {Remus, R. and Quasthoff, U. and Heyer, G.},
year = {2010}
}
"""

_DESCRIPTION = """\
SentimentWortschatz, or SentiWS for short, is a publicly available German-language resource for sentiment analysis, and pos-tagging. The POS tags are ["NN", "VVINF", "ADJX", "ADV"] -> ["noun", "verb", "adjective", "adverb"], and positive and negative polarity bearing words are weighted within the interval of [-1, 1].
"""

_HOMEPAGE = ""

_LICENSE = "Creative Commons Attribution-Noncommercial-Share Alike 3.0 Unported License"

_URLs = ["https://pcai056.informatik.uni-leipzig.de/downloads/etc/SentiWS/SentiWS_v2.0.zip"]


class SentiWS(datasets.GeneratorBasedBuilder):
    """SentiWS: German-language resource for sentiment analysis, pos-tagging"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="pos-tagging", version=VERSION, description="This covers pos-tagging task"),
        datasets.BuilderConfig(
            name="sentiment-scoring",
            version=VERSION,
            description="This covers the sentiment-scoring in [-1, 1] corresponding to (negative, positive) sentiment",
        ),
    ]

    DEFAULT_CONFIG_NAME = "pos-tagging"

    def _info(self):

        if (
            self.config.name == "pos-tagging"
        ):  # the pos-tags are ["NN", "VVINF", "ADJX", "ADV"] -> ["noun", "verb", "adjective", "adverb"]
            features = datasets.Features(
                {
                    "word": datasets.Value("string"),
                    "pos-tag": datasets.ClassLabel(names=["NN", "VVINF", "ADJX", "ADV"]),
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "word": datasets.Value("string"),
                    "sentiment-score": datasets.Value("float32"),
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
        my_urls = _URLs
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "sourcefiles": [
                        os.path.join(data_dir[0], f)
                        for f in ["SentiWS_v2.0_Positive.txt", "SentiWS_v2.0_Negative.txt"]
                    ],
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, sourcefiles, split):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        for file_idx, filepath in enumerate(sourcefiles):
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    word = row.split("|")[0]
                    if self.config.name == "pos-tagging":
                        tag = row.split("|")[1].split("\t")[0]
                        yield f"{file_idx}_{id_}", {"word": word, "pos-tag": tag}
                    else:
                        sentiscore = row.split("|")[1].split("\t")[1]
                        yield f"{file_idx}_{id_}", {"word": word, "sentiment-score": float(sentiscore)}
