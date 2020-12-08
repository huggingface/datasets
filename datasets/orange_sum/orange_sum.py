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
"""OrangeSum dataset"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@article{eddine2020barthez,
  title={BARThez: a Skilled Pretrained French Sequence-to-Sequence Model},
  author={Eddine, Moussa Kamal and Tixier, Antoine J-P and Vazirgiannis, Michalis},
  journal={arXiv preprint arXiv:2010.12321},
  year={2020}
}
"""

_DESCRIPTION = """\
The OrangeSum dataset was inspired by the XSum dataset. It was created by scraping the "Orange Actu" website: https://actu.orange.fr/. Orange S.A. is a large French multinational telecommunications corporation, with 266M customers worldwide. Scraped pages cover almost a decade from Feb 2011 to Sep 2020. They belong to five main categories: France, world, politics, automotive, and society. The society category is itself divided into 8 subcategories: health, environment, people, culture, media, high-tech, unsual ("insolite" in French), and miscellaneous.

Each article featured a single-sentence title as well as a very brief abstract, both professionally written by the author of the article. These two fields were extracted from each page, thus creating two summarization tasks: OrangeSum Title and OrangeSum Abstract.
"""

_URL_DATA = {
    "abstract": "https://raw.githubusercontent.com/Tixierae/OrangeSum/main/data/docs/splits/abstract.tgz",
    "title": "https://raw.githubusercontent.com/Tixierae/OrangeSum/main/data/docs/splits/title.tgz",
}

_DOCUMENT = "text"
_SUMMARY = "summary"


class OrangeSum(datasets.GeneratorBasedBuilder):
    """OrangeSum: a french abstractive summarization dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="abstract", description="Abstracts used as summaries", version=VERSION),
        datasets.BuilderConfig(name="title", description="Titles used as summaries", version=VERSION),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    _DOCUMENT: datasets.Value("string"),
                    _SUMMARY: datasets.Value("string"),
                }
            ),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage="https://github.com/Tixierae/OrangeSum/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL_DATA[self.config.name])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "valid",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(
            os.path.join(filepath, self.config.name, "{}.source".format(split)), encoding="utf-8"
        ) as f_source, open(
            os.path.join(filepath, self.config.name, "{}.target".format(split)), encoding="utf-8"
        ) as f_target:
            for idx, (document, summary) in enumerate(zip(f_source, f_target)):
                yield idx, {_DOCUMENT: document, _SUMMARY: summary}
