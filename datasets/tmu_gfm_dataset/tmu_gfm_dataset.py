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
"""TMU-GFM-Dataset."""


import csv

import datasets


_CITATION = """\
@inproceedings{yoshimura-etal-2020-reference,
    title = "{SOME}: Reference-less Sub-Metrics Optimized for Manual Evaluations of Grammatical Error Correction",
    author = "Yoshimura, Ryoma  and
      Kaneko, Masahiro  and
      Kajiwara, Tomoyuki  and
      Komachi, Mamoru",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.coling-main.573",
    pages = "6516--6522",
    abstract = "We propose a reference-less metric trained on manual evaluations of system outputs for grammatical error correction (GEC). Previous studies have shown that reference-less metrics are promising; however, existing metrics are not optimized for manual evaluations of the system outputs because no dataset of the system output exists with manual evaluation. This study manually evaluates outputs of GEC systems to optimize the metrics. Experimental results show that the proposed metric improves correlation with the manual evaluation in both system- and sentence-level meta-evaluation. Our dataset and metric will be made publicly available.",
}
"""

_DESCRIPTION = """\
A dataset for GEC metrics with manual evaluations of grammaticality, fluency, and meaning preservation for system outputs. \
More detail about the creation of the dataset can be found in Yoshimura et al. (2020).
"""

_HOMEPAGE = "https://github.com/tmu-nlp/TMU-GFM-Dataset"

_LICENSE = ""

_URLs = {
    "default": "https://raw.githubusercontent.com/tmu-nlp/TMU-GFM-Dataset/main/tmu-gfm-dataset.csv",
}


class TmuGfmDataset(datasets.GeneratorBasedBuilder):
    """TMU-GFM-Dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "source": datasets.Value("string"),
                "output": datasets.Value("string"),
                "grammer": datasets.Sequence(datasets.Value("int32")),
                "fluency": datasets.Sequence(datasets.Value("int32")),
                "meaning": datasets.Sequence(datasets.Value("int32")),
                "system": datasets.Value("string"),
                "ave_g": datasets.Value("float"),
                "ave_f": datasets.Value("float"),
                "ave_m": datasets.Value("float"),
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
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_url = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_url,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            data = csv.reader(f)
            _ = next(data)
            for id_, row in enumerate(data):
                yield id_, {
                    "source": row[0],
                    "output": row[1],
                    "grammer": row[2].split(","),
                    "fluency": row[3].split(","),
                    "meaning": row[4].split(","),
                    "system": row[5],
                    "ave_g": row[6],
                    "ave_f": row[7],
                    "ave_m": row[8],
                }
