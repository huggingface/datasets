# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""Universal Declaration of Human Rights"""

from __future__ import absolute_import, division, print_function

import glob
import os
import xml.etree.ElementTree as ET

import datasets


_DESCRIPTION = """\
The Universal Declaration of Human Rights (UDHR) is a milestone document in the history of human rights. Drafted by
representatives with different legal and cultural backgrounds from all regions of the world, it set out, for the
first time, fundamental human rights to be universally protected. The Declaration was adopted by the UN General
Assembly in Paris on 10 December 1948 during its 183rd plenary meeting. The dataset includes translations of the
document in 464 languages and dialects.

© 1996 – 2009 The Office of the High Commissioner for Human Rights

This plain text version prepared by the “UDHR in Unicode” project, https://www.unicode.org/udhr.
"""

_WEBPAGE = "https://www.ohchr.org/EN/UDHR/Pages/UDHRIndex.aspx"

# XML for meta-info about language and TXT for text
_XML_DOWNLOAD_URL = "https://unicode.org/udhr/assemblies/udhr_xml.zip"
_TXT_DOWNLOAD_URL = "https://unicode.org/udhr/assemblies/udhr_txt.zip"


class UDHN(datasets.GeneratorBasedBuilder):
    """Universal Declaration of Human Rights"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "lang_key": datasets.Value("string"),
                    "lang_name": datasets.Value("string"),
                    "iso639-3": datasets.Value("string"),
                    "iso15924": datasets.Value("string"),
                }
            ),
            homepage=_WEBPAGE,
        )

    def _split_generators(self, dl_manager):
        xml_dir = dl_manager.download_and_extract(_XML_DOWNLOAD_URL)
        txt_dir = dl_manager.download_and_extract(_TXT_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"xml_dir": xml_dir, "txt_dir": txt_dir}),
        ]

    def _generate_examples(self, xml_dir, txt_dir):
        xml_paths = glob.glob(os.path.join(xml_dir, "udhr_*.xml"))
        for i, xml_path in enumerate(xml_paths):
            lang_attr = ET.parse(xml_path).getroot().attrib
            lang = lang_attr["key"]

            txt_path = os.path.join(txt_dir, f"udhr_{lang}.txt")
            assert os.path.exists(txt_path), f"xml file {xml_path} found with no corresponding txt file"

            with open(txt_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[6:]  # ignore first 6 lines (metainfo)
            text = "\n".join([line.strip() for line in lines if len(line.strip()) > 0])

            yield i, {
                "text": text,
                "lang_key": lang,
                "lang_name": lang_attr["n"],
                "iso639-3": lang_attr["iso639-3"],
                "iso15924": lang_attr["iso15924"],
            }
