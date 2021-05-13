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

"""Adversarial Examples for SQuAD"""


import json

import datasets


_CITATION = """\
@inproceedings{jia-liang-2017-adversarial,
    title = "Adversarial Examples for Evaluating Reading Comprehension Systems",
    author = "Jia, Robin  and
      Liang, Percy",
    booktitle = "Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D17-1215",
    doi = "10.18653/v1/D17-1215",
    pages = "2021--2031",
    abstract = "Standard accuracy metrics indicate that reading comprehension systems are making rapid progress, but the extent to which these systems truly understand language remains unclear. To reward systems with real language understanding abilities, we propose an adversarial evaluation scheme for the Stanford Question Answering Dataset (SQuAD). Our method tests whether systems can answer questions about paragraphs that contain adversarially inserted sentences, which are automatically generated to distract computer systems without changing the correct answer or misleading humans. In this adversarial setting, the accuracy of sixteen published models drops from an average of 75% F1 score to 36%; when the adversary is allowed to add ungrammatical sequences of words, average accuracy on four models decreases further to 7%. We hope our insights will motivate the development of new models that understand language more precisely.",
}

"""

_DESCRIPTION = """\
Here are two different adversaries, each of which uses a different procedure to pick the sentence it adds to the paragraph:
AddSent: Generates up to five candidate adversarial sentences that don't answer the question, but have a lot of words in common with the question. Picks the one that most confuses the model.
AddOneSent: Similar to AddSent, but just picks one of the candidate sentences at random. This adversary is does not query the model in any way.
"""

_HOMEPAGE = "https://worksheets.codalab.org/worksheets/0xc86d3ebe69a3427d91f9aaa63f7d1e7d/"
_LICENSE = "MIT License"

_URLS = {
    "AddSent": "https://worksheets.codalab.org/rest/bundles/0xb765680b60c64d088f5daccac08b3905/contents/blob/",
    "AddOneSent": "https://worksheets.codalab.org/rest/bundles/0x3ac9349d16ba4e7bb9b5920e3b1af393/contents/blob/",
}


class SquadAdversarial(datasets.GeneratorBasedBuilder):
    """Adversarial SQuAD dataset"""

    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="AddSent", version=VERSION, description=_DESCRIPTION),
        datasets.BuilderConfig(name="AddOneSent", version=VERSION, description=_DESCRIPTION),
    ]

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
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

        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files[self.config.name]}
            )
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
            for example in squad["data"]:
                title = example.get("title", "").strip()
                for paragraph in example["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
