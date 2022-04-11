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

"""News Popularity in Multiple Social Media Platforms Data Set: social sharing data across Facebook, Google+ and LinkedIn for 100k news items on the topics of: economy, microsoft, obama and palestine."""


import csv

import datasets


_CITATION = """\
@article{Moniz2018MultiSourceSF,
  title={Multi-Source Social Feedback of Online News Feeds},
  author={N. Moniz and L. Torgo},
  journal={ArXiv},
  year={2018},
  volume={abs/1801.07055}
}
"""

_DESCRIPTION = """
This is a large data set of news items and their respective social feedback on multiple platforms: Facebook, Google+ and LinkedIn.
The collected data relates to a period of 8 months, between November 2015 and July 2016, accounting for about 100,000 news items on four different topics: economy, microsoft, obama and palestine.
This data set is tailored for evaluative comparisons in predictive analytics tasks, although allowing for tasks in other research areas such as topic detection and tracking, sentiment analysis in short text, first story detection or news recommendation.
"""

_HOMEPAGE = "https://archive.ics.uci.edu/ml/datasets/News+Popularity+in+Multiple+Social+Media+Platforms"

_LICENSE = "Creative Commons Attribution 4.0 International License (CC-BY)"

_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00432/Data/News_Final.csv"


_VERSION = datasets.Version("1.0.0")


class Newspop(datasets.GeneratorBasedBuilder):
    __doc__

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "title": datasets.Value("string"),
                    "headline": datasets.Value("string"),
                    "source": datasets.Value("string"),
                    "topic": datasets.Value("string"),
                    "publish_date": datasets.Value("string"),
                    "facebook": datasets.Value("int32"),
                    "google_plus": datasets.Value("int32"),
                    "linked_in": datasets.Value("int32"),
                }
            ),
            supervised_keys=None,
            version=_VERSION,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_path},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            csv_reader = csv.reader(
                f,
                quotechar='"',
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL,
            )
            next(csv_reader)
            for line_id, row in enumerate(csv_reader):
                (
                    id,
                    title,
                    headline,
                    source,
                    topic,
                    publish_date,
                    _,
                    _,
                    facebook,
                    google_plus,
                    linked_in,
                ) = row
                if "e" in id:
                    # 1 number is written as 1e+05
                    id = int(float(id))
                else:
                    id = int(id)
                facebook = int(facebook)
                google_plus = int(google_plus)
                linked_in = int(linked_in)
                yield (
                    line_id,
                    {
                        "id": id,
                        "title": title,
                        "headline": headline,
                        "source": source,
                        "topic": topic,
                        "publish_date": publish_date,
                        "facebook": facebook,
                        "google_plus": google_plus,
                        "linked_in": linked_in,
                    },
                )
