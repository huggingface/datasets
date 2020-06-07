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
"""Toronto BooksCorpus dataset."""

from __future__ import absolute_import, division, print_function

import glob
import os
import re

import requests

from tqdm import tqdm

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

_GDRIVE_FILE_ID = "16KCjV9z_FHm8LgZw05RSuk4EsAWPOP_z"

class BookscorpusConfig(nlp.BuilderConfig):
    """BuilderConfig for BooksCorpus."""

    def __init__(self, **kwargs):
        """BuilderConfig for BooksCorpus.
        Args:
        **kwargs: keyword arguments forwarded to super.
        """
        super(BookscorpusConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )

class Bookscorpus(nlp.GeneratorBasedBuilder):
    """BooksCorpus dataset."""

    BUILDER_CONFIGS = [BookscorpusConfig(name="plain_text", description="Plain text",)]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {"text": nlp.Value("string"),}
            ),
            supervised_keys=None,
            homepage="https://yknzhu.wixsite.com/mbweb",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, archive):
        for _, ex in self._generate_examples(archive):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        downloaded_path_or_paths = dl_manager.download_custom(_GDRIVE_FILE_ID, download_file_from_google_drive)
        arch_path = dl_manager.extract(downloaded_path_or_paths)
        
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"directory": arch_path}),
        ]

    def _generate_examples(self, directory):
        files = [os.path.join(directory, 'books_large_p1.txt'),
                 os.path.join(directory, 'books_large_p2.txt'),]
        _id = 0
        for txt_file in files:
            with open(txt_file, mode="r") as f:
                for line in f:
                    yield _id, {'text': line.strip()}
                    _id += 1

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, leave=False) as bar:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        bar.update(CHUNK_SIZE)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)
