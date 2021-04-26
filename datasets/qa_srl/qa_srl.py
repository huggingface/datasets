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
"""TODO: Add a description here."""


import datasets


_CITATION = """\
@InProceedings{huggingface:dataset,
title = {QA-SRL: Question-Answer Driven Semantic Role Labeling},
authors={Luheng He, Mike Lewis, Luke Zettlemoyer},
year={2015}
publisher = {cs.washington.edu},
howpublished={\\url{https://dada.cs.washington.edu/qasrl/#page-top}},
}
"""


_DESCRIPTION = """\
The dataset contains question-answer pairs to model verbal predicate-argument structure. The questions start with wh-words (Who, What, Where, What, etc.) and contain a verb predicate in the sentence; the answers are phrases in the sentence.
There were 2 datsets used in the paper, newswire and wikipedia. Unfortunately the newswiredataset is built from CoNLL-2009 English training set that is covered under license
Thus, we are providing only Wikipedia training set here. Please check README.md for more details on newswire dataset.
For the Wikipedia domain, randomly sampled sentences from the English Wikipedia (excluding questions and sentences with fewer than 10 or more than 60 words) were taken.
This new dataset is designed to solve this great NLP task and is crafted with a lot of care.
"""

_HOMEPAGE = "https://dada.cs.washington.edu/qasrl/#page-top"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""


_URLs = {
    "wiki_train": "https://dada.cs.washington.edu/qasrl/data/wiki1.train.qa",
    "wiki_dev": "https://dada.cs.washington.edu/qasrl/data/wiki1.dev.qa",
    "wiki_test": "https://dada.cs.washington.edu/qasrl/data/wiki1.test.qa",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class QaSrl(datasets.GeneratorBasedBuilder):
    """QA-SRL: Question-Answer Driven Semantic Role Labeling (qa_srl) corpus"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text", version=VERSION, description="This provides WIKIPEDIA dataset for qa_srl corpus"
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "plain_text"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        features = datasets.Features(
            {
                "sentence": datasets.Value("string"),
                "sent_id": datasets.Value("string"),
                "predicate_idx": datasets.Value("int32"),
                "predicate": datasets.Value("string"),
                "question": datasets.Sequence(datasets.Value("string")),
                "answers": datasets.Sequence(datasets.Value("string")),
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
        """Returns SplitGenerators."""

        train_fpath = dl_manager.download(_URLs["wiki_train"])
        dev_fpath = dl_manager.download(_URLs["wiki_dev"])
        test_fpath = dl_manager.download(_URLs["wiki_test"])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": train_fpath,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": dev_fpath,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": test_fpath,
                },
            ),
        ]

    def _generate_examples(self, filepath):

        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:

            qa_counter = 0
            # Start reading entries
            sent_id, predicates_cnt = f.readline().rstrip("\n").split("\t")
            while True:

                sentence = f.readline().rstrip("\n")

                # Loop for every predicate
                predicates_counter = int(predicates_cnt)
                while predicates_counter != 0:
                    predicates_counter -= 1
                    predicate_details = f.readline().rstrip("\n").split("\t")
                    predicate_idx, predicate, qa_pairs_cnt = (
                        predicate_details[0],
                        predicate_details[1],
                        predicate_details[2],
                    )
                    pairs = int(qa_pairs_cnt)

                    while pairs != 0:
                        pairs -= 1
                        line = f.readline().rstrip("\n").split("\t")
                        question = line[:8]
                        answers_list = line[8:]
                        qa_counter += 1

                        if "###" in answers_list[0]:
                            answers = [answer.strip() for answer in answers_list[0].split("###")]
                        else:
                            answers = answers_list

                        yield qa_counter, {
                            "sentence": sentence,
                            "sent_id": sent_id,
                            "predicate_idx": predicate_idx,
                            "predicate": predicate,
                            "question": question,
                            "answers": answers,
                        }

                # Pass the blank line
                f.readline()
                nextline = f.readline()
                if not nextline:

                    break
                else:
                    sent_id, predicates_cnt = nextline.rstrip("\n").split("\t")
