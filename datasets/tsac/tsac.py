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
Tunisian Sentiment Analysis Corpus.

About 17k user comments manually annotated to positive and negative polarities. This corpus is collected from Facebook users comments written on official pages of Tunisian radios and TV channels namely Mosaique FM, JawhraFM, Shemes FM, HiwarElttounsi TV and Nessma TV. The corpus is collected from a period spanning January 2015 until June 2016.
"""
_HOMEPAGE_URL = "https://github.com/fbougares/TSAC"
_CITATION = """\
@inproceedings{medhaffar-etal-2017-sentiment,
    title = "Sentiment Analysis of {T}unisian Dialects: Linguistic Ressources and Experiments",
    author = "Medhaffar, Salima  and
      Bougares, Fethi  and
      Est{`e}ve, Yannick  and
      Hadrich-Belguith, Lamia",
    booktitle = "Proceedings of the Third {A}rabic Natural Language Processing Workshop",
    month = apr,
    year = "2017",
    address = "Valencia, Spain",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W17-1307",
    doi = "10.18653/v1/W17-1307",
    pages = "55--61",
    abstract = "Dialectal Arabic (DA) is significantly different from the Arabic language taught in schools and used in written communication and formal speech (broadcast news, religion, politics, etc.). There are many existing researches in the field of Arabic language Sentiment Analysis (SA); however, they are generally restricted to Modern Standard Arabic (MSA) or some dialects of economic or political interest. In this paper we are interested in the SA of the Tunisian Dialect. We utilize Machine Learning techniques to determine the polarity of comments written in Tunisian Dialect. First, we evaluate the SA systems performances with models trained using freely available MSA and Multi-dialectal data sets. We then collect and annotate a Tunisian Dialect corpus of 17.000 comments from Facebook. This corpus allows us a significant accuracy improvement compared to the best model trained on other Arabic dialects or MSA data. We believe that this first freely available corpus will be valuable to researchers working in the field of Tunisian Sentiment Analysis and similar areas.",
}
"""

_TRAIN_POS_URL = "https://raw.githubusercontent.com/fbougares/TSAC/master/train_pos.txt"
_TRAIN_NEG_URL = "https://raw.githubusercontent.com/fbougares/TSAC/master/train_neg.txt"
_TEST_POS_URL = "https://raw.githubusercontent.com/fbougares/TSAC/master/test_pos.txt"
_TEST_NEG_URL = "https://raw.githubusercontent.com/fbougares/TSAC/master/test_neg.txt"


class TSAC(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "target": datasets.ClassLabel(names=["1", "-1"]),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_pos_path = dl_manager.download_and_extract(_TRAIN_POS_URL)
        train_neg_path = dl_manager.download_and_extract(_TRAIN_NEG_URL)
        test_pos_path = dl_manager.download_and_extract(_TEST_POS_URL)
        test_neg_path = dl_manager.download_and_extract(_TEST_NEG_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"pospath": train_pos_path, "negpath": train_neg_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"pospath": test_pos_path, "negpath": test_neg_path},
            ),
        ]

    def _generate_examples(self, pospath, negpath):
        sentence_counter = 0

        with open(pospath, encoding="utf-8") as f:
            for row in f:
                row = row.strip()
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "sentence": row,
                        "target": "1",
                    },
                )
                yield result
                sentence_counter += 1

        with open(negpath, encoding="utf-8") as f:
            for row in f:
                row = row.strip()
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "sentence": row,
                        "target": "-1",
                    },
                )
                yield result
                sentence_counter += 1
