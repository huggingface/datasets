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
"""TODO: Add a description here."""


import os
from collections import namedtuple

import datasets


_CITATION = """\
@inproceedings{Toutanova2016ADA,
  title={A Dataset and Evaluation Metrics for Abstractive Compression of Sentences and Short Paragraphs},
  author={Kristina Toutanova and Chris Brockett and Ke M. Tran and Saleema Amershi},
  booktitle={EMNLP},
  year={2016}
}
"""

_DESCRIPTION = """\
This dataset contains sentences and short paragraphs with corresponding shorter (compressed) versions. There are up to five compressions for each input text, together with quality judgements of their meaning preservation and grammaticality. The dataset is derived using source texts from the Open American National Corpus (ww.anc.org) and crowd-sourcing.
"""

_HOMEPAGE = "https://msropendata.com/datasets/f8ce2ec9-7fbd-48f7-a8bb-2d2279373563"

_LICENSE = "Microsoft Research Data License Agreement"


_SOURCE_LABELS = ["source_id", "domain", "source_text"]
_COMPRESSION_LABELS = ["compressed_text", "judge_id", "num_ratings", "ratings"]
SourceInfo = namedtuple("SourceInfo", _SOURCE_LABELS)
CompressionInfo = namedtuple("CompressionInfo", _COMPRESSION_LABELS)


class MsrTextCompression(datasets.GeneratorBasedBuilder):
    """This dataset contains sentences and short paragraphs with corresponding shorter (compressed) versions. There are up to five compressions for each input text, together with quality judgements of their meaning preservation and grammaticality. The dataset is derived using source texts from the Open American National Corpus (ww.anc.org) and crowd-sourcing."""

    VERSION = datasets.Version("1.1.0")
    _ENCODING = "utf-8-sig"

    @property
    def manual_download_instructions(self):
        return """\
  You should download the dataset from https://www.microsoft.com/en-us/download/details.aspx?id=54262
  The webpage requires registration.
  Unzip and please put the files from the extracted RawData folder under the following names
  train.tsv, valid.tsv, and test.tsv in a dir of your choice,
  which will be used as a manual_dir, e.g. `~/.manual_dir/msr_text_compression`
  The data can then be loaded via:
  `datasets.load_dataset("msr_text_compression", data_dir="~/.manual_dir/msr_text_compression")`.
  """

    def _info(self):

        # Define features
        source = {k: datasets.Value("string") for k in _SOURCE_LABELS}
        target = {
            "compressed_text": datasets.Value("string"),
            "judge_id": datasets.Value("string"),
            "num_ratings": datasets.Value("int64"),
            "ratings": datasets.Sequence(datasets.Value("int64")),
        }
        targets = {"targets": datasets.Sequence(target)}
        feature_dict = {**source, **targets}

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(feature_dict),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('msr_text_compression', data_dir=...)` per the manual download instructions: {self.manual_download_instructions}"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"input_file": os.path.join(data_dir, "train.tsv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"input_file": os.path.join(data_dir, "valid.tsv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"input_file": os.path.join(data_dir, "test.tsv")},
            ),
        ]

    def _parse_source(self, s):
        source_id, domain, text = [x.strip() for x in s.split("\t")]
        return SourceInfo(source_id, domain, text)._asdict()

    def _parse_ratings(self, num_ratings, ratings):
        """Parses raw ratings into list of ints
        Args:
            num_ratings: int
            ratings: List[str]
        Returns:
            List[int] with len == num_ratings
        """

        # ratings contains both numeric ratings (actual ratings) and qualitative descriptions
        # we only wish to keep the numeric ratings
        assert num_ratings * 2 == len(ratings)

        return [int(r) for r in ratings[:: len(ratings) // num_ratings]]

    def _parse_target(self, target):
        text, judge, num_ratings, *ratings = [t.strip() for t in target.split("\t")]
        num_ratings = int(num_ratings)
        ratings = self._parse_ratings(num_ratings, ratings)
        return CompressionInfo(text, judge, num_ratings, ratings)._asdict()

    def _generate_examples(self, input_file):
        """Yields examples.

        Files are encoded with BOM markers, hence the use of utf-8-sig as codec
        """
        with open(input_file, encoding=self._ENCODING) as f:
            for id_, line in enumerate(f):
                source_info, *targets_info = line.split("|||")

                source = self._parse_source(source_info)
                targets = {"targets": [self._parse_target(target) for target in targets_info]}

                yield id_, {**source, **targets}
