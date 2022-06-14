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


import os
import xml.etree.ElementTree as ET

import datasets


_DESCRIPTION = """\
The Universal Declaration of Human Rights (UDHR) is a milestone document in the history of human rights. Drafted by
representatives with different legal and cultural backgrounds from all regions of the world, it set out, for the
first time, fundamental human rights to be universally protected. The Declaration was adopted by the UN General
Assembly in Paris on 10 December 1948 during its 183rd plenary meeting. The dataset includes translations of the
document in 464+ languages and dialects.

© 1996 – 2009 The Office of the High Commissioner for Human Rights

This plain text version prepared by the “UDHR in Unicode” project, https://www.unicode.org/udhr.
"""

_HOMEPAGE = "https://www.ohchr.org/en/universal-declaration-of-human-rights"

_URL = "https://unicode.org/udhr/assemblies/udhr_xml.zip"


class UDHN(datasets.GeneratorBasedBuilder):
    """Universal Declaration of Human Rights"""

    VERSION = datasets.Version("1.0.0")

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
                    "bcp47": datasets.Value("string"),
                }
            ),
            homepage=_HOMEPAGE,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"file_paths": dl_manager.iter_files(dl_dir)}
            ),
        ]

    def _generate_examples(self, file_paths):
        for id_, path in enumerate(file_paths):
            if os.path.basename(path).startswith("udhr_"):
                root = ET.parse(path).getroot()
                text = "\n".join([line.strip() for line in root.itertext() if line.strip()])
                yield id_, {
                    "text": text,
                    "lang_key": root.get("key"),
                    "lang_name": root.get("n"),
                    "iso639-3": root.get("iso639-3"),
                    "iso15924": root.get("iso15924"),
                    "bcp47": root.get("{http://www.w3.org/XML/1998/namespace}lang"),
                }
