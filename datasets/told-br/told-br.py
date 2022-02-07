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
"""Toxic/Abusive Tweets Multilabel Classification Dataset for Brazilian Portuguese."""


import os

import pandas as pd

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{DBLP:journals/corr/abs-2010-04543,
  author    = {Joao Augusto Leite and
               Diego F. Silva and
               Kalina Bontcheva and
               Carolina Scarton},
  title     = {Toxic Language Detection in Social Media for Brazilian Portuguese:
               New Dataset and Multilingual Analysis},
  journal   = {CoRR},
  volume    = {abs/2010.04543},
  year      = {2020},
  url       = {https://arxiv.org/abs/2010.04543},
  eprinttype = {arXiv},
  eprint    = {2010.04543},
  timestamp = {Tue, 15 Dec 2020 16:10:16 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2010-04543.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
ToLD-Br is the biggest dataset for toxic tweets in Brazilian Portuguese, crowdsourced
by 42 annotators selected from a pool of 129 volunteers. Annotators were selected aiming
to create a plural group in terms of demographics (ethnicity, sexual orientation, age, gender).
Each tweet was labeled by three annotators in 6 possible categories:
LGBTQ+phobia,Xenophobia, Obscene, Insult, Misogyny and Racism.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/JAugusto97/ToLD-Br"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "https://github.com/JAugusto97/ToLD-Br/blob/main/LICENSE_ToLD-Br.txt "

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)

_URLS = {
    "multilabel": "https://raw.githubusercontent.com/JAugusto97/ToLD-Br/main/ToLD-BR.csv",
    "binary": "https://github.com/JAugusto97/ToLD-Br/raw/main/experiments/data/1annotator.zip",
}


class ToldBr(datasets.GeneratorBasedBuilder):
    """Toxic/Abusive Tweets Classification Dataset for Brazilian Portuguese."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="multilabel",
            version=VERSION,
            description="""
            Full multilabel dataset with target values ranging
            from 0 to 3 representing the votes from each annotator.
            """,
        ),
        datasets.BuilderConfig(
            name="binary",
            version=VERSION,
            description="""
            Binary classification dataset version separated in train, dev and test test.
            A text is considered toxic if at least one of the multilabel classes were labeled
            by at least one annotator.
            """,
        ),
    ]

    DEFAULT_CONFIG_NAME = "binary"

    def _info(self):
        if self.config.name == "binary":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["not-toxic", "toxic"]),
                }
            )
        else:
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "homophobia": datasets.ClassLabel(names=["zero_votes", "one_vote", "two_votes", "three_votes"]),
                    "obscene": datasets.ClassLabel(names=["zero_votes", "one_vote", "two_votes", "three_votes"]),
                    "insult": datasets.ClassLabel(names=["zero_votes", "one_vote", "two_votes", "three_votes"]),
                    "racism": datasets.ClassLabel(names=["zero_votes", "one_vote", "two_votes", "three_votes"]),
                    "misogyny": datasets.ClassLabel(names=["zero_votes", "one_vote", "two_votes", "three_votes"]),
                    "xenophobia": datasets.ClassLabel(names=["zero_votes", "one_vote", "two_votes", "three_votes"]),
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION, features=features, homepage=_HOMEPAGE, license=_LICENSE, citation=_CITATION
        )

    def _split_generators(self, dl_manager):
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)
        if self.config.name == "binary":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"filepath": os.path.join(data_dir, "1annotator/ptbr_train_1annotator.csv")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"filepath": os.path.join(data_dir, "1annotator/ptbr_test_1annotator.csv")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"filepath": os.path.join(data_dir, "1annotator/ptbr_validation_1annotator.csv")},
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir),
                    },
                )
            ]

    def _generate_examples(self, filepath):
        df = pd.read_csv(filepath, engine="python")
        for key, row in enumerate(df.itertuples()):
            if self.config.name == "multilabel":
                yield key, {
                    "text": row.text,
                    "homophobia": int(float(row.homophobia)),
                    "obscene": int(float(row.obscene)),
                    "insult": int(float(row.insult)),
                    "racism": int(float(row.racism)),
                    "misogyny": int(float(row.misogyny)),
                    "xenophobia": int(float(row.xenophobia)),
                }
            else:
                yield key, {"text": row.text, "label": int(row.toxic)}
