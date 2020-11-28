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
"""Fine-grained Named Entity Recognition in Legal Documents"""

from __future__ import absolute_import, division, print_function

import datasets


_CITATION = """\
@inproceedings{leitner2019fine,
  author = {Elena Leitner and Georg Rehm and Julian Moreno-Schneider},
  title = {{Fine-grained Named Entity Recognition in Legal Documents}},
  booktitle = {Semantic Systems. The Power of AI and Knowledge
                  Graphs. Proceedings of the 15th International Conference
                  (SEMANTiCS 2019)},
  year = 2019,
  editor = {Maribel Acosta and Philippe Cudré-Mauroux and Maria
                  Maleshkova and Tassilo Pellegrini and Harald Sack and York
                  Sure-Vetter},
  keywords = {aip},
  publisher = {Springer},
  series = {Lecture Notes in Computer Science},
  number = {11702},
  address = {Karlsruhe, Germany},
  month = 9,
  note = {10/11 September 2019},
  pages = {272--287},
  pdf = {https://link.springer.com/content/pdf/10.1007%2F978-3-030-33220-4_20.pdf}
}
"""

_DESCRIPTION = """\
We describe a dataset developed for Named Entity Recognition in German federal court decisions.
It consists of approx. 67,000 sentences with over 2 million tokens.
The resource contains 54,000 manually annotated entities, mapped to 19 fine-grained semantic classes:
person, judge, lawyer, country, city, street, landscape, organization, company, institution, court, brand, law,
ordinance, European legal norm, regulation, contract, court decision, and legal literature.
The legal documents were, furthermore, automatically annotated with more than 35,000 TimeML-based time expressions.
The dataset, which is available under a CC-BY 4.0 license in the CoNNL-2002 format,
was developed for training an NER service for German legal documents in the EU project Lynx.
"""

_URL = "https://raw.githubusercontent.com/elenanereiss/Legal-Entity-Recognition/master/data/ler.conll"


class Ler(datasets.GeneratorBasedBuilder):
    """
    We describe a dataset developed for Named Entity Recognition in German federal court decisions.
    It consists of approx. 67,000 sentences with over 2 million tokens.
    The resource contains 54,000 manually annotated entities, mapped to 19 fine-grained semantic classes:
    person, judge, lawyer, country, city, street, landscape, organization, company, institution, court, brand, law,
    ordinance, European legal norm, regulation, contract, court decision, and legal literature.
    The legal documents were, furthermore, automatically annotated with more than 35,000 TimeML-based time expressions.
    The dataset, which is available under a CC-BY 4.0 license in the CoNNL-2002 format,
    was developed for training an NER service for German legal documents in the EU project Lynx.
    """

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.ClassLabel(
                            names=[
                                "O",
                                "B-PER",
                                "I-PER",
                                "B-RR",
                                "I-RR",
                                "B-AN",
                                "I-AN",
                                "B-LD",
                                "I-LD",
                                "B-ST",
                                "I-ST",
                                "B-STR",
                                "I-STR",
                                "B-LDS",
                                "I-LDS",
                                "B-ORG",
                                "I-ORG",
                                "B-UN",
                                "I-UN",
                                "B-INN",
                                "I-INN",
                                "B-GRT",
                                "I-GRT",
                                "B-MRK",
                                "I-MRK",
                                "B-GS",
                                "I-GS",
                                "B-VO",
                                "I-VO",
                                "B-EUN",
                                "I-EUN",
                                "B-VS",
                                "I-VS",
                                "B-VT",
                                "I-VT",
                                "B-RS",
                                "I-RS",
                                "B-LIT",
                                "I-LIT",
                            ]
                        )
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=datasets.info.SupervisedKeysData(input="tokens", output="ner_tags"),
            # Homepage of the dataset for documentation
            homepage="https://github.com/elenanereiss/Legal-Entity-Recognition",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_file = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_file},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, "r", encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {"id": guid, "tokens": tokens, "ner_tags": ner_tags}
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    # conll2002 tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
