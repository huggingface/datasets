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
"""\
This dataset gathers 728,321 biographies from Wikipedia. It aims at evaluating text generation
algorithms. For each article, we provide the first paragraph and the infobox.
"""


import os

import datasets


_CITATION = """\
@article{DBLP:journals/corr/LebretGA16,
  author    = {R{\'{e}}mi Lebret and
               David Grangier and
               Michael Auli},
  title     = {Generating Text from Structured Data with Application to the Biography
               Domain},
  journal   = {CoRR},
  volume    = {abs/1603.07771},
  year      = {2016},
  url       = {http://arxiv.org/abs/1603.07771},
  archivePrefix = {arXiv},
  eprint    = {1603.07771},
  timestamp = {Mon, 13 Aug 2018 16:48:30 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/LebretGA16.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
This dataset gathers 728,321 biographies from wikipedia. It aims at evaluating text generation
algorithms. For each article, we provide the first paragraph and the infobox (both tokenized).
For each article, we extracted the first paragraph (text), the infobox (structured data). Each
infobox is encoded as a list of (field name, field value) pairs. We used Stanford CoreNLP
(http://stanfordnlp.github.io/CoreNLP/) to preprocess the data, i.e. we broke the text into
sentences and tokenized both the text and the field values. The dataset was randomly split in
three subsets train (80%), valid (10%), test (10%).
"""

_HOMEPAGE = "https://github.com/DavidGrangier/wikipedia-biography-dataset"

_LICENSE = "CC BY-SA 3.0"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://drive.google.com/uc?export=download&id=1L7aoUXzHPzyzQ0ns4ApBbYepsjFOtXil"


def _get_table(infobox_line):
    """Converts the infobox into a one row table."""
    cells = infobox_line.split("\t")
    # remove empty cells
    cells = list(filter(lambda x: x.find("<none>") == -1, cells))
    columns = set([cell[0 : cell.split(":")[0].rfind("_")] for cell in cells])
    table = {col: dict() for col in columns}
    for cell in cells:
        delimiter_position_value = cell.find(":")
        column_index = cell[0:delimiter_position_value]
        value = cell[delimiter_position_value + 1 :]
        delimiter_column_index = column_index.rfind("_")
        column = column_index[0:delimiter_column_index]
        index = column_index[delimiter_column_index + 1 :]
        table[column][index] = value
    infobox_line_as_table = []
    for column in table.keys():
        row_value = " ".join([table[column][index] for index in sorted(table[column].keys())])
        infobox_line_as_table.append(
            {
                "column_header": column,
                "row_number": 1,
                "content": row_value,
            }
        )
    return infobox_line_as_table


class WikiBio(datasets.GeneratorBasedBuilder):
    """Infoboxes and first paragraph from Wikipedia biography pages."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "input_text": {
                    "table": datasets.Sequence(
                        {
                            "column_header": datasets.Value("string"),
                            "row_number": datasets.Value("int16"),
                            "content": datasets.Value("string"),
                        }
                    ),
                    "context": datasets.Value("string"),
                },
                "target_text": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=("input_text", "target_text"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)
        data_path = os.path.join(data_dir, "wikipedia-biography-dataset")
        return [
            datasets.SplitGenerator(
                name=datasets.Split("train"),
                gen_kwargs={
                    "id_file": os.path.join(data_path, "train", "train.id"),
                    "infobox_file": os.path.join(data_path, "train", "train.box"),
                    "nb_lines_file": os.path.join(data_path, "train", "train.nb"),
                    "sentences_file": os.path.join(data_path, "train", "train.sent"),
                    "article_title_file": os.path.join(data_path, "train", "train.title"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("test"),
                gen_kwargs={
                    "id_file": os.path.join(data_path, "test", "test.id"),
                    "infobox_file": os.path.join(data_path, "test", "test.box"),
                    "nb_lines_file": os.path.join(data_path, "test", "test.nb"),
                    "sentences_file": os.path.join(data_path, "test", "test.sent"),
                    "article_title_file": os.path.join(data_path, "test", "test.title"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split("val"),
                gen_kwargs={
                    "id_file": os.path.join(data_path, "valid", "valid.id"),
                    "infobox_file": os.path.join(data_path, "valid", "valid.box"),
                    "nb_lines_file": os.path.join(data_path, "valid", "valid.nb"),
                    "sentences_file": os.path.join(data_path, "valid", "valid.sent"),
                    "article_title_file": os.path.join(data_path, "valid", "valid.title"),
                },
            ),
        ]

    def _generate_examples(self, id_file, infobox_file, nb_lines_file, sentences_file, article_title_file):
        """Yields examples."""
        with open(id_file, "r", encoding="utf-8") as id_src, open(
            infobox_file, "r", encoding="utf-8"
        ) as infobox_src, open(nb_lines_file, "r", encoding="utf-8") as nb_lines_src, open(
            sentences_file, "r", encoding="utf-8"
        ) as sentences_src, open(
            article_title_file, "r", encoding="utf-8"
        ) as article_title_src:
            for id_, infobox, nb_lines, article_title in zip(id_src, infobox_src, nb_lines_src, article_title_src):
                target_text = []
                for _ in range(int(nb_lines)):
                    target_text.append(sentences_src.readline())
                yield id_, {
                    "input_text": {"table": _get_table(infobox), "context": article_title},
                    "target_text": "".join(target_text),
                }
