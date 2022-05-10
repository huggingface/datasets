# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""TR-News dataset."""

import os

import pandas as pd

import datasets
from datasets.tasks import Summarization


_DESCRIPTION = """\
TR-News is mainly a text summarization dataset for Turkish, however it can be used utilized for 
other tasks such as text classification and language modelling. It is constructed 
from three different news sources: NTV, Cumhuriyet, and Habertürk websites. It contains 
a total of 307,562 articles with the article count from each source being, respectively,
222,301, 44,990, and 40,271. The articles’ date varies in the range of 2009-2020. 
The dataset contains articles from a total of 121 various different domains 
(e.g. Domestic, World, Sports, Economy, Health, Life, Art, Technology, Education, Politics)
where some being sub-categories of others. 
"""

_CITATION = """\
@article{10.1007/s10579-021-09568-y, 
    year = {2022}, 
    title = {{Abstractive text summarization and new large-scale datasets for agglutinative languages Turkish and Hungarian}}, 
    author = {Baykara, Batuhan and Güngör, Tunga}, 
    journal = {Language Resources and Evaluation}, 
    issn = {1574-020X}, 
    doi = {10.1007/s10579-021-09568-y},
    pages = {1--35}
}
"""

_URL = "https://drive.google.com/uc?export=download&id=14MESFZp65H3TMvbh8QGoMfXDENdhizn9"


class TRNews(datasets.GeneratorBasedBuilder):
    """TR-News dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "url": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "abstract": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "topic": datasets.Value("string"),
                    "tags": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "source": datasets.Value("string"),
                }
            ),
            homepage="https://github.com/batubayk/news_datasets",
            citation=_CITATION,
            task_templates=[Summarization(text_column="content", summary_column="abstract")],
        )

    def _split_generators(self, dl_manager):
        dl_path = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(dl_path, "train.tsv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(dl_path, "validation.tsv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(dl_path, "test.tsv")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Generate TR-News examples."""
        df = pd.read_csv(filepath, sep="\t")

        for idx, row in df.iterrows():
            yield idx, {
                "url": row["url"],
                "title": row["title"],
                "abstract": row["abstract"],
                "content": row["content"],
                "topic": row["topic"],
                "tags": row["tags"],
                "date": row["date"],
                "author": row["author"],
                "source": row["source"],
            }
