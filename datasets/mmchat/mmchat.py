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
import os

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
    "mmchat": ["https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat.tgz"],
    "mmchat_hf": ["https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_hf.tgz"],
    "mmchat_raw": [
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split0.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split1.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split2.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split3.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split4.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split5.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split6.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split7.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_raw/MMChat_split8.tgz",
    ],
    "mmchat_lccc_filtered": [
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split0.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split1.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split2.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split3.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split4.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split5.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split6.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split7.tgz",
        "https://huggingface.co/datasets/silver/mmchat/resolve/main/mmchat_lccc_filtered/MMChat_lccc_flt_split8.tgz",
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
                        "dialog_files": [os.path.join(i, "dialog_train.jsonl") for i in data_dir],
                        "weibo_files": [os.path.join(i, "weibo_train.jsonl") for i in data_dir],
                        "img_files": [os.path.join(i, "img_url_train.jsonl") for i in data_dir],
                        "label_files": [],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "dialog_files": [os.path.join(i, "dialog_test.jsonl") for i in data_dir],
                        "weibo_files": [os.path.join(i, "weibo_test.jsonl") for i in data_dir],
                        "img_files": [os.path.join(i, "img_url_test.jsonl") for i in data_dir],
                        "label_files": [],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "dialog_files": [os.path.join(i, "dialog_dev.jsonl") for i in data_dir],
                        "weibo_files": [os.path.join(i, "weibo_dev.jsonl") for i in data_dir],
                        "img_files": [os.path.join(i, "img_url_dev.jsonl") for i in data_dir],
                        "label_files": [],
                    },
                ),
            ]
        elif self.config.name == "mmchat_hf":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "dialog_files": [os.path.join(i, "dialog.jsonl") for i in data_dir],
                        "weibo_files": [os.path.join(i, "weibo.jsonl") for i in data_dir],
                        "img_files": [os.path.join(i, "weibo_img_expanded_url.jsonl") for i in data_dir],
                        "label_files": [os.path.join(i, "human_annotation.jsonl") for i in data_dir],
                    },
                ),
            ]
        elif self.config.name == "mmchat_lccc_filtered":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "dialog_files": [os.path.join(i, "dialog_lccc_flt.jsonl") for i in data_dir],
                        "weibo_files": [os.path.join(i, "weibo_lccc_flt.jsonl") for i in data_dir],
                        "img_files": [os.path.join(i, "weibo_img_expanded_url_lccc_flt.jsonl") for i in data_dir],
                        "label_files": [],
                    },
                ),
            ]
        elif self.config.name == "mmchat_raw":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "dialog_files": [os.path.join(i, "dialog.jsonl") for i in data_dir],
                        "weibo_files": [os.path.join(i, "weibo.jsonl") for i in data_dir],
                        "img_files": [os.path.join(i, "weibo_img_expanded_url.jsonl") for i in data_dir],
                        "label_files": [],
                    },
                ),
            ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, dialog_files, weibo_files, img_files, label_files):
        id = 0
        assert len(dialog_files) == len(weibo_files) == len(img_files)
        if len(label_files) == 0:
            label_files = [None] * len(dialog_files)
        for dialog_file, weibo_file, img_file, label_file in zip(dialog_files, weibo_files, img_files, label_files):
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
                                    "dialog_image_related": True
                                    if label["dialog_image_relativeness"] == "1"
                                    else False,
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
