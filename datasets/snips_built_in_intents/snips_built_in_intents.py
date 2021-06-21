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

# Lint as: python3
"""Snips built in intents (2016-12-built-in-intents) dataset."""


import json

import datasets
from datasets.tasks import TextClassification


_DESCRIPTION = """\
Snips' built in intents dataset was initially used to compare different voice assistants and released as a public dataset hosted at
https://github.com/sonos/nlu-benchmark 2016-12-built-in-intents. The dataset contains 328 utterances over 10 intent classes. The
related paper mentioned on the github page is https://arxiv.org/abs/1805.10190 and a related Medium post is
https://medium.com/snips-ai/benchmarking-natural-language-understanding-systems-d35be6ce568d .
"""

_CITATION = """\
@article{DBLP:journals/corr/abs-1805-10190,
  author    = {Alice Coucke and
               Alaa Saade and
               Adrien Ball and
               Th{\'{e}}odore Bluche and
               Alexandre Caulier and
               David Leroy and
               Cl{\'{e}}ment Doumouro and
               Thibault Gisselbrecht and
               Francesco Caltagirone and
               Thibaut Lavril and
               Ma{\"{e}}l Primet and
               Joseph Dureau},
  title     = {Snips Voice Platform: an embedded Spoken Language Understanding system
               for private-by-design voice interfaces},
  journal   = {CoRR},
  volume    = {abs/1805.10190},
  year      = {2018},
  url       = {http://arxiv.org/abs/1805.10190},
  archivePrefix = {arXiv},
  eprint    = {1805.10190},
  timestamp = {Mon, 13 Aug 2018 16:46:59 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1805-10190.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/sonos/nlu-benchmark/master/2016-12-built-in-intents/benchmark_data.json"
)


class SnipsBuiltInIntents(datasets.GeneratorBasedBuilder):
    """Snips built in intents (2016-12-built-in-intents) dataset."""

    def _info(self):
        # ToDo: Consider adding an alternate configuration for the entity slots. The default is to only return the intent labels.

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "ComparePlaces",
                            "RequestRide",
                            "GetWeather",
                            "SearchPlace",
                            "GetPlaceDetails",
                            "ShareCurrentLocation",
                            "GetTrafficInformation",
                            "BookRestaurant",
                            "GetDirections",
                            "ShareETA",
                        ]
                    ),
                }
            ),
            homepage="https://github.com/sonos/nlu-benchmark/tree/master/2016-12-built-in-intents",
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        # Note: The source dataset doesn't have a train-test split.
        # ToDo: Consider splitting the data into train-test sets and re-hosting.
        samples_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": samples_path}),
        ]

    def _generate_examples(self, filepath):
        """Snips built in intent examples."""
        num_examples = 0

        with open(filepath, encoding="utf-8") as file_obj:
            snips_dict = json.load(file_obj)
            domains = snips_dict["domains"]

            for domain_dict in domains:
                intents = domain_dict["intents"]

                for intent_dict in intents:
                    label = intent_dict["benchmark"]["Snips"]["original_intent_name"]
                    queries = intent_dict["queries"]

                    for query_dict in queries:
                        query_text = query_dict["text"]

                        yield num_examples, {"text": query_text, "label": label}
                        num_examples += 1  # Explicitly keep track of the number of examples.
