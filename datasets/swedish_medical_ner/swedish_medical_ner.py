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
"""SwedMedNER: A Named Entity Recognition Dataset on medical texts in Swedish"""


import re

import datasets


_CITATION = """\
@inproceedings{almgrenpavlovmogren2016bioner,
  title={Named Entity Recognition in Swedish Medical Journals with Deep Bidirectional Character-Based LSTMs},
  author={Simon Almgren, Sean Pavlov, Olof Mogren},
  booktitle={Proceedings of the Fifth Workshop on Building and Evaluating Resources for Biomedical Text Mining (BioTxtM 2016)},
  pages={1},
  year={2016}
}
"""


_DESCRIPTION = """\
SwedMedNER is a dataset for training and evaluating Named Entity Recognition systems on medical texts in Swedish.
It is derived from medical articles on the Swedish Wikipedia, Läkartidningen, and 1177 Vårdguiden.
"""


_LICENSE = """\
Creative Commons Attribution-ShareAlike 4.0 International Public License (CC BY-SA 4.0)
See http://creativecommons.org/licenses/by-sa/4.0/ for the summary of the license.
"""


_URL = "https://github.com/olofmogren/biomedical-ner-data-swedish"


_DATA_URL = "https://raw.githubusercontent.com/olofmogren/biomedical-ner-data-swedish/master/"


class SwedishMedicalNerConfig(datasets.BuilderConfig):
    """BuilderConfig for SwedMedNER"""

    def __init__(self, **kwargs):
        """
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SwedishMedicalNerConfig, self).__init__(**kwargs)


class SwedishMedicalNer(datasets.GeneratorBasedBuilder):
    """SwedMedNER: A Named Entity Recognition Dataset on medical texts in Swedish"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="wiki", version=VERSION, description="The Swedish Wikipedia part of the dataset"),
        datasets.BuilderConfig(name="lt", version=VERSION, description="The Läkartidningen part of the dataset"),
        datasets.BuilderConfig(name="1177", version=VERSION, description="The 1177 Vårdguiden part of the dataset"),
    ]

    def _info(self):
        if self.config.name == "wiki":
            features = datasets.Features(
                {
                    "sid": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "entities": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "type": datasets.ClassLabel(
                                names=["Disorder and Finding", "Pharmaceutical Drug", "Body Structure"]
                            ),
                        }
                    ),
                }
            )
        elif self.config.name == "lt":
            features = datasets.Features(
                {
                    "sid": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "entities": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "type": datasets.ClassLabel(
                                names=["Disorder and Finding", "Pharmaceutical Drug", "Body Structure"]
                            ),
                        }
                    ),
                }
            )
        elif self.config.name == "1177":
            features = datasets.Features(
                {
                    "sid": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "entities": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "type": datasets.ClassLabel(
                                names=["Disorder and Finding", "Pharmaceutical Drug", "Body Structure"]
                            ),
                        }
                    ),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_URL,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "wiki": _DATA_URL + "Wiki_annotated_60.txt",
            "lt": _DATA_URL + "LT_annotated_60.txt",
            "1177": _DATA_URL + "1177_annotated_sentences.txt",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        if self.config.name == "wiki":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["wiki"]})
            ]
        elif self.config.name == "lt":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["lt"]})
            ]
        elif self.config.name == "1177":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["1177"]})
            ]

    def _generate_examples(self, filepath):
        """Yields examples as (key, example) tuples."""

        def find_type(s, e):
            if (s == "(") and (e == ")"):
                return "Disorder and Finding"
            elif (s == "[") and (e == "]"):
                return "Pharmaceutical Drug"
            elif (s == "{") and (e == "}"):
                return "Body Structure"

        pattern = r"\[([^\[\]()]+)\]|\(([^\[\]()]+)\)|\{([^\[\]()]+)\}"
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                sentence = row.replace("\n", "")

                if self.config.name == "1177":
                    targets = [
                        {
                            "start": m.start(0),
                            "end": m.end(0),
                            "text": sentence[m.start(0) + 2 : m.end(0) - 2],
                            "type": find_type(sentence[m.start(0)], sentence[m.end(0) - 1]),
                        }
                        for m in re.finditer(pattern, sentence)
                    ]
                    yield id_, {
                        "sid": self.config.name + "_" + str(id_),
                        "sentence": sentence,
                        "entities": targets if targets else [],
                    }
                else:
                    targets = [
                        {
                            "start": m.start(0),
                            "end": m.end(0),
                            "text": sentence[m.start(0) + 1 : m.end(0) - 1],
                            "type": find_type(sentence[m.start(0)], sentence[m.end(0) - 1]),
                        }
                        for m in re.finditer(pattern, sentence)
                    ]
                    yield id_, {
                        "sid": self.config.name + "_" + str(id_),
                        "sentence": sentence,
                        "entities": targets if targets else [],
                    }
