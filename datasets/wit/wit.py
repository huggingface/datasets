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


import pandas as pd

import datasets


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

_URLs = [f"https://storage.googleapis.com/gresearch/wit/wit_v1.train.all-{i:05}-of-00010.tsv.gz" for i in range(0, 10)]

_FEATURES_LIST = [
    ("language", datasets.Value("string")),
    ("page_url", datasets.Value("string")),
    ("image_url", datasets.Value("string")),
    ("page_title", datasets.Value("string")),
    ("section_title", datasets.Value("string")),
    ("hierarchical_section_title", datasets.Value("string")),
    ("caption_reference_description", datasets.Value("string")),
    ("caption_attribution_description", datasets.Value("string")),
    ("caption_alt_text_description", datasets.Value("string")),
    ("mime_type", datasets.Value("string")),
    ("original_height", datasets.Value("int32")),
    ("original_width", datasets.Value("int32")),
    ("is_main_image", datasets.Value("bool")),
    ("attribution_passes_lang_id", datasets.Value("bool")),
    ("page_changed_recently", datasets.Value("bool")),
    ("context_page_description", datasets.Value("string")),
    ("context_section_description", datasets.Value("string")),
]
_FEATURES = datasets.Features(dict(_FEATURES_LIST))


class WIT(datasets.GeneratorBasedBuilder):
    """WIT is a large multimodal multilingual dataset."""

    VERSION = datasets.Version("0.0.1")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=_FEATURES,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        files = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": files,
                },
            ),
        ]

    def _generate_examples(self, files):
        idx = 0
        for file in files:
            with open(file, "r", encoding="utf-8") as fi:
                for line in fi:
                    yield idx, {
                        feature_name: value if value != "" else None
                        for feature_name, value in zip([feature[0] for feature in _FEATURES_LIST], line.split("\t"))
                    }
