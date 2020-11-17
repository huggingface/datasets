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
"""The BookCorpus dataset based on Shawn Presser's work https://github.com/soskek/bookcorpus/issues/27 """

from __future__ import absolute_import, division, print_function

import glob
import os
import pathlib

import datasets


_DESCRIPTION = """\
Books are a rich source of both fine-grained information, how a character, \
an object or a scene looks like, as well as high-level semantics, what \
someone is thinking, feeling and how these states evolve through a story.\

This version of bookcorpus has 17868 dataset items (books). Each item contains \
two fields: title and text. The title is the name of the book (just the file name) \
while text contains unprocessed book text. The bookcorpus has been prepared by \
Shawn Presser and is generously hosted by The-Eye. The-Eye is a non-profit, community \
driven platform dedicated to the archiving and long-term preservation of any and \
all data including but by no means limited to... websites, books, games, software, \
video, audio, other digital-obscura and ideas.
"""

_CITATION = """\
@InProceedings{Zhu_2015_ICCV,
    title = {Aligning Books and Movies: Towards Story-Like Visual Explanations by Watching Movies and Reading Books},
    author = {Zhu, Yukun and Kiros, Ryan and Zemel, Rich and Salakhutdinov, Ruslan and Urtasun, Raquel and Torralba, Antonio and Fidler, Sanja},
    booktitle = {The IEEE International Conference on Computer Vision (ICCV)},
    month = {December},
    year = {2015}
}
"""
_PROJECT_URL = "https://github.com/soskek/bookcorpus/issues/27"
_DOWNLOAD_URL = "https://the-eye.eu/public/AI/pile_preliminary_components/books1.tar.gz"


class BookCorpusOpenConfig(datasets.BuilderConfig):
    """BuilderConfig for BookCorpus."""

    def __init__(self, **kwargs):
        """BuilderConfig for BookCorpus.
        Args:
        **kwargs: keyword arguments forwarded to super.
        """
        super(BookCorpusOpenConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class BookCorpusOpen(datasets.GeneratorBasedBuilder):
    """BookCorpus dataset."""

    BUILDER_CONFIGS = [
        BookCorpusOpenConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_PROJECT_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"directory": arch_path}),
        ]

    def _generate_examples(self, directory):
        glob_target = os.path.join(directory, "**/*.epub.txt")
        book_files = glob.glob(glob_target, recursive=True)
        book_files = sorted(book_files)
        _id = 0
        for book_file_path in book_files:
            path = pathlib.PurePath(book_file_path)
            with open(book_file_path, mode="r", encoding="utf-8") as f:
                yield _id, {"title": str(path.name), "text": f.read()},
                _id += 1
