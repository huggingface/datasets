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
On social media, Arabic speakers tend to express themselves in their own local dialect. To do so, Tunisians use "Tunisian Arabizi", which consists in supplementing numerals to the Latin script rather than the Arabic alphabet. TUNIZI is the first Tunisian Arabizi Dataset including 3K sentences, balanced, covering different topics, preprocessed and annotated as positive and negative.
"""
_HOMEPAGE_URL = "https://github.com/chaymafourati/TUNIZI-Sentiment-Analysis-Tunisian-Arabizi-Dataset"
_URL = "https://raw.githubusercontent.com/chaymafourati/TUNIZI-Sentiment-Analysis-Tunisian-Arabizi-Dataset/master/TUNIZI-Dataset.txt"
_CITATION = """\
@inproceedings{Chayma2020,
title={TUNIZI: a Tunisian Arabizi sentiment analysis Dataset},
author={Fourati, Chayma and Messaoudi, Abir and Haddad, Hatem},
booktitle={AfricaNLP Workshop, Putting Africa on the NLP Map. ICLR 2020, Virtual Event},
volume = {arXiv:3091079},
year = {2020},
url = {https://arxiv.org/submit/3091079},
}
"""


class Tunizi(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.9.1")

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
        path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        with open(datapath, encoding="utf-8") as f:
            for sentence_counter, row in enumerate(f):
                row = row.strip()
                target, sentence = row.split(";")
                if target.startswith("%") or target.startswith('"'):
                    target = target[1:]
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "sentence": sentence,
                        "target": target,
                    },
                )
                yield result
