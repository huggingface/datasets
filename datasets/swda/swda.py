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
"""
Switchboard Dialog Act Corpus
The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2,
with turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information
about the associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s.
"""

from __future__ import absolute_import, division, print_function

import datasets


# Citation as described here: https://github.com/cgpotts/swda#citation.
_CITATION = """\
@techreport{Jurafsky-etal:1997,
    Address = {Boulder, CO},
    Author = {Jurafsky, Daniel and Shriberg, Elizabeth and Biasca, Debra},
    Institution = {University of Colorado, Boulder Institute of Cognitive Science},
    Number = {97-02},
    Title = {Switchboard {SWBD}-{DAMSL} Shallow-Discourse-Function Annotation Coders Manual, Draft 13},
    Year = {1997}}

@article{Shriberg-etal:1998,
    Author = {Shriberg, Elizabeth and Bates, Rebecca and Taylor, Paul and Stolcke, Andreas and Jurafsky, \
    Daniel and Ries, Klaus and Coccaro, Noah and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
    Journal = {Language and Speech},
    Number = {3--4},
    Pages = {439--487},
    Title = {Can Prosody Aid the Automatic Classification of Dialog Acts in Conversational Speech?},
    Volume = {41},
    Year = {1998}}

@article{Stolcke-etal:2000,
    Author = {Stolcke, Andreas and Ries, Klaus and Coccaro, Noah and Shriberg, Elizabeth and Bates, Rebecca and \
    Jurafsky, Daniel and Taylor, Paul and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
    Journal = {Computational Linguistics},
    Number = {3},
    Pages = {339--371},
    Title = {Dialogue Act Modeling for Automatic Tagging and Recognition of Conversational Speech},
    Volume = {26},
    Year = {2000}}
"""


# Description of dataset gathered from: https://github.com/cgpotts/swda#overview.
_DESCRIPTION = """\
The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2 with
turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information about the
associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s.
The SwDA is not inherently linked to the Penn Treebank 3 parses of Switchboard, and it is far from straightforward to
align the two resources. In addition, the SwDA is not distributed with the Switchboard's tables of metadata about the
conversations and their participants.
"""

# Homepage gathered from: https://github.com/cgpotts/swda#overview.
_HOMEPAGE = "http://compprag.christopherpotts.net/swda.html"

# More details about the license: https://creativecommons.org/licenses/by-nc-sa/3.0/.
_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License"

# Dataset main url.
_URL = "https://github.com/NathanDuran/Switchboard-Corpus/raw/master/swda_data/"


class Swda(datasets.GeneratorBasedBuilder):
    """
    Switchboard Dialog Act Corpus
    The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2,
    with turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information
    about the associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s.
    """

    # Splits url extensions for train, validation and test.
    _URLS = {"train": _URL + "train_set.txt", "dev": _URL + "val_set.txt", "test": _URL + "test_set.txt"}

    def _info(self):
        """
        Specify the datasets.DatasetInfo object which contains informations and typings for the dataset.
        """

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types.
            features=datasets.Features(
                {
                    "speaker": datasets.ClassLabel(
                        num_classes=2,
                        names=[
                            "A",
                            "B",
                        ],
                    ),
                    "utterance_text": datasets.Value("string"),
                    "dialogue_act_tag": datasets.ClassLabel(
                        num_classes=41,
                        names=[
                            "sd",
                            "b",
                            "sv",
                            "%",
                            "aa",
                            "ba",
                            "qy",
                            "ny",
                            "fc",
                            "qw",
                            "nn",
                            "bk",
                            "h",
                            "qy^d",
                            "bh",
                            "^q",
                            "bf",
                            'fo_o_fw_"_by_bc',
                            "na",
                            "ad",
                            "^2",
                            "b^m",
                            "qo",
                            "qh",
                            "^h",
                            "ar",
                            "ng",
                            "br",
                            "no",
                            "fp",
                            "qrr",
                            "arp_nd",
                            "t3",
                            "oo_co_cc",
                            "aap_am",
                            "t1",
                            "bd",
                            "^g",
                            "qw^d",
                            "fa",
                            "ft",
                        ],
                    ),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """
        Returns SplitGenerators.
        This method is tasked with downloading/extracting the data and defining the splits.
        """

        urls_to_download = self._URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"], "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"], "split": "validation"}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """
        Yields examples.
        This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        The key is not important, it's more here for legacy reason (legacy from tfds).
        """

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):

                # Parse row into speaker info | utterance text | dialogue act tag.
                parsed_row = row.rstrip("\r\n").split("|")

                # Also returning dialogue act integer label.
                yield f"{split}-{id_}", {
                    "speaker": parsed_row[0],
                    "utterance_text": parsed_row[1],
                    "dialogue_act_tag": parsed_row[2],
                }
