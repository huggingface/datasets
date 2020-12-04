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
"""TupleInf Open IE Dataset"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@article{Khot2017AnsweringCQ,
  title={Answering Complex Questions Using Open Information Extraction},
  author={Tushar Khot and A. Sabharwal and Peter Clark},
  journal={ArXiv},
  year={2017},
  volume={abs/1704.05572}
}
"""

_DESCRIPTION = """\
The TupleInf Open IE dataset contains Open IE tuples extracted from 263K sentences that were used by the solver \
in “Answering Complex Questions Using Open Information Extraction” (referred as Tuple KB, T). \
These sentences were collected from a large Web corpus using training questions from 4th and 8th grade as queries. \
This dataset contains 156K sentences collected for 4th grade questions and 107K sentences for 8th grade questions. \
Each sentence is followed by the Open IE v4 tuples using their simple format.
"""

_HOMEPAGE = "https://allenai.org/data/tuple-ie"

_URL = "https://ai2-datasets.s3-us-west-2.amazonaws.com/tuple-ie/TupleInfKB.zip"

_DOMAIN_FILES = {"4th_grade": "4thGradeOpenIE.txt", "8th_grade": "8thGradeOpenIE.txt"}


class TupleIEConfig(datasets.BuilderConfig):
    """BuilderConfig for TupleIE"""

    def __init__(self, *args, domains=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.domains = domains


class TupleIE(datasets.GeneratorBasedBuilder):
    """TupleInf Open IE Dataset"""

    BUILDER_CONFIGS = [
        TupleIEConfig(
            name="all",
            domains=list(_DOMAIN_FILES.keys()),
            description="collected using training questions from 4th and 8th grade as queries.",
        )
    ] + [
        TupleIEConfig(
            name=name, domains=[name], description=f"collected using training questions from {name} as queries."
        )
        for name in _DOMAIN_FILES.keys()
    ]
    BUILDER_CONFIG_CLASS = TupleIEConfig
    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "tuples": datasets.features.Sequence(
                        {
                            "score": datasets.Value("float"),
                            "tuple_text": datasets.Value("string"),
                            "context": datasets.Value("string"),
                            "arg1": datasets.Value("string"),
                            "rel": datasets.Value("string"),
                            "arg2s": datasets.features.Sequence(datasets.Value("string")),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.join(dl_manager.download_and_extract(_URL), "TupleInfKB")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_dir": data_dir},
            )
        ]

    def _generate_examples(self, data_dir):
        """ Yields examples. """
        id_ = -1
        for domain in self.config.domains:
            with open(os.path.join(data_dir, _DOMAIN_FILES[domain]), encoding="utf-8") as f:
                all_text = f.read()
            samples = all_text.split("\n\n")
            for sample in samples:
                rows = sample.split("\n")
                item = {"sentence": rows[0], "tuples": []}
                tuple_lines = rows[1:]
                for tuple_line in tuple_lines:
                    score, tuple_text = tuple_line.split(" ", 1)
                    context, arg1, rel, arg2s = self._decode_tuple_text(tuple_text)
                    item["tuples"].append(
                        {
                            "score": score,
                            "tuple_text": tuple_text,
                            "context": context,
                            "arg1": arg1,
                            "rel": rel,
                            "arg2s": arg2s,
                        }
                    )
                id_ += 1
                yield id_, item

    def _decode_tuple_text(self, tuple_text):
        """Decompose the tuple text into arguments and relations

        Args:
            tuple_text (str): Format of extraction text:
            .. code-block::
                {Context(<context>):}(<arg1>; <rel>; {[L|T]:}<arg2_1>; {[L|T]:}<arg2_2>; ...)

        .. note::
            * ``{}`` means one can be optionally appear
            * ``[L|T]`` means ``L`` or ``T``
            * ``L`` means spatial/location argument
            * ``T`` means temporal argument
            * We can have multiple arg2s
        """
        context = ""
        arg1 = ""
        rel = ""
        arg2s = []
        if tuple_text.startswith("Context("):
            context, tuple_text = tuple_text.split(":", 1)
            context = context[len("Context(") : -1]

        args = tuple_text[1:-1].split("; ")
        arg1, rel = args[:2]
        arg2s = args[2:]
        return context, arg1, rel, arg2s
