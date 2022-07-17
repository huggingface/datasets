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
"""MANtIS: a novel Multi-Domain Information Seeking Dialogues Dataset"""


import json
import os

from yarl import URL

import datasets


_CITATION = """\
@misc{penha2019mantis,
    title={Introducing MANtIS: a novel Multi-Domain Information Seeking Dialogues Dataset},
    author={Gustavo Penha, Alexandru Balan and Claudia Hauff},
    year={2019},
    eprint={1912.04639},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
MANtIS is a multi-domain dialogue dataset containing more than 80000 information-seeking
conversations from the community question-answering portal Stack Exchange. Unlike previous
information-seeking dialogue datasets that focus on only one domain, MANtIS has diverse
conversations from 14 different sites, such as physics, travel and worldbuilding. Additionaly,
all dialogues have a url, providing grounding to the conversations. It can be used for the
following tasks: conversation response ranking/generation and user intent prediction.
"""

_HOMEPAGE = "https://guzpenha.github.io/MANtIS/"

_LICENSE = ""

_URL = "https://drive.google.com/uc?id=1cWEbTC4klLQDLej--IG2OAZIT4AX549A&export=download"


class Mantis(datasets.GeneratorBasedBuilder):
    """MANtIS is a multi-domain dialogue dataset containing information-seeking conversations"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "category": datasets.Value("string"),
                "title": datasets.Value("string"),
                "dialog_time": datasets.Value("string"),
                "utterances": [
                    {
                        "utterance": datasets.Value("string"),
                        "actor_type": datasets.Value("string"),
                        "utterance_time": datasets.Value("string"),
                        "is_answer": datasets.Value("bool"),
                        "id": datasets.Value("string"),
                        "votes": datasets.Value("int32"),
                        "utterance_pos": datasets.Value("int32"),
                        "user_name": datasets.Value("string"),
                    }
                ],
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "merged_train.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "merged_test.json"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "merged_dev.json"),
                    "split": "dev",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key, row in data.items():
                utterances = []
                for val in row["utterances"]:
                    utterances.append(
                        {
                            "utterance": val["utterance"],
                            "actor_type": val["actor_type"],
                            "utterance_time": val["utterance_time"],
                            "is_answer": val["is_answer"],
                            "id": val["id"],
                            "votes": val["votes"],
                            "utterance_pos": val["utterance_pos"],
                            "user_name": val["user_name"],
                        }
                    )

                yield key, {
                    "id": key,
                    "category": row["category"],
                    "title": row["title"],
                    "dialog_time": row["dialog_time"],
                    "utterances": utterances,
                }
