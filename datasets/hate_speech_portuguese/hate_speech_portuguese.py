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
"""Portuguese dataset for hate speech detection composed of 5,668 tweets with binary annotations (i.e. 'hate' vs. 'no-hate')."""


import csv

import datasets


_CITATION = """\
@inproceedings{fortuna-etal-2019-hierarchically,
title = "A Hierarchically-Labeled {P}ortuguese Hate Speech Dataset",
author = "Fortuna, Paula  and
    Rocha da Silva, Jo{\\~a}o  and
    Soler-Company, Juan  and
    Wanner, Leo  and
    Nunes, S{\'e}rgio",
booktitle = "Proceedings of the Third Workshop on Abusive Language Online",
month = aug,
year = "2019",
address = "Florence, Italy",
publisher = "Association for Computational Linguistics",
url = "https://www.aclweb.org/anthology/W19-3510",
doi = "10.18653/v1/W19-3510",
pages = "94--104",
abstract = "Over the past years, the amount of online offensive speech has been growing steadily. To successfully cope with it, machine learning are applied. However, ML-based techniques require sufficiently large annotated datasets. In the last years, different datasets were published, mainly for English. In this paper, we present a new dataset for Portuguese, which has not been in focus so far. The dataset is composed of 5,668 tweets. For its annotation, we defined two different schemes used by annotators with different levels of expertise. Firstly, non-experts annotated the tweets with binary labels ({`}hate{'} vs. {`}no-hate{'}). Secondly, expert annotators classified the tweets following a fine-grained hierarchical multiple label scheme with 81 hate speech categories in total. The inter-annotator agreement varied from category to category, which reflects the insight that some types of hate speech are more subtle than others and that their detection depends on personal perception. This hierarchical annotation scheme is the main contribution of the presented work, as it facilitates the identification of different types of hate speech and their intersections. To demonstrate the usefulness of our dataset, we carried a baseline classification experiment with pre-trained word embeddings and LSTM on the binary classified data, with a state-of-the-art outcome.",
}
"""

_DESCRIPTION = """\
Portuguese dataset for hate speech detection composed of 5,668 tweets with binary annotations (i.e. 'hate' vs. 'no-hate').
"""

_HOMEPAGE = "https://github.com/paulafortuna/Portuguese-Hate-Speech-Dataset"

_LICENSE = "Unknown"

_URL = "https://github.com/paulafortuna/Portuguese-Hate-Speech-Dataset/raw/master/2019-05-28_portuguese_hate_speech_binary_classification.csv"


class HateSpeechPortuguese(datasets.GeneratorBasedBuilder):
    """Portuguese dataset for hate speech detection composed of 5,668 tweets with binary annotations (i.e. 'hate' vs. 'no-hate')."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["no-hate", "hate"]),
                    "hatespeech_G1": datasets.Value("string"),
                    "annotator_G1": datasets.Value("string"),
                    "hatespeech_G2": datasets.Value("string"),
                    "annotator_G2": datasets.Value("string"),
                    "hatespeech_G3": datasets.Value("string"),
                    "annotator_G3": datasets.Value("string"),
                }
            ),
            supervised_keys=("text", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_file = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_file,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)
            for id_, row in enumerate(reader):
                if id_ == 0:
                    continue

                yield id_, {
                    "text": row[0],
                    "label": "hate" if row[1] == "1" else "no-hate",
                    "hatespeech_G1": row[2],
                    "annotator_G1": row[3],
                    "hatespeech_G2": row[4],
                    "annotator_G2": row[5],
                    "hatespeech_G3": row[6],
                    "annotator_G3": row[7],
                }
