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
""""The Finnish News Corpus for Named Entity Recognition dataset."""


import csv

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{ruokolainen2019finnish,
  title={A finnish news corpus for named entity recognition},
  author={Ruokolainen, Teemu and Kauppinen, Pekka and Silfverberg, Miikka and Lind{\'e}n, Krister},
  journal={Language Resources and Evaluation},
  pages={1--26},
  year={2019},
  publisher={Springer}
}
"""

_DESCRIPTION = """\
The directory data contains a corpus of Finnish technology related news articles with a manually prepared
named entity annotation (digitoday.2014.csv). The text material was extracted from the archives of Digitoday,
a Finnish online technology news source (www.digitoday.fi). The corpus consists of 953 articles
(193,742 word tokens) with six named entity classes (organization, location, person, product, event, and date).
The corpus is available for research purposes and can be readily used for development of NER systems for Finnish.
"""

_URLS = {
    "train": "https://github.com/mpsilfve/finer-data/raw/master/data/digitoday.2014.train.csv",
    "dev": "https://github.com/mpsilfve/finer-data/raw/master/data/digitoday.2014.dev.csv",
    "test": "https://github.com/mpsilfve/finer-data/raw/master/data/digitoday.2015.test.csv",
    "test_wikipedia": "https://github.com/mpsilfve/finer-data/raw/master/data/wikipedia.test.csv",
}


class FinerConfig(datasets.BuilderConfig):
    """BuilderConfig for FiNER dataset."""

    def __init__(self, **kwargs):
        """BuilderConfig for FiNER dataset.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(FinerConfig, self).__init__(**kwargs)


class Finer(datasets.GeneratorBasedBuilder):
    """FiNER dataset."""

    BUILDER_CONFIGS = [
        FinerConfig(
            name="finer",
            version=datasets.Version("1.0.0"),
            description="A Finnish News Corpus for Named Entity Recognition dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-DATE",
                                "B-EVENT",
                                "B-LOC",
                                "B-ORG",
                                "B-PER",
                                "B-PRO",
                                "I-DATE",
                                "I-EVENT",
                                "I-LOC",
                                "I-ORG",
                                "I-PER",
                                "I-PRO",
                            ]
                        )
                    ),
                    "nested_ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-DATE",
                                "B-EVENT",
                                "B-LOC",
                                "B-ORG",
                                "B-PER",
                                "B-PRO",
                                "I-DATE",
                                "I-EVENT",
                                "I-LOC",
                                "I-ORG",
                                "I-PER",
                                "I-PRO",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/mpsilfve/finer-data",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        downloaded_files = dl_manager.download_and_extract(_URLS)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
            datasets.SplitGenerator(
                name=datasets.Split("test_wikipedia"), gen_kwargs={"filepath": downloaded_files["test_wikipedia"]}
            ),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating 🇫🇮 examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            data = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            current_tokens = []
            current_ner_tags = []
            current_nested_ner_tags = []
            sentence_counter = 0
            for row in data:
                if row and "" not in row:
                    token, label, nested_label = row[:3]
                    current_tokens.append(token)
                    current_ner_tags.append(label)
                    current_nested_ner_tags.append(nested_label)
                else:
                    # New sentence
                    if not current_tokens:
                        # Consecutive empty lines will cause empty sentences
                        continue
                    assert len(current_tokens) == len(current_ner_tags), "💔 between len of tokens & labels"
                    assert len(current_ner_tags) == len(
                        current_nested_ner_tags
                    ), "💔 between len of labels & nested labels"
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "tokens": current_tokens,
                            "ner_tags": current_ner_tags,
                            "nested_ner_tags": current_nested_ner_tags,
                        },
                    )
                    sentence_counter += 1
                    current_tokens = []
                    current_ner_tags = []
                    current_nested_ner_tags = []
                    yield sentence
            # Don't forget last sentence in dataset 🧐
            if current_tokens:
                yield sentence_counter, {
                    "id": str(sentence_counter),
                    "tokens": current_tokens,
                    "ner_tags": current_ner_tags,
                    "nested_ner_tags": current_nested_ner_tags,
                }
