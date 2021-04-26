# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""The Winograd Schema Challenge Dataset"""

import xml.etree.ElementTree as ET

import datasets


_DESCRIPTION = """\
A Winograd schema is a pair of sentences that differ in only one or two words and that contain an ambiguity that is
resolved in opposite ways in the two sentences and requires the use of world knowledge and reasoning for its
resolution. The schema takes its name from a well-known example by Terry Winograd:

> The city councilmen refused the demonstrators a permit because they [feared/advocated] violence.

If the word is ``feared'', then ``they'' presumably refers to the city council; if it is ``advocated'' then ``they''
presumably refers to the demonstrators.
"""

_CITATION = """\
@inproceedings{levesque2012winograd,
  title={The winograd schema challenge},
  author={Levesque, Hector and Davis, Ernest and Morgenstern, Leora},
  booktitle={Thirteenth International Conference on the Principles of Knowledge Representation and Reasoning},
  year={2012},
  organization={Citeseer}
}
"""

_HOMPAGE = "https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html"
_DOWNLOAD_URL = "https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WSCollection.xml"


class WinogradWSCConfig(datasets.BuilderConfig):
    """BuilderConfig for WinogradWSC."""

    def __init__(self, *args, language=None, inds=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.inds = set(inds) if inds is not None else None

    def is_in_range(self, id):
        """Takes an index and tells you if it belongs to the configuration's subset"""
        return id in self.inds if self.inds is not None else True


class WinogradWSC(datasets.GeneratorBasedBuilder):
    """The Winograd Schema Challenge Dataset"""

    BUILDER_CONFIG_CLASS = WinogradWSCConfig
    BUILDER_CONFIGS = [
        WinogradWSCConfig(
            name="wsc285",
            description="Full set of winograd examples",
        ),
        WinogradWSCConfig(
            name="wsc273",
            description="A commonly-used subset of examples. Identical to 'wsc285' but without the last 12 examples.",
            inds=list(range(273)),
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "pronoun": datasets.Value("string"),
                    "pronoun_loc": datasets.Value("int32"),
                    "quote": datasets.Value("string"),
                    "quote_loc": datasets.Value("int32"),
                    "options": datasets.Sequence(datasets.Value("string")),
                    "label": datasets.ClassLabel(num_classes=2),
                    "source": datasets.Value("string"),
                }
            ),
            homepage=_HOMPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": path}),
        ]

    def _cleanup_whitespace(self, text):
        return " ".join(text.split())

    def _generate_examples(self, filepath):
        tree = ET.parse(filepath)
        for id, schema in enumerate(tree.getroot()):
            if not self.config.is_in_range(id):
                continue

            text_root = schema.find("text")
            quote_root = schema.find("quote")

            text_left = self._cleanup_whitespace(text_root.findtext("txt1", ""))
            text_right = self._cleanup_whitespace(text_root.findtext("txt2", ""))
            quote_left = self._cleanup_whitespace(quote_root.findtext("quote1", ""))
            quote_right = self._cleanup_whitespace(quote_root.findtext("quote2", ""))
            pronoun = self._cleanup_whitespace(text_root.findtext("pron"))

            features = {}
            features["text"] = " ".join([text_left, pronoun, text_right]).strip()
            features["quote"] = " ".join([quote_left, pronoun, quote_right]).strip()

            features["pronoun"] = pronoun
            features["options"] = [
                self._cleanup_whitespace(option.text) for option in schema.find("answers").findall("answer")
            ]

            answer_txt = self._cleanup_whitespace(schema.findtext("correctAnswer"))
            features["label"] = int("B" in answer_txt)  # convert "  A. " or " B " strings to a 0/1 index

            features["pronoun_loc"] = len(text_left) + 1 if len(text_left) > 0 else 0
            features["quote_loc"] = features["pronoun_loc"] - (len(quote_left) + 1 if len(quote_left) > 0 else 0)
            features["source"] = self._cleanup_whitespace(schema.findtext("source"))

            yield id, features
