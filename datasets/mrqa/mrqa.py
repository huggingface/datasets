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
"""MRQA 2019 Shared task dataset."""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
@inproceedings{fisch2019mrqa,
    title={{MRQA} 2019 Shared Task: Evaluating Generalization in Reading Comprehension},
    author={Adam Fisch and Alon Talmor and Robin Jia and Minjoon Seo and Eunsol Choi and Danqi Chen},
    booktitle={Proceedings of 2nd Machine Reading for Reading Comprehension (MRQA) Workshop at EMNLP},
    year={2019},
}
"""

_DESCRIPTION = """\
The MRQA 2019 Shared Task focuses on generalization in question answering.
An effective question answering system should do more than merely
interpolate from the training set to answer test examples drawn
from the same distribution: it should also be able to extrapolate
to out-of-distribution examples — a significantly harder challenge.

The dataset is a collection of 18 existing QA dataset (carefully selected
subset of them) and converted to the same format (SQuAD format). Among
these 18 datasets, six datasets were made available for training,
six datasets were made available for development, and the final six
for testing. The dataset is released as part of the MRQA 2019 Shared Task.
"""

_HOMEPAGE = "https://mrqa.github.io/2019/shared.html"

_LICENSE = "Unknwon"

_URLs = {
    # Train sub-datasets
    "train+SQuAD": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/SQuAD.jsonl.gz",
    "train+NewsQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/NewsQA.jsonl.gz",
    "train+TriviaQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/TriviaQA-web.jsonl.gz",
    "train+SearchQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/SearchQA.jsonl.gz",
    "train+HotpotQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/HotpotQA.jsonl.gz",
    "train+NaturalQuestions": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/train/NaturalQuestionsShort.jsonl.gz",
    # Validation sub-datasets
    "validation+SQuAD": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/SQuAD.jsonl.gz",
    "validation+NewsQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/NewsQA.jsonl.gz",
    "validation+TriviaQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/TriviaQA-web.jsonl.gz",
    "validation+SearchQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/SearchQA.jsonl.gz",
    "validation+HotpotQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/HotpotQA.jsonl.gz",
    "validation+NaturalQuestions": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/NaturalQuestionsShort.jsonl.gz",
    # Test sub-datasets
    "test+BioASQ": "http://participants-area.bioasq.org/MRQA2019/",  # BioASQ.jsonl.gz
    "test+DROP": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/DROP.jsonl.gz",
    "test+DuoRC": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/DuoRC.ParaphraseRC.jsonl.gz",
    "test+RACE": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/RACE.jsonl.gz",
    "test+RelationExtraction": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/RelationExtraction.jsonl.gz",
    "test+TextbookQA": "https://s3.us-east-2.amazonaws.com/mrqa/release/v2/dev/TextbookQA.jsonl.gz",
}


class Mrqa(datasets.GeneratorBasedBuilder):
    """MRQA 2019 Shared task dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="plain_text", description="Plain text", version=VERSION),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # Format is derived from https://github.com/mrqa/MRQA-Shared-Task-2019#mrqa-format
            features=datasets.Features(
                {
                    "subset": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "context_tokens": datasets.Sequence(
                        {
                            "tokens": datasets.Value("string"),
                            "offsets": datasets.Value("int32"),
                        }
                    ),
                    "qid": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "question_tokens": datasets.Sequence(
                        {
                            "tokens": datasets.Value("string"),
                            "offsets": datasets.Value("int32"),
                        }
                    ),
                    "detected_answers": datasets.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "char_spans": datasets.Sequence(
                                {
                                    "start": datasets.Value("int32"),
                                    "end": datasets.Value("int32"),
                                }
                            ),
                            "token_spans": datasets.Sequence(
                                {
                                    "start": datasets.Value("int32"),
                                    "end": datasets.Value("int32"),
                                }
                            ),
                        }
                    ),
                    "answers": datasets.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths_dict": data_dir,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepaths_dict": data_dir,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepaths_dict": data_dir,
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, filepaths_dict, split):
        """Yields examples."""
        for source, filepath in filepaths_dict.items():
            if split not in source:
                continue
            with open(filepath, encoding="utf-8") as f:
                header = next(f)
                subset = json.loads(header)["header"]["dataset"]

                for row in f:
                    paragraph = json.loads(row)
                    context = paragraph["context"].strip()
                    context_tokens = [{"tokens": t[0], "offsets": t[1]} for t in paragraph["context_tokens"]]
                    for qa in paragraph["qas"]:
                        qid = qa["qid"]
                        question = qa["question"].strip()
                        question_tokens = [{"tokens": t[0], "offsets": t[1]} for t in qa["question_tokens"]]
                        detected_answers = []
                        for detect_ans in qa["detected_answers"]:
                            detected_answers.append(
                                {
                                    "text": detect_ans["text"].strip(),
                                    "char_spans": [{"start": t[0], "end": t[1]} for t in detect_ans["char_spans"]],
                                    "token_spans": [{"start": t[0], "end": t[1]} for t in detect_ans["token_spans"]],
                                }
                            )
                        answers = qa["answers"]
                        yield qid, {
                            "subset": subset,
                            "context": context,
                            "context_tokens": context_tokens,
                            "qid": qid,
                            "question": question,
                            "question_tokens": question_tokens,
                            "detected_answers": detected_answers,
                            "answers": answers,
                        }
