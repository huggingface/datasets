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

"""Times of India News Headlines Dataset"""


import csv
import os

import datasets


_CITATION = """\
@data{DVN/DPQMQH_2020,
author = {Kulkarni, Rohit},
publisher = {Harvard Dataverse},
title = {{Times of India News Headlines}},
year = {2020},
version = {V1},
doi = {10.7910/DVN/DPQMQH},
url = {https://doi.org/10.7910/DVN/DPQMQH}
}
"""

_DESCRIPTION = """\
This news dataset is a persistent historical archive of noteable events in the Indian subcontinent from start-2001 to mid-2020, recorded in realtime by the journalists of India. It contains approximately 3.3 million events published by Times of India. Times Group as a news agency, reaches out a very wide audience across Asia and drawfs every other agency in the quantity of english articles published per day. Due to the heavy daily volume over multiple years, this data offers a deep insight into Indian society, its priorities, events, issues and talking points and how they have unfolded over time. It is possible to chop this dataset into a smaller piece for a more focused analysis, based on one or more facets.
"""

_PUBLISH_DATE = "publish_date"
_HEADLINE_CATEGORY = "headline_category"
_HEADLINE_TEXT = "headline_text"

_HOMEPAGE = "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/J7BYRX"
_LICENSE = "https://creativecommons.org/publicdomain/zero/1.0/"

_FILENAME = "india-news-headlines.csv"


class TimesOfIndiaNewsHeadlines(datasets.GeneratorBasedBuilder):
    """Times of India News Dataset: a dataset of persistent historical archive of noteable events in the Indian subcontinent from start-2001 to mid-2020, recorded in realtime by the journalists of India."""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/DPQMQH/P2Z4PM and manually download the dataset. Once it is completed, a csv file named india-news-headlines.csv will be appeared in your Downloads folder or whichever folder your browser chooses to save files to. You can then move that file under <path/to/folder>. The <path/to/folder> can e.g. be "~/manual_data". times_of_india_news_headlines can then be loaded using the following command `datasets.load_dataset("times_of_india_news_headlines", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        feature_names = [_PUBLISH_DATE, _HEADLINE_CATEGORY, _HEADLINE_TEXT]
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({k: datasets.Value("string") for k in feature_names}),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path_to_manual_file = os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), _FILENAME)
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('times_of_india_news_headlines', data_dir=...)` that includes a file name {_FILENAME}. Manual download instructions: {self.manual_download_instructions})"
            )
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"path": path_to_manual_file})]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(path, encoding="utf8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", skipinitialspace=True, quoting=csv.QUOTE_ALL
            )
            for id_, row in enumerate(csv_reader):
                publish_date, headline_category, headline_text = row
                yield id_, {
                    _PUBLISH_DATE: str(publish_date),
                    _HEADLINE_CATEGORY: headline_category,
                    _HEADLINE_TEXT: headline_text,
                }
