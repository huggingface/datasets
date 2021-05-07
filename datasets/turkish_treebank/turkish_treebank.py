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
@inproceedings{kayadelen-ozturel-bohnet:2020:LREC,
  author = {Kayadelen, Tolga  and  \"{O}zt\"{u}rel, Adnan  and  Bohnet, Bernd},
  title = {A Gold Standard Dependency Treebank for Turkish},
  booktitle = {Proceedings of The 12th Language Resources and Evaluation
    Conference},
  month = {May},
  year = {2020},
  address = {Marseille, France},
  publisher = {European Language Resources Association},
  pages = {5158--5165},
  url = {https://www.aclweb.org/anthology/2020.lrec-1.634}
}
"""

_DESCRIPTION = """\
Turkish Web Treebank (TWT, ISLRN: 177-333-742-633-6) consists of 4,851 sentences (66,466 words, and 81,370 inflectional groups), which are manually annotated for segmentation, morphology, part-of-speech and dependency relations. It is composed of two sections: web and Wikipedia. Web section is built by sampling and annotating 2,541 sentences from a representative set of Turkish Forum, Blog, How-to, Review & Guides webpages. Wikipedia section is built by sampling a sentence from 2,310 Turkish Wikipedia pages and annotating them.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/turkish-treebanks"

_WEB_URL = "https://raw.githubusercontent.com/google-research-datasets/turkish-treebanks/master/data/web.conllu"
_WIKI_URL = "https://raw.githubusercontent.com/google-research-datasets/turkish-treebanks/master/data/wiki.conllu"
_VERSION = "1.0.0"
_SOURCES = ["wiki", "web"]
_ALL = "all"


class TurkishTreebankConfig(datasets.BuilderConfig):
    def __init__(self, *args, sources=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sources = sources


class TurkishTreebank(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        TurkishTreebankConfig(name=source, sources=[source], description=f"Source: {source}.") for source in _SOURCES
    ] + [
        TurkishTreebankConfig(
            name=_ALL,
            sources=_SOURCES,
            description=f"All sources included: wiki, web",
            version=datasets.Version(_VERSION),
        )
    ]
    BUILDER_CONFIG_CLASS = TurkishTreebankConfig
    DEFAULT_CONFIG_NAME = _ALL

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
                    "feats": datasets.Sequence(datasets.Value("string")),
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
        wiki_path = dl_manager.download_and_extract(_WIKI_URL)
        web_path = dl_manager.download_and_extract(_WEB_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": {"wiki": wiki_path, "web": web_path}},
            )
        ]

    def _generate_examples(self, datapath):
        counter = 0
        for source in self.config.sources:
            with open(datapath[source], "r", encoding="utf-8") as data_file:
                tokenlist = list(conllu.parse_incr(data_file))
                for sent in tokenlist:
                    res = {
                        "id": counter,
                        "token_ids": [token["id"] for token in sent],
                        "tokens": [str(token["form"]) for token in sent],
                        "lemmas": [str(token["lemma"]) for token in sent],
                        "upos_tags": [str(token["upos"]) for token in sent],
                        "xpos_tags": [str(token["xpos"]) for token in sent],
                        "feats": [str(token["feats"]) for token in sent],
                        "head": [str(token["head"]) for token in sent],
                        "deprel": [str(token["deprel"]) for token in sent],
                        "deps": [str(token["deps"]) for token in sent],
                        "misc": [str(token["misc"]) for token in sent],
                    }
                    yield counter, res
                    counter += 1
