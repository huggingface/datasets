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
"""Wikipedia-based Image Text (WIT) Dataset is a large multimodal multilingual dataset"""


import os

import datasets
import pandas as pd


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """
@article{srinivasan2021wit,
  title={WIT: Wikipedia-based Image Text Dataset for Multimodal Multilingual Machine Learning},
  author={Srinivasan, Krishna and Raman, Karthik and Chen, Jiecao and Bendersky, Michael and Najork, Marc},
  journal={arXiv preprint arXiv:2103.01913},
  year={2021}
}
"""

# You can copy an official description
_DESCRIPTION = """
Wikipedia-based Image Text (WIT) Dataset is a large multimodal multilingual dataset.
WIT is composed of a curated set of 37.6 million entity rich image-text examples with 11.5 million unique images across 108 Wikipedia languages.
Its size enables WIT to be used as a pretraining dataset for multimodal machine learning models.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/wit"

_LICENSE = "Data is available under the Creative Commons Attribution-ShareAlike 3.0 Unported license."

N_FILES = 10

_URLs = [
    f"https://storage.googleapis.com/gresearch/wit/wit_v1.train.all-{i:05}-of-00010.tsv.gz" for i in range(0, N_FILES)
]

_FEATURES = datasets.Features(
    {
        "language": datasets.Value("string"),
        "page_url": datasets.Value("string"),
        "image_url": datasets.Value("string"),
        "page_title": datasets.Value("string"),
        "section_title": datasets.Value("string"),
        "hierarchical_section_title": datasets.Value("string"),
        "caption_reference_description": datasets.Value("string"),
        "caption_attribution_description": datasets.Value("string"),
        "caption_alt_text_description": datasets.Value("string"),
        "mime_type": datasets.Value("string"),
        "original_height": datasets.Value("string"),
        "original_width": datasets.Value("string"),
        "is_main_image": datasets.Value("string"),
        "attribution_passes_lang_id": datasets.Value("string"),
        "page_changed_recently": datasets.Value("string"),
        "context_page_description": datasets.Value("string"),
        "context_section_description": datasets.Value("string"),
    }
)


class WIT(datasets.GeneratorBasedBuilder):
    """WIT is a large multimodal multilingual dataset."""

    VERSION = datasets.Version("0.0.1")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=_FEATURES,  # Here we define them above because they are different between the two configurations
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
        URLs = dl_manager.download(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "data": URLs,
                },
            ),
        ]

    def _generate_examples(
        self, data  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        id_ = -1
        for chunk in data:
            df = pd.read_csv(chunk, compression="gzip", sep="\t")
            column_names = list(df.columns)

            for _, row in df.iterrows():
                id_ += 1

                yield id_, {k: row[k] for k in column_names}
