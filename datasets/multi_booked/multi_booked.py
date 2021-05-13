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
"""MultiBooked dataset."""

import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import datasets


_CITATION = """\
@inproceedings{Barnes2018multibooked,
    author={Barnes, Jeremy and Lambert, Patrik and Badia, Toni},
    title={MultiBooked: A corpus of Basque and Catalan Hotel Reviews Annotated for Aspect-level Sentiment Classification},
    booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC'18)},
    year = {2018},
    month = {May},
    date = {7-12},
    address = {Miyazaki, Japan},
    publisher = {European Language Resources Association (ELRA)},
    language = {english}
}
"""

_DESCRIPTION = """\
MultiBooked is a corpus of Basque and Catalan Hotel Reviews Annotated for Aspect-level Sentiment Classification.

The corpora are compiled from hotel reviews taken mainly from booking.com. The corpora are in Kaf/Naf format, which is
an xml-style stand-off format that allows for multiple layers of annotation. Each review was sentence- and
word-tokenized and lemmatized using Freeling for Catalan and ixa-pipes for Basque. Finally, for each language two
annotators annotated opinion holders, opinion targets, and opinion expressions for each review, following the
guidelines set out in the OpeNER project.
"""

_HOMEPAGE = "http://hdl.handle.net/10230/33928"

_LICENSE = "CC-BY 3.0"

_URL = "https://github.com/jerbarnes/multibooked/archive/master.zip"


class MultiBooked(datasets.GeneratorBasedBuilder):
    """MultiBooked dataset."""

    VERSION = datasets.Version("0.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="ca", description="MultiBooked dataset in Catalan language."),
        datasets.BuilderConfig(name="eu", description="MultiBooked dataset in Basque language."),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.features.Sequence(
                        {
                            "wid": datasets.Value("string"),
                            "sent": datasets.Value("string"),
                            "para": datasets.Value("string"),
                            "word": datasets.Value("string"),
                        }
                    ),
                    "terms": datasets.features.Sequence(
                        {
                            "tid": datasets.Value("string"),
                            "lemma": datasets.Value("string"),
                            "morphofeat": datasets.Value("string"),
                            "pos": datasets.Value("string"),
                            "target": datasets.features.Sequence(datasets.Value("string")),
                        }
                    ),
                    "opinions": datasets.features.Sequence(
                        {
                            "oid": datasets.Value("string"),
                            "opinion_holder_target": datasets.features.Sequence(datasets.Value("string")),
                            "opinion_target_target": datasets.features.Sequence(datasets.Value("string")),
                            "opinion_expression_polarity": datasets.features.ClassLabel(
                                names=["StrongNegative", "Negative", "Positive", "StrongPositive"]
                            ),
                            "opinion_expression_target": datasets.features.Sequence(datasets.Value("string")),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "dirpath": os.path.join(data_dir, "multibooked-master", "corpora", self.config.name),
                },
            ),
        ]

    def _generate_examples(self, dirpath):
        for id_, filepath in enumerate(sorted(Path(dirpath).iterdir())):
            example = defaultdict(lambda: defaultdict(list))
            with open(filepath, encoding="utf-8") as f:
                for _, elem in ET.iterparse(f):
                    if elem.tag == "text":
                        for child in elem:
                            # sometimes wid is missing in the eu configuration
                            example["text"]["wid"].append(child.attrib.get("wid", ""))
                            example["text"]["sent"].append(child.attrib["sent"])
                            example["text"]["para"].append(child.attrib["para"])
                            example["text"]["word"].append(child.text)
                    elif elem.tag == "terms":
                        for child in elem:
                            # sometimes tid is missing in the eu configuration
                            example["terms"]["tid"].append(child.attrib.get("tid", ""))
                            example["terms"]["lemma"].append(child.attrib["lemma"])
                            example["terms"]["morphofeat"].append(child.attrib["morphofeat"])
                            example["terms"]["pos"].append(child.attrib["pos"])
                            targets = []
                            for target in child.findall("span/target"):
                                targets.append(target.attrib["id"])
                            example["terms"]["target"].append(targets)
                    elif elem.tag == "opinions":
                        for child in elem:
                            example["opinions"]["oid"].append(child.attrib["oid"])
                            # Opinion holder
                            opinion_holder = child.find("opinion_holder")
                            targets = []
                            for target in opinion_holder.findall("span/target"):
                                targets.append(target.attrib["id"])
                            example["opinions"]["opinion_holder_target"].append(targets)
                            # Opinion target
                            opinion_target = child.find("opinion_target")
                            targets = []
                            for target in opinion_target.findall("span/target"):
                                targets.append(target.attrib["id"])
                            example["opinions"]["opinion_target_target"].append(targets)
                            # Opinion expression
                            opinion_expression = child.find("opinion_expression")
                            example["opinions"]["opinion_expression_polarity"].append(
                                opinion_expression.attrib["polarity"]
                            )
                            targets = []
                            for target in opinion_expression.findall("span/target"):
                                targets.append(target.attrib["id"])
                            example["opinions"]["opinion_expression_target"].append(targets)
            yield id_, example
