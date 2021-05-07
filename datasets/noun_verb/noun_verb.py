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
import conllu

import datasets


_CITATION = """\
@InProceedings{NOUNVERB,
  title = {A Challenge Set and Methods for Noun-Verb Ambiguity},
  author = {Ali Elkahky and Kellie Webster and Daniel Andor and Emily Pitler},
  booktitle = {Proceedings of EMNLP},
  year = {2018}
}
"""

_DESCRIPTION = """\
This dataset contains naturally-occurring English sentences that feature non-trivial noun-verb ambiguity.

English part-of-speech taggers regularly make egregious errors related to noun-verb ambiguity, despite having achieved 97%+ accuracy on the WSJ Penn Treebank since 2002. These mistakes have been difficult to quantify and make taggers less useful to downstream tasks such as translation and text-to-speech synthesis.

Below are some examples from the dataset:

- Certain insects can damage plumerias, such as mites, flies, or aphids. NOUN
- Mark which area you want to distress. VERB

All tested existing part-of-speech taggers mistag both of these examples, tagging flies as a verb and Mark as a noun.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/noun-verb"

_TRAIN_URL = "https://raw.githubusercontent.com/google-research-datasets/noun-verb/master/train.conll"
_DEV_URL = "https://raw.githubusercontent.com/google-research-datasets/noun-verb/master/dev.conll"
_TEST_URL = "https://raw.githubusercontent.com/google-research-datasets/noun-verb/master/test.conll"


class NounVerb(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "token_ids": datasets.Sequence(datasets.Value("int32")),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "lemmas": datasets.Sequence(datasets.Value("string")),
                    "upos_tags": datasets.Sequence(datasets.Value("string")),
                    "xpos_tags": datasets.Sequence(datasets.Value("string")),
                    "feats": [
                        {
                            "POS": datasets.Value("string"),
                            "fPOS": datasets.Value("string"),
                        }
                    ],
                    "head": datasets.Sequence(datasets.Value("string")),
                    "deprel": datasets.Sequence(datasets.Value("string")),
                    "deps": datasets.Sequence(datasets.Value("string")),
                    "misc": datasets.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_URL)
        valid_path = dl_manager.download_and_extract(_DEV_URL)
        test_path = dl_manager.download_and_extract(_TEST_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": train_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"datapath": valid_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"datapath": test_path},
            ),
        ]

    def _generate_examples(self, datapath):
        counter = 0
        with open(datapath, "r", encoding="utf-8") as data_file:
            tokenlist = list(conllu.parse_incr(data_file))
            for sent in tokenlist:
                res = {
                    "id": counter,
                    "token_ids": [token["id"] for token in sent],
                    "tokens": [str(token["form"]) for token in sent],
                    "lemmas": [str(token["lemma"]) for token in sent],
                    "upos_tags": [str(token["upos"]) for token in sent],
                    "xpos_tags": [str(token["xpos"]) for token in sent],
                    "feats": [
                        token["feats"] if token["feats"] is not None else {"POS": "None", "fPOS": "None"}
                        for token in sent
                    ],
                    "head": [str(token["head"]) for token in sent],
                    "deprel": [str(token["deprel"]) for token in sent],
                    "deps": [str(token["deps"]) for token in sent],
                    "misc": [str(token["misc"]) for token in sent],
                }
                yield counter, res
                counter += 1
