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
"""The BookCorpus dataset."""


import datasets


_DESCRIPTION = """\
Twi Text C3 is the largest Twi texts collected and used to train FastText embeddings in the
YorubaTwi Embedding paper: https://www.aclweb.org/anthology/2020.lrec-1.335/
"""

_CITATION = """\
@inproceedings{alabi-etal-2020-massive,
    title = "Massive vs. Curated Embeddings for Low-Resourced Languages: the Case of Yoruba and {T}wi",
    author = "Alabi, Jesujoba  and
      Amponsah-Kaakyire, Kwabena  and
      Adelani, David  and
      Espa{\\~n}a-Bonet, Cristina",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.335",
    pages = "2754--2762",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
"""

URL = "https://drive.google.com/uc?export=download&id=1s8NSFT4Kz0caKZ4VybPNzt88F8ZanprY"


class TwiTextC3Config(datasets.BuilderConfig):
    """BuilderConfig for Twi Text C3."""

    def __init__(self, **kwargs):
        """BuilderConfig for BookCorpus.
        Args:
        **kwargs: keyword arguments forwarded to super.
        """
        super(TwiTextC3Config, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class TwiTextC3(datasets.GeneratorBasedBuilder):
    """Twi Text C3 dataset."""

    BUILDER_CONFIGS = [
        TwiTextC3Config(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/2020.lrec-1.335/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": arch_path}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, mode="r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            for id, line in enumerate(lines):
                yield id, {"text": line.strip()}
