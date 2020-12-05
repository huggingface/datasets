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
"""C3 Parallel Corpora"""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
@article{sun2019investigating,
  title={Investigating Prior Knowledge for Challenging Chinese Machine Reading Comprehension},
  author={Sun, Kai and Yu, Dian and Yu, Dong and Cardie, Claire},
  journal={Transactions of the Association for Computational Linguistics},
  year={2020},
  url={https://arxiv.org/abs/1904.09679v3}
}
"""

_DESCRIPTION = """\
Machine reading comprehension tasks require a machine reader to answer questions relevant to the given document. In this paper, we present the first free-form multiple-Choice Chinese machine reading Comprehension dataset (C^3), containing 13,369 documents (dialogues or more formally written mixed-genre texts) and their associated 19,577 multiple-choice free-form questions collected from Chinese-as-a-second-language examinations.
We present a comprehensive analysis of the prior knowledge (i.e., linguistic, domain-specific, and general world knowledge) needed for these real-world problems. We implement rule-based and popular neural methods and find that there is still a significant performance gap between the best performing model (68.5%) and human readers (96.0%), especially on problems that require prior knowledge. We further study the effects of distractor plausibility and data augmentation based on translated relevant datasets for English on model performance. We expect C^3 to present great challenges to existing systems as answering 86.8% of questions requires both knowledge within and beyond the accompanying document, and we hope that C^3 can serve as a platform to study how to leverage various kinds of prior knowledge to better understand a given written or orally oriented text.
"""

_URL = "https://raw.githubusercontent.com/nlpdata/c3/master/data/"


class C3Config(datasets.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self, type_, **kwargs):
        """

        Args:
            pair: the language pair to consider
            zip_file: The location of zip file containing original data
            **kwargs: keyword arguments forwarded to super.
        """
        self.type_ = type_
        super().__init__(**kwargs)


class C3(datasets.GeneratorBasedBuilder):
    """C3 is the first free-form multiple-Choice Chinese machine reading Comprehension dataset, containing 13,369 documents (dialogues or more formally written mixed-genre texts) and their associated 19,577 multiple-choice free-form questions collected from Chinese-as-a-second language examinations."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIG_CLASS = C3Config
    BUILDER_CONFIGS = [
        C3Config(
            name="mixed",
            description="Mixed genre questions",
            version=datasets.Version("1.0.0"),
            type_="mixed",
        ),
        C3Config(
            name="dialog",
            description="Dialog questions",
            version=datasets.Version("1.0.0"),
            type_="dialog",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "documents": datasets.Sequence(datasets.Value("string")),
                    "document_id": datasets.Value("string"),
                    "questions": datasets.Sequence(
                        {
                            "question": datasets.Value("string"),
                            "answer": datasets.Value("string"),
                            "choice": datasets.Sequence(datasets.Value("string")),
                        }
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/nlpdata/c3",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # m or d
        T = self.config.type_[0]
        files = [_URL + f"c3-{T}-{split}.json" for split in ["train", "test", "dev"]]
        dl_dir = dl_manager.download_and_extract(files)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filename": dl_dir[0],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filename": dl_dir[1],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filename": dl_dir[2],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filename, split):
        """ Yields examples. """
        with open(filename, "r", encoding="utf-8") as sf:
            data = json.load(sf)
            for id_, (documents, questions, document_id) in enumerate(data):
                yield id_, {
                    "documents": documents,
                    "questions": questions,
                    "document_id": document_id,
                }
