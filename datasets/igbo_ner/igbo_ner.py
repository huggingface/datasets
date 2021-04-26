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
"""Igbo Named Entity Recognition Dataset"""


import datasets


_CITATION = """\
@misc{ezeani2020igboenglish,
    title={Igbo-English Machine Translation: An Evaluation Benchmark},
    author={Ignatius Ezeani and Paul Rayson and Ikechukwu Onyenwe and Chinedu Uchechukwu and Mark Hepple},
    year={2020},
    eprint={2004.00648},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Igbo Named Entity Recognition Dataset
"""

_HOMEPAGE = "https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_ner"

_URLs = {
    "ner_data": "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_ner/igbo_data.txt",
    "free_text": "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_ner/igbo_data10000.txt",
}


class IgboNer(datasets.GeneratorBasedBuilder):
    """Dataset from the Igbo NER Project"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="ner_data",
            version=VERSION,
            description="This dataset contains the named entity and all the sentences containing that entity.",
        ),
        datasets.BuilderConfig(
            name="free_text", version=VERSION, description="This dataset contains all sentences used for NER."
        ),
    ]

    DEFAULT_CONFIG_NAME = "ner_data"

    def _info(self):
        if self.config.name == "ner_data":
            features = datasets.Features(
                {
                    "content_n": datasets.Value("string"),
                    "named_entity": datasets.Value("string"),
                    "sentences": datasets.Sequence(datasets.Value("string")),
                }
            )
        else:
            features = datasets.Features(
                {
                    "sentences": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        dictionary = {}
        with open(filepath, "r", encoding="utf-8-sig") as f:
            if self.config.name == "ner_data":
                for id_, row in enumerate(f):
                    row = row.strip().split("\t")
                    content_n = row[0]
                    if content_n in dictionary.keys():
                        (dictionary[content_n]["sentences"]).append(row[1])
                    else:
                        dictionary[content_n] = {}
                        dictionary[content_n]["named_entity"] = row[1]
                        dictionary[content_n]["sentences"] = [row[1]]
                    yield id_, {
                        "content_n": content_n,
                        "named_entity": dictionary[content_n]["named_entity"],
                        "sentences": dictionary[content_n]["sentences"],
                    }
            else:
                for id_, row in enumerate(f):
                    yield id_, {
                        "sentences": row.strip(),
                    }
