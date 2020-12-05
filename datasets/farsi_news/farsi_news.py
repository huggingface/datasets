# Copyright 2020 the HuggingFace Datasets Authors.
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
"""Farsi News Datasets: Hamshahri and RadioFarda"""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
"""

_DESCRIPTION = """\
Contains Farsi (Persian) datasets for Machine Learning tasks, particularly NLP.
These datasets have been extracted from the RSS feed of two Farsi news agency websites:

- Hamshahri
- RadioFarda
"""

_URL = "https://raw.githubusercontent.com/sci2lab/Farsi-datasets/master/farsi_news/"
_URLS = {
    "hamshahri": _URL + "hamshahri.json",
    "radiofarda": _URL + "radiofarda.json",
}


class FarsiNews(datasets.GeneratorBasedBuilder):
    """Farsi News Datasets: Hamshahri and RadioFarda"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "link": datasets.Value("string"),
                    "tags": datasets.features.Sequence(datasets.Value("string")),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/sci2lab/Farsi-datasets",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = _URLS
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name="hamshahri",
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["hamshahri"], "split": "hamshahri"},
            ),
            datasets.SplitGenerator(
                name="radiofarda",
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["radiofarda"], "split": "radiofarda"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, example in enumerate(data):
                yield id_, example
