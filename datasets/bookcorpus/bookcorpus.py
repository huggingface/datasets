# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""The BookCorpus dataset."""

from __future__ import absolute_import, division, print_function

import glob
import os
import re

import nlp


_DESCRIPTION = """\
Books are a rich source of both fine-grained information, how a character, \
an object or a scene looks like, as well as high-level semantics, what \
someone is thinking, feeling and how these states evolve through a story.\
This work aims to align books to their movie releases in order to provide\
rich descriptive explanations for visual content that go semantically far\
beyond the captions available in current datasets. \
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

URL = "https://storage.googleapis.com/huggingface-nlp/datasets/bookcorpus/bookcorpus.tar.bz2"


class BookcorpusConfig(nlp.BuilderConfig):
    """BuilderConfig for BookCorpus."""

    def __init__(self, **kwargs):
        """BuilderConfig for BookCorpus.
        Args:
        **kwargs: keyword arguments forwarded to super.
        """
        super(BookcorpusConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )


class Bookcorpus(nlp.GeneratorBasedBuilder):
    """BookCorpus dataset."""

    BUILDER_CONFIGS = [BookcorpusConfig(name="plain_text", description="Plain text",)]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({"text": nlp.Value("string"),}),
            supervised_keys=None,
            homepage="https://yknzhu.wixsite.com/mbweb",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, archive):
        for _, ex in self._generate_examples(archive):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(URL)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"directory": arch_path}),
        ]

    def _generate_examples(self, directory):
        files = [
            os.path.join(directory, "books_large_p1.txt"),
            os.path.join(directory, "books_large_p2.txt"),
        ]
        _id = 0
        for txt_file in files:
            with open(txt_file, mode="r") as f:
                for line in f:
                    yield _id, {"text": line.strip()}
                    _id += 1
