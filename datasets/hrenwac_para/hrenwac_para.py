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
"""Croatian-English parallel corpus hrenWaC"""

import datasets


_CITATION = """
  @misc{11356/1058,
 title = {Croatian-English parallel corpus {hrenWaC} 2.0},
 author = {Ljube{\v s}i{\'c}, Nikola and Espl{\'a}-Gomis, Miquel and Ortiz Rojas, Sergio and Klubi{\v c}ka, Filip and Toral, Antonio},
 url = {http://hdl.handle.net/11356/1058},
 note = {Slovenian language resource repository {CLARIN}.{SI}},
 copyright = {{CLARIN}.{SI} User Licence for Internet Corpora},
 year = {2016} }
"""

_DESCRIPTION = """
The hrenWaC corpus version 2.0 consists of parallel Croatian-English texts crawled from the .hr top-level domain for Croatia.
The corpus was built with Spidextor (https://github.com/abumatran/spidextor), a tool that glues together the output of SpiderLing used for crawling and Bitextor used for bitext extraction. The accuracy of the extracted bitext on the segment level is around 80% and on the word level around 84%.
"""

_LICENSE = "CC BY-SA 3.0"

_HOMEPAGE = "http://nlp.ffzg.hr/resources/corpora/hrenwac/"
_URLS = "http://nlp.ffzg.hr/data/corpora/hrenwac/hrenwac.en-hr.txt.gz"


class HrenwacPara(datasets.GeneratorBasedBuilder):
    """Croatian-English parallel corpus hrenWaC"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="hrenWaC",
            version=VERSION,
            description="The hrenWaC dataset.",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"translation": datasets.features.Translation(languages=("en", "hr"))}),
            supervised_keys=("en", "hr"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download_and_extract({"train": _URLS})
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_file["train"],
                },
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf8") as f:
            en = ""
            hr = ""
            i = -1
            for id_, row in enumerate(f):
                if id_ % 3 == 0:
                    en = row.strip()
                if id_ % 3 == 1:
                    hr = row.strip()
                if id_ % 3 == 2:
                    i = i + 1
                    yield i, {
                        "translation": {
                            "en": en,
                            "hr": hr,
                        }
                    }
