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
"""The WebNLG corpus"""

from __future__ import absolute_import, division, print_function

import os
import xml.etree.cElementTree as ET
from collections import defaultdict
from glob import glob
from os.path import join as pjoin

import datasets


_CITATION = """\
@inproceedings{web_nlg,
  author    = {Claire Gardent and
               Anastasia Shimorina and
               Shashi Narayan and
               Laura Perez{-}Beltrachini},
  editor    = {Regina Barzilay and
               Min{-}Yen Kan},
  title     = {Creating Training Corpora for {NLG} Micro-Planners},
  booktitle = {Proceedings of the 55th Annual Meeting of the
               Association for Computational Linguistics,
               {ACL} 2017, Vancouver, Canada, July 30 - August 4,
               Volume 1: Long Papers},
  pages     = {179--188},
  publisher = {Association for Computational Linguistics},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-1017},
  doi       = {10.18653/v1/P17-1017}
}
"""

_DESCRIPTION = """\
The WebNLG challenge consists in mapping data to text. The training data consists
of Data/Text pairs where the data is a set of triples extracted from DBpedia and the text is a verbalisation
of these triples. For instance, given the 3 DBpedia triples shown in (a), the aim is to generate a text such as (b).

a. (John_E_Blaha birthDate 1942_08_26) (John_E_Blaha birthPlace San_Antonio) (John_E_Blaha occupation Fighter_pilot)
b. John E Blaha, born in San Antonio on 1942-08-26, worked as a fighter pilot

As the example illustrates, the task involves specific NLG subtasks such as sentence segmentation
(how to chunk the input data into sentences), lexicalisation (of the DBpedia properties),
aggregation (how to avoid repetitions) and surface realisation
(how to build a syntactically correct and natural sounding text).
"""

_URL = "https://gitlab.com/shimorina/webnlg-dataset/-/archive/master/webnlg-dataset-master.zip"

_FILE_PATHS = {
    "webnlg_challenge_2017": {
        "train": [f"webnlg_challenge_2017/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"webnlg_challenge_2017/dev/{i}triples/" for i in range(1, 8)],
        "test": ["webnlg_challenge_2017/test/"],
    },
    "release_v1": {"full": [f"release_v1/xml/{i}triples" for i in range(1, 8)]},
    "release_v2": {
        "train": [f"release_v2/xml/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"release_v2/xml/dev/{i}triples/" for i in range(1, 8)],
        "test": [f"release_v2/xml/test/{i}triples/" for i in range(1, 8)],
    },
    "release_v2_constrained": {
        "train": [f"release_v2_constrained/xml/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"release_v2_constrained/xml/dev/{i}triples/" for i in range(1, 8)],
        "test": [f"release_v2_constrained/xml/test/{i}triples/" for i in range(1, 8)],
    },
    "release_v2.1": {
        "train": [f"release_v2.1/xml/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"release_v2.1/xml/dev/{i}triples/" for i in range(1, 8)],
        "test": [f"release_v2.1/xml/test/{i}triples/" for i in range(1, 8)],
    },
    "release_v2.1_constrained": {
        "train": [f"release_v2.1_constrained/xml/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"release_v2.1_constrained/xml/dev/{i}triples/" for i in range(1, 8)],
        "test": [f"release_v2.1_constrained/xml/test/{i}triples/" for i in range(1, 8)],
    },
    "release_v3.0_en": {
        "train": [f"release_v3.0/en/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"release_v3.0/en/dev/{i}triples/" for i in range(1, 8)],
        "test": [f"release_v3.0/en/test/" for i in range(1, 8)],
    },
    "release_v3.0_ru": {
        "train": [f"release_v3.0/ru/train/{i}triples/" for i in range(1, 8)],
        "dev": [f"release_v3.0/ru/dev/{i}triples/" for i in range(1, 8)],
        "test": [f"release_v3.0/ru/test/" for i in range(1, 8)],
    },
}


def et_to_dict(tree):
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


def parse_entry(entry):
    res = {}
    otriple_set_list = entry["originaltripleset"]
    res["original_triple_sets"] = [{"otriple_set": otriple_set["otriple"]} for otriple_set in otriple_set_list]
    mtriple_set_list = entry["modifiedtripleset"]
    res["modified_triple_sets"] = [{"mtriple_set": mtriple_set["mtriple"]} for mtriple_set in mtriple_set_list]
    res["category"] = entry["category"]
    res["eid"] = entry["eid"]
    res["size"] = int(entry["size"])
    res["lex"] = {
        "comment": [ex.get("comment", "") for ex in entry.get("lex", [])],
        "lid": [ex.get("lid", "") for ex in entry.get("lex", [])],
        "text": [ex.get("text", "") for ex in entry.get("lex", [])],
    }
    res["shape"] = entry.get("shape", "")
    res["shape_type"] = entry.get("shape_type", "")
    return res


def xml_file_to_examples(filename):
    tree = ET.parse(filename).getroot()
    examples = et_to_dict(tree)["benchmark"]["entries"][0]["entry"]
    return [parse_entry(entry) for entry in examples]


class WebNlg(datasets.GeneratorBasedBuilder):
    """The WebNLG corpus"""

    VERSION = datasets.Version("3.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="webnlg_challenge_2017", description="WebNLG Challenge 2017 data, covers 10 DBpedia categories."
        ),
        datasets.BuilderConfig(name="release_v1", description="Covers 15 DBpedia categories."),
        datasets.BuilderConfig(
            name="release_v2", description="Includes release_v1 and test data from the WebNLG challenge."
        ),
        datasets.BuilderConfig(
            name="release_v2_constrained",
            description="Same data as v2, the split into train/dev/test is more challenging.",
        ),
        datasets.BuilderConfig(name="release_v2.1", description="5,667 texts from v2 were cleaned."),
        datasets.BuilderConfig(
            name="release_v2.1_constrained",
            description="Same data as v2.1, the split into train/dev/test is more challenging.",
        ),
        datasets.BuilderConfig(
            name="release_v3.0_en", description="WebNLG+ data used in the WebNLG challenge 2020. English."
        ),
        datasets.BuilderConfig(
            name="release_v3.0_ru", description="WebNLG+ data used in the WebNLG challenge 2020. Russian."
        ),
    ]

    def _info(self):
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
                    }
                ),
                "2017_test_category": datasets.Value("string"),
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
            homepage="https://webnlg-challenge.loria.fr/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=spl,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filedirs": [
                        os.path.join(data_dir, "webnlg-dataset-master", dir_suf) for dir_suf in dir_suffix_list
                    ],
                },
            )
            for spl, dir_suffix_list in _FILE_PATHS[self.config.name].items()
        ]

    def _generate_examples(self, filedirs):
        """ Yields examples. """

        id_ = 0
        for xml_location in filedirs:
            for xml_file in sorted(glob(pjoin(xml_location, "*.xml"))):
                test_cat = xml_file.split("/")[-1][:-4] if "webnlg_challenge_2017/test" in xml_file else ""
                for exple_dict in xml_file_to_examples(xml_file):
                    exple_dict["2017_test_category"] = test_cat
                    id_ += 1
                    yield id_, exple_dict
