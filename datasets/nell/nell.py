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
"""NELL: Never Ending Language Learner"""

from __future__ import absolute_import, division, print_function

from html import unescape
from urllib.parse import unquote

import datasets


_CITATION = """\
Never-Ending Learning.
T. Mitchell, W. Cohen, E. Hruschka, P. Talukdar, J. Betteridge, A. Carlson, B. Dalvi, M. Gardner, B. Kisiel, J. Krishnamurthy, N. Lao, K. Mazaitis, T. Mohamed, N. Nakashole, E. Platanios, A. Ritter, M. Samadi, B. Settles, R. Wang, D. Wijaya, A. Gupta, X. Chen, A. Saparov, M. Greaves, J. Welling. In Proceedings of the Conference on Artificial Intelligence (AAAI), 2015
"""


_DESCRIPTION = """This dataset provides version 1115 of the belief
extracted by CMU's Never Ending Language Learner (NELL) and version
1110 of the candidate belief extracted by NELL. See
http://rtw.ml.cmu.edu/rtw/overview.  NELL is an open information
extraction system that attempts to read the Clueweb09 of 500 million
web pages (http://boston.lti.cs.cmu.edu/Data/clueweb09/) and general
web searches.

The dataset has 4 configurations: nell_belief, nell_candidate,
nell_belief_sentences, and nell_candidate_sentences. nell_belief is
certainties of belief are lower. The two sentences config extracts the
CPL sentence patterns filled with the applicable 'best' literal string
for the entities filled into the sentence patterns. And also provides
sentences found using web searches containing the entities and
relationships.

There are roughly 21M entries for nell_belief_sentences, and 100M
sentences for nell_candidate_sentences.
"""


_LICENSE = """There does not appear to be a license for this dataset. It is made available by Carnegie Mellon University at http://rtw.ml.cmu.edu/rtw/resources
"""

_URLs = {
    "nell_belief": "http://rtw.ml.cmu.edu/resources/results/08m/NELL.08m.1115.esv.csv.gz",
    "nell_candidate": "http://rtw.ml.cmu.edu/resources/results/08m/NELL.08m.1110.cesv.csv.gz",
    "nell_belief_sentences": "http://rtw.ml.cmu.edu/resources/results/08m/NELL.08m.1115.esv.csv.gz",
    "nell_candidate_sentences": "http://rtw.ml.cmu.edu/resources/results/08m/NELL.08m.1110.cesv.csv.gz",
}


class Nell(datasets.GeneratorBasedBuilder):
    """NELL dataset for knowledge bases and knowledge graphs and underlying sentences."""

    VERSION = datasets.Version("0.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="nell_belief", description="The beliefs in raw data form", version="1115.0.0"),
        datasets.BuilderConfig(
            name="nell_candidate", description="The candidate beliefs in raw data form", version="1110.0.0"
        ),
        datasets.BuilderConfig(
            name="nell_belief_sentences",
            description="The underlying sentences available for the nell beliefs",
            version="1115.0.0",
        ),
        datasets.BuilderConfig(
            name="nell_candidate_sentences",
            description="The underlying sentences available for the nell candidate beliefs",
            version="1110.0.0",
        ),
    ]

    DEFAULT_CONFIG_NAME = "nell"

    def _info(self):
        if self.config.name in ("nell_belief", "nell_candidate"):
            features = datasets.Features(
                {
                    "entity": datasets.Value("string"),
                    "relation": datasets.Value("string"),
                    "value": datasets.Value("string"),
                    "iteration_of_promotion": datasets.Value("string"),
                    "probability": datasets.Value("string"),
                    "source": datasets.Value("string"),
                    "entity_literal_strings": datasets.Value("string"),
                    "value_literal_strings": datasets.Value("string"),
                    "best_entity_literal_string": datasets.Value("string"),
                    "best_value_literal_string": datasets.Value("string"),
                    "categories_for_entity": datasets.Value("string"),
                    "categories_for_value": datasets.Value("string"),
                    "candidate_source": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "entity": datasets.Value("string"),
                    "relation": datasets.Value("string"),
                    "value": datasets.Value("string"),
                    "probability": datasets.Value(
                        "string"
                    ),  # if we change this to float there will be a PyArrow error:  OverflowError: There was an overflow in the <class 'pyarrow.lib.FloatArray'>. Try to reduce writer_batch_size to have batches smaller than 2GB
                    "sentence": datasets.Value("string"),
                    "count": datasets.Value("int32"),
                    "url": datasets.Value("string"),
                    "sentence_type": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="http://rtw.ml.cmu.edu/rtw/",
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
        """ Yields examples from the NELL belief knowledge base and candidate bleifs knowledge base if the config is 'nell_belief' and 'nell_candidate', respectively, otherwise yields the sentences for two dataset if the config is 'nell_belief_sentences' and 'nell_candidate_sentences' respectively. """

        with open(filepath, encoding="utf-8") as f:
            id_ = -1
            for row in f:
                row = row.strip().split("\t")
                if "[" in row[3]:
                    row[3] = row[3].strip("[]").split(",")[0]
                if "[" in row[4]:
                    row[4] = row[4].strip("[]").split(",")[0]
                if self.config.name in ("nell_belief", "nell_candidate"):
                    id_ += 1
                    yield id_, {
                        "entity": row[0],
                        "relation": row[1],
                        "value": row[2],
                        "iteration_of_promotion": row[3],
                        "probability": row[4],
                        "source": row[5],
                        "entity_literal_strings": row[6],
                        "value_literal_strings": row[7],
                        "best_entity_literal_string": row[8],
                        "best_value_literal_string": row[9],
                        "categories_for_entity": row[10],
                        "categories_for_value": row[11],
                        "candidate_source": row[12],
                    }
                else:
                    best_arg1 = row[8]
                    best_arg2 = row[9]
                    iter_type = ""
                    for s2 in unquote(row[12]).strip("[]").split("-Iter"):
                        if iter_type in ("CPL", "OE"):
                            arr = unescape(s2.split(">", 1)[-1].strip("-").replace("+", " ")).split("\t")
                            la = len(arr)
                            count = 0
                            url = ""
                            for i in range(0, la, 2):
                                sentence = arr[i]
                                if i + 1 == la:
                                    count = 1
                                    url = ""
                                else:
                                    try:
                                        count = int(arr[i + 1].split(",")[0])
                                        url = ""
                                    except ValueError:
                                        count = 1
                                        url = ""
                                        if arr[i + 1].startswith("http"):
                                            url = arr[i + 1].split(",")[0]
                                if iter_type == "CPL":
                                    if "_" in sentence:
                                        sentence = sentence.replace("_", "[[ " + best_arg1 + " ]]")
                                    elif "arg1" in sentence:
                                        sentence = sentence.replace("arg1", "[[ " + best_arg1 + " ]]").replace(
                                            "arg2", "[[ " + best_arg2 + " ]]"
                                        )
                                    else:
                                        continue
                                if sentence.endswith("CPL"):
                                    sentence = sentence[:-5]
                                if sentence.endswith("OE"):
                                    sentence = sentence[:-4]
                                id_ += 1
                                yield id_, {
                                    "entity": row[0].replace("candidate:", "").replace("concept:", ""),
                                    "relation": row[1].replace("candidate:", "").replace("concept:", ""),
                                    "value": row[2].replace("candidate:", "").replace("concept:", ""),
                                    "probability": row[
                                        4
                                    ],  # if we change this to float(row[4]) there will be a PyArrow error:  OverflowError: There was an overflow in the <class 'pyarrow.lib.FloatArray'>. Try to reduce writer_batch_size to have batches smaller than 2GB
                                    "sentence": sentence,
                                    "count": int(count),
                                    "url": url,
                                    "sentence_type": iter_type,
                                }
                        iter_type = s2.split(",")[-1].strip("+")
