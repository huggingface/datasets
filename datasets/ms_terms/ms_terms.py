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
"""The Microsoft Terminology Collection."""

from __future__ import absolute_import, division, print_function

import os
import xml.etree.ElementTree as ElementTree

import datasets


_DESCRIPTION = """\
The Microsoft Terminology Collection can be used to develop localized versions of applications that integrate with Microsoft products.
It can also be used to integrate Microsoft terminology into other terminology collections or serve as a base IT glossary
for language development in the nearly 100 languages available. Terminology is provided in .tbx format, an industry standard for terminology exchange.
"""

_LICENSE = """\
See the Microsoft Language Portal Materials License and the Microsoft Terms of Use for details.
"""

_ENTRY_ID = "entry_id"
_TERM_SOURCE = "term_source"
_TERM_POS = "pos"
_TERM_DEFINITION = "definition"
_TERM_TARGET = "term_target"

_FILENAME = "MicrosoftTermCollection.tbx"


class MsTerms(datasets.GeneratorBasedBuilder):
    """The Microsoft Terminology Collection."""

    VERSION = datasets.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://www.microsoft.com/en-us/language/terminology,
    and manually download the language of your interest. Once it is completed,
    a file named MicrosoftTermCollection.tbx will be appeared in your Downloads folder
    or whichever folder your browser chooses to save files to.
    You can then move MicrosoftTermCollection.tbx under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    ms_terms can then be loaded using the following command `datasets.load_dataset("ms_terms", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        feature_names = [_ENTRY_ID, _TERM_SOURCE, _TERM_POS, _TERM_DEFINITION, _TERM_TARGET]
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({k: datasets.Value("string") for k in feature_names}),
            supervised_keys=None,
            homepage="https://www.microsoft.com/en-us/language/terminology",
            citation="",
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path_to_manual_file = os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), _FILENAME)

        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('ms_terms', data_dir=...)` that includes a file name {}. Manual download instructions: {})".format(
                    path_to_manual_file, _FILENAME, self.manual_download_instructions
                )
            )
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"path": path_to_manual_file})]

    def _generate_examples(self, path=None, title_set=None):
        tree = ElementTree.parse(path)
        root = tree.getroot()
        for i, entry in enumerate(root.findall(".//termEntry")):
            entry_id = entry.attrib.get("id")
            langsets = entry.findall("./langSet")
            if len(langsets) != 2:
                continue

            term_source = langsets[0].find(".//term").text
            term_definition = langsets[0].find(".//descrip").text
            term_pos = langsets[0].find(".//termNote").text
            term_target = langsets[1].find(".//term").text
            yield i, {
                _ENTRY_ID: entry_id,
                _TERM_SOURCE: term_source,
                _TERM_POS: term_pos,
                _TERM_DEFINITION: term_definition,
                _TERM_TARGET: term_target,
            }
