# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Discourse marker prediction with 174 different markers"""


import csv
import os
import textwrap

import datasets


_Discovery_CITATION = """@inproceedings{sileo-etal-2019-mining,
    title = "Mining Discourse Markers for Unsupervised Sentence Representation Learning",
    author = "Sileo, Damien  and
      Van De Cruys, Tim  and
      Pradel, Camille  and
      Muller, Philippe",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N19-1351",
    pages = "3477--3486",
    abstract = "Current state of the art systems in NLP heavily rely on manually annotated datasets, which are expensive to construct. Very little work adequately exploits unannotated data {--} such as discourse markers between sentences {--} mainly because of data sparseness and ineffective extraction methods. In the present work, we propose a method to automatically discover sentence pairs with relevant discourse markers, and apply it to massive amounts of data. Our resulting dataset contains 174 discourse markers with at least 10k examples each, even for rare markers such as {``}coincidentally{''} or {``}amazingly{''}. We use the resulting data as supervision for learning transferable sentence embeddings. In addition, we show that even though sentence representation learning through prediction of discourse marker yields state of the art results across different transfer tasks, it{'}s not clear that our models made use of the semantic relation between sentences, thus leaving room for further improvements.",
}
"""

_Discovery_DESCRIPTION = r"""\
Discourse marker prediction with 174 different markers
https://github.com/synapse-developpement/Discovery
"""

DATA_URL = "https://www.dropbox.com/s/aox84z90nyyuikz/discovery.zip?dl=1"


LABELS = [
    "[no-conn]",
    "absolutely,",
    "accordingly",
    "actually,",
    "additionally",
    "admittedly,",
    "afterward",
    "again,",
    "already,",
    "also,",
    "alternately,",
    "alternatively",
    "although,",
    "altogether,",
    "amazingly,",
    "and",
    "anyway,",
    "apparently,",
    "arguably,",
    "as_a_result,",
    "basically,",
    "because_of_that",
    "because_of_this",
    "besides,",
    "but",
    "by_comparison,",
    "by_contrast,",
    "by_doing_this,",
    "by_then",
    "certainly,",
    "clearly,",
    "coincidentally,",
    "collectively,",
    "consequently",
    "conversely",
    "curiously,",
    "currently,",
    "elsewhere,",
    "especially,",
    "essentially,",
    "eventually,",
    "evidently,",
    "finally,",
    "first,",
    "firstly,",
    "for_example",
    "for_instance",
    "fortunately,",
    "frankly,",
    "frequently,",
    "further,",
    "furthermore",
    "generally,",
    "gradually,",
    "happily,",
    "hence,",
    "here,",
    "historically,",
    "honestly,",
    "hopefully,",
    "however",
    "ideally,",
    "immediately,",
    "importantly,",
    "in_contrast,",
    "in_fact,",
    "in_other_words",
    "in_particular,",
    "in_short,",
    "in_sum,",
    "in_the_end,",
    "in_the_meantime,",
    "in_turn,",
    "incidentally,",
    "increasingly,",
    "indeed,",
    "inevitably,",
    "initially,",
    "instead,",
    "interestingly,",
    "ironically,",
    "lastly,",
    "lately,",
    "later,",
    "likewise,",
    "locally,",
    "luckily,",
    "maybe,",
    "meaning,",
    "meantime,",
    "meanwhile,",
    "moreover",
    "mostly,",
    "namely,",
    "nationally,",
    "naturally,",
    "nevertheless",
    "next,",
    "nonetheless",
    "normally,",
    "notably,",
    "now,",
    "obviously,",
    "occasionally,",
    "oddly,",
    "often,",
    "on_the_contrary,",
    "on_the_other_hand",
    "once,",
    "only,",
    "optionally,",
    "or,",
    "originally,",
    "otherwise,",
    "overall,",
    "particularly,",
    "perhaps,",
    "personally,",
    "plus,",
    "preferably,",
    "presently,",
    "presumably,",
    "previously,",
    "probably,",
    "rather,",
    "realistically,",
    "really,",
    "recently,",
    "regardless,",
    "remarkably,",
    "sadly,",
    "second,",
    "secondly,",
    "separately,",
    "seriously,",
    "significantly,",
    "similarly,",
    "simultaneously",
    "slowly,",
    "so,",
    "sometimes,",
    "soon,",
    "specifically,",
    "still,",
    "strangely,",
    "subsequently,",
    "suddenly,",
    "supposedly,",
    "surely,",
    "surprisingly,",
    "technically,",
    "thankfully,",
    "then,",
    "theoretically,",
    "thereafter,",
    "thereby,",
    "therefore",
    "third,",
    "thirdly,",
    "this,",
    "though,",
    "thus,",
    "together,",
    "traditionally,",
    "truly,",
    "truthfully,",
    "typically,",
    "ultimately,",
    "undoubtedly,",
    "unfortunately,",
    "unsurprisingly,",
    "usually,",
    "well,",
    "yet,",
]


class DiscoveryConfig(datasets.BuilderConfig):
    """BuilderConfig for Discovery."""

    def __init__(
        self,
        text_features,
        label_classes=None,
        process_label=lambda x: x,
        **kwargs,
    ):
        """BuilderConfig for Discovery.
        Args:
          text_features: `dict[string, string]`, map from the name of the feature
            dict for each text field to the name of the column in the tsv file
          label_column: `string`, name of the column in the tsv file corresponding
            to the label
          data_url: `string`, url to download the zip file from
          data_dir: `string`, the path to the folder containing the tsv files in the
            downloaded zip
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          label_classes: `list[string]`, the list of classes if the label is
            categorical. If not provided, then the label will be of type
            `datasets.Value('float32')`.
          process_label: `Function[string, any]`, function  taking in the raw value
            of the label and processing it to the form required by the label feature
          **kwargs: keyword arguments forwarded to super.
        """

        super(DiscoveryConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)

        self.text_features = text_features
        self.label_column = "label"
        self.label_classes = LABELS
        self.data_url = DATA_URL
        self.data_dir = os.path.join("discovery", self.name)
        self.citation = textwrap.dedent(_Discovery_CITATION)
        self.process_label = process_label
        self.description = ""
        self.url = ""


class Discovery(datasets.GeneratorBasedBuilder):
    """Discourse marker prediction with 174 different markers"""

    BUILDER_CONFIG_CLASS = DiscoveryConfig

    BUILDER_CONFIGS = [
        DiscoveryConfig(
            name="discovery",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
        DiscoveryConfig(
            name="discoverysmall",
            text_features={"sentence1": "sentence1", "sentence2": "sentence2"},
        ),
    ]

    def _info(self):
        features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features.keys()}
        if self.config.label_classes:
            features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)
        else:
            features["label"] = datasets.Value("float32")
        features["idx"] = datasets.Value("int32")
        return datasets.DatasetInfo(
            description=_Discovery_DESCRIPTION,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _Discovery_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url)
        data_dir = os.path.join(dl_dir, self.config.data_dir)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_file": os.path.join(data_dir or "", "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_file": os.path.join(data_dir or "", "dev.tsv"),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_file": os.path.join(data_dir or "", "test.tsv"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, data_file, split):
        process_label = self.config.process_label
        label_classes = self.config.label_classes
        with open(data_file, encoding="utf8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)

            for n, row in enumerate(reader):
                example = {feat: row[col] for feat, col in self.config.text_features.items()}
                example["idx"] = n

                if self.config.label_column in row:
                    label = row[self.config.label_column]
                    if label_classes and label not in label_classes:
                        label = int(label) if label else None
                    example["label"] = process_label(label)
                else:
                    example["label"] = process_label(-1)
                yield example["idx"], example
