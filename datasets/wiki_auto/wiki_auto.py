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
"""WikiAuto dataset for Text Simplification"""


import json

import datasets


_CITATION = """\
@inproceedings{acl/JiangMLZX20,
  author    = {Chao Jiang and
               Mounica Maddela and
               Wuwei Lan and
               Yang Zhong and
               Wei Xu},
  editor    = {Dan Jurafsky and
               Joyce Chai and
               Natalie Schluter and
               Joel R. Tetreault},
  title     = {Neural {CRF} Model for Sentence Alignment in Text Simplification},
  booktitle = {Proceedings of the 58th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2020, Online, July 5-10, 2020},
  pages     = {7943--7960},
  publisher = {Association for Computational Linguistics},
  year      = {2020},
  url       = {https://www.aclweb.org/anthology/2020.acl-main.709/}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
WikiAuto provides a set of aligned sentences from English Wikipedia and Simple English Wikipedia
as a resource to train sentence simplification systems. The authors first crowd-sourced a set of manual alignments
between sentences in a subset of the Simple English Wikipedia and their corresponding versions in English Wikipedia
(this corresponds to the `manual` config), then trained a neural CRF system to predict these alignments.
The trained model was then applied to the other articles in Simple English Wikipedia with an English counterpart to
create a larger corpus of aligned sentences (corresponding to the `auto`, `auto_acl`, `auto_full_no_split`, and `auto_full_with_split`  configs here).
"""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "CC-BY-SA 3.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "manual": {
        "train": "https://www.dropbox.com/sh/ohqaw41v48c7e5p/AACdl4UPKtu7CMMa-CJhz4G7a/wiki-manual/train.tsv?dl=1",
        "dev": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-manual/dev.tsv",
        "test": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-manual/test.tsv",
    },
    "auto_acl": {
        "normal": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/ACL2020/train.src",
        "simple": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/ACL2020/train.dst",
    },
    "auto_full_no_split": {
        "normal": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/GEM2021/full_no_split/train.src",
        "simple": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/GEM2021/full_no_split/train.dst",
    },
    "auto_full_with_split": {
        "normal": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/GEM2021/full_with_split/train.src",
        "simple": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/GEM2021/full_with_split/train.dst",
    },
    "auto": {
        "part_1": "https://www.dropbox.com/sh/ohqaw41v48c7e5p/AAATBDhU1zpdcT5x5WgO8DMaa/wiki-auto-all-data/wiki-auto-part-1-data.json?dl=1",
        "part_2": "https://www.dropbox.com/sh/ohqaw41v48c7e5p/AAATgPkjo_tPt9z12vZxJ3MRa/wiki-auto-all-data/wiki-auto-part-2-data.json?dl=1",
    },
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class WikiAuto(datasets.GeneratorBasedBuilder):
    """WikiAuto dataset for sentence simplification"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="manual",
            version=VERSION,
            description="A set of 10K Wikipedia sentence pairs aligned by crowd workers.",
        ),
        datasets.BuilderConfig(
            name="auto_acl",
            version=VERSION,
            description="Automatically aligned and filtered sentence pairs used to train the ACL2020 system.",
        ),
        datasets.BuilderConfig(
            name="auto_full_no_split",
            version=VERSION,
            description="All automatically aligned sentence pairs without sentence splitting.",
        ),
        datasets.BuilderConfig(
            name="auto_full_with_split",
            version=VERSION,
            description="All automatically aligned sentence pairs with sentence splitting.",
        ),
        datasets.BuilderConfig(
            name="auto", version=VERSION, description="A large set of automatically aligned sentence pairs."
        ),
    ]

    DEFAULT_CONFIG_NAME = "auto"

    def _info(self):
        if self.config.name == "manual":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "alignment_label": datasets.ClassLabel(names=["notAligned", "aligned", "partialAligned"]),
                    "normal_sentence_id": datasets.Value("string"),
                    "simple_sentence_id": datasets.Value("string"),
                    "normal_sentence": datasets.Value("string"),
                    "simple_sentence": datasets.Value("string"),
                    "gleu_score": datasets.Value("float32"),
                }
            )
        elif (
            self.config.name == "auto_acl"
            or self.config.name == "auto_full_no_split"
            or self.config.name == "auto_full_with_split"
        ):
            features = datasets.Features(
                {
                    "normal_sentence": datasets.Value("string"),
                    "simple_sentence": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "example_id": datasets.Value("string"),
                    "normal": {
                        "normal_article_id": datasets.Value("int32"),
                        "normal_article_title": datasets.Value("string"),
                        "normal_article_url": datasets.Value("string"),
                        "normal_article_content": datasets.Sequence(
                            {
                                "normal_sentence_id": datasets.Value("string"),
                                "normal_sentence": datasets.Value("string"),
                            }
                        ),
                    },
                    "simple": {
                        "simple_article_id": datasets.Value("int32"),
                        "simple_article_title": datasets.Value("string"),
                        "simple_article_url": datasets.Value("string"),
                        "simple_article_content": datasets.Sequence(
                            {
                                "simple_sentence_id": datasets.Value("string"),
                                "simple_sentence": datasets.Value("string"),
                            }
                        ),
                    },
                    "paragraph_alignment": datasets.Sequence(
                        {
                            "normal_paragraph_id": datasets.Value("string"),
                            "simple_paragraph_id": datasets.Value("string"),
                        }
                    ),
                    "sentence_alignment": datasets.Sequence(
                        {
                            "normal_sentence_id": datasets.Value("string"),
                            "simple_sentence_id": datasets.Value("string"),
                        }
                    ),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/chaojiang06/wiki-auto",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        if self.config.name in ["manual", "auto"]:
            return [
                datasets.SplitGenerator(
                    name=spl,
                    gen_kwargs={
                        "filepaths": data_dir,
                        "split": spl,
                    },
                )
                for spl in data_dir
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name="full",
                    gen_kwargs={"filepaths": data_dir, "split": "full"},
                )
            ]

    def _generate_examples(self, filepaths, split):
        if self.config.name == "manual":
            keys = [
                "alignment_label",
                "simple_sentence_id",
                "normal_sentence_id",
                "simple_sentence",
                "normal_sentence",
                "gleu_score",
            ]
            with open(filepaths[split], encoding="utf-8") as f:
                for id_, line in enumerate(f):
                    values = line.strip().split("\t")
                    assert len(values) == 6, f"Not enough fields in ---- {line} --- {values}"
                    yield id_, dict(
                        [(k, val) if k != "gleu_score" else (k, float(val)) for k, val in zip(keys, values)]
                    )
        elif (
            self.config.name == "auto_acl"
            or self.config.name == "auto_full_no_split"
            or self.config.name == "auto_full_with_split"
        ):
            with open(filepaths["normal"], encoding="utf-8") as fi:
                with open(filepaths["simple"], encoding="utf-8") as fo:
                    for id_, (norm_se, simp_se) in enumerate(zip(fi, fo)):
                        yield id_, {
                            "normal_sentence": norm_se,
                            "simple_sentence": simp_se,
                        }
        else:
            dataset_dict = json.load(open(filepaths[split], encoding="utf-8"))
            for id_, (eid, example_dict) in enumerate(dataset_dict.items()):
                res = {
                    "example_id": eid,
                    "normal": {
                        "normal_article_id": example_dict["normal"]["id"],
                        "normal_article_title": example_dict["normal"]["title"],
                        "normal_article_url": example_dict["normal"]["url"],
                        "normal_article_content": {
                            "normal_sentence_id": [
                                sen_id for sen_id, sen_txt in example_dict["normal"]["content"].items()
                            ],
                            "normal_sentence": [
                                sen_txt for sen_id, sen_txt in example_dict["normal"]["content"].items()
                            ],
                        },
                    },
                    "simple": {
                        "simple_article_id": example_dict["simple"]["id"],
                        "simple_article_title": example_dict["simple"]["title"],
                        "simple_article_url": example_dict["simple"]["url"],
                        "simple_article_content": {
                            "simple_sentence_id": [
                                sen_id for sen_id, sen_txt in example_dict["simple"]["content"].items()
                            ],
                            "simple_sentence": [
                                sen_txt for sen_id, sen_txt in example_dict["simple"]["content"].items()
                            ],
                        },
                    },
                    "paragraph_alignment": {
                        "normal_paragraph_id": [
                            norm_id for simp_id, norm_id in example_dict.get("paragraph_alignment", [])
                        ],
                        "simple_paragraph_id": [
                            simp_id for simp_id, norm_id in example_dict.get("paragraph_alignment", [])
                        ],
                    },
                    "sentence_alignment": {
                        "normal_sentence_id": [
                            norm_id for simp_id, norm_id in example_dict.get("sentence_alignment", [])
                        ],
                        "simple_sentence_id": [
                            simp_id for simp_id, norm_id in example_dict.get("sentence_alignment", [])
                        ],
                    },
                }
                yield id_, res
