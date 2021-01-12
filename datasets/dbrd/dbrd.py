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
"""Dutch Book Review Dataset"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_DESCRIPTION = """\
The Dutch Book Review Dataset (DBRD) contains over 110k book reviews of which \
22k have associated binary sentiment polarity labels. It is intended as a \
benchmark for sentiment classification in Dutch and created due to a lack of \
annotated datasets in Dutch that are suitable for this task.
"""

_CITATION = """\
@article{DBLP:journals/corr/abs-1910-00896,
  author    = {Benjamin van der Burgh and
               Suzan Verberne},
  title     = {The merits of Universal Language Model Fine-tuning for Small Datasets
               - a case with Dutch book reviews},
  journal   = {CoRR},
  volume    = {abs/1910.00896},
  year      = {2019},
  url       = {http://arxiv.org/abs/1910.00896},
  archivePrefix = {arXiv},
  eprint    = {1910.00896},
  timestamp = {Fri, 04 Oct 2019 12:28:06 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1910-00896.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DOWNLOAD_URL = "https://github.com/benjaminvdb/DBRD/releases/download/v3.0/DBRD_v3.tgz"


class DBRDConfig(datasets.BuilderConfig):
    """BuilderConfig for DBRD."""

    def __init__(self, **kwargs):
        """BuilderConfig for DBRD.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(DBRDConfig, self).__init__(version=datasets.Version("3.0.0", ""), **kwargs)


class DBRD(datasets.GeneratorBasedBuilder):
    """Dutch Book Review Dataset."""

    BUILDER_CONFIGS = [
        DBRDConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"text": datasets.Value("string"), "label": datasets.features.ClassLabel(names=["neg", "pos"])}
            ),
            supervised_keys=None,
            homepage="https://github.com/benjaminvdb/DBRD",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, archive):
        for _, ex in self._generate_examples(archive, os.path.join("DBRD", "train")):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "DBRD")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"directory": os.path.join(data_dir, "train")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"directory": os.path.join(data_dir, "test")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split("unsupervised"),
                gen_kwargs={"directory": os.path.join(data_dir, "unsup"), "labeled": False},
            ),
        ]

    def _generate_examples(self, directory, labeled=True):
        """Generate DBRD examples."""
        # For labeled examples, extract the label from the path.
        if labeled:
            files = {
                "pos": sorted(os.listdir(os.path.join(directory, "pos"))),
                "neg": sorted(os.listdir(os.path.join(directory, "neg"))),
            }
            for key in files:
                for id_, file in enumerate(files[key]):
                    filepath = os.path.join(directory, key, file)
                    with open(filepath, encoding="UTF-8") as f:
                        yield key + "_" + str(id_), {"text": f.read(), "label": key}
        else:
            unsup_files = sorted(os.listdir(directory))
            for id_, file in enumerate(unsup_files):
                filepath = os.path.join(directory, file)
                with open(filepath, encoding="UTF-8") as f:
                    yield id_, {"text": f.read(), "label": -1}
