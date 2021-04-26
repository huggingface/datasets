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
"""XED: A multilingual fine-grained emotion dataset. The dataset consists of humanannotated Finnish (25k) and English sentences (30k)."""


import datasets


_CITATION = """\
@inproceedings{ohman2020xed,
  title={XED: A Multilingual Dataset for Sentiment Analysis and Emotion Detection},
  author={{\"O}hman, Emily and P{\"a}mies, Marc and Kajava, Kaisla and Tiedemann, J{\"o}rg},
  booktitle={The 28th International Conference on Computational Linguistics (COLING 2020)},
  year={2020}
}
"""

_DESCRIPTION = """\
A multilingual fine-grained emotion dataset. The dataset consists of human annotated Finnish (25k) and English sentences (30k). Plutchik’s
core emotions are used to annotate the dataset with the addition of neutral to create a multilabel multiclass
dataset. The dataset is carefully evaluated using language-specific BERT models and SVMs to
show that XED performs on par with other similar datasets and is therefore a useful tool for
sentiment analysis and emotion detection.
"""

_HOMEPAGE = ""

_LICENSE = "License: Creative Commons Attribution 4.0 International License (CC-BY)"

_URLs = {
    "en_annotated": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/en-annotated.tsv",
    "fi_annotated": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/fi-annotated.tsv",
    "en_neutral": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/neu_en.txt",
    "fi_neutral": "https://raw.githubusercontent.com/Helsinki-NLP/XED/master/AnnotatedData/neu_fi.txt",
}


class XedEnFi(datasets.GeneratorBasedBuilder):
    """XED: A multilingual fine-grained emotion dataset. The dataset consists of humanannotated Finnish (25k) and English sentences (30k)."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="en_annotated", version=VERSION, description="English, Covers 8 classes without neutral"
        ),
        datasets.BuilderConfig(name="en_neutral", version=VERSION, description="English, Covers neutral"),
        datasets.BuilderConfig(
            name="fi_annotated", version=VERSION, description="Finnish, Covers 8 classes without neutral"
        ),
        datasets.BuilderConfig(name="fi_neutral", version=VERSION, description="Finnish, Covers neutral"),
    ]

    def _info(self):
        if self.config.name == "en_annotated" or self.config.name == "fi_annotated":
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "labels": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "neutral",
                                "anger",
                                "anticipation",
                                "disgust",
                                "fear",
                                "joy",
                                "sadness",
                                "surprise",
                                "trust",
                            ]
                        )
                    )
                    # the number indicates the emotion in ascending alphabetical order: neutral:0, anger:1, anticipation:2, disgust:3, fear:4, joy:5, #sadness:6, surprise:7, trust:8 in the text.
                }
            )
        else:
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "labels": datasets.features.ClassLabel(
                        names=[
                            "neutral",
                            "anger",
                            "anticipation",
                            "disgust",
                            "fear",
                            "joy",
                            "sadness",
                            "surprise",
                            "trust",
                        ]
                    ),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir[self.config.name]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                if self.config.name == "en_neutral":
                    sentence = line[1:].strip()
                    labels = "neutral"
                elif self.config.name == "fi_neutral":
                    sentence = line.split("\t")[1].strip()
                    labels = "neutral"
                else:
                    sentence = line.split("\t")[0]
                    labels = list(map(int, line.split("\t")[1].split(",")))

                yield id_, {"sentence": sentence, "labels": labels}
