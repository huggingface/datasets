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
"""Hatexplain: A Benchmark Dataset for Explainable Hate Speech Detection"""


import json

import datasets


_CITATION = """\
@misc{mathew2020hatexplain,
      title={HateXplain: A Benchmark Dataset for Explainable Hate Speech Detection},
      author={Binny Mathew and Punyajoy Saha and Seid Muhie Yimam and Chris Biemann and Pawan Goyal and Animesh Mukherjee},
      year={2020},
      eprint={2012.10289},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

# You can copy an official description
_DESCRIPTION = """\
Hatexplain is the first benchmark hate speech dataset covering multiple aspects of the issue. \
Each post in the dataset is annotated from three different perspectives: the basic, commonly used 3-class classification \
(i.e., hate, offensive or normal), the target community (i.e., the community that has been the victim of \
hate speech/offensive speech in the post), and the rationales, i.e., the portions of the post on which their labelling \
decision (as hate, offensive or normal) is based.
"""

_HOMEPAGE = ""

_LICENSE = "cc-by-4.0"

_URL = "https://raw.githubusercontent.com/punyajoy/HateXplain/master/Data/"
_URLS = {
    "dataset": _URL + "dataset.json",
    "post_id_divisions": _URL + "post_id_divisions.json",
}


class HatexplainConfig(datasets.BuilderConfig):
    """BuilderConfig for Hatexplain."""

    def __init__(self, **kwargs):
        """BuilderConfig for Hatexplain.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(HatexplainConfig, self).__init__(**kwargs)


class Hatexplain(datasets.GeneratorBasedBuilder):
    """Hatexplain: A Benchmark Dataset for Explainable Hate Speech Detection"""

    BUILDER_CONFIGS = [
        HatexplainConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "annotators": datasets.features.Sequence(
                        {
                            "label": datasets.ClassLabel(names=["hatespeech", "normal", "offensive"]),
                            "annotator_id": datasets.Value("int32"),
                            "target": datasets.Sequence(datasets.Value("string")),
                        }
                    ),
                    "rationales": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("int32"))),
                    "post_tokens": datasets.features.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage="",
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        downloaded_files = dl_manager.download_and_extract(_URLS)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files, "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files, "split": "val"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files, "split": "test"}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """This function returns the examples depending on split"""

        with open(filepath["post_id_divisions"], encoding="utf-8") as f:
            post_id_divisions = json.load(f)
        with open(filepath["dataset"], encoding="utf-8") as f:
            dataset = json.load(f)

        for id_, tweet_id in enumerate(post_id_divisions[split]):
            info = dataset[tweet_id]
            annotators, rationales, post_tokens = info["annotators"], info["rationales"], info["post_tokens"]

            yield id_, {"id": tweet_id, "annotators": annotators, "rationales": rationales, "post_tokens": post_tokens}
