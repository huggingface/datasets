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
The dataset consists of 9008 sentences that are labelled with fine-grained polarity in the range from -2 to 2 (negative to postive). The quality of the fine-grained is not cross validated and is therefore subject to uncertainties; however, the simple polarity has been cross validated and therefore is considered to be more correct.
"""
_HOMEPAGE_URL = "https://github.com/steffan267/Sentiment-Analysis-on-Danish-Social-Media"
_URL = (
    "https://raw.githubusercontent.com/steffan267/Sentiment-Analysis-on-Danish-Social-Media/master/all_sentences.tsv"
)
_CITATION = "https://github.com/lucaspuvis/SAM/blob/master/Thesis.pdf"


class DanishPoliticalComments(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.9.1")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "target": datasets.features.ClassLabel(names=["2", "1", "0", "-1", "-2"]),
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
            for row in f:
                row = row.strip()
                target, sentence = row.split("\t")
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "sentence": sentence,
                        "target": target,
                    },
                )
                sentence_counter += 1
                yield result
