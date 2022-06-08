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
                    "document": {
                        "id": datasets.Value("string"),
                        "kind": datasets.Value("string"),
                        "url": datasets.Value("string"),
                        "file_size": datasets.Value("int32"),
                        "word_count": datasets.Value("int32"),
                        "start": datasets.Value("string"),
                        "end": datasets.Value("string"),
                        "summary": {
                            "text": datasets.Value("string"),
                            "tokens": datasets.features.Sequence(datasets.Value("string")),
                            "url": datasets.Value("string"),
                            "title": datasets.Value("string"),
                        },
                        "text": datasets.Value("string"),
                    },
                    "question": {
                        "text": datasets.Value("string"),
                        "tokens": datasets.features.Sequence(datasets.Value("string")),
                    },
                    "answers": [
                        {
                            "text": datasets.Value("string"),
                            "tokens": datasets.features.Sequence(datasets.Value("string")),
                        }
                    ],
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

        if not os.path.exists(manual_dir):
            raise FileNotFoundError(
                f"{manual_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('narrativeqa_manual', data_dir=...)` that includes the stories downloaded from the original repository. Manual download instructions: {self.manual_download_instructions}"
            )

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
        """Yields examples."""

        documents = {}
        with open(data_dir["documents"], encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["set"] != split:
                    continue
                documents[row["document_id"]] = row

        summaries = {}
        with open(data_dir["summaries"], encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["set"] != split:
                    continue
                summaries[row["document_id"]] = row

        onlyfiles = [f for f in listdir(manual_dir) if isfile(join(manual_dir, f))]
        story_texts = {}
        for i in onlyfiles:
            if "content" in i:
                with open(os.path.join(manual_dir, i), "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    story_texts[i.split(".")[0]] = text

        with open(data_dir["qaps"], encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for id_, row in enumerate(reader):
                if row["set"] != split:
                    continue
                document_id = row["document_id"]
                document = documents[document_id]
                summary = summaries[document_id]
                full_text = story_texts[document_id]
                res = {
                    "document": {
                        "id": document["document_id"],
                        "kind": document["kind"],
                        "url": document["story_url"],
                        "file_size": document["story_file_size"],
                        "word_count": document["story_word_count"],
                        "start": document["story_start"],
                        "end": document["story_end"],
                        "summary": {
                            "text": summary["summary"],
                            "tokens": summary["summary_tokenized"].split(),
                            "url": document["wiki_url"],
                            "title": document["wiki_title"],
                        },
                        "text": full_text,
                    },
                    "question": {"text": row["question"], "tokens": row["question_tokenized"].split()},
                    "answers": [
                        {"text": row["answer1"], "tokens": row["answer1_tokenized"].split()},
                        {"text": row["answer2"], "tokens": row["answer2_tokenized"].split()},
                    ],
                }
                yield id_, res
