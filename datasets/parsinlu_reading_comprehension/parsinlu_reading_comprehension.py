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
"""ParsiNLU Persian reading comprehension task"""


import json

import datasets


logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@article{huggingface:dataset,
    title = {ParsiNLU: A Suite of Language Understanding Challenges for Persian},
    authors = {Khashabi, Daniel and Cohan, Arman and Shakeri, Siamak and Hosseini, Pedram and Pezeshkpour, Pouya and Alikhani, Malihe and Aminnaseri, Moin and Bitaab, Marzieh and Brahman, Faeze and Ghazarian, Sarik and others},
    year={2020}
    journal = {arXiv e-prints},
    eprint = {2012.06154},
}
"""

# You can copy an official description
_DESCRIPTION = """\
A Persian reading comprehenion task (generating an answer, given a question and a context paragraph).
The questions are mined using Google auto-complete, their answers and the corresponding evidence documents are manually annotated by native speakers.
"""

_HOMEPAGE = "https://github.com/persiannlp/parsinlu/"

_LICENSE = "CC BY-NC-SA 4.0"

_URL = "https://raw.githubusercontent.com/persiannlp/parsinlu/master/data/reading_comprehension/"
_URLs = {
    "train": _URL + "train.jsonl",
    "dev": _URL + "dev.jsonl",
    "test": _URL + "eval.jsonl",
}


class ParsinluReadingComprehension(datasets.GeneratorBasedBuilder):
    """ParsiNLU Persian reading comprehension task."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="parsinlu-repo", version=VERSION, description="ParsiNLU repository: reading-comprehension"
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "question": datasets.Value("string"),
                "url": datasets.Value("string"),
                "context": datasets.Value("string"),
                "answers": datasets.features.Sequence(
                    {
                        "answer_start": datasets.Value("int32"),
                        "answer_text": datasets.Value("string"),
                    }
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["dev"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        logger.info("generating examples from = %s", filepath)

        def get_answer_index(passage, answer):
            return passage.index(answer) if answer in passage else -1

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                answer = data["answers"]
                if type(answer[0]) == str:
                    answer = [{"answer_start": get_answer_index(data["passage"], x), "answer_text": x} for x in answer]
                else:
                    answer = [{"answer_start": x[0], "answer_text": x[1]} for x in answer]
                yield id_, {
                    "question": data["question"],
                    "url": str(data["url"]),
                    "context": data["passage"],
                    "answers": answer,
                }
