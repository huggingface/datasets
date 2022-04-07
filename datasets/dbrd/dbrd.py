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


import datasets
from datasets.tasks import TextClassification


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
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"files": dl_manager.iter_archive(archive), "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"files": dl_manager.iter_archive(archive), "split": "test"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split("unsupervised"),
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split": "unsup", "labeled": False},
            ),
        ]

    def _generate_examples(self, files, split, labeled=True):
        """Generate DBRD examples."""
        # For labeled examples, extract the label from the path.
        if labeled:
            for path, f in files:
                if path.startswith(f"DBRD/{split}"):
                    label = {"pos": 1, "neg": 0}[path.split("/")[2]]
                    yield path, {"text": f.read().decode("utf-8"), "label": label}
        else:
            for path, f in files:
                if path.startswith(f"DBRD/{split}"):
                    yield path, {"text": f.read().decode("utf-8"), "label": -1}
