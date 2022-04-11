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

"""arXiv Dataset."""


import json
import os

import datasets


_CITATION = """\
@misc{clement2019arxiv,
    title={On the Use of ArXiv as a Dataset},
    author={Colin B. Clement and Matthew Bierbaum and Kevin P. O'Keeffe and Alexander A. Alemi},
    year={2019},
    eprint={1905.00075},
    archivePrefix={arXiv},
    primaryClass={cs.IR}
}
"""

_DESCRIPTION = """\
A dataset of 1.7 million arXiv articles for applications like trend analysis, paper recommender engines, category prediction, co-citation networks, knowledge graph construction and semantic search interfaces.
"""

_HOMEPAGE = "https://www.kaggle.com/Cornell-University/arxiv"
_LICENSE = "https://creativecommons.org/publicdomain/zero/1.0/"

_ID = "id"
_SUBMITTER = "submitter"
_AUTHORS = "authors"
_TITLE = "title"
_COMMENTS = "comments"
_JOURNAL_REF = "journal-ref"
_DOI = "doi"
_REPORT_NO = "report-no"
_CATEGORIES = "categories"
_LICENSE = "license"
_ABSTRACT = "abstract"
_UPDATE_DATE = "update_date"

_FILENAME = "arxiv-metadata-oai-snapshot.json"


class ArxivDataset(datasets.GeneratorBasedBuilder):
    """arXiv Dataset: arXiv dataset and metadata of 1.7M+ scholarly papers across STEM"""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://www.kaggle.com/Cornell-University/arxiv,
    and manually download the dataset. Once it is completed,
    a zip folder named archive.zip will be appeared in your Downloads folder
    or whichever folder your browser chooses to save files to. Extract that folder
    and you would get a arxiv-metadata-oai-snapshot.json file
    You can then move that file under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    arxiv_dataset can then be loaded using the following command `datasets.load_dataset("arxiv_dataset", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        feature_names = [
            _ID,
            _SUBMITTER,
            _AUTHORS,
            _TITLE,
            _COMMENTS,
            _JOURNAL_REF,
            _DOI,
            _REPORT_NO,
            _CATEGORIES,
            _LICENSE,
            _ABSTRACT,
            _UPDATE_DATE,
        ]
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
                "{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('arxiv_dataset', data_dir=...)` that includes a file name {_FILENAME}. Manual download instructions: {self.manual_download_instructions})"
            )
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"path": path_to_manual_file})]

    def _generate_examples(self, path=None, title_set=None):
        """Yields examples."""
        with open(path, encoding="utf8") as f:
            for i, entry in enumerate(f):
                data = dict(json.loads(entry))
                yield i, {
                    _ID: data["id"],
                    _SUBMITTER: data["submitter"],
                    _AUTHORS: data["authors"],
                    _TITLE: data["title"],
                    _COMMENTS: data["comments"],
                    _JOURNAL_REF: data["journal-ref"],
                    _DOI: data["doi"],
                    _REPORT_NO: data["report-no"],
                    _CATEGORIES: data["categories"],
                    _LICENSE: data["license"],
                    _ABSTRACT: data["abstract"],
                    _UPDATE_DATE: data["update_date"],
                }
