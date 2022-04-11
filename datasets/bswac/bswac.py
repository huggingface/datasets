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
"""Bosnian web corpus bsWaC 1.1"""

import datasets


_CITATION = """
 @misc{11356/1062,
 title = {Bosnian web corpus {bsWaC} 1.1},
 author = {Ljube{\v s}i{\'c}, Nikola and Klubi{\v c}ka, Filip},
 url = {http://hdl.handle.net/11356/1062},
 note = {Slovenian language resource repository {CLARIN}.{SI}},
 copyright = {Creative Commons - Attribution-{ShareAlike} 4.0 International ({CC} {BY}-{SA} 4.0)},
 year = {2016} }
"""

_DESCRIPTION = """\
The Bosnian web corpus bsWaC was built by crawling the .ba top-level domain in 2014. The corpus was near-deduplicated on paragraph level, normalised via diacritic restoration, morphosyntactically annotated and lemmatised. The corpus is shuffled by paragraphs. Each paragraph contains metadata on the URL, domain and language identification (Bosnian vs. Croatian vs. Serbian).

Version 1.0 of this corpus is described in http://www.aclweb.org/anthology/W14-0405. Version 1.1 contains newer and better linguistic annotations.
"""

_LICENSE = "CC BY-SA 4.0"

_HOMEPAGE = "http://nlp.ffzg.hr/resources/corpora/bswac/"
_URLS = [
    "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1062/bsWaC1.1.01.xml.gz",
    "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1062/bsWaC1.1.02.xml.gz",
    "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1062/bsWaC1.1.03.xml.gz",
]


class Bswac(datasets.GeneratorBasedBuilder):
    """Bosnian web corpus bsWaC"""

    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="bswac",
            version=VERSION,
            description="The bsWac dataset.",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_file,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        for file_idx, fp in enumerate(filepath):
            with open(fp, encoding="utf8") as f:
                for row_idx, row in enumerate(f):
                    yield f"{file_idx}_{row_idx}", {
                        "sentence": row.strip(),
                    }
