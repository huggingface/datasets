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


from html import unescape
from urllib.parse import unquote

import datasets


_CITATION = """\
@inproceedings{mitchell2015,
  added-at = {2015-01-27T15:35:24.000+0100},
  author = {Mitchell, T. and Cohen, W. and Hruscha, E. and Talukdar, P. and Betteridge, J. and Carlson, A. and Dalvi, B. and Gardner, M. and Kisiel, B. and Krishnamurthy, J. and Lao, N. and Mazaitis, K. and Mohammad, T. and Nakashole, N. and Platanios, E. and Ritter, A. and Samadi, M. and Settles, B. and Wang, R. and Wijaya, D. and Gupta, A. and Chen, X. and Saparov, A. and Greaves, M. and Welling, J.},
  biburl = {https://www.bibsonomy.org/bibtex/263070703e6bb812852cca56574aed093/hotho},
  booktitle = {AAAI},
  description = {Papers by William W. Cohen},
  interhash = {52d0d71f6f5b332dabc1412f18e3a93d},
  intrahash = {63070703e6bb812852cca56574aed093},
  keywords = {learning nell ontology semantic toread},
  note = {: Never-Ending Learning in AAAI-2015},
  timestamp = {2015-01-27T15:35:24.000+0100},
  title = {Never-Ending Learning},
  url = {http://www.cs.cmu.edu/~wcohen/pubs.html},
  year = 2015
}
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


_LICENSE = """
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
                    "score": datasets.Value("string"),
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
                    "score": datasets.Value("string"),
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
        """Yields examples from the NELL belief knowledge base and candidate bleifs knowledge base if the config is 'nell_belief' and 'nell_candidate', respectively, otherwise yields the sentences for two dataset if the config is 'nell_belief_sentences' and 'nell_candidate_sentences' respectively."""

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
                        "entity": row[0].strip(),
                        "relation": row[1].strip(),
                        "value": row[2].strip(),
                        "iteration_of_promotion": row[3].strip(),
                        "score": row[4].strip(),
                        "source": row[5].strip(),
                        "entity_literal_strings": row[6].strip(),
                        "value_literal_strings": row[7].strip(),
                        "best_entity_literal_string": row[8].strip(),
                        "best_value_literal_string": row[9].strip(),
                        "categories_for_entity": row[10].strip(),
                        "categories_for_value": row[11].strip(),
                        "candidate_source": row[12].strip(),
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
                                    "entity": row[0].replace("candidate:", "").replace("concept:", "").strip(),
                                    "relation": row[1].replace("candidate:", "").replace("concept:", "").strip(),
                                    "value": row[2].replace("candidate:", "").replace("concept:", "").strip(),
                                    "score": row[4].strip(),
                                    "sentence": sentence.strip(),
                                    "count": int(count),
                                    "url": url.strip(),
                                    "sentence_type": iter_type,
                                }
                        iter_type = s2.split(",")[-1].strip("+")
