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
"""FewRel Dataset."""


import json

import datasets


_CITATION = """@inproceedings{han-etal-2018-fewrel,
    title = "{F}ew{R}el: A Large-Scale Supervised Few-Shot Relation Classification Dataset with State-of-the-Art Evaluation",
    author = "Han, Xu and Zhu, Hao and Yu, Pengfei and Wang, Ziyun and Yao, Yuan and Liu, Zhiyuan and Sun, Maosong",
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
    month = oct # "-" # nov,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D18-1514",
    doi = "10.18653/v1/D18-1514",
    pages = "4803--4809"
}

@inproceedings{gao-etal-2019-fewrel,
    title = "{F}ew{R}el 2.0: Towards More Challenging Few-Shot Relation Classification",
    author = "Gao, Tianyu and Han, Xu and Zhu, Hao and Liu, Zhiyuan and Li, Peng and Sun, Maosong and Zhou, Jie",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1649",
    doi = "10.18653/v1/D19-1649",
    pages = "6251--6256"
}
"""

_DESCRIPTION = """\
FewRel is a large-scale few-shot relation extraction dataset, which contains more than one hundred relations and tens of thousands of annotated instances cross different domains.
"""

_HOMEPAGE = "https://thunlp.github.io/"

_LICENSE = "https://raw.githubusercontent.com/thunlp/FewRel/master/LICENSE"

DATA_URL = "https://raw.githubusercontent.com/thunlp/FewRel/master/data/"
_URLs = {
    "train_wiki": DATA_URL + "train_wiki.json",
    "val_nyt": DATA_URL + "val_nyt.json",
    "val_pubmed": DATA_URL + "val_pubmed.json",
    "val_semeval": DATA_URL + "val_semeval.json",
    "val_wiki": DATA_URL + "val_wiki.json",
    "pid2name": DATA_URL + "pid2name.json",
    "pubmed_unsupervised": DATA_URL + "pubmed_unsupervised.json",
}


class FewRel(datasets.GeneratorBasedBuilder):
    """The FewRelDataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="default", version=VERSION, description="This covers the entire FewRel dataset."),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "relation": datasets.Value("string"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "head": {
                    "text": datasets.Value("string"),
                    "type": datasets.Value("string"),
                    "indices": datasets.Sequence(datasets.Sequence(datasets.Value("int64"))),
                },
                "tail": {
                    "text": datasets.Value("string"),
                    "type": datasets.Value("string"),
                    "indices": datasets.Sequence(datasets.Sequence(datasets.Value("int64"))),
                },
                "names": datasets.Sequence(datasets.Value("string"))
                # These are the features of your dataset like images, labels ...
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split(key),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir[key],
                    "pid2name": data_dir["pid2name"],
                    "return_names": key in ["train_wiki", "val_wiki", "val_nyt"],
                },
            )
            for key in data_dir.keys()
            if key != "pid2name"
        ]

    def _generate_examples(self, filepath, pid2name, return_names):
        """Yields examples."""
        pid2name_dict = {}
        with open(pid2name, encoding="utf-8") as f:
            data = json.load(f)
        for key in list(data.keys()):
            name_1 = data[key][0]
            name_2 = data[key][1]
            pid2name_dict[key] = [name_1, name_2]

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            id = 0
            for key in list(data.keys()):
                for items in data[key]:
                    tokens = items["tokens"]
                    h_0 = items["h"][0]
                    h_1 = items["h"][1]
                    h_2 = items["h"][2]
                    t_0 = items["t"][0]
                    t_1 = items["t"][1]
                    t_2 = items["t"][2]
                    id += 1
                    yield id, {
                        "relation": key,
                        "tokens": tokens,
                        "head": {"text": h_0, "type": h_1, "indices": h_2},
                        "tail": {"text": t_0, "type": t_1, "indices": t_2},
                        "names": pid2name_dict[key]
                        if return_names
                        else [
                            key,
                        ],
                    }
        else:  # For `pubmed_unsupervised.json`
            id = 0
            for items in data:
                tokens = items["tokens"]
                h_0 = items["h"][0]
                h_1 = items["h"][1]
                h_2 = items["h"][2]
                t_0 = items["t"][0]
                t_1 = items["t"][1]
                t_2 = items["t"][2]
                id += 1
                yield id, {
                    "relation": "",
                    "tokens": tokens,
                    "head": {"text": h_0, "type": h_1, "indices": h_2},
                    "tail": {"text": t_0, "type": t_1, "indices": t_2},
                    "names": [
                        "",
                    ],
                }
