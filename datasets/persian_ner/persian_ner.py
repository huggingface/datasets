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
"""ArmanPerosNERCorpus - the first manually-annotated Persian NER corpus."""


import os

import datasets


_CITATION = """\
@inproceedings{poostchi-etal-2016-personer,
    title = "{P}erso{NER}: {P}ersian Named-Entity Recognition",
    author = "Poostchi, Hanieh  and
      Zare Borzeshi, Ehsan  and
      Abdous, Mohammad  and
      Piccardi, Massimo",
    booktitle = "Proceedings of {COLING} 2016, the 26th International Conference on Computational Linguistics: Technical Papers",
    month = dec,
    year = "2016",
    address = "Osaka, Japan",
    publisher = "The COLING 2016 Organizing Committee",
    url = "https://www.aclweb.org/anthology/C16-1319",
    pages = "3381--3389",
    abstract = "Named-Entity Recognition (NER) is still a challenging task for languages with low digital resources. The main difficulties arise from the scarcity of annotated corpora and the consequent problematic training of an effective NER pipeline. To abridge this gap, in this paper we target the Persian language that is spoken by a population of over a hundred million people world-wide. We first present and provide ArmanPerosNERCorpus, the first manually-annotated Persian NER corpus. Then, we introduce PersoNER, an NER pipeline for Persian that leverages a word embedding and a sequential max-margin classifier. The experimental results show that the proposed approach is capable of achieving interesting MUC7 and CoNNL scores while outperforming two alternatives based on a CRF and a recurrent neural network.",
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
The dataset includes 250,015 tokens and 7,682 Persian sentences in total. It is available in 3 folds to be used in turn as training and test sets. The NER tags are in IOB format.
"""

_HOMEPAGE = ""

_LICENSE = "Creative Commons Attribution 4.0 International License"

_URL = "https://github.com/HaniehP/PersianNER/raw/master/ArmanPersoNERCorpus.zip"


class PersianNER(datasets.GeneratorBasedBuilder):
    """ArmanPerosNERCorpus - the first manually-annotated Persian NER corpus."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="fold1", version=VERSION, description="This is the first fold  of the ArmanPersoNERCorpus"
        ),
        datasets.BuilderConfig(
            name="fold2", version=VERSION, description="This is the second fold  of the ArmanPersoNERCorpus"
        ),
        datasets.BuilderConfig(
            name="fold3", version=VERSION, description="This is the third fold  of the ArmanPersoNERCorpus"
        ),
    ]

    DEFAULT_CONFIG_NAME = "fold1"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
            {
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(
                    datasets.ClassLabel(
                        names=[
                            "O",
                            "I-event",
                            "I-fac",
                            "I-loc",
                            "I-org",
                            "I-pers",
                            "I-pro",
                            "B-event",
                            "B-fac",
                            "B-loc",
                            "B-org",
                            "B-pers",
                            "B-pro",
                        ]
                    )
                ),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=("tokens", "ner_tags"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"train_{self.config.name}.txt"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, f"test_{self.config.name}.txt"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, "r", encoding="utf-8") as f:
            id_ = 0
            tokens = []
            ner_labels = []
            for line in f:
                stripped_line = line.strip(" \n")  # strip away whitespaces AND new line characters
                if len(stripped_line) == 0:
                    # If line is empty, it means we reached the end of a sentence.
                    # We can yield the tokens and labels
                    if len(tokens) > 0 and len(ner_labels) > 0:
                        yield id_, {
                            "tokens": tokens,
                            "ner_tags": ner_labels,
                        }
                    else:
                        # Do not yield if tokens or ner_labels is empty
                        # It can be the case if several empty lines are contiguous
                        continue
                    # Then we need to increment the _id and reset the tokens and ner_labels list
                    id_ += 1
                    tokens = []
                    ner_labels = []
                else:
                    token, ner_label = line.split(" ")  # Retrieve token and label
                    tokens.append(token)
                    ner_labels.append(ner_label)
