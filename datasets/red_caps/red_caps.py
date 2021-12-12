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
"""RedCaps dataset."""


import json
import os
import re

import datasets

from .red_caps_utils import SUBREDDIT_TO_YEAR, SUBREDDITS, SUBREDDITS_WITH_YEAR


_CITATION = """\
@misc{desai2021redcaps,
      title={RedCaps: web-curated image-text data created by the people, for the people}, 
      author={Karan Desai and Gaurav Kaul and Zubin Aysola and Justin Johnson},
      year={2021},
      eprint={2111.11431},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
"""

_DESCRIPTION = """\
RedCaps is a large-scale dataset of 12M image-text pairs collected from Reddit
"""

_HOMEPAGE = "https://redcaps.xyz/"

_LICENSE = "CC BY 4.0"

_URL = "https://www.dropbox.com/s/cqtdpsl4hewlli1/redcaps_v1.0_annotations.zip?dl=1"


def _config_name_to_subreddits_with_year(config_name):
    if config_name == "all":
        return SUBREDDITS_WITH_YEAR
    elif re.match(".*_\d{4}$", config_name):
        return [config_name]
    else:
        return [f"{config_name}_{year}" for year in SUBREDDIT_TO_YEAR[config_name]]


def _config_name_to_description(config_name):
    if config_name == "all":
        return "Contains data from all the subreddits"
    else:
        if re.match(".*_\d{4}$", config_name):
            subreddit, year = config_name.split("_")
            year_str = "2008 - 2017" if year == "2017" else year
        else:
            subreddit = config_name
            year_str = ", ".join(
                ["2008 - 2017" if year == "2017" else year for year in SUBREDDIT_TO_YEAR[config_name]]
            )
        return f"Contains data from the {subreddit} subreddit posted in {year_str}"


class RedCapsConfig(datasets.BuilderConfig):
    """BuilderConfig for RedCaps."""

    def __init__(self, **kwargs):
        """BuilderConfig for RedCaps.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        kwargs["description"] = _config_name_to_description(kwargs["name"])
        super(RedCapsConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class RedCaps(datasets.GeneratorBasedBuilder):
    """RedCaps dataset."""

    BUILDER_CONFIGS = [
        RedCapsConfig(name="all"),
    ]
    BUILDER_CONFIGS += [RedCapsConfig(name=subreddit) for subreddit in SUBREDDITS]
    BUILDER_CONFIGS += [RedCapsConfig(name=subreddit_with_year) for subreddit_with_year in SUBREDDITS_WITH_YEAR]

    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        features = datasets.Features(
            {
                "image_id": datasets.Value("string"),
                "author": datasets.Value("string"),
                "image_url": datasets.Image(),
                "raw_caption": datasets.Value("string"),
                "caption": datasets.Value("string"),
                "subreddit": datasets.ClassLabel(names=SUBREDDITS),
                "score": datasets.Value("int32"),
                "created_utc": datasets.Value("timestamp[s]"),
                "permalink": datasets.Value("string"),
                "crosspost_parents": datasets.Sequence(datasets.Value("string")),
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
        annotations_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "annotations_dir": annotations_dir,
                    "subreddits": _config_name_to_subreddits_with_year(self.config.name),
                },
            ),
        ]

    def _generate_examples(self, annotations_dir, subreddits):
        annotations_dir = os.path.join(annotations_dir, "annotations")
        idx = 0
        for subreddit in subreddits:
            subreddit_file = os.path.join(annotations_dir, subreddit + ".json")
            with open(subreddit_file, encoding="utf-8") as f:
                data = json.load(f)
                for annot in data["annotations"]:
                    yield idx, {
                        "image_id": annot["image_id"],
                        "author": annot["author"],
                        "image_url": annot["url"],
                        "raw_caption": annot["raw_caption"],
                        "caption": annot["caption"],
                        "subreddit": annot["subreddit"],
                        "score": annot["score"] if "score" in annot else None,
                        "created_utc": annot["created_utc"],
                        "permalink": annot["permalink"],
                        "crosspost_parents": annot["crosspost_parents"]
                        if "crosspost_parents" in annot and annot["crosspost_parents"]
                        else None,
                    }
                    idx += 1
