# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""Introduction to AMTTL CWS Dataset"""

import logging

import datasets


_CITATION = """\
@inproceedings{xing2018adaptive,
  title={Adaptive multi-task transfer learning for Chinese word segmentation in medical text},
  author={Xing, Junjie and Zhu, Kenny and Zhang, Shaodian},
  booktitle={Proceedings of the 27th International Conference on Computational Linguistics},
  pages={3619--3630},
  year={2018}
}
"""

_DESCRIPTION = """\
Chinese word segmentation (CWS) trained from open source corpus faces dramatic performance drop
when dealing with domain text, especially for a domain with lots of special terms and diverse
writing styles, such as the biomedical domain. However, building domain-specific CWS requires
extremely high annotation cost. In this paper, we propose an approach by exploiting domain-invariant
knowledge from high resource to low resource domains. Extensive experiments show that our mode
achieves consistently higher accuracy than the single-task CWS and other transfer learning
baselines, especially when there is a large disparity between source and target domains.

This dataset is the accompanied medical Chinese word segmentation (CWS) dataset.
The tags are in BIES scheme.

For more details see https://www.aclweb.org/anthology/C18-1307/
"""

_URL = "https://raw.githubusercontent.com/adapt-sjtu/AMTTL/master/medical_data/"
_TRAINING_FILE = "forum_train.txt"
_DEV_FILE = "forum_dev.txt"
_TEST_FILE = "forum_test.txt"


class AmttlConfig(datasets.BuilderConfig):
    """BuilderConfig for AMTTL"""

    def __init__(self, **kwargs):
        """BuilderConfig for AMTTL.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(AmttlConfig, self).__init__(**kwargs)


class Amttl(datasets.GeneratorBasedBuilder):
    """AMTTL Chinese Word Segmentation dataset."""

    BUILDER_CONFIGS = [
        AmttlConfig(
            name="amttl",
            version=datasets.Version("1.0.0"),
            description="AMTTL medical Chinese word segmentation dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B",
                                "I",
                                "E",
                                "S",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/C18-1307/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            tags = []
            for line in f:
                line_stripped = line.strip()
                if line_stripped == "":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "tags": tags,
                        }
                        guid += 1
                        tokens = []
                        tags = []
                else:
                    splits = line_stripped.split("\t")
                    if len(splits) == 1:
                        splits.append("O")
                    tokens.append(splits[0])
                    tags.append(splits[1])
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "tags": tags,
            }
