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
"""Benchmark Dataset for Learning to Intervene in Online Hate Speech"""


import csv
import json
import os
import re

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{qian-etal-2019-benchmark,
    title = "A Benchmark Dataset for Learning to Intervene in Online Hate Speech",
    author = "Qian, Jing  and
      Bethke, Anna  and
      Liu, Yinyin  and
      Belding, Elizabeth  and
      Wang, William Yang",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D19-1482",
    doi = "10.18653/v1/D19-1482",
    pages = "4755--4764",
    abstract = "Countering online hate speech is a critical yet challenging task, but one which can be aided by the use of Natural Language Processing (NLP) techniques. Previous research has primarily focused on the development of NLP methods to automatically and effectively detect online hate speech while disregarding further action needed to calm and discourage individuals from using hate speech in the future. In addition, most existing hate speech datasets treat each post as an isolated instance, ignoring the conversational context. In this paper, we propose a novel task of generative hate speech intervention, where the goal is to automatically generate responses to intervene during online conversations that contain hate speech. As a part of this work, we introduce two fully-labeled large-scale hate speech intervention datasets collected from Gab and Reddit. These datasets provide conversation segments, hate speech labels, as well as intervention responses written by Mechanical Turk Workers. In this paper, we also analyze the datasets to understand the common intervention strategies and explore the performance of common automatic response generation methods on these new datasets to provide a benchmark for future research.",
}

"""

_DESCRIPTION = """\
In order to encourage strategies of countering online hate speech, this benchmark introduces a novel task of generative hate speech intervention along with two fully-labeled datasets collected from Gab and Reddit. Distinct from existing hate speech datasets, these datasets retain their conversational context and introduce human-written intervention responses. Due to the data collecting strategy, all the posts in the datasets are manually labeled as hate or non-hate speech by Mechanical Turk workers, so they can also be used for the hate speech detection task.
"""

_HOMEPAGE = "https://github.com/jing-qian/A-Benchmark-Dataset-for-Learning-to-Intervene-in-Online-Hate-Speech"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

_URLs = {
    'gab': "https://raw.githubusercontent.com/jing-qian/A-Benchmark-Dataset-for-Learning-to-Intervene-in-Online-Hate-Speech/master/data/gab.csv",
    'reddit': "https://raw.githubusercontent.com/jing-qian/A-Benchmark-Dataset-for-Learning-to-Intervene-in-Online-Hate-Speech/master/data/reddit.csv",
}


class HateSpeechIntervention(datasets.GeneratorBasedBuilder):
    """Gab and Reddit hate speech intervention datasets."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="gab", version=VERSION, description="Dataset of posts from Gab"),
        datasets.BuilderConfig(name="reddit", version=VERSION, description="Dataset of posts from Reddit"),
    ]

    DEFAULT_CONFIG_NAME = "gab"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.features.Sequence(datasets.Value("string")),
                "text": datasets.features.Sequence(datasets.Value("string")),
                "hate_speech_idx": datasets.features.Sequence(datasets.Value("int32")),
                "response": datasets.features.Sequence(datasets.Value("string"))
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
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name="full",
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "full",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """ Yields examples as (key, example) tuples. """
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8", newline='') as f:
            csv_reader = csv.reader(
                f, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True, 
            )
            comment_end = re.compile('[\"\'], [\'\"]')
            for id_, row in enumerate(csv_reader):
                if id_ == 0:
                    keys = row[:]
                else:
                    res = dict([(k, v) for k, v in zip(keys, row)])
                    # remove number bullets and put in list
                    for feat in ['id', 'text']:
                        temp = res[feat].strip().split("\n")
                        for ind in range(len(temp)):
                            temp[ind] = temp[ind][2:].strip()
                        res[feat] = temp
                    for feat in ['hate_speech_idx', 'response']:
                        if res[feat] == 'n/a':
                            res[feat] = []
                        else:
                            res[feat] = res[feat].strip('][')
                            if feat == 'hate_speech_idx':
                                res[feat] = [int(x) for x in res[feat].split(',')]
                            if feat == 'response':
                                res[feat] = re.split('[\"\'], [\'\"]', res[feat])
                    yield (id_ - 1), res
