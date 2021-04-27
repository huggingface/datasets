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
"""Conceptnet 5.7.0 and OMCSNet raw data"""


import json

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
Robyn Speer, Joshua Chin, and Catherine Havasi. 2017. "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge." In proceedings of AAAI 31.
}
"""

# You can copy an official description
_DESCRIPTION = """This dataset is designed to provide training data
for common sense relationships pulls together from various sources.

The dataset is multi-lingual. See langauge codes and language info
here: https://github.com/commonsense/conceptnet5/wiki/Languages


This dataset provides an interface for the conceptnet5 csv file, and
some (but not all) of the raw text data used to build conceptnet5:
omcsnet_sentences_free.txt, and omcsnet_sentences_more.txt.

One use of this dataset would be to learn to extract the conceptnet
relationship from the omcsnet sentences.

Conceptnet5 has 34,074,917 relationships. Of those relationships,
there are 2,176,099 surface text sentences related to those 2M
entries.

omcsnet_sentences_free has 898,161 lines. omcsnet_sentences_more has
2,001,736 lines.

Original downloads are available here
https://github.com/commonsense/conceptnet5/wiki/Downloads. For more
information, see: https://github.com/commonsense/conceptnet5/wiki

The omcsnet data comes with the following warning from the authors of
the above site: Remember: this data comes from various forms of
crowdsourcing. Sentences in these files are not necessarily true,
useful, or appropriate.

"""


_LICENSE = """
This work includes data from ConceptNet 5, which was compiled by the
Commonsense Computing Initiative. ConceptNet 5 is freely available under
the Creative Commons Attribution-ShareAlike license (CC BY SA 3.0) from
http://conceptnet.io.

The included data was created by contributors to Commonsense Computing
projects, contributors to Wikimedia projects, DBPedia, OpenCyc, Games
with a Purpose, Princeton University's WordNet, Francis Bond's Open
Multilingual WordNet, and Jim Breen's JMDict.

There are various othe licenses. See:
https://github.com/commonsense/conceptnet5/wiki/Copying-and-sharing-ConceptNet
"""

_URLs = {
    "conceptnet5": "https://s3.amazonaws.com/conceptnet/downloads/2019/edges/conceptnet-assertions-5.7.0.csv.gz",
    "omcs_sentences_free": "https://s3.amazonaws.com/conceptnet/downloads/2018/omcs-sentences-free.txt",
    "omcs_sentences_more": "https://s3.amazonaws.com/conceptnet/downloads/2018/omcs-sentences-more.txt",
}


class Conceptnet5(datasets.GeneratorBasedBuilder):
    """Conceptnet5 dataset for common sense graphs and underlying sentences."""

    VERSION = datasets.Version("0.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="conceptnet5", description="The relationships defined by conceptnet5", version="5.7.0"
        ),
        datasets.BuilderConfig(name="omcs_sentences_free", description="OMCSNet free form text", version="5.7.0"),
        datasets.BuilderConfig(
            name="omcs_sentences_more",
            description="OMCSNet free form text, and text from templates, games, responses to questions, and so on",
            version="5.7.0",
        ),
    ]

    DEFAULT_CONFIG_NAME = "conceptnet5"

    def _info(self):
        if self.config.name == "conceptnet5":
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "full_rel": datasets.Value("string"),
                    "rel": datasets.Value("string"),
                    "arg1": datasets.Value("string"),
                    "arg2": datasets.Value("string"),
                    "lang": datasets.Value("string"),
                    "extra_info": datasets.Value("string"),
                    "weight": datasets.Value("float"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "raw_data": datasets.Value("string"),
                    "lang": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/commonsense/conceptnet5/wiki",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples from the conceptnet5 graph if the config is 'conceptnet5', otherwise yields the sentences for omcs."""

        with open(filepath, "rb") as f:
            for id_, row in enumerate(f):
                if self.config.name == "conceptnet5":
                    row = row.split(b"\t")
                    s = row[4]
                    data = json.loads(s)
                    lang1 = row[2].split(b"/")[2].decode("utf-8")
                    lang2 = row[3].split(b"/")[2].decode("utf-8")
                    if lang1 == lang2:
                        lang = lang1
                    else:
                        lang = lang1 + "/" + lang2
                    if "surfaceText" in data:
                        sentence = data["surfaceText"].strip()
                    else:
                        sentence = ""
                    if b"weight" in data:
                        weight = float(data[b"weight"])
                    else:
                        weight = 1.0
                    yield id_, {
                        "sentence": sentence,
                        "full_rel": row[0].decode("utf-8"),
                        "rel": row[1].decode("utf-8"),
                        "arg1": row[2].decode("utf-8"),
                        "arg2": row[3].decode("utf-8"),
                        "lang": lang,
                        "extra_info": row[4].decode("utf-8"),
                        "weight": weight,
                    }
                else:
                    row = row.decode("utf-8").strip()
                    data = row.split("\t")
                    if len(data) > 1:
                        sentence = data[1]
                        lang = data[4]
                    else:
                        continue
                    yield id_, {
                        "raw_data": row,
                        "sentence": sentence,
                        "lang": lang,
                    }
