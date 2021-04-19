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
"""Korean HateSpeech Dataset"""


import csv

import datasets


_CITATION = """\
@inproceedings{moon-etal-2020-beep,
    title = "{BEEP}! {K}orean Corpus of Online News Comments for Toxic Speech Detection",
    author = "Moon, Jihyung  and
      Cho, Won Ik  and
      Lee, Junbum",
    booktitle = "Proceedings of the Eighth International Workshop on Natural Language Processing for Social Media",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.socialnlp-1.4",
    pages = "25--31",
    abstract = "Toxic comments in online platforms are an unavoidable social issue under the cloak of anonymity. Hate speech detection has been actively done for languages such as English, German, or Italian, where manually labeled corpus has been released. In this work, we first present 9.4K manually labeled entertainment news comments for identifying Korean toxic speech, collected from a widely used online news platform in Korea. The comments are annotated regarding social bias and hate speech since both aspects are correlated. The inter-annotator agreement Krippendorff{'}s alpha score is 0.492 and 0.496, respectively. We provide benchmarks using CharCNN, BiLSTM, and BERT, where BERT achieves the highest score on all tasks. The models generally display better performance on bias identification, since the hate speech detection is a more subjective issue. Additionally, when BERT is trained with bias label for hate speech detection, the prediction score increases, implying that bias and hate are intertwined. We make our dataset publicly available and open competitions with the corpus and benchmarks.",
}
"""

_DESCRIPTION = """\
Human-annotated Korean corpus collected from a popular domestic entertainment news aggregation platform
for toxic speech detection. Comments are annotated for gender bias, social bias and hate speech.
"""

_HOMEPAGE = "https://github.com/kocohub/korean-hate-speech"

_LICENSE = "Creative Commons"

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/kocohub/korean-hate-speech/master/labeled/train.tsv"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/kocohub/korean-hate-speech/master/labeled/dev.tsv"


class KorHate(datasets.GeneratorBasedBuilder):
    """Korean Corpus of Online News Comments for Toxic Speech Detection"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        features = datasets.Features(
            {
                "comments": datasets.Value("string"),
                "contain_gender_bias": datasets.features.ClassLabel(names=["False", "True"]),
                "bias": datasets.features.ClassLabel(names=["none", "gender", "others"]),
                "hate": datasets.features.ClassLabel(names=["hate", "offensive", "none"]),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Korean HateSpeech examples"""

        with open(filepath, encoding="utf-8") as tsv_file:
            tsv_reader = csv.DictReader(tsv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(tsv_reader):
                yield id_, {
                    "comments": row["comments"],
                    "contain_gender_bias": row["contain_gender_bias"],
                    "bias": row["bias"],
                    "hate": row["hate"],
                }
