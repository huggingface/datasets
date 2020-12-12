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
"""Indo-Aryan Language Identification Shared Task Dataset"""

from __future__ import absolute_import, division, print_function

import datasets


_CITATION = """\
@proceedings{ws-2018-nlp-similar,
    title = "Proceedings of the Fifth Workshop on {NLP} for Similar Languages, Varieties and Dialects ({V}ar{D}ial 2018)",
    editor = {Zampieri, Marcos  and
      Nakov, Preslav  and
      Ljube{\v{s}}i{\'c}, Nikola  and
      Tiedemann, J{\"o}rg  and
      Malmasi, Shervin  and
      Ali, Ahmed},
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-3900",
}
"""

_DESCRIPTION = """\
This datasets in introduced as task which aimed at identifying 5 closely-related languages of Indo-Aryan language family – Hindi (also known as Khari Boli), Braj Bhasha, Awadhi, Bhojpuri and Magahi. These languages form part of a continuum starting from Western Uttar Pradesh (Hindi and Braj Bhasha) to Eastern Uttar Pradesh (Awadhi and Bhojpuri) and the neighbouring Eastern state of Bihar (Bhojpuri and Magahi). For this task, participants were provided with a dataset of approximately 15,000 sentences in each language, mainly from the domain of literature, published over the web as well as in print.
"""

_URL = "https://raw.githubusercontent.com/kmi-linguistics/vardial2018/master/dataset/{}.txt"


class Ilist(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"language_id": datasets.Value("string"), "text": datasets.Value("string")}),
            supervised_keys=None,
            homepage="https://github.com/kmi-linguistics/vardial2018",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        tr_file = dl_manager.download_and_extract(_URL.format("train"))
        tst_file = dl_manager.download_and_extract(_URL.format("gold"))
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
        """ Yields examples. """
        with open(filepath, "r", encoding="utf-8") as file:
            reader = file.read().split("\n")
            for idx, row in enumerate(reader):
                row = row.split("\t")
                if len(row) == 1:
                    continue
                yield idx, {"language_id": row[1], "text": row[0]}
