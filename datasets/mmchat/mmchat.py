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
MMChat is a large-scale dialogue dataset that contains image-grounded dialogues in Chinese.
Each dialogue in MMChat is associated with one or more images (maximum 9 images per dialogue).
We design various strategies to ensure the quality of the dialogues in MMChat.
"""

import json

import datasets


_CITATION = """\
@inproceedings{zheng2022MMChat,
author    = {Zheng, Yinhe and Chen, Guanyi and Liu, Xin and Sun, Jian},
title     = {MMChat: Multi-Modal Chat Dataset on Social Media},
booktitle = {Proceedings of The 13th Language Resources and Evaluation Conference},
year      = {2022},
publisher = {European Language Resources Association},
}

@inproceedings{wang2020chinese,
  title     = {A Large-Scale Chinese Short-Text Conversation Dataset},
  author    = {Wang, Yida and Ke, Pei and Zheng, Yinhe and Huang, Kaili and Jiang, Yong and Zhu, Xiaoyan and Huang, Minlie},
  booktitle = {NLPCC},
  year      = {2020},
  url       = {https://arxiv.org/abs/2008.03946}
}
"""

_DESCRIPTION = """\
MMChat is a large-scale dialogue dataset that contains image-grounded dialogues in Chinese.
Each dialogue in MMChat is associated with one or more images (maximum 9 images per dialogue).
We design various strategies to ensure the quality of the dialogues in MMChat.
"""

_HOMEPAGE = "https://github.com/silverriver/MMChat"

_LICENSE = "MIT"

_URLS = {
    "mmchat": {
        "train": [
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/dialog_train.jsonl.gz",
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/img_url_train.jsonl.gz",
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/weibo_train.jsonl.gz",
        ],
        "dev": [
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/dialog_dev.jsonl.gz",
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/img_url_dev.jsonl.gz",
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/weibo_dev.jsonl.gz",
        ],
        "test": [
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/dialog_test.jsonl.gz",
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/img_url_test.jsonl.gz",
            "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat/weibo_test.jsonl.gz",
        ],
    },
    "mmchat_hf": [
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_hf/dialog.jsonl.gz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_hf/weibo_img_expanded_url.jsonl.gz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_hf/weibo.jsonl.gz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_hf/human_annotation.jsonl.gz",
    ],
    "mmchat_raw": [
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/dialog_raw.jsonl.gz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/weibo_img_expanded_url_raw.jsonl.gz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/weibo_raw.jsonl.gz",
    ],
    "mmchat_lccc_filtered": [
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/dialog_lccc_flt.jsonl.gz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/weibo_img_expanded_url_lccc_flt.jsonl.gz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/weibo_lccc_flt.jsonl.gz",
    ],
}


class MMChat(datasets.GeneratorBasedBuilder):
    """Multi-Modal Chat Dataset."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="mmchat", version=VERSION, description="The MMChat dataset"),
        datasets.BuilderConfig(name="mmchat_hf", version=VERSION, description="Human filtered version of MMChat"),
        datasets.BuilderConfig(name="mmchat_raw", version=VERSION, description="Raw dialogues in MMChat"),
        datasets.BuilderConfig(name="mmchat_lccc_filtered", version=VERSION, description="LCCC filtered MMChat"),
    ]

    DEFAULT_CONFIG_NAME = "mmchat"

    def _info(self):
        if self.config.name in ["mmchat", "mmchat_raw", "mmchat_lccc_filtered"]:
            features = datasets.Features(
                {
                    "dialog": [datasets.Value("string")],
                    "weibo_content": datasets.Value("string"),
                    "imgs": [datasets.Value("string")],
                }
            )
        else:
            features = datasets.Features(
                {
                    "dialog": [datasets.Value("string")],
                    "weibo_content": datasets.Value("string"),
                    "imgs": [datasets.Value("string")],
                    "labels": {
                        "image_qualified": datasets.Value("bool"),
                        "dialog_qualified": datasets.Value("bool"),
                        "dialog_image_related": datasets.Value("bool"),
                    },
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
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)
        if self.config.name == "mmchat":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "dialog_file": data_dir["train"][0],
                        "weibo_file": data_dir["train"][2],
                        "img_file": data_dir["train"][1],
                        "label_file": None,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "dialog_file": data_dir["test"][0],
                        "weibo_file": data_dir["test"][2],
                        "img_file": data_dir["test"][1],
                        "label_file": None,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "dialog_file": data_dir["dev"][0],
                        "weibo_file": data_dir["dev"][2],
                        "img_file": data_dir["dev"][1],
                        "label_file": None,
                    },
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "dialog_file": data_dir[0],
                        "weibo_file": data_dir[2],
                        "img_file": data_dir[1],
                        "label_file": data_dir[3] if len(data_dir) == 4 else None,
                    },
                ),
            ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, dialog_file, weibo_file, img_file, label_file):
        id = 0
        if label_file is not None:
            label_f = open(label_file, encoding="utf-8")

        with open(dialog_file, encoding="utf-8") as dialog_f, open(weibo_file, encoding="utf-8") as weibo_f, open(
            img_file, encoding="utf-8"
        ) as img_f:
            while True:
                try:
                    dialog_line = dialog_f.readline().strip()
                    if len(dialog_line) == 0:
                        break
                    dialog = json.loads(dialog_line)  # dialog_f.readline())
                    weibo = json.loads(weibo_f.readline())
                    if self.config.name == "mmchat":
                        imgs = img_f.readline().strip().split(";")
                    else:
                        imgs = json.loads(img_f.readline())["weibo_img"].split(";")

                    if self.config.name == "mmchat_hf":
                        label = json.loads(label_f.readline())
                        # Yields examples as (key, example) tuples
                        yield id, {
                            "dialog": dialog,
                            "weibo_content": weibo,
                            "imgs": imgs,
                            "labels": {
                                "image_qualified": True if label["image_quality"] == "1" else False,
                                "dialog_qualified": True if label["dialog_quality"] == "1" else False,
                                "dialog_image_related": True if label["dialog_image_relativeness"] == "1" else False,
                            },
                        }
                    else:
                        yield id, {
                            "dialog": dialog,
                            "weibo_content": weibo,
                            "imgs": imgs,
                        }
                    id += 1
                except EOFError:
                    break
        if label_file is not None:
            label_f.close()
