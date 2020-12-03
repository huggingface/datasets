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
"""Recognizing the flow of time in a story is a crucial aspect of understanding it. Prior work related to time has primarily focused on identifying temporal expressions or relative sequencing of events, but here we propose computationally annotating each line of a book with wall clock times, even in the absence of explicit time-descriptive phrases. To do so, we construct a data set of hourly time phrases from 52,183 fictional books."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@misc{kim2020time,
      title={What time is it? Temporal Analysis of Novels},
      author={Allen Kim and Charuta Pethe and Steven Skiena},
      year={2020},
      eprint={2011.04124},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
A clean data resource containing all explicit time references in a dataset of 52,183 novels whose full text is available via Project Gutenberg.
"""

_HOMEPAGE = "https://github.com/allenkim/what-time-is-it"

_LICENSE = "[More Information needed]"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "gutenberg": "https://github.com/TevenLeScao/what-time-is-it/blob/master/gutenberg_time_phrases.zip?raw=true",
}


class GutenbergTime(datasets.GeneratorBasedBuilder):
    """Novel extracts with time-of-the-day information"""

    VERSION = datasets.Version("1.1.3")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="gutenberg", description="Data pulled from the Gutenberg project"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "guten_id": datasets.Value("string"),
                "hour_reference": datasets.Value("string"),
                "time_phrase": datasets.Value("string"),
                "is_ambiguous": datasets.Value("bool_"),
                "time_pos_start": datasets.Value("int64"),
                "time_pos_end": datasets.Value("int64"),
                "tok_context": datasets.Value("string"),
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
        data = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data, "gutenberg_time_phrases.csv"),
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, filepath, split):

        with open(filepath, encoding="utf8") as f:
            data = csv.reader(f)
            next(data)
            for id_, row in enumerate(data):
                yield id_, {
                    "guten_id": row[0],
                    "hour_reference": row[1],
                    "time_phrase": row[2],
                    "is_ambiguous": row[3],
                    "time_pos_start": row[4],
                    "time_pos_end": row[5],
                    "tok_context": row[6],
                }
