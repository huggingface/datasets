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
"""German Common Crawl"""

from __future__ import absolute_import, division, print_function

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{wenzek2020ccnet,
  title={CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data},
  author={Wenzek, Guillaume and Lachaux, Marie-Anne and Conneau, Alexis and Chaudhary, Vishrav and Guzm{\'a}n, Francisco and Joulin, Armand and Grave, {\'E}douard},
  booktitle={Proceedings of The 12th Language Resources and Evaluation Conference},
  pages={4003--4012},
  year={2020}
}
"""

_DESCRIPTION = """\
German Extract from Common Crawl (High Quality only)
This Dataset is for pretraining a German Language Model (Unsupervised) or tune a Multilingual Model specifically to German"""


_URL = [
    "https://s3.amazonaws.com/datasets.huggingface.co/datasets/datasets/german-nlp-group/german_common_crawl/de_head_0000_2015-48.tar.gz",
    "https://s3.amazonaws.com/datasets.huggingface.co/datasets/datasets/german-nlp-group/german_common_crawl/de_head_0000_2016-18.tar.gz",
]


class GermanCommonCrawl(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="data_only", version=VERSION, description="Only the website text without metadata"
        ),
        datasets.BuilderConfig(
            name="first_part",
            version=VERSION,
            description="Download only one part (2 GB) instead of everythong (200 GB)",
        ),
        datasets.BuilderConfig(name="metadata", version=VERSION, description="Metadata and raw text"),
    ]

    DEFAULT_CONFIG_NAME = "metadata"

    def _info(self):
        if self.config.name == "data_only":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "raw_content": datasets.Value("string"),
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "url": datasets.Value("string"),
                    "date_download": datasets.Value("string"),
                    "digest": datasets.Value("string"),
                    "length": datasets.Value("int32"),
                    "nlines": datasets.Value("int32"),
                    "source_domain": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "raw_content": datasets.Value("string"),
                    "cc_segment": datasets.Value("string"),
                    "original_nlines": datasets.Value("int32"),
                    "original_length": datasets.Value("int32"),
                    "language": datasets.Value("string"),
                    "language_score": datasets.Value("int32"),
                    "perplexity": datasets.Value("int32"),
                    "bucket": datasets.Value("string"),
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
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        if self.config.name == "first_part":
            files = [dl_manager.download_and_extract(_URL[0])]

        else:
            files = []
            for URL in _URL:
                files.append(dl_manager.download_and_extract(URL))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "files": files,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, files, split):
        """ Yields examples. """

        for filepath in files:
            with open(filepath, "r", encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    try:
                        data = eval(row)
                    except ValueError:
                        data = eval(row.replace(chr(0), ""))
                    except SyntaxError:
                        None

                    if self.config.name == "data_only":
                        yield id_, {
                            "raw_content": data["raw_content"],
                        }
                    else:
                        yield id_, data
