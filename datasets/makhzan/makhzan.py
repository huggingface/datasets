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
"""An Urdu text corpus for machine learning, natural language processing and linguistic analysis."""


import re
import xml.etree.ElementTree as ET
from pathlib import Path

import datasets


_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
authors={huggingface, Inc.
},
year={2020}
}
"""

_DESCRIPTION = """\
An Urdu text corpus for machine learning, natural language processing and linguistic analysis.
"""

_HOMEPAGE = "https://matnsaz.net/en/makhzan"

_LICENSE = "All files in the /text directory are covered under standard copyright. Each piece of text has been included in this repository with explicity permission of respective copyright holders, who are identified in the <meta> tag for each file. You are free to use this text for analysis, research and development, but you are not allowed to redistribute or republish this text. Some cases where a less restrictive license could apply to files in the /text directory are presented below. In some cases copyright free text has been digitally reproduced through the hard work of our collaborators. In such cases we have credited the appropriate people where possible in a notes field in the file's metadata, and we strongly encourage you to contact them before redistributing this text in any form. Where a separate license is provided along with the text, we have provided corresponding data in the publication field in a file's metadata."

_SHA = "99db56552d6781dcd184bdd3466bce15fd0a1ec0"

_DOWNLOAD_URL = "https://github.com/zeerakahmed/makhzan/archive/" + _SHA + ".zip"


class Makhzan(datasets.GeneratorBasedBuilder):
    """Makhzan - An Urdu text corpus for machine learning, natural language processing and linguistic analysis."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "file_id": datasets.Value("string"),
                "metadata": datasets.Value("string"),
                "title": datasets.Value("string"),
                "num-words": datasets.Value("int64"),
                "contains-non-urdu-languages": datasets.Value("string"),
                "document_body": datasets.Value("string")
                # These are the features of your dataset like images, labels ...
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
        data_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_dir": data_dir},
            )
        ]

    def _generate_examples(self, data_dir):
        """Yields examples."""
        data_dir_path = Path(data_dir)
        data_dir_path = data_dir_path / ("makhzan-" + _SHA) / "text"
        file_paths = sorted(data_dir_path.glob(r"*.xml"))
        for id_, file_path in enumerate(file_paths):
            with file_path.open(encoding="utf-8") as f:
                example = {
                    "file_id": "",
                    "metadata": "",
                    "title": "",
                    "num-words": 0,
                    "contains-non-urdu-languages": "",
                    "document_body": "",
                }
                xml = self._fix_format(f.read())
                root = ET.fromstring(xml)
                if root.tag == "document":
                    example["file_id"] = file_path.name
                    metadata = root.find("meta")
                    if metadata:
                        example["metadata"] = ET.tostring(metadata, encoding="unicode")
                        example["title"] = metadata.find("title").text
                        example["num-words"] = int(metadata.find("num-words").text)
                        example["contains-non-urdu-languages"] = metadata.find("contains-non-urdu-languages").text
                    else:
                        raise ValueError('Missing tag "<meta>"')
                    document_body = root.find("body")
                    if document_body:
                        example["document_body"] = ET.tostring(document_body, encoding="unicode")
                    else:
                        raise ValueError('Missing tag "<body>"')
                else:
                    raise ValueError('Missing tag "<document>"')
                yield id_, example

    def _fix_format(self, xml):
        if "</body>" not in xml:
            # add missing closing body
            xml = xml.replace("</document>", "</body></document>")
        if "</document>" not in xml:
            # add missing closing document
            xml = xml.replace("</body>", "</body></document>")
        if xml.count("section>") % 2 == 1:
            # remove last closing section
            xml = xml[::-1].replace("</section>"[::-1], "", 1)[::-1]
        # fix bad heading
        xml = re.sub(r"<heading>(.+)<heading>", r"<heading>\g<1></heading>", xml)
        # fix bad annotation
        xml = re.sub(r"<</p>/annotation>", r"</p></annotation>", xml)
        return xml
