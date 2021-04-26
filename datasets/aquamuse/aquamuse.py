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
"""AQuaMuSe is a novel scalable approach to automatically mine dual query based multi-document summarization datasets for extractive and abstractive summaries using question answering dataset (Google Natural Questions) and large document corpora (Common Crawl)"""


import os
from os import listdir
from os.path import isfile, join

import tensorflow as tf

import datasets


_CITATION = """\
@misc{kulkarni2020aquamuse,
      title={AQuaMuSe: Automatically Generating Datasets for Query-Based Multi-Document Summarization},
      author={Sayali Kulkarni and Sheide Chammas and Wan Zhu and Fei Sha and Eugene Ie},
      year={2020},
      eprint={2010.12694},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """AQuaMuSe is a novel scalable approach to automatically mine dual query based multi-document summarization datasets for extractive and abstractive summaries using question answering dataset (Google Natural Questions) and large document corpora (Common Crawl)"""

_HOMEPAGE = "https://github.com/google-research-datasets/aquamuse"

_LICENSE = ""

zipped_data_url = "https://github.com/google-research-datasets/aquamuse/raw/main/v2/aquamuse_v2.zip"


class Aquamuse(datasets.GeneratorBasedBuilder):
    """Dataset for Query-based Multi-Document Summarization"""

    VERSION = datasets.Version("2.3.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="abstractive", version=VERSION, description="Abstractive query-based multi-document summarization"
        ),
        datasets.BuilderConfig(
            name="extractive", version=VERSION, description="Extractive query-based multi-document summarization"
        ),
    ]

    # DEFAULT_CONFIG_NAME = "abstractive"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
            {
                "query": datasets.Value("string"),
                "input_urls": datasets.Sequence(datasets.Value("string")),
                "target": datasets.Value("string"),
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

        if self.config.name == "abstractive":
            data_dir = dl_manager.download_and_extract(zipped_data_url)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "v2.3/abstractive/train/"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "v2.3/abstractive/test/"),
                        "split": "test",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "v2.3/abstractive/dev/"),
                        "split": "dev",
                    },
                ),
            ]

        else:
            data_dir = dl_manager.download_and_extract(zipped_data_url)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "v2.3/extractive/train/"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "v2.3/extractive/test/"),
                        "split": "test",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "v2.3/extractive/dev/"),
                        "split": "dev",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        filepath = [join(filepath, f) for f in listdir(filepath) if isfile(join(filepath, f))]
        filepath = sorted(filepath)
        raw_dataset = tf.data.TFRecordDataset(filepath)
        for id_, raw_record in enumerate(raw_dataset):
            example = tf.train.Example()
            example.ParseFromString(raw_record.numpy())
            yield id_, {
                "query": example.features.feature["query"].bytes_list.value[0].decode(),
                "input_urls": example.features.feature["input_urls"].bytes_list.value[0].decode().split("<EOD>"),
                "target": example.features.feature["target"].bytes_list.value[0].decode(),
            }
