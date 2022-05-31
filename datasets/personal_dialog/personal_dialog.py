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
"""
The PersonalDialog dataset is a large-scale multi-turn Chinese dialogue dataset containing various traits from a large number of speakers. 
We are releasing about 5M sessions of carefully filtered dialogues.
Each utterance in PersonalDialog is associated with a speaker marked with traits like Gender, Location, Interest Tags. 
"""

import json
import datasets


_CITATION = """\
@article{zheng2019personalized,
  title   = {Personalized dialogue generation with diversified traits},
  author  = {Zheng, Yinhe and Chen, Guanyi and Huang, Minlie and Liu, Song and Zhu, Xuan},
  journal = {arXiv preprint arXiv:1901.09672},
  year    = {2019}
}

@inproceedings{zheng2020pre,
  title     = {A pre-training based personalized dialogue generation model with persona-sparse data},
  author    = {Zheng, Yinhe and Zhang, Rongsheng and Huang, Minlie and Mao, Xiaoxi},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  volume    = {34},
  number    = {05},
  pages     = {9693--9700},
  year      = {2020}
}
"""

_DESCRIPTION = """\
The PersonalDialog dataset is a large-scale multi-turn Chinese dialogue dataset containing various traits from a large number of speakers. 
We are releasing about 5M sessions of carefully filtered dialogues.
Each utterance in PersonalDialog is associated with a speaker marked with traits like Gender, Location, Interest Tags. 
"""

_HOMEPAGE = "https://github.com/silverriver/PersonalDilaog"

_LICENSE = "MIT"

_URLS = {
    "train": "https://huggingface.co/datasets/silver/personal_dialog/resolve/main/dialogues_train.jsonl.gz",
    "valid": [
        "https://huggingface.co/datasets/silver/personal_dialog/resolve/main/dev_biased.jsonl.gz",
        "https://huggingface.co/datasets/silver/personal_dialog/resolve/main/dev_random.jsonl.gz",
    ],
    "test": [
        "https://huggingface.co/datasets/silver/personal_dialog/resolve/main/test_biased.jsonl.gz",
        "https://huggingface.co/datasets/silver/personal_dialog/resolve/main/test_random.jsonl.gz",
    ],
}


class PersonalDialog(datasets.GeneratorBasedBuilder):
    """Chinese Dialogues with Personal Traits."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "dialog": [datasets.Value("string")],
                "profile": [{
                    "tag": [datasets.Value("string")],
                    "loc": datasets.Value("string"),
                    "gender": datasets.Value("string"),
                }],
                "uid": [datasets.Value("int32")],
                "responder_profile": {
                    "tag": [datasets.Value("string")],
                    "loc": datasets.Value("string"),
                    "gender": datasets.Value("string"),
                },
                "golden_response": datasets.Value("string"),
                "is_biased": datasets.Value("bool")
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
        urls = _URLS
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_files": [data_dir['train']],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_files": [data_dir['valid'][0], data_dir['valid'][1]],
                    "split": "valid",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_files": [data_dir['test'][0], data_dir['test'][1]],
                    "split": "test",
                },
            ),
        ]


    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, data_files, split):
        id = 0
        for file_i, data_file in enumerate(data_files):
            with open(data_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if len(line) == 0: continue
                    line = json.loads(line)

                    profile = [{
                        "tag": i["tag"][0].split(";"), 
                        "loc": i["loc"], "gender": i["gender"]} for i in line["profile"]]
                    dialog = [i[0] for i in line["dialog"]]

                    if split == "train":
                        yield id, {
                            "dialog": dialog,
                            "profile": profile,
                            "uid": line['uid'],
                            "responder_profile": None,
                            "golden_response": None,
                            "is_biased": None,

                        }
                    else:
                        yield id, {
                            "dialog": dialog,
                            "profile": profile,
                            "uid": line['uid'],
                            "responder_profile": {
                                "tag": line["responder_profile"]["tag"][0].split(";"),
                                "loc": line["responder_profile"]["loc"],
                                "gender": line["responder_profile"]["gender"]
                            },
                            "golden_response": line["golden_response"][0],
                            "is_biased": True if file_i == 0 else False,
                        }
                    id += 1
