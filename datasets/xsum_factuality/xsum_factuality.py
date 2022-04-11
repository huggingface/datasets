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
"""XSum Hallucination Annotations: Faithfulness and factuality annotations of XSum summaries"""


import csv
import os

import datasets


_CITATION = """\
@InProceedings{maynez_acl20,
  author =      "Joshua Maynez and Shashi Narayan and Bernd Bohnet and Ryan Thomas Mcdonald",
  title =       "On Faithfulness and Factuality in Abstractive Summarization",
  booktitle =   "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
  year =        "2020",
  pages = "1906--1919",
  address = "Online",
}
"""

_DESCRIPTION = """\
Neural abstractive summarization models are highly prone to hallucinate content that is unfaithful to the input
document. The popular metric such as ROUGE fails to show the severity of the problem. The dataset consists of
faithfulness and factuality annotations of abstractive summaries for the XSum dataset. We have crowdsourced 3 judgements
 for each of 500 x 5 document-system pairs. This will be a valuable resource to the abstractive summarization community.
"""

_HOMEPAGE = "https://research.google/tools/datasets/xsum-hallucination-annotations/"

_LICENSE = "https://creativecommons.org/licenses/by/4.0/"

_URL = "https://raw.githubusercontent.com/google-research-datasets/xsum_hallucination_annotations/master/"
_URLs = {
    "factuality": _URL + "factuality_annotations_xsum_summaries.csv",
    "hallucination": _URL + "hallucination_annotations_xsum_summaries.csv",
}


class XsumFactualityConfig(datasets.BuilderConfig):
    """BuilderConfig for XsumFactuality"""

    def __init__(self, **kwargs):
        """BuilderConfig for XsumFactuality.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(XsumFactualityConfig, self).__init__(**kwargs)


class XsumFactuality(datasets.GeneratorBasedBuilder):
    """XSum Hallucination Annotations: Faithfulness and factuality annotations of XSum summaries"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        XsumFactualityConfig(
            name="xsum_factuality",
            version=datasets.Version("1.1.0"),
            description="Raters are shown the news article and the system summary, and are tasked with "
            "identifying and annotating the spans that aren't supported by the input article.",
        ),
        XsumFactualityConfig(
            name="xsum_faithfulness",
            version=datasets.Version("1.1.0"),
            description="Raters are shown the news article and the hallucinated system summary, and are "
            "tasked with assessing the summary whether it is factual or not.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "xsum_factuality"

    def _info(self):
        if self.config.name == "xsum_factuality":
            features = datasets.Features(
                {
                    "bbcid": datasets.Value("int32"),
                    "system": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "is_factual": datasets.ClassLabel(names=["no", "yes"]),
                    "worker_id": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "bbcid": datasets.Value("int32"),
                    "system": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "hallucination_type": datasets.ClassLabel(names=["intrinsic", "extrinsic"]),
                    "hallucinated_span_start": datasets.Value("int32"),
                    "hallucinated_span_end": datasets.Value("int32"),
                    "worker_id": datasets.Value("string"),
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

        data_dir = dl_manager.download_and_extract(_URLs)
        if self.config.name == "xsum_factuality":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir["factuality"]),
                        "split": "factuality",
                    },
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir["hallucination"]),
                        "split": "hallucination",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            f_csv = csv.reader(f, delimiter=",", quotechar='"')

            next(f_csv)
            for id_, data in enumerate(f_csv):

                if self.config.name == "xsum_factuality":
                    bbcid, system, summary, is_factual, worker_id = data

                    is_factual = -1 if is_factual == "NULL" else is_factual

                    yield id_, {
                        "bbcid": bbcid,
                        "system": system,
                        "summary": summary,
                        "is_factual": is_factual,
                        "worker_id": worker_id,
                    }
                else:
                    (
                        bbcid,
                        system,
                        summary,
                        hallucination_type,
                        hallucinated_span,
                        hallucinated_span_start,
                        hallucinated_span_end,
                        worker_id,
                    ) = data

                    hallucination_type = -1 if hallucination_type == "NULL" else hallucination_type

                    yield id_, {
                        "bbcid": bbcid,
                        "system": system,
                        "summary": summary,
                        "hallucination_type": hallucination_type,
                        "hallucinated_span_start": hallucinated_span_start,
                        "hallucinated_span_end": hallucinated_span_end,
                        "worker_id": worker_id,
                    }
