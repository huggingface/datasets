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
"""Google Wellformed Query Dataset"""


import datasets


_CITATION = """\
@misc{faruqui2018identifying,
      title={Identifying Well-formed Natural Language Questions},
      author={Manaal Faruqui and Dipanjan Das},
      year={2018},
      eprint={1808.09419},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Google's query wellformedness dataset was created by crowdsourcing well-formedness annotations for 25,100 queries from the Paralex corpus. Every query was annotated by five raters each with 1/0 rating of whether or not the query is well-formed.
"""

_URL = "https://raw.githubusercontent.com/google-research-datasets/query-wellformedness/master/{}.tsv"


class GoogleWellformedQuery(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"rating": datasets.Value("float"), "content": datasets.Value("string")}),
            supervised_keys=None,
            homepage="https://github.com/google-research-datasets/query-wellformedness",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        tr_file = dl_manager.download_and_extract(_URL.format("train"))
        tst_file = dl_manager.download_and_extract(_URL.format("test"))
        dev_file = dl_manager.download_and_extract(_URL.format("dev"))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": tr_file,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": tst_file,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": dev_file,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, "r", encoding="utf-8") as file:
            reader = file.read().split("\n")
            for idx, row in enumerate(reader):
                row = row.split("\t")
                if len(row) == 1:
                    continue
                yield idx, {"rating": row[1], "content": row[0]}
