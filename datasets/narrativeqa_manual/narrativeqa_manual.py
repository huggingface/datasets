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
"""NarrativeQA Reading Comprehension Challenge"""

from __future__ import absolute_import, division, print_function

import csv
import os
from os import listdir
from os.path import isfile, join

import datasets


_CITATION = """\
@article{kovcisky2018narrativeqa,
  title={The narrativeqa reading comprehension challenge},
  author={Ko{\v{c}}isk{\'y}, Tom{\'a}{\v{s}} and Schwarz, Jonathan and Blunsom, Phil and Dyer, Chris and Hermann, Karl Moritz and Melis, G{\'a}bor and Grefenstette, Edward},
  journal={Transactions of the Association for Computational Linguistics},
  volume={6},
  pages={317--328},
  year={2018},
  publisher={MIT Press}
}
"""


_DESCRIPTION = """\
The Narrative QA Manual dataset is a reading comprehension \
dataset, in which the reader must answer questions about stories \
by reading entire books or movie scripts. \
The QA tasks are designed so that successfully answering their questions \
requires understanding the underlying narrative rather than \
relying on shallow pattern matching or salience.\\
THIS DATASET REQUIRES A MANUALLY DOWNLOADED FILE! \
Because of a script in the original repository which downloads the stories from original URLs everytime, \
The links are sometimes broken or invalid.  \
Therefore, you need to manually download the stories for this dataset using the script provided by the authors \
(https://github.com/deepmind/narrativeqa/blob/master/download_stories.sh). Running the shell script creates a folder named "tmp" \
in the root directory and downloads the stories there. This folder containing the stories\
can be used to load the dataset via `datasets.load_dataset("narrativeqa_manual", data_dir="<path/to/folder>")`.                """


_HOMEPAGE = "https://deepmind.com/research/publications/narrativeqa-reading-comprehension-challenge"
_LICENSE = "https://github.com/deepmind/narrativeqa/blob/master/LICENSE"


# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://github.com/deepmind/narrativeqa"
_URLS = {
    "documents": "https://raw.githubusercontent.com/deepmind/narrativeqa/master/documents.csv",
    "summaries": "https://raw.githubusercontent.com/deepmind/narrativeqa/master/third_party/wikipedia/summaries.csv",
    "qaps": "https://raw.githubusercontent.com/deepmind/narrativeqa/master/qaps.csv",
}


class NarrativeqaManual(datasets.GeneratorBasedBuilder):
    """The NarrativeQA Manual dataset"""

    VERSION = datasets.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """ You need to manually download the stories for this dataset using the script provided by the authors \
                (https://github.com/deepmind/narrativeqa/blob/master/download_stories.sh). Running the shell script creates a folder named "tmp"\
                in the root directory and downloads the stories there. This folder containing the stories\
                can be used to load the dataset via `datasets.load_dataset("narrativeqa_manual", data_dir="<path/to/folder>")."""

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "kind": datasets.Value("string"),
                    "story_url": datasets.Value("string"),
                    "story_file_size": datasets.Value("string"),
                    "wiki_url": datasets.Value("string"),
                    "wiki_title": datasets.Value("string"),
                    "story_word_count": datasets.Value("string"),
                    "story_start": datasets.Value("string"),
                    "story_end": datasets.Value("string"),
                    "story_text": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "summary_tokenized": datasets.Value("string"),
                    "qaps": datasets.features.Sequence(
                        {
                            "question": datasets.Value("string"),
                            "answer1": datasets.Value("string"),
                            "answer2": datasets.Value("string"),
                            "question_tokenized": datasets.Value("string"),
                            "answer1_tokenized": datasets.Value("string"),
                            "answer2_tokenized": datasets.Value("string"),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLS)
        manual_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": data_dir,
                    "manual_dir": manual_dir,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_dir": data_dir,
                    "manual_dir": manual_dir,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_dir": data_dir,
                    "manual_dir": manual_dir,
                    "split": "valid",
                },
            ),
        ]

    def _generate_examples(self, data_dir, manual_dir, split):
        """ Yields examples. """

        documents = data_dir["documents"]
        summaries = data_dir["summaries"]
        qaps = data_dir["qaps"]
        data_dict = {}

        with open(documents, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            _ = next(csv_reader)
            for id_, row in enumerate(csv_reader):
                if row:
                    if row[1] != split:
                        continue
                    else:
                        data_dict[row[0]] = {
                            "document_id": row[0],
                            "kind": row[2],
                            "story_url": row[3],
                            "story_file_size": row[4],
                            "wiki_url": row[5],
                            "wiki_title": row[6],
                            "story_word_count": row[7],
                            "story_start": row[8],
                            "story_end": row[9],
                            "question-answers": [],
                        }

        onlyfiles = [f for f in listdir(manual_dir) if isfile(join(manual_dir, f))]

        story_texts = {}
        for i in onlyfiles:
            if "content" in i:
                with open(os.path.join(manual_dir, i), "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    story_texts[i.split(".")[0]] = text

        if not os.path.exists(manual_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('narrativeqa_manual', data_dir=...)` that includes the stories downloaded from the original repository. Manual download instructions: {}".format(
                    manual_dir, self.manual_download_instructions
                )
            )

        with open(summaries, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            _ = next(csv_reader)

            for id_, row in enumerate(csv_reader):
                if row:
                    if row[1] != split:
                        continue
                    else:
                        data_dict[row[0]]["summary"] = row[2]
                        data_dict[row[0]]["summary_tokenized"] = row[3]
                        data_dict[row[0]]["story_text"] = str(story_texts.get(row[0], ""))

        with open(qaps, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            _ = next(csv_reader)
            for id_, row in enumerate(csv_reader):
                if row:
                    if row[1] != split:
                        continue
                    else:
                        data_dict[row[0]]["question-answers"].append(
                            {
                                "question": row[2],
                                "answer1": row[3],
                                "answer2": row[4],
                                "question_tokenized": row[5],
                                "answer1_tokenized": row[6],
                                "answer2_tokenized": row[7],
                            }
                        )

        for keys in data_dict:
            yield keys, {
                "id": data_dict[keys]["document_id"],
                "kind": data_dict[keys]["kind"],
                "story_url": data_dict[keys]["story_url"],
                "story_file_size": data_dict[keys]["story_file_size"],
                "wiki_url": data_dict[keys]["wiki_url"],
                "wiki_title": data_dict[keys]["wiki_title"],
                "story_word_count": data_dict[keys]["story_word_count"],
                "story_start": data_dict[keys]["story_start"],
                "story_end": data_dict[keys]["story_end"],
                "qaps": data_dict[keys]["question-answers"],
                "story_text": data_dict[keys]["story_text"],
                "summary": data_dict[keys]["summary"],
                "summary_tokenized": data_dict[keys]["summary_tokenized"],
            }
