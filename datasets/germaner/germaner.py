# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
import datasets


_DESCRIPTION = """\
GermaNER is a freely available statistical German Named Entity Tagger based on conditional random fields(CRF). The tagger is trained and evaluated on the NoSta-D Named Entity dataset, which was used in the GermEval 2014 for named entity recognition. The tagger comes close to the performance of the best (proprietary) system in the competition with 77% F-measure (this is the latest result; the one reported in the paper is 76%) test set performance on the four standard NER classes (PERson, LOCation, ORGanisation and OTHer).

We describe a range of features and their influence on German NER classification and provide a comparative evaluation and some analysis of the results. The software components, the training data and all data used for feature generation are distributed under permissive licenses, thus this tagger can be used in academic and commercial settings without restrictions or fees. The tagger is available as a command-line tool and as an Apache UIMA component.
"""
_HOMEPAGE_URL = "https://github.com/tudarmstadt-lt/GermaNER"
_URL = "https://raw.githubusercontent.com/tudarmstadt-lt/GermaNER/a206b554feca263d740302449fff0776c66d0040/data/v0.9.1/full_train.tsv"
_CITATION = """\
@inproceedings{Benikova2015GermaNERFO,
  title={GermaNER: Free Open German Named Entity Recognition Tool},
  author={Darina Benikova and S. Yimam and Prabhakaran Santhanam and Chris Biemann},
  booktitle={GSCL},
  year={2015}
}
"""


class GermaNER(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.9.1")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B-LOC",
                                "B-ORG",
                                "B-OTH",
                                "B-PER",
                                "I-LOC",
                                "I-ORG",
                                "I-OTH",
                                "I-PER",
                                "O",
                            ]
                        )
                    ),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        sentence_counter = 0
        with open(datapath, encoding="utf-8") as f:
            current_words = []
            current_labels = []
            for row in f:
                row = row.rstrip()
                row_split = row.split()
                if len(row_split) == 2:
                    token, label = row_split
                    current_words.append(token)
                    current_labels.append(label)
                else:
                    if not current_words:
                        continue
                    assert len(current_words) == len(current_labels), "word len doesnt match label length"
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "tokens": current_words,
                            "ner_tags": current_labels,
                        },
                    )
                    sentence_counter += 1
                    current_words = []
                    current_labels = []
                    yield sentence

            # if something remains:
            if current_words:
                sentence = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "tokens": current_words,
                        "ner_tags": current_labels,
                    },
                )
                yield sentence
