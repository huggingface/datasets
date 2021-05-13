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
"""Google Sentence Compression dataset"""


import gzip
import json

import datasets


_CITATION = """\
@inproceedings{filippova-altun-2013-overcoming,
    title = "Overcoming the Lack of Parallel Data in Sentence Compression",
    author = "Filippova, Katja  and
      Altun, Yasemin",
    booktitle = "Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing",
    month = oct,
    year = "2013",
    address = "Seattle, Washington, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D13-1155",
    pages = "1481--1491",
}
"""

_DESCRIPTION = """\
Large corpus of uncompressed and compressed sentences from news articles.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/sentence-compression"


_URLs = {
    datasets.Split.VALIDATION: [
        "https://github.com/google-research-datasets/sentence-compression/raw/master/data/comp-data.eval.json.gz"
    ],
    datasets.Split.TRAIN: [
        f"https://github.com/google-research-datasets/sentence-compression/raw/master/data/sent-comp.train{str(i).zfill(2)}.json.gz"
        for i in range(1, 11)
    ],
}


class SentComp(datasets.GeneratorBasedBuilder):
    """Google Setence Compression dataset"""

    def _info(self):
        node_features = {
            "form": datasets.Value("string"),
            "type": datasets.Value("string"),
            "mid": datasets.Value("string"),
            "word": datasets.features.Sequence(
                {
                    "id": datasets.Value("int32"),
                    "form": datasets.Value("string"),
                    "stem": datasets.Value("string"),
                    "tag": datasets.Value("string"),
                }
            ),
            "gender": datasets.Value("int32"),
            "head_word_index": datasets.Value("int32"),
        }
        compression_edge_features = {
            "parent_id": datasets.Value("int32"),
            "child_id": datasets.Value("int32"),
        }
        edge_features = {**compression_edge_features, "label": datasets.Value("string")}
        entity_features = {
            "start": datasets.Value("int32"),
            "end": datasets.Value("int32"),
            "head": datasets.Value("int32"),
            "name": datasets.Value("string"),
            "type": datasets.Value("string"),
            "mid": datasets.Value("string"),
            "is_proper_name_entity": datasets.Value("bool"),
            "gender": datasets.Value("int32"),
        }
        tree_features = {
            "id": datasets.Value("string"),
            "sentence": datasets.Value("string"),
            "node": datasets.features.Sequence(node_features),
            "edge": datasets.features.Sequence(edge_features),
            "entity_mention": datasets.features.Sequence(entity_features),
        }
        compression_features = {
            "text": datasets.Value("string"),
            "edge": datasets.features.Sequence(compression_edge_features),
        }

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "graph": tree_features,
                    "compression": compression_features,
                    "headline": datasets.Value("string"),
                    "compression_ratio": datasets.Value("float"),
                    "doc_id": datasets.Value("string"),
                    "source_tree": tree_features,
                    "compression_untransformed": compression_features,
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        return [
            datasets.SplitGenerator(
                name=split,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepaths": dl_manager.download(_URLs[split])},
            )
            for split in _URLs
        ]

    def _generate_examples(self, filepaths):
        """Yields examples."""
        id_ = -1
        for ix, filepath in enumerate(filepaths):
            with gzip.open(filepath, mode="rt", encoding="utf-8") as f:
                all_text = f.read()

            # in the data file, it's in the form of JSON objects, separated with '\n\n' characters
            # we'll format the file to be able to read with json package
            all_text = "[" + all_text + "]"
            all_text = all_text.replace("}\n\n{", "},\n{")

            samples = json.loads(all_text)
            for sample in samples:
                # add some default values
                for node in sample["graph"]["node"] + sample["source_tree"]["node"]:
                    if "type" not in node:
                        node["type"] = ""
                    if "mid" not in node:
                        node["mid"] = ""

                id_ += 1
                yield id_, sample
