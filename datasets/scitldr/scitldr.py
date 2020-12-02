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
"""Dataset for TLDR: Extreme Summarization of Scientific Documents"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_SOURCE = "source"
_TARGET = "target"

_CITATION = """\
@article{cachola2020tldr,
  title={{TLDR}: Extreme Summarization of Scientific Documents},
  author={Isabel Cachola and Kyle Lo and Arman Cohan and Daniel S. Weld},
  journal={arXiv:2004.15011},
  year={2020},
}
"""

_DESCRIPTION = """\
A new multi-target dataset of 5.4K TLDRs over 3.2K papers.
SCITLDR contains both author-written and expert-derived TLDRs,
where the latter are collected using a novel annotation protocol
that produces high-quality summaries while minimizing annotation burden.
"""


_LICENSE = "Apache License 2.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "Abstract": "https://raw.githubusercontent.com/allenai/scitldr/master/SciTLDR-Data/SciTLDR-A/",
    "AIC": "https://raw.githubusercontent.com/allenai/scitldr/master/SciTLDR-Data/SciTLDR-AIC/",
    "FullText": "https://raw.githubusercontent.com/allenai/scitldr/master/SciTLDR-Data/SciTLDR-FullText/",
}

_TRAIN_DATA = "train.jsonl"
_TEST_DATA = "test.jsonl"
_VALID_DATA = "dev.jsonl"


# There are several preprocessing scripts given in the original SciTLDR GitHub repository to preprocess this data.
class Scitldr(datasets.GeneratorBasedBuilder):
    """Dataset for TLDR: Extreme Summarization of Scientific Documents."""

    VERSION = datasets.Version("1.1.0")

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('scitldr', 'Abstract')
    # data = datasets.load_dataset('scitldr', 'AIC')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="Abstract", description="This part contains only abstracts of the paper"),
        datasets.BuilderConfig(
            name="AIC",
            description="This part contains Abstracts, Introduction and Conclusion (AIC) sections of the paper",
        ),
        datasets.BuilderConfig(name="FullText", description="This part contains the full text of the paper"),
    ]

    DEFAULT_CONFIG_NAME = (
        "Abstract"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        if self.config.name == "AIC":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "source": datasets.Sequence(datasets.Value("string")),
                    "source_labels": datasets.Sequence(datasets.ClassLabel(num_classes=2, names=[0, 1])),
                    "rouge_scores": datasets.Sequence(datasets.Value("float32")),
                    "paper_id": datasets.Value("string"),
                    "ic": datasets.Value("bool_"),
                    "target": datasets.features.Sequence(datasets.Value("string"))
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:
            features = datasets.Features(
                {
                    "source": datasets.Sequence(datasets.Value("string")),
                    "source_labels": datasets.Sequence(
                        datasets.ClassLabel(num_classes=2, names=["non-oracle", "oracle"])
                    ),
                    "rouge_scores": datasets.Sequence(datasets.Value("float32")),
                    "paper_id": datasets.Value("string"),
                    "target": datasets.Sequence(datasets.Value("string"))
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
            supervised_keys=(_SOURCE, _TARGET),
            # Homepage of the dataset for documentation
            homepage="https://github.com/allenai/scitldr",
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
        urls = {
            "train": os.path.join(_URLs[self.config.name], _TRAIN_DATA),
            "valid": os.path.join(_URLs[self.config.name], _VALID_DATA),
            "test": os.path.join(_URLs[self.config.name], _TEST_DATA),
        }
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir["train"]), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir["test"]), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir["valid"]), "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "AIC":
                    yield id_, {
                        "source": data["source"],
                        "source_labels": data["source_labels"],
                        "rouge_scores": data["rouge_scores"],
                        "paper_id": data["paper_id"],
                        "ic": True if data["ic"] else False,
                        "target": data["target"],
                    }
                else:
                    yield id_, {
                        "source": data["source"],
                        "source_labels": data["source_labels"],
                        "rouge_scores": data["rouge_scores"],
                        "paper_id": data["paper_id"],
                        "target": data["target"],
                    }
