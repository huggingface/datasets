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
"""TODO: Add a description here."""


import os

import datasets


_CITATION = """\
@Misc{johnsonetal2014,
 author = {Johnson, Kyle P. and Patrick Burns and John Stewart and Todd Cook},
 title = {CLTK: The Classical Language Toolkit},
 url = {https://github.com/cltk/cltk},
 year = {2014--2020},
}
"""

_DESCRIPTION = """\
This dataset combines some of the classical Sanskrit texts.
"""

_HOMEPAGE = "https://github.com/parmarsuraj99/hf_datasets/tree/master/sanskrit_classic"

_LICENSE = ""

_URLs = {
    "combined": "https://github.com/parmarsuraj99/hf_datasets/raw/master/sanskrit_classic/combined.zip",
}


class SanskritClassic(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="combined", version=VERSION, description="This is combined version of classical texts"
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "combined.txt"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                yield id_, {
                    "text": row,
                }
