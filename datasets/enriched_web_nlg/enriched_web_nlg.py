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
"""The Enriched WebNLG corpus"""


import itertools
import os
import xml.etree.cElementTree as ET
from collections import defaultdict
from glob import glob
from os.path import join as pjoin

import datasets


_CITATION = """\
@InProceedings{ferreiraetal2018,
  author = 	"Castro Ferreira, Thiago and Moussallem, Diego and Wubben, Sander and Krahmer, Emiel",
  title = 	"Enriching the WebNLG corpus",
  booktitle = 	"Proceedings of the 11th International Conference on Natural Language Generation",
  year = 	"2018",
  series = {INLG'18},
  publisher = 	"Association for Computational Linguistics",
  address = 	"Tilburg, The Netherlands",
}
"""

_DESCRIPTION = """\
WebNLG is a valuable resource and benchmark for the Natural Language Generation (NLG) community. However, as other NLG benchmarks, it only consists of a collection of parallel raw representations and their corresponding textual realizations. This work aimed to provide intermediate representations of the data for the development and evaluation of popular tasks in the NLG pipeline architecture (Reiter and Dale, 2000), such as Discourse Ordering, Lexicalization, Aggregation and Referring Expression Generation.
"""

_HOMEPAGE = "https://github.com/ThiagoCF05/webnlg"

_LICENSE = "CC Attribution-Noncommercial-Share Alike 4.0 International"

_SHA = "12ca34880b225ebd1eb9db07c64e8dd76f7e5784"

_URL = f"https://github.com/ThiagoCF05/webnlg/archive/{_SHA}.zip"

_FILE_PATHS = {
    "en": {
        "train": [f"webnlg-{_SHA}/data/v1.5/en/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"webnlg-{_SHA}/data/v1.5/en/dev/{i}triples/" for i in range(1, 8)],
        "test": [f"webnlg-{_SHA}/data/v1.5/en/test/{i}triples/" for i in range(1, 8)],
    },
    "de": {
        "train": [f"webnlg-{_SHA}/data/v1.5/de/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"webnlg-{_SHA}/data/v1.5/de/dev/{i}triples/" for i in range(1, 8)],
    },
}


def et_to_dict(tree):
    """Takes the xml tree within a dataset file and returns a dictionary with entry data"""
    dct = {tree.tag: {} if tree.attrib else None}
    children = list(tree)
    if children:
        dd = defaultdict(list)
        for dc in map(et_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        dct = {tree.tag: dd}
    if tree.attrib:
        dct[tree.tag].update((k, v) for k, v in tree.attrib.items())
    if tree.text:
        text = tree.text.strip()
        if children or tree.attrib:
            if text:
                dct[tree.tag]["text"] = text
        else:
            dct[tree.tag] = text
    return dct


def parse_entry(entry, config_name):
    """Takes the dictionary corresponding to an entry and returns a dictionary with:
    - Proper feature naming
    - Default values
    - Proper typing"""
    res = {}
    otriple_set_list = entry["originaltripleset"]
    res["original_triple_sets"] = [{"otriple_set": otriple_set["otriple"]} for otriple_set in otriple_set_list]
    mtriple_set_list = entry["modifiedtripleset"]
    res["modified_triple_sets"] = [{"mtriple_set": mtriple_set["mtriple"]} for mtriple_set in mtriple_set_list]
    res["category"] = entry["category"]
    res["eid"] = entry["eid"]
    res["size"] = int(entry["size"])
    lex = entry["lex"]
    # Some entries are misformed, with None instead of the sorted triplet information.
    entry_triples = [
        ex["sortedtripleset"][0] if ex["sortedtripleset"][0] is not None else {"sentence": []} for ex in lex
    ]
    # the xml structure is inconsistent; sorted triplets are often separated in several dictionaries, so we sum them.
    sorted_triples = [
        list(itertools.chain.from_iterable(item.get("striple", []) for item in entry["sentence"]))
        for entry in entry_triples
    ]
    res["lex"] = {
        "comment": [ex.get("comment", "") for ex in lex],
        "lid": [ex.get("lid", "") for ex in lex],
        # all of the sequence are within their own 1-element sublist, thus the [0]
        "text": [ex.get("text", [""])[0] for ex in lex],
        "template": [ex.get("template", [""])[0] for ex in lex],
        "sorted_triple_sets": sorted_triples,
    }
    # only present in the en version
    if config_name == "en":
        res["lex"]["lexicalization"] = [ex.get("lexicalization", [""])[0] for ex in lex]
    res["shape"] = entry.get("shape", "")
    res["shape_type"] = entry.get("shape_type", "")
    return res


def xml_file_to_examples(filename, config_name):
    tree = ET.parse(filename).getroot()
    examples = et_to_dict(tree)["benchmark"]["entries"][0]["entry"]
    return [parse_entry(entry, config_name) for entry in examples]


class EnrichedWebNlg(datasets.GeneratorBasedBuilder):
    """The WebNLG corpus"""

    VERSION = datasets.Version("1.5.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="en", description="Enriched English version of the WebNLG data"),
        datasets.BuilderConfig(name="de", description="Enriched German version of the WebNLG data"),
    ]

    def _info(self):
        if self.config.name == "en":
            features = datasets.Features(
                {
                    "category": datasets.Value("string"),
                    "size": datasets.Value("int32"),
                    "eid": datasets.Value("string"),
                    "original_triple_sets": datasets.Sequence(
                        {"otriple_set": datasets.Sequence(datasets.Value("string"))}
                    ),
                    "modified_triple_sets": datasets.Sequence(
                        {"mtriple_set": datasets.Sequence(datasets.Value("string"))}
                    ),
                    "shape": datasets.Value("string"),
                    "shape_type": datasets.Value("string"),
                    "lex": datasets.Sequence(
                        {
                            "comment": datasets.Value("string"),
                            "lid": datasets.Value("string"),
                            "text": datasets.Value("string"),
                            "template": datasets.Value("string"),
                            "sorted_triple_sets": datasets.Sequence(datasets.Value("string")),
                            # only present in the en version
                            "lexicalization": datasets.Value("string"),
                        }
                    ),
                }
            )
        else:
            features = datasets.Features(
                {
                    "category": datasets.Value("string"),
                    "size": datasets.Value("int32"),
                    "eid": datasets.Value("string"),
                    "original_triple_sets": datasets.Sequence(
                        {"otriple_set": datasets.Sequence(datasets.Value("string"))}
                    ),
                    "modified_triple_sets": datasets.Sequence(
                        {"mtriple_set": datasets.Sequence(datasets.Value("string"))}
                    ),
                    "shape": datasets.Value("string"),
                    "shape_type": datasets.Value("string"),
                    "lex": datasets.Sequence(
                        {
                            "comment": datasets.Value("string"),
                            "lid": datasets.Value("string"),
                            "text": datasets.Value("string"),
                            "template": datasets.Value("string"),
                            "sorted_triple_sets": datasets.Sequence(datasets.Value("string")),
                        }
                    ),
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        # Downloading the repo adds the current commit sha to the directory, so we can't specify the directory
        # name in advance.
        split_files = {
            split: [os.path.join(data_dir, dir_suf) for dir_suf in dir_suffix_list]
            for split, dir_suffix_list in _FILE_PATHS[self.config.name].items()
        }
        return [
            datasets.SplitGenerator(
                name=split,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filedirs": filedirs},
            )
            for split, filedirs in split_files.items()
        ]

    def _generate_examples(self, filedirs):
        """Yields examples."""

        id_ = 0
        for xml_location in filedirs:
            for xml_file in sorted(glob(pjoin(xml_location, "*.xml"))):
                for exple_dict in xml_file_to_examples(xml_file, self.config.name):
                    id_ += 1
                    yield id_, exple_dict
