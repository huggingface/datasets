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
"""TODO: Add a description here."""


import json

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{roy2020lareqa,
  title={LAReQA: Language-agnostic answer retrieval from a multilingual pool},
  author={Roy, Uma and Constant, Noah and Al-Rfou, Rami and Barua, Aditya and Phillips, Aaron and Yang, Yinfei},
  journal={arXiv preprint arXiv:2004.05484},
  year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
XQuAD-R is a retrieval version of the XQuAD dataset (a cross-lingual extractive QA dataset). Like XQuAD, XQUAD-R is an 11-way parallel dataset, where each question appears in 11 different languages and has 11 parallel correct answers across the languages.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/google-research-datasets/lareqa"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://github.com/google-research-datasets/lareqa/raw/master/xquad-r/"
_LANG = ["ar", "de", "zh", "vi", "en", "es", "hi", "el", "th", "tr", "ru"]


class XquadRConfig(datasets.BuilderConfig):

    """BuilderConfig for XquadR"""

    def __init__(self, lang, **kwargs):
        """
        Args:
            lang: string, language for the input text
            **kwargs: keyword arguments forwarded to super.
        """
        super(XquadRConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.lang = lang


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class XquadR(datasets.GeneratorBasedBuilder):
    """TODO(xquad-r): Short description of my dataset."""

    # TODO(xquad-r): Set up version.
    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIGS = [XquadRConfig(name=f"{lang}", description=_DESCRIPTION, lang=lang) for lang in _LANG]

    def _info(self):
        # TODO(xquad-r): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(xquad-r): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {lang: _URL + f"{lang}.json" for lang in _LANG}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files[self.config.lang]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(xquad-r): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for article in data["data"]:
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
