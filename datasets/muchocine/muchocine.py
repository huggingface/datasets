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


import glob
import os
import re
from xml.dom.minidom import parseString

import datasets


# no BibTeX citation
_CITATION = ""

_DESCRIPTION = """\
The Muchocine reviews dataset contains 3,872 longform movie reviews in Spanish language,
each with a shorter summary review, and a rating on a 1-5 scale.
"""

_LICENSE = "CC-BY-2.1"

_URLs = {"default": "http://www.lsi.us.es/~fermin/corpusCine.zip"}


class Muchocine(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.1.1")

    def _info(self):
        features = datasets.Features(
            {
                "review_body": datasets.Value("string"),
                "review_summary": datasets.Value("string"),
                "star_rating": datasets.Value("int32"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="http://www.lsi.us.es/~fermin/index.php/Datasets",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths": sorted(glob.glob(os.path.join(data_dir, "corpusCriticasCine", "*.xml"))),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepaths, split):
        for filepath in filepaths:
            with open(filepath, encoding="latin-1") as f:
                id = re.search(r"\d+\.xml", filepath)[0][:-4]

                txt = f.read()
                txt = txt.replace("&ldquo;", '"').replace("&rdquo;", '"').replace("&hellip;", "")
                txt = txt.replace("&lsquo;", '"').replace("&rsquo;", '"').replace("&prime;", "")
                txt = txt.replace("&agrave;", "à").replace("&ndash;", "-").replace("&egrave;", "è")
                txt = txt.replace("&ouml;", "ö").replace("&ccedil;", "ç").replace("&", "and")
                try:
                    doc = parseString(txt)
                except Exception as e:
                    # skip 6 malformed xml files, for example unescaped < and >
                    _ = e
                    continue

                btxt = ""
                review_bod = doc.getElementsByTagName("body")
                if len(review_bod) > 0:
                    for node in review_bod[0].childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            btxt += node.data + " "

                rtxt = ""
                review_summ = doc.getElementsByTagName("summary")
                if len(review_summ) > 0:
                    for node in review_summ[0].childNodes:
                        if node.nodeType == node.TEXT_NODE:
                            rtxt += node.data + " "

                yield id, {
                    "review_body": btxt,
                    "review_summary": rtxt,
                    "star_rating": int(doc.documentElement.attributes["rank"].value),
                }
