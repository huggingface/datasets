# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""TODO(scicite): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """
@InProceedings{Cohan2019Structural,
  author={Arman Cohan and Waleed Ammar and Madeleine Van Zuylen and Field Cady},
  title={Structural Scaffolds for Citation Intent Classification in Scientific Publications},
  booktitle={NAACL},
  year={2019}
}
"""

_DESCRIPTION = """
This is a dataset for classifying citation intents in academic papers.
The main citation intent label for each Json object is specified with the label
key while the citation context is specified in with a context key. Example:
{
 'string': 'In chacma baboons, male-infant relationships can be linked to both
    formation of friendships and paternity success [30,31].'
 'sectionName': 'Introduction',
 'label': 'background',
 'citingPaperId': '7a6b2d4b405439',
 'citedPaperId': '9d1abadc55b5e0',
 ...
 }
You may obtain the full information about the paper using the provided paper ids
with the Semantic Scholar API (https://api.semanticscholar.org/).
The labels are:
Method, Background, Result
"""

_SOURCE_NAMES = ["properNoun", "andPhrase", "acronym", "etAlPhrase", "explicit", "acronymParen", "nan"]


class Scicite(datasets.GeneratorBasedBuilder):
    """This is a dataset for classifying citation intents in academic papers."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "string": datasets.Value("string"),
                    "sectionName": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["method", "background", "result"]),
                    "citingPaperId": datasets.Value("string"),
                    "citedPaperId": datasets.Value("string"),
                    "excerpt_index": datasets.Value("int32"),
                    "isKeyCitation": datasets.Value("bool"),
                    "label2": datasets.features.ClassLabel(
                        names=["supportive", "not_supportive", "cant_determine", "none"]
                    ),
                    "citeEnd": datasets.Value("int64"),
                    "citeStart": datasets.Value("int64"),
                    "source": datasets.features.ClassLabel(names=_SOURCE_NAMES),
                    "label_confidence": datasets.Value("float32"),
                    "label2_confidence": datasets.Value("float32"),
                    "id": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/allenai/scicite",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_paths = dl_manager.download_and_extract(
            {
                "scicite": "https://s3-us-west-2.amazonaws.com/ai2-s2-research/scicite/scicite.tar.gz",
            }
        )
        path = os.path.join(dl_paths["scicite"], "scicite")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"path": os.path.join(path, "train.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"path": os.path.join(path, "dev.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"path": os.path.join(path, "test.jsonl")},
            ),
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(path, encoding="utf-8") as f:
            unique_ids = {}
            for line in f:
                d = json.loads(line)
                unique_id = str(d["unique_id"])
                if unique_id in unique_ids:
                    continue
                unique_ids[unique_id] = True
                yield unique_id, {
                    "string": d["string"],
                    "label": str(d["label"]),
                    "sectionName": str(d["sectionName"]),
                    "citingPaperId": str(d["citingPaperId"]),
                    "citedPaperId": str(d["citedPaperId"]),
                    "excerpt_index": int(d["excerpt_index"]),
                    "isKeyCitation": bool(d["isKeyCitation"]),
                    "label2": str(d.get("label2", "none")),
                    "citeEnd": _safe_int(d["citeEnd"]),
                    "citeStart": _safe_int(d["citeStart"]),
                    "source": str(d["source"]),
                    "label_confidence": float(d.get("label_confidence", 0.0)),
                    "label2_confidence": float(d.get("label2_confidence", 0.0)),
                    "id": str(d["id"]),
                }


def _safe_int(a):
    try:
        # skip NaNs
        return int(a)
    except ValueError:
        return -1
